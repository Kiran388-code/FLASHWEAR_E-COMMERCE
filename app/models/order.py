from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    status: Mapped[str] = mapped_column(String(50), default="PLACED", nullable=False) # PLACED, PAID, RESERVED, WAREHOUSE_RECEIVED, PICKED, PACKED, DISPATCHED, RIDER_ASSIGNED, RIDER_PICKED, ON_DELIVERY, DELIVERED, COMPLETED
    step_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False) # 1 to 12
    
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    items_summary: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    
    delivery_address: Mapped[str] = mapped_column(Text, nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), default="UPI", nullable=False)
    payment_status: Mapped[str] = mapped_column(String(50), default="SUCCESS", nullable=False)
    
    eta_minutes: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    delivery_otp: Mapped[str] = mapped_column(String(10), default="2587", nullable=False)
    
    rider_id: Mapped[int] = mapped_column(Integer, nullable=True)
    rider_name: Mapped[str] = mapped_column(String(100), nullable=True, default="Rahul Kumar")
    rider_phone: Mapped[str] = mapped_column(String(20), nullable=True, default="+91 9876543210")
    
    warehouse_id: Mapped[int] = mapped_column(Integer, nullable=True, default=1)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False
    )

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[str] = mapped_column(String(20), nullable=True)
    color: Mapped[str] = mapped_column(String(50), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    location_code: Mapped[str] = mapped_column(String(50), nullable=True, default="A12-03-02")
