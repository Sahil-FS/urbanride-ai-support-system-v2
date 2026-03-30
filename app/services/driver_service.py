def get_driver(driver_id: str):
    return {
        "driver_id": driver_id,
        "name": "Rajesh",
        "rating": 4.8,
        "phone": "+919876543210",
        "vehicle": "MH12AB1234"
    }

def call_driver(driver_id: str):
    driver = get_driver(driver_id)
    return {
        "message": f"Calling {driver['name']} at {driver['phone']}"
    }
