import json
import urllib.parse
import urllib.request

# Your API KEYS (replace with your own keys)
from config import MAPBOX_TOKEN, MBTA_API_KEY

# Base URLs for APIs
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, 
    return a Python JSON object containing the response to that request.
    """
    with urllib.request.urlopen(url) as f:
        response_text = f.read().decode('utf-8')
        response_data = json.loads(response_text)
    return response_data

def get_lat_long(place_name: str) -> tuple[float, float]:
    """
    Given a place name or address, return a (latitude, longitude) tuple 
    with the coordinates of the given place.
    """
    query = urllib.parse.quote(place_name)
    url = f'{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}&types=poi'
    response_data = get_json(url)
    coordinates = response_data['features'][0]['geometry']['coordinates']
    longitude, latitude = coordinates
    return latitude, longitude

def get_nearest_station(latitude: float, longitude: float) -> tuple[str, bool]:
    """
    Given latitude and longitude, return a (station_name) tuple 
    for the nearest MBTA station to the given coordinates.
    """
    url = f'{MBTA_BASE_URL}?sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}&api_key={MBTA_API_KEY}'
    response_data = get_json(url)
    if not response_data['data']:
        return "No station found", False
    nearest_station_data = response_data['data'][0]
    station_name = nearest_station_data['attributes']['name']
    return station_name

def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return nearest MBTA stop
    """
    latitude, longitude = get_lat_long(place_name)
    station_name = get_nearest_station(latitude, longitude)
    if not station_name or station_name == "No station found":
        return None, False
    return station_name

def main():
    """
    Test all the above functions here.
    """
    print(get_lat_long('Harrison Avenue'))
    latitude = 42.336848
    longitude = -71.071797
    print(get_nearest_station(latitude, longitude))
    print(find_stop_near("345 Harrison Avenue"))

if __name__ == '__main__':
    main()
