import json
import os
import requests

from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
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

EMBED_MODEL = "qllama/multilingual-e5-small"

qdrant = QdrantClient(url=QDRANT_URL)


def create_embedding(text: str):
    response = requests.post(
        f"{OLLAMA_URL}/api/embed",
        json={
            "model": EMBED_MODEL,
            "input": "passage: " + text
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["embeddings"][0]


with open("places.json", "r", encoding="utf-8") as f:
    places = json.load(f)


# Узнаем размерность эмбеддинга
test_vector = create_embedding("test")

vector_size = len(test_vector)


# Создаем коллекцию заново
if qdrant.collection_exists(COLLECTION_NAME):
    qdrant.delete_collection(COLLECTION_NAME)

qdrant.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=vector_size,
        distance=Distance.COSINE
    )
)

points = []

for idx, place in enumerate(places):

    text = f"""
Name: {place['name']}

Category: {place['category']}

Description:
{place[('descripti'
        'on')]}
"""

    vector = create_embedding(text)

    points.append(
        PointStruct(
            id=idx,
            vector=vector,
            payload=place
        )
    )

qdrant.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)
