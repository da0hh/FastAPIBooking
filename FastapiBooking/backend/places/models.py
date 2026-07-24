from database import Base
from sqlalchemy import String, Text, DateTime, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

class Place(Base):
    __tablename__ = "places"

    place_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    category: Mapped[str] =mapped_column(String(50), nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    place_address_url: Mapped[str] = mapped_column(Text)