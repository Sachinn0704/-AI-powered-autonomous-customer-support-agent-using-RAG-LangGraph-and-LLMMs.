from langgraph.graph import StateGraph, END
from typing import TypedDict

from tools import (
    lookup_order,
    check_refund_policy,
    get_customer_history,
    fraud_check
)


class RefundState(TypedDict):
    order_number: str
    order: dict
    policy: dict
    history: dict
    fraud: dict
    decision: str
    reason: str


def investigate_order(state: RefundState):
    order = lookup_order(state["order_number"])

    return {"order": order}


def investigate_policy(state: RefundState):
    policy = check_refund_policy(state["order"])

    return {"policy": policy}


def investigate_history(state: RefundState):
    if not state["order"].get("found"):
        return {"history": {"total_refund_requests": 0}}

    history = get_customer_history(
        state["order"]["customer_id"]
    )

    return {"history": history}


def investigate_fraud(state: RefundState):
    if not state["order"].get("found"):
        return {"fraud": {"risk": "high", "reason": "Order not found"}}

    fraud = fraud_check(
        state["order"]["customer_id"],
        state["order"]["amount"]
    )

    return {"fraud": fraud}


def make_decision(state: RefundState):
    if not state["order"].get("found"):
        return {
            "decision": "rejected",
            "reason": "Order not found"
        }

    if not state["policy"]["eligible"]:
        return {
            "decision": "rejected",
            "reason": state["policy"]["reason"]
        }

    if state["fraud"]["risk"] == "high":
        return {
            "decision": "human_review",
            "reason": state["fraud"]["reason"]
        }

    return {
        "decision": "approved",
        "reason": "Order passed the basic refund and risk checks"
    }


workflow = StateGraph(RefundState)

workflow.add_node("order_lookup", investigate_order)
workflow.add_node("policy_check", investigate_policy)
workflow.add_node("customer_history", investigate_history)
workflow.add_node("fraud_check", investigate_fraud)
workflow.add_node("decision", make_decision)

workflow.set_entry_point("order_lookup")

workflow.add_edge("order_lookup", "policy_check")
workflow.add_edge("policy_check", "customer_history")
workflow.add_edge("customer_history", "fraud_check")
workflow.add_edge("fraud_check", "decision")
workflow.add_edge("decision", END)

refund_agent = workflow.compile()


def process_refund(order_number):
    initial_state = {
        "order_number": order_number,
        "order": {},
        "policy": {},
        "history": {},
        "fraud": {},
        "decision": "",
        "reason": ""
    }

    return refund_agent.invoke(initial_state)