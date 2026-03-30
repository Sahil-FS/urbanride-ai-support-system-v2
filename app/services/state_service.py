import json
import time

# Safe Redis Initialization
try:
    import redis
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    # Test connection
    redis_client.ping()
    USE_REDIS = True
except:
    USE_REDIS = False
    memory_store = {}

def default_state():
    return {
        "current_intent": None,
        "step": None,
        "context": {},
        "history": [],
        "fallback_count": 0,
        "last_intent": None,
        "last_message": None,
        "last_intent_time": 0
    }

def get_state(user_id):
    if USE_REDIS:
        try:
            data = redis_client.get(user_id)
            if data:
                return json.loads(data.decode("utf-8"))
        except:
            pass
    else:
        return memory_store.get(user_id, default_state())

    return default_state()

def save_state(user_id, state):
    if USE_REDIS:
        try:
            redis_client.set(user_id, json.dumps(state))
        except:
            pass
    else:
        memory_store[user_id] = state

def set_state(user_id, state):
    save_state(user_id, state)

def update_state(user_id: int, intent: str):
    state = get_state(user_id)
    state["history"].append(intent)
    state["current_intent"] = intent
    save_state(user_id, state)

def increment_fallback(user_id):
    state = get_state(user_id)
    state["fallback_count"] = state.get("fallback_count", 0) + 1
    save_state(user_id, state)
    return state["fallback_count"]

def reset_fallback(user_id):
    state = get_state(user_id)
    state["fallback_count"] = 0
    save_state(user_id, state)

def get_last_state(user_id):
    """Retrieve the last processed intent, message and timestamp."""
    state = get_state(user_id)
    return {
        "intent": state.get("last_intent"),
        "message": state.get("last_message"),
        "timestamp": state.get("last_intent_time", 0)
    }

def set_last_state(user_id, intent, message):
    """Store the current intent and message as the last state with current timestamp."""
    state = get_state(user_id)
    state["last_intent"] = intent
    state["last_message"] = message
    state["last_intent_time"] = time.time()
    save_state(user_id, state)

def clear_state(user_id: int):
    if USE_REDIS:
        try:
            redis_client.delete(user_id)
        except:
            pass
    else:
        if user_id in memory_store:
            del memory_store[user_id]
