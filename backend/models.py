from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)

    orders = relationship("Order", back_populates="customer")
    refunds = relationship("RefundRequest", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product = Column(String(150), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(50), default="delivered")

    customer = relationship("Customer", back_populates="orders")


class RefundRequest(Base):
    __tablename__ = "refund_requests"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_number = Column(String(50), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(50), default="pending")
    risk_level = Column(String(30), default="unknown")
    decision = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="refunds")


class InvestigationLog(Base):
    __tablename__ = "investigation_logs"

    id = Column(Integer, primary_key=True, index=True)
    refund_id = Column(Integer, ForeignKey("refund_requests.id"))
    action = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
class ReturnRequest(Base):
    __tablename__ = "return_requests"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    order_number = Column(
        String(50),
        nullable=False
    )

    reason = Column(
        Text,
        nullable=False
    )

    status = Column(
        String(50),
        default="submitted"
    )

    decision = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )