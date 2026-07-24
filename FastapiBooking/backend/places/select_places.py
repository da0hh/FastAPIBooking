import json
import random
import os

def get_3_popular_places():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "places.json")

    with open(file_path, "r", encoding="utf-8") as f:
        places = json.load(f)

    random_places = random.sample(places, 3)

    return random_places