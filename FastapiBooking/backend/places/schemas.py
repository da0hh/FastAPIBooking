from pydantic import BaseModel

class PlaceOut(BaseModel):
    name: str
    city: str
    rating: float
    description: str
