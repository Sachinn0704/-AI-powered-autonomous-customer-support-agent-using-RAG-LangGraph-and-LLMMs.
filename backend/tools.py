import httpx
from datetime import date

from database import SessionLocal
from models import RefundRequest


ORDER_API = "http://127.0.0.1:8001"


def lookup_order(order_number):

    try:
        response = httpx.get(
            f"{ORDER_API}/orders/{order_number}",
            timeout=10
        )

        if response.status_code == 404:
            return {
                "found": False,
                "message": "Order not found"
            }

        response.raise_for_status()

        order = response.json()

        return {
            "found": True,
            **order
        }

    except httpx.RequestError as error:
        raise RuntimeError(
            f"External order API unavailable: {error}"
        )


def check_refund_policy(order):

    if not order.get("found"):
        return {
            "eligible": False,
            "reason": "Order does not exist"
        }

    if order["order_status"] != "delivered":
        return {
            "eligible": False,
            "reason": "Order has not been delivered"
        }

    if order["payment_status"] != "paid":
        return {
            "eligible": False,
            "reason": "Payment has not been completed"
        }

    delivery_date = date.fromisoformat(
        order["delivery_date"]
    )

    days_since_delivery = (
        date.today() - delivery_date
    ).days

    if days_since_delivery > 30:
        return {
            "eligible": False,
            "reason": "Refund period of 30 days has expired"
        }

    return {
        "eligible": True,
        "reason": "Order meets the basic refund policy",
        "days_since_delivery": days_since_delivery
    }


def get_customer_history(customer_id):

    db = SessionLocal()

    try:
        refunds = db.query(RefundRequest).filter(
            RefundRequest.customer_id == customer_id
        ).all()

        return {
            "total_refund_requests": len(refunds),
            "previous_refunds": [
                {
                    "id": refund.id,
                    "status": refund.status
                }
                for refund in refunds
            ]
        }

    finally:
        db.close()


def fraud_check(customer_id, amount):

    db = SessionLocal()

    try:
        previous_requests = db.query(
            RefundRequest
        ).filter(
            RefundRequest.customer_id == customer_id
        ).count()

        if previous_requests >= 3:
            return {
                "risk": "high",
                "reason": "Customer has three or more previous refund requests"
            }

        if amount > 10000:
            return {
                "risk": "high",
                "reason": "Refund amount exceeds automatic review limit"
            }

        return {
            "risk": "low",
            "reason": "No suspicious activity detected by basic checks"
        }

    finally:
        db.close()


def cancel_order(order_number):

    try:
        response = httpx.post(
            f"{ORDER_API}/orders/{order_number}/cancel",
            timeout=10
        )

        if response.status_code >= 400:
            try:
                message = response.json().get(
                    "detail",
                    "Cancellation failed"
                )
            except ValueError:
                message = "Cancellation failed"

            return {
                "success": False,
                "message": message
            }

        return response.json()

    except httpx.RequestError as error:
        raise RuntimeError(
            f"Cancellation service unavailable: {error}"
        )


def check_return_eligibility(order):
    from datetime import date

    if not order.get("found"):
        return {
            "eligible": False,
            "reason": "Order not found"
        }

    if order["order_status"] != "delivered":
        return {
            "eligible": False,
            "reason": "Only delivered orders can be returned"
        }

    delivery_date = date.fromisoformat(order["delivery_date"])

    days_since_delivery = (
        date.today() - delivery_date
    ).days

    if days_since_delivery > 30:
        return {
            "eligible": False,
            "reason": "The 30-day return period has expired"
        }

    return {
        "eligible": True,
        "reason": "Order is eligible for return",
        "days_since_delivery": days_since_delivery
    }