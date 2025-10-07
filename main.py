import requests
from fastapi import FastAPI

app = FastAPI(title="Local Weather Tracker")

@app.get("/weather/{city}")
def get_weather(city: str):
    """Get the current weather for a given city."""
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    resp = requests.get(geo_url, params={"name": city, "count": 1})
    data = resp.json()

    if not data.get("results"):
        return {"error": f"City '{city}' not found"}
    
    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_resp = requests.get(weather_url, params={
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    })
    weather_data = weather_resp.json()
    weather = weather_data["current_weather"]
    
    return { 
        "city": city,
        "latitude": lat,
        "longitude": lon,
        "temperature": weather["temperature"],
        "windspeed": weather["windspeed"],
        "time": weather["time"]
    }
 