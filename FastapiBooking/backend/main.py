from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from flask import Request

from database import Base, engine
from contextlib import asynccontextmanager
import json

from book_place.router import router as booking_router
from comments.router import router as comments_router
from login.router import router as login_router
#from reviews.router import router as reviews_router
from places.router import router as places_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(comments_router, prefix="/comments", tags=["comments"])
app.include_router(booking_router, prefix="/book", tags=["book"])
app.include_router(login_router, prefix="/login", tags=["login"])
#app.include_router(reviews_router, prefix="/reviews", tags=["reviews"])
app.include_router(places_router, prefix="/places", tags=["places"])

@app.get("/health", tags=["meta"])
async def health():
    return {"status": "ok"}

# print suggested offers
#@app.post("/", response_model=)
#def suggested_places():

LOG_FILE = "requests.json"
@app.middleware("http")
async def process_request(request: Request, call_next):

    client_ip = request.client.host

    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        client_ip = forwarded.split(",")[0].strip()

    method = request.method
    url = str(request.url)
    user_agent = request.headers.get("User-Agent", "Unknown")

    response = await call_next(request)

    log_entry = {
        "ip": client_ip,
        "url": url,
        "user_agent": user_agent,
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    return response