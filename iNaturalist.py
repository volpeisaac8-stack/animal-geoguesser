import requests
import random
import os
from animals import animals


def get_random_animal():

    animal = random.choice(animals)

    url = "https://api.inaturalist.org/v1/observations"

    params = {
        "taxon_name": animal,
        "photos": "true",
        "quality_grade": "research",
        "captive": "false",
        "per_page": 50
    }

    response = requests.get(url, params=params)

    data = response.json()

    result = random.choice(data["results"])

    if len(data["results"]) == 0:
        return get_random_animal()

    name = result["taxon"].get(
    "preferred_common_name",
    result["taxon"]["name"]
    )

    lat = result["geojson"]["coordinates"][1]
    lon = result["geojson"]["coordinates"][0]

    photo_url = result["photos"][0]["url"]
    photo_url = photo_url.replace("square", "large")

    # download image
    img_data = requests.get(photo_url).content

    image_path = "images/current.jpg"

    with open(image_path, "wb") as f:
        f.write(img_data)

    return {
        "name": name,
        "lat": lat,
        "lon": lon,
        "image": image_path
    }