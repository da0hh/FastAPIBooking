from database import Base
from sqlalchemy import String, Text, DateTime, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    place_name: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_available: Mapped[bool] = mapped_column(default=True)
    category: Mapped[str] = mapped_column(Text)

    booked_for: Mapped[datetime] = mapped_column(DateTime(timezone=True))