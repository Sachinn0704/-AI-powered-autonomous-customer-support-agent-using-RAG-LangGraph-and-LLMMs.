from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from schemas import ChatRequest
from support_agent import handle_customer_message
from tools import cancel_order
from schemas import RefundRequestCreate, ChatRequest
from support_agent import handle_customer_message
from tools import lookup_order, cancel_order
from support_agent import handle_customer_message
from tools import lookup_order, cancel_order
from models import ReturnRequest
from tools import check_return_eligibility

from schemas import RefundRequestCreate, ChatRequest
from agent import process_refund
from support_agent import handle_customer_message

from database import Base, engine, get_db
from models import Customer, RefundRequest, InvestigationLog
from schemas import RefundRequestCreate
from agent import process_refund
from tools import lookup_order


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ResolveAI",
    description="Autonomous Customer Refund Resolution Agent",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {"message": "ResolveAI API is running"}


@app.post("/refunds")
def submit_refund(
    request: RefundRequestCreate,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == request.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    try:
        order = lookup_order(request.order_number)
    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    if not order.get("found"):
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order["customer_id"] != request.customer_id:
        raise HTTPException(
            status_code=403,
            detail="This order does not belong to this customer"
        )

    try:
        result = process_refund(request.order_number)
    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    status = result["decision"]

    refund = RefundRequest(
        customer_id=request.customer_id,
        order_number=request.order_number,
        reason=request.reason,
        status="pending_review" if status == "human_review" else status,
        risk_level=result["fraud"]["risk"],
        decision=result["reason"]
    )

    db.add(refund)
    db.commit()
    db.refresh(refund)

    log = InvestigationLog(
        refund_id=refund.id,
        action="agent_investigation",
        details=str(result)
    )

    db.add(log)
    db.commit()

    return {
        "message": "Refund investigation completed",
        "refund_id": refund.id,
        "status": refund.status,
        "risk_level": refund.risk_level,
        "decision": refund.decision
    }


@app.get("/refunds")
def get_refunds(db: Session = Depends(get_db)):
    refunds = db.query(RefundRequest).order_by(
        RefundRequest.id.desc()
    ).all()

    return [
        {
            "id": refund.id,
            "customer_id": refund.customer_id,
            "order_number": refund.order_number,
            "reason": refund.reason,
            "status": refund.status,
            "risk_level": refund.risk_level,
            "decision": refund.decision
        }
        for refund in refunds
    ]


@app.get("/refunds/{refund_id}/logs")
def get_refund_logs(
    refund_id: int,
    db: Session = Depends(get_db)
):
    refund = db.query(RefundRequest).filter(
        RefundRequest.id == refund_id
    ).first()

    if not refund:
        raise HTTPException(
            status_code=404,
            detail="Refund not found"
        )

    logs = db.query(InvestigationLog).filter(
        InvestigationLog.refund_id == refund_id
    ).all()

    return [
        {
            "action": log.action,
            "details": log.details,
            "created_at": log.created_at
        }
        for log in logs
    ]
@app.post("/chat")
def customer_chat(request: ChatRequest):
    result = handle_customer_message(request.message)

    return {
        "success": True,
        "intent": result["intent"],
        "reply": result["reply"],
        "order_number": result.get("order_number")
    }
def customer_chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    result = handle_customer_message(request.message)

    intent = result["intent"]
        # Handle product return requests
    if intent == "return" and result.get("order_number"):

        customer = db.query(Customer).filter(
            Customer.id == request.customer_id
        ).first()

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        order_number = result["order_number"]

        try:
            order = lookup_order(order_number)

        except RuntimeError as error:
            raise HTTPException(
                status_code=503,
                detail=str(error)
            )

        if not order.get("found"):
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        if order["customer_id"] != request.customer_id:
            raise HTTPException(
                status_code=403,
                detail="This order does not belong to this customer"
            )

        eligibility = check_return_eligibility(order)

        if not eligibility["eligible"]:
            return {
                "success": False,
                "intent": intent,
                "reply": eligibility["reason"]
            }

        return_request = ReturnRequest(
            customer_id=request.customer_id,
            order_number=order_number,
            reason=request.message,
            status="submitted",
            decision=eligibility["reason"]
        )

        try:
            db.add(return_request)
            db.commit()
            db.refresh(return_request)

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Unable to save return request"
            )

        return {
            "success": True,
            "intent": intent,
            "return_id": return_request.id,
            "status": return_request.status,
            "reply": (
                f"Your return request has been submitted successfully!\n\n"
                f"Order: {order_number}\n"
                f"Product: {order['product']}\n"
                f"Return ID: {return_request.id}\n"
                f"Status: {return_request.status}"
            )
        }
        # Handle order cancellation
    if intent == "cancellation" and result.get("order_number"):

        customer = db.query(Customer).filter(
            Customer.id == request.customer_id
        ).first()

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        order_number = result["order_number"]

        try:
            order = lookup_order(order_number)

            if not order.get("found"):
                raise HTTPException(
                    status_code=404,
                    detail="Order not found"
                )

            if order["customer_id"] != request.customer_id:
                raise HTTPException(
                    status_code=403,
                    detail="This order does not belong to this customer"
                )

            cancellation = cancel_order(order_number)

        except RuntimeError as error:
            raise HTTPException(
                status_code=503,
                detail=str(error)
            )

        if not cancellation["success"]:
            return {
                "success": False,
                "intent": intent,
                "reply": cancellation["message"]
            }

        return {
            "success": True,
            "intent": intent,
            "order_number": order_number,
            "status": cancellation["status"],
            "reply": (
                f"Your order has been cancelled successfully!\n\n"
                f"Order: {order_number}\n"
                f"Product: {order['product']}\n"
                f"Status: cancelled"
            )
        }

    # Handle refund requests
    if intent == "refund" and result.get("order_number"):

        customer = db.query(Customer).filter(
            Customer.id == request.customer_id
        ).first()

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        order_number = result["order_number"]

        try:
            order = lookup_order(order_number)

            if not order.get("found"):
                raise HTTPException(
                    status_code=404,
                    detail="Order not found"
                )

            if order["customer_id"] != request.customer_id:
                raise HTTPException(
                    status_code=403,
                    detail="This order does not belong to this customer"
                )

            agent_result = process_refund(order_number)

        except RuntimeError as error:
            raise HTTPException(
                status_code=503,
                detail=str(error)
            )

        decision = agent_result["decision"]

        refund = RefundRequest(
            customer_id=request.customer_id,
            order_number=order_number,
            reason=request.message,
            status=(
                "pending_review"
                if decision == "human_review"
                else decision
            ),
            risk_level=agent_result["fraud"]["risk"],
            decision=agent_result["reason"]
        )

        try:
            db.add(refund)
            db.flush()

            log = InvestigationLog(
                refund_id=refund.id,
                action="agent_investigation",
                details=str(agent_result)
            )

            db.add(log)
            db.commit()
            db.refresh(refund)

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Unable to save refund investigation"
            )

        reply = (
            f"Your refund investigation is complete.\n\n"
            f"Order: {order_number}\n"
            f"Refund ID: {refund.id}\n"
            f"Status: {refund.status}\n"
            f"Risk Level: {refund.risk_level}\n\n"
            f"Decision: {refund.decision}"
        )

        if refund.status == "pending_review":
            reply += "\n\nYour request has been escalated to our human support team."

        return {
            "success": True,
            "intent": intent,
            "reply": reply,
            "refund_id": refund.id,
            "status": refund.status
        }

    return {
        "success": True,
        "intent": intent,
        "reply": result["reply"],
        "order_number": result.get("order_number")
    }
# RAG Knowledge Base API

from rag_pipeline import retrieve_context


@app.post("/knowledge")
def knowledge_chat(request: ChatRequest):

    result = retrieve_context(request.message)

    return {
        "success": result["success"],
        "question": result["question"],
        "reply": result["answer"],
        "sources": result["sources"]
    }


# RAG + LLM AI Chat API

from ai_rag_agent import ask_ai


@app.post("/ai-chat")
def ai_chat(request: ChatRequest):

    result = ask_ai(request.message)

    return {
        "success": result["success"],
        "question": request.message,
        "reply": result["reply"],
        "sources": result.get("sources", [])
    }

