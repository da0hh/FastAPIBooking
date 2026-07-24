from database import Base
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Login(Base):
    __tablename__ = "Login"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text)
    date_registration: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
