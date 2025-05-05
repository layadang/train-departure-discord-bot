from requests.auth import HTTPBasicAuth
import requests
import os
import json
import pprint
import pytz
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def refresh_all_stops():
    """_summary_
    """
    mbta_api_url = os.getenv("MBTA_API_URL")
    mbta_api_key = os.getenv("MBTA_API_KEY")
    headers = {'Accept': 'application/json'}
    auth = HTTPBasicAuth('apikey', mbta_api_key)

    endpoint_call = "/stops"
    url = mbta_api_url + endpoint_call
    req = requests.get(url=url, headers=headers, auth=auth)

    with open("all_stops.json", "w", encoding='utf-8') as json_file:
        json.dump(req.json(), json_file, ensure_ascii=False, indent=4)

def get_stop_id_by_name(station: str, platform: str) -> str:
    """_summary_

    Args:
        station (str): _description_
        platform (str): _description_

    Returns:
        str: _description_
    """
    with open("all_stops.json") as json_file:
        all_stops = json.load(json_file)
        all_stops_data = all_stops["data"]

    for stop in all_stops_data:
        station_name = stop["attributes"]["name"]
        platform_name = stop["attributes"]["platform_name"]
        
        if (station == station_name) and (platform == platform_name):
            return stop["id"]
    
    return f"Station '{station}' at platform '{platform}' not found."

def get_departure_time(station: str, platform: str) -> list[int, int]:
    """_summary_

    Args:
        station (str): _description_
        platform (str): _description_

    Returns:
        list[int, int]: _description_
    """
    mbta_api_url = os.getenv("MBTA_API_URL")
    mbta_api_key = os.getenv("MBTA_API_KEY")
    headers = {'Accept': 'application/json'}
    auth = HTTPBasicAuth('apikey', mbta_api_key)

    stop_id = get_stop_id_by_name(station, platform)

    endpoint_call = f"/predictions?filter[stop]={stop_id}"
    url = f"{mbta_api_url}{endpoint_call}"
    req = requests.get(url=url, headers=headers, auth=auth).json()

    current_time = datetime.now(pytz.timezone("America/New_York")) 

    all_predictions = req["data"]
    all_arrival_times = []
    for data in all_predictions:
        all_arrival_times.append(data["attributes"]["arrival_time"])

    arrival_time_objects = []
    for arrival_time_str in all_arrival_times:
        arrival_time = datetime.fromisoformat(arrival_time_str)
        if arrival_time > current_time:
            arrival_time_objects.append(arrival_time)

    closest_arrival_time = min(arrival_time_objects, key=lambda x: x - current_time)

    time_difference = closest_arrival_time - current_time
    total_seconds = int(time_difference.total_seconds())

    minutes_left = total_seconds // 60
    seconds_left = total_seconds % 60

    return minutes_left, seconds_left
