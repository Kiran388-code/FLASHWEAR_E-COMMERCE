from datetime import datetime, timezone
from sqlalchemy import String, Integer, Boolean, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Rider(Base):
    __tablename__ = "riders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    current_lat: Mapped[float] = mapped_column(Float, default=12.9716)
    current_lng: Mapped[float] = mapped_column(Float, default=77.5946)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    total_earnings: Mapped[float] = mapped_column(Float, default=0.0)
    rating: Mapped[float] = mapped_column(Float, default=4.9)
