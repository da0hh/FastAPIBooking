from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import List
import os
import json

from places.models import Place
from places.schemas import PlaceOut
from places.select_places import get_3_popular_places

router = APIRouter()

@router.get("/place-list", response_model=List[PlaceOut])
async def places_list(db: AsyncSession = Depends(get_db)):
    places = await db.scalars(select(Place))

    return places.all()

@router.get("/get-place/{place_name}", response_model=PlaceOut)
async def get_place(place_name: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "places.json") # или "..", "places.json"

    if not os.path.exists(file_path):
        raise HTTPException(detail="JSON file not found", status_code=500)

    with open(file_path, "r", encoding="utf-8") as f:
        places = json.load(f)

    for place in places:
        if place["name"] == place_name:
            return place

    raise HTTPException(
        detail=f"Place '{place_name}' not found in JSON file",
        status_code=404
    )

@router.post("/category/{category}", response_model=PlaceOut)
async def find_places_category(category: str, db: AsyncSession = Depends(get_db)):
    places = await db.scalars(select(Place).filter(Place.category == category))

    return places.all()

@router.post("/city/{city}", response_model=PlaceOut)
async def find_places_city(city: str, db: AsyncSession = Depends(get_db)):
    places = await db.scalars(select(Place).where(Place.city == city))

    return places.all()

@router.get("/descriptions")
async def get_descriptions(db: AsyncSession = Depends(get_db)):
    result = await db.scalars(select(Place))
    places = result.all()

    return [
        {
            "id": place.id,
            "description": place.description
        }
        for place in places
    ]

@router.get("/popular3places")
async def get_popular_places():
    return get_3_popular_places()