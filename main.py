from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route("/")
def home_view():
    """Home view function."""
    return jsonify({
        "message": "Welcome to the Local Weather Tracker!",
    })

@app.route("/about")
def about_view():
    """About view function."""
    return jsonify({"message": "This is the about page of the Local Weather Tracker."})

@app.route("/weather/<city>", methods=["GET"])
def get_weather(city):
    """Get the current weather for a specific city using Open-Meteo API."""
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_resp = requests.get(geo_url, params={"name": city, "count": 1})
    geo_data = geo_resp.json()

    if not geo_data.get("results"):
        return jsonify({"error": f"City '{city}' not found"}), 404

    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_resp = requests.get(weather_url, params={
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    })
    weather_data = weather_resp.json().get("current_weather", {})

    return jsonify({
        "city": city,
        "latitude": lat,
        "longitude": lon,
        "temperature_c": weather_data.get("temperature"),
        "windspeed_kmh": weather_data.get("windspeed"),
        "observation_time": weather_data.get("time")
    })

@app.route("/ingest", methods=["GET", "POST"])
def create_observation():
    """Create a new observation."""
    city = request.args.get("city")
    country = request.args.get("country")
    if not city or not country:
        return jsonify({"error": "Please provide both city and country in your request"}), 400
    
    return jsonify({
        "id": 1,
        "city": city,
        "country": country,
        "latitude": 0.0,
        "longitude": 0.0,
        "temperature_c": 20.0,
        "windspeed_kmh": 5.0,
        "observation_time": "2025-10-20T12:00:00Z",
        "notes": None,
        "message": "pass."
    })

@app.route("/observations", methods=["GET"])
def read_all_observations():
    """Read all observations."""
    pass

@app.route("/observations/<int:observation_id>", methods=["GET"])
def read_one_observation(observation_id):
    """Read a single observation."""
    pass

@app.route("/observations/<int:observation_id>", methods=["PUT"])
def update_observation(observation_id):
    """Update an existing observation."""
    pass

@app.route("/observations/<int:observation_id>", methods=["DELETE"])
def delete_observation(observation_id):
    """Delete an observation."""
    pass

if __name__ == "__main__":
    app.run(debug=True)
