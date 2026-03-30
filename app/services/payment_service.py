def get_payment_status(user_id: int):
    return {
        "status": "FAILED",
        "amount": 250,
        "reason": "Insufficient balance"
    }

def retry_payment(user_id: int):
    return {
        "status": "SUCCESS",
        "message": "Payment retried successfully"
    }

def get_refund_status(user_id: int):
    return {
        "ZZstatus": "PROCESSING",
        "amount": 120
    }
