import requests
import json
import os

from config import BASEURL

def generate_food_place():
    url = BASEURL + "/v1/generatePlace"
    response = requests.get(url)

    return response.json()

def fetch_all_places(): 
    url = BASEURL + "/v1/places"
    response = requests.get(url)

    return response.json()

def fetch_all_categories(): 
    url = BASEURL + "/v1/admin/categories"
    response = requests.get(url)
    categories = response.json().get('categories', [])
    return categories

def fetch_all_locations():
    url = BASEURL + "/v1/admin/locations"
    response = requests.get(url)
    locations = response.json().get('locations', [])
    return locations

def format_places(places_response): 
    places = places_response.get('places', [])
    if not places:
        return "No places found."

    formatted_places = []
    for place in places:
        place_id = place.get('id', 'Unknown ID')
        name = place.get('name', 'Unknown')
        description = place.get('description', 'No description')
        category = place.get('category', 'Uncategorized')
        location = place.get('location', 'Location not specified')
        is_halal = "Halal" if place.get('is_halal') else "Not Halal"
        is_vegetarian = "Vegetarian" if place.get('is_vegetarian') else "Non-Vegetarian"
        
        formatted_place = (
            f"ID: {place_id}\n"
            f"Name: {name}\n"
            f"Description: {description}\n"
            f"Category: {category}\n"
            f"Location: {location}\n"
            f"Halal: {is_halal}\n"
            f"Vegetarian: {is_vegetarian}\n"
            "---------------------------\n"
        )
        formatted_places.append(formatted_place)

    return "\n".join(formatted_places)

def delete_place_api(id):
    url = BASEURL + "/v1/admin/deletePlace/" + id
    response = requests.get(url)

    return response.json()

def add_place_api(name, description, category, is_halal, is_vegetarian, location):

    url = BASEURL + "/v1/admin/updatePlace"
    headers = {"Content-Type": "application/json"}
    data = {
        "id": 0,  
        "name": name,
        "description": description,
        "category": str(category),
        "is_halal": is_halal,
        "is_vegetarian": is_vegetarian,
        "location": str(location)
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()