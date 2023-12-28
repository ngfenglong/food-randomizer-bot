import requests
import os


def generate_food_place() -> dict:
    BASEURL = os.getenv("API_URL")

    url = BASEURL + "/v1/generatePlace"
    response = requests.get(url)

    return response.json()