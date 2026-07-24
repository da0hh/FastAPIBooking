from pydantic import BaseModel, field_serializer
from typing import Literal
from datetime import datetime

class ChoosePlace(BaseModel):
    user_id: int
    city: str
    prefers: str

class MakeBook(BaseModel):
    user_id: int
    city: str
    place_name: str
    booked_for: datetime


class BookRead(BaseModel):
    user_id: int
    book_id: int
    city: str
    place_name: str
    booked_for: datetime
    is_available: bool
    created_at: datetime

class BookEdit(BaseModel):
    user_id: int
    book_id: int
    place_name: str
    created_at: datetime

class BookCancel(BaseModel):
    book_id: int
    password: str