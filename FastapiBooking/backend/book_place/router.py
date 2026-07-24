from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import json

from chaindoc import get_llm

from book_place.schemas import MakeBook, ChoosePlace, BookRead
from book_place.models import Book

from database import get_db

router = APIRouter()

@router.post("/make-book", response_model=MakeBook)
async def make_book(payload: MakeBook, db: AsyncSession = Depends(get_db)):
    stmt = await db.scalars(select(Book).filter(Book.place_name == payload.place_name))
    all_bookings = stmt.first()

    if all_bookings is not None:
        raise HTTPException(status_code=400, detail="This place is already booked at this time")

    category_ = None
    places = None
    with open("places/places.json", "r", encoding="utf-8") as f:
        places = json.load(f)
    for place in places:
        if place["city"] == payload.city and place["name"] == payload.place_name:
            category_ = place["category"]

    book_place = Book(
        user_id=payload.user_id,
        city=payload.city,
        place_name=payload.place_name,
        category=category_,
        booked_for=payload.booked_for,
        is_available=False
    )

    db.add(book_place)
    await db.commit()
    await db.refresh(book_place)

    return MakeBook(
        user_id=book_place.user_id,
        city=book_place.city,
        place_name=book_place.place_name,
        booked_for=book_place.booked_for,
    )

@router.post("/ai")
async def suggested_bookings_list(payload: ChoosePlace):
    answer = get_llm(
        payload.city,
        payload.prefers
    )

    return answer

@router.delete("/delete-booking/{book_id}")
async def delete_user_book(book_id: int, db: AsyncSession = Depends(get_db)):
    needed_booking = await db.get(Book, book_id)

    if not needed_booking:
        raise HTTPException(status_code=404, detail="Not found")

    await db.delete(needed_booking)
    await db.commit()

    return {"ok": True}


@router.get("/user-bookings/{user_id}", response_model=list[BookRead])
async def bookings_list(user_id: int, db: AsyncSession = Depends(get_db)):
    bookings = await db.scalars(select(Book).where(Book.user_id == user_id))
    return bookings.all()