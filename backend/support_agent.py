import re

from tools import lookup_order


def detect_intent(message):
    text = message.lower()

    if any(word in text for word in [
        "refund", "money back", "return my money"
    ]):
        return "refund"

    if any(word in text for word in [
        "return", "replace", "exchange"
    ]):
        return "return"

    if any(word in text for word in [
        "cancel", "cancellation"
    ]):
        return "cancellation"

    if any(word in text for word in [
        "track", "tracking", "where is my order",
        "delivery status", "order status", "delivered"
    ]):
        return "order_tracking"

    if any(word in text for word in [
        "payment", "charged", "transaction"
    ]):
        return "payment"

    if any(word in text for word in [
        "complaint", "problem", "issue", "not working", "defective"
    ]):
        return "complaint"

    return "general_support"


def extract_order_number(message):
    match = re.search(r"\bORD\d+\b", message.upper())
    return match.group(0) if match else None


def handle_customer_message(message):

    intent = detect_intent(message)
    order_number = extract_order_number(message)

    if intent == "order_tracking":

        if not order_number:
            return {
                "intent": intent,
                "reply": "Please provide your order number, such as ORD1001."
            }

        try:
            order = lookup_order(order_number)
        except RuntimeError:
            return {
                "intent": intent,
                "reply": "The order service is temporarily unavailable."
            }

        if not order.get("found"):
            return {
                "intent": intent,
                "reply": f"I couldn't find order {order_number}."
            }

        reply = (
            f"Order Number: {order['order_number']}\n"
            f"Product: {order['product']}\n"
            f"Amount: ₹{order['amount']}\n"
            f"Order Status: {order['order_status']}\n"
            f"Payment Status: {order['payment_status']}"
        )

        return {
            "intent": intent,
            "reply": reply,
            "order_number": order_number
        }

    if intent == "refund":

        if not order_number:
            return {
                "intent": intent,
                "reply": "Please provide your order number to investigate your refund."
            }

        return {
            "intent": intent,
            "order_number": order_number,
            "reply": "I'm investigating your refund request. Please wait."
        }

    if intent == "cancellation":

        if not order_number:
            return {
                "intent": intent,
                "reply": "Please provide your order number. For example, ORD1005."
            }

        return {
            "intent": intent,
            "order_number": order_number,
            "reply": "I'm checking whether your order is eligible for cancellation."
        }

    if intent == "return":

        if not order_number:
            return {
                "intent": intent,
                "reply": "Please provide your order number to initiate a return."
            }

        return {
            "intent": intent,
            "order_number": order_number,
            "reply": "I'm checking your order's return eligibility."
        }

    if intent == "payment":
        return {
            "intent": intent,
            "reply": "Please describe your payment problem so I can help investigate it."
        }

    if intent == "complaint":
        return {
            "intent": intent,
            "reply": "I'm sorry you're experiencing this problem. Please describe it in more detail."
        }

    return {
        "intent": intent,
        "reply": "Hello! I'm ResolveAI. I can help with order tracking, refunds, returns, cancellations and payment issues."
    }