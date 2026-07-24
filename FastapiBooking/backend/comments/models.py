from database import Base
from sqlalchemy import String, Text, DateTime, func, Float
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class CommentBase(Base):
    __tablename__ = "Commentaries"

    user_id: Mapped[int] = mapped_column(nullable=False)
    comment_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    rate: Mapped[str] = mapped_column(String(15))


