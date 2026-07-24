from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
import datetime

from comments.schemas import Comment, CommentCreate
from comments.models import CommentBase

router = APIRouter()

@router.get("/list-comments", response_model=list[Comment])
async def list_comments(db: AsyncSession = Depends(get_db)):
    all_comments = await db.scalars(select(CommentBase).order_by(CommentBase.created_at.desc()))
    return all_comments

@router.post("/create-comment", response_model=Comment)
async def create_comment(payload: CommentCreate, db: AsyncSession = Depends(get_db)):
    comment = CommentBase(
        user_id=payload.user_id,
        name=payload.name,
        body=payload.body,
        rate=payload.rate
    )

    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    return comment

@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, db: AsyncSession = Depends((get_db))):
    needed_comment = await db.get(CommentBase, comment_id)

    if not needed_comment:
        raise HTTPException(status_code=404, detail="Not found")

    await db.delete(needed_comment)
    await db.commit()

    return "{\"ok\": True}"