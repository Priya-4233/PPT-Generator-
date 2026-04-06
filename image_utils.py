import os
import requests
import random
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

HEADERS = {
    "Authorization": PEXELS_API_KEY
}


def get_image(query: str):
    if not PEXELS_API_KEY:
        return None

    url = "https://api.pexels.com/v1/search"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params={
                "query": query,
                "per_page": 10,
                "page": random.randint(1, 3)
            },
            timeout=10
        )

        data = response.json()
        photos = data.get("photos", [])

        if photos:
            return random.choice(photos)["src"]["medium"]

    except Exception as e:
        print("⚠️ Image fetch error:", e)

    return None