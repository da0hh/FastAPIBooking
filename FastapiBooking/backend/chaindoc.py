import os
import requests

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue
)


OLLAMA_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://ollama:11434"
)

QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://qdrant:6333"
)

COLLECTION_NAME = "places"

LLM_MODEL = "phi4-mini"

EMBED_MODEL = "qllama/multilingual-e5-small"


qdrant = QdrantClient(
    url=QDRANT_URL
)


# ==========================
# EMBEDDINGS
# ==========================

def create_embedding(text: str, is_query: bool = True):
    prefix = "query: " if is_query else "passage: "
    response = requests.post(
        f"{OLLAMA_URL}/api/embed",
        json={
            "model": EMBED_MODEL,
            "input": prefix + text
        },
        timeout=120
    )
    response.raise_for_status()
    return response.json()["embeddings"][0]


# ==========================
# SEARCH
# ==========================

def search_places(city: str, preferences: str):
    query = f"""
    User request:

    {preferences}

    Find places whose category and description best match this request.
    """
    vector = create_embedding(query, is_query=True)

    result = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        query_filter=Filter(
            must=[FieldCondition(key="city", match=MatchValue(value=city))]
        ),
        limit=10,
        with_payload=True
    )

    total = qdrant.count(
        collection_name=COLLECTION_NAME,
        count_filter=Filter(must=[FieldCondition(key="city", match=MatchValue(value=city))])
    )
    print("Всего точек по городу:", total.count)
    for p in result.points:
        print(p.score, p.payload.get("name"))

    return [item.payload for item in result.points]

# ==========================
# OLLAMA
# ==========================

def ask_ollama(prompt: str):
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7}
        },
        timeout=180
    )
    response.raise_for_status()
    return response.json()["response"]



# ==========================
# MAIN
# ==========================

def get_llm(city: str, prefers: str):

    places = search_places(city, prefers)

    print("FOUND:", len(places))
    print(places)

    print(places)

    if len(places) == 0:
        return {
            "places": [],
            "answer": "No suitable places found."
        }

    context = "\n\n".join(
        f"""
    Name: {p['name']}
    Category: {p['category']}
    Rating: {p['rating']}
    Description: {p['description']}
    Address: {p['place_address_url']}
    """
        for p in places
    )

    prompt = f"""
You are an AI travel assistant.
The user is looking for places in {city}.
User request: 
{prefers}
Below is a list of available places.

For every place pay attention to:
- category
- description
- rating

Categories can be:

Hotel
Restaurant
Museum
Entertainment
Landmark
Park

The user may describe them without using these exact words.

Examples:
hotel = accommodation, sleep, stay overnight
restaurant = food, eat, dinner, lunch
museum = history, exhibition, art
park = nature, walk, relax
landmark = famous place, sightseeing
Choose according to meaning, not exact words.

Recommend only places that really match the user's request.
If the user asks for hotels, do not recommend museums.
If the user asks for restaurants, do not recommend hotels.
If the user asks for parks, recommend parks.
If several places fit, rank them by relevance.

Available places:
{context}

Explain briefly why each place fits.

Return recommendations ONLY from the provided places.

Never invent new places.

Recommend only places that best satisfy the user's request.

Ignore places whose category clearly does not match the request.
"""

    answer = ask_ollama(prompt)

    return {
        "places": places,
        "answer": answer
    }