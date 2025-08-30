from flask import Blueprint, request, jsonify
from weather_utils import get_cached_weather, fetch_onecall_weather
from habit_suggestions import suggest_habits_based_on_weather

weather_bp = Blueprint('weather', __name__)

@weather_bp.route("/weather-habits", methods=["GET"])
def weather_and_habits():
    location = request.args.get("location", "Dhaka")
    weather_data = get_cached_weather(location)
    if not weather_data or "coord" not in weather_data:
        return jsonify({"error": "Could not retrieve weather data"}), 500

    lat = weather_data["coord"]["lat"]
    lon = weather_data["coord"]["lon"]
    forecast_data = fetch_onecall_weather(lat, lon)

    habit_suggestions = suggest_habits_based_on_weather(weather_data)

    hourly = forecast_data.get("hourly", []) if forecast_data else []
    daily = forecast_data.get("daily", []) if forecast_data else []

    return jsonify({
        "weather": weather_data,
        "habit_suggestions": habit_suggestions,
        "hourly": hourly,
        "daily": daily
    })
