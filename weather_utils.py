import requests
import json
from datetime import datetime, timedelta
from models import db, WeatherPreference
import os
from dotenv import load_dotenv

load_dotenv() 

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def fetch_weather_from_api(location):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_onecall_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&exclude=minutely,alerts"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def get_cached_weather(location):
    weather_entry = WeatherPreference.query.filter_by(user_location=location).first()
    now = datetime.utcnow()
    if weather_entry and weather_entry.last_updated and (now - weather_entry.last_updated) < timedelta(minutes=30):
        return json.loads(weather_entry.weather_data)

    fresh_data = fetch_weather_from_api(location)
    if not fresh_data:
        if weather_entry:
            return json.loads(weather_entry.weather_data)
        return None

    if not weather_entry:
        weather_entry = WeatherPreference(user_location=location)
        db.session.add(weather_entry)

    weather_entry.weather_data = json.dumps(fresh_data)
    weather_entry.last_updated = now
    db.session.commit()
    return fresh_data
