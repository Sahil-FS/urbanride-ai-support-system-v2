import time
from app.services.cron_service import escalate_old_tickets

INTERVAL_SECONDS = 60 * 60 * 24  # 24 hours

if __name__ == "__main__":
    while True:
        print("[CRON] Running escalation job...")
        escalate_old_tickets()
        time.sleep(INTERVAL_SECONDS)
