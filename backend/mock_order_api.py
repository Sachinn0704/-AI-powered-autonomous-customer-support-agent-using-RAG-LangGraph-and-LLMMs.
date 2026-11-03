from fastapi import FastAPI, HTTPException
from datetime import date, timedelta

app = FastAPI(
    title="External E-Commerce Order API",
    description="Simulated external order management service",
    version="1.0"
)

orders = {
    "ORD1001": {
        "order_number": "ORD1001",
        "customer_id": 1,
        "product": "Wireless Headphones",
        "amount": 2500,
        "order_status": "delivered",
        "payment_status": "paid",
        "delivery_date": str(date.today() - timedelta(days=5))
    },

    "ORD1002": {
        "order_number": "ORD1002",
        "customer_id": 2,
        "product": "Smart Watch",
        "amount": 4500,
        "order_status": "delivered",
        "payment_status": "paid",
        "delivery_date": str(date.today() - timedelta(days=12))
    },

    "ORD1003": {
        "order_number": "ORD1003",
        "customer_id": 3,
        "product": "Bluetooth Speaker",
        "amount": 1800,
        "order_status": "shipped",
        "payment_status": "paid",
        "delivery_date": None
    },
    "ORD1004": {
        "order_number": "ORD1004",
        "customer_id": 1,
        "product": "Premium Laptop",
        "amount": 25000,
        "order_status": "delivered",
        "payment_status": "paid",
        "delivery_date": str(date.today() - timedelta(days=2))
    },
    "ORD1005": {
    "order_number": "ORD1005",
    "customer_id": 2,
    "product": "Gaming Mouse",
    "amount": 1500,
    "order_status": "processing",
    "payment_status": "paid",
    "delivery_date": None
},
}


@app.get("/")
def home():
    return {
        "message": "External E-Commerce API is running"
    }


@app.get("/orders")
def get_all_orders():
    return {
        "total_orders": len(orders),
        "orders": list(orders.values())
    }
@app.get("/orders/{order_number}")
def get_order(order_number: str):

    order = orders.get(order_number)

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order

@app.post("/orders/{order_number}/cancel")
def cancel_order(order_number: str):

    order = orders.get(order_number)

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order["order_status"] == "cancelled":
        raise HTTPException(
            status_code=400,
            detail="Order is already cancelled"
        )

    if order["order_status"] != "processing":
        raise HTTPException(
            status_code=400,
            detail="Only processing orders can be cancelled"
        )

    order["order_status"] = "cancelled"

    return {
        "success": True,
        "order_number": order_number,
        "status": "cancelled",
        "message": "Order cancelled successfully"
    }