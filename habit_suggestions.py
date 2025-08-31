def suggest_habits_based_on_weather(weather_data):
    """
    Suggest habits based on the current weather conditions.

    Expected input: OpenWeatherMap JSON response dictionary

    Returns: A list of habit suggestion strings.
    """
    suggestions = []

    if not weather_data or "weather" not in weather_data:
        return ["No weather data available for suggestions."]

    weather_main = weather_data["weather"][0]["main"].lower()
    temp = weather_data.get("main", {}).get("temp", 20)   

    if weather_main in ["clear", "sunny"]:
        suggestions.append("Great weather for jogging or outdoor exercise!")
        suggestions.append("Perfect day to practice gardening.")
    elif weather_main in ["rain", "drizzle"]:
        suggestions.append("Too wet outside; try indoor yoga or meditation.")
        suggestions.append("Reading a book at home sounds great today.")
    elif weather_main in ["snow"]:
        suggestions.append("Stay warm! Consider indoor workouts or stretching.")
        suggestions.append("Try planning healthy meals or hydration habits.")
    elif weather_main in ["clouds"]:
        if temp >= 15:
            suggestions.append("Nice and cool. Good day for walking or cycling.")
        else:
            suggestions.append("A cooler cloudy day—perfect for light indoor exercises.")
    else:
        suggestions.append("Maintain your usual habit routine.")

    return suggestions
