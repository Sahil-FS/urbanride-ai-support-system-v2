def get_active_ride(user_id: int):
    return {
        "ride_id": "RIDE123",
        "driver_id": "DR123",
        "status": "ONGOING",
        "pickup": "Hinjewadi Phase 1",
        "drop": "Pune Station",
        "eta_minutes": 3
    }

def cancel_ride(ride_id: str):
    return {
        "ride_id": ride_id,
        "status": "CANCELLED"
    }

def get_ride_status(user_id: int):
    return {
        "status": "DRIVER_LATE",
        "delay_minutes": 5
    }
