from typing import Literal
from pydantic import BaseModel
from datetime import datetime


class Comment(BaseModel):
    user_id: int
    comment_id: int
    name: str
    body: str
    rate: Literal["Positive", "Negative"]
    created_at: datetime


class CommentCreate(BaseModel):
    user_id: int
    name: str
    body: str
    rate: Literal["Positive", "Negative"]