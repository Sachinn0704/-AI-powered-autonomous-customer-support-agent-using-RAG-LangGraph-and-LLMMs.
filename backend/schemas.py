from pydantic import BaseModel, Field


class RefundRequestCreate(BaseModel):
    customer_id: int
    order_number: str
    reason: str = Field(min_length=5, max_length=500)


class RefundResponse(BaseModel):
    id: int
    customer_id: int
    order_number: str
    reason: str
    status: str
    risk_level: str
    decision: str | None

class ChatRequest(BaseModel):
    customer_id: int = Field(gt=0)
    message: str = Field(min_length=1, max_length=2000)