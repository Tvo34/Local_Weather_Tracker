from flask import Flask, jsonify, request, render_template
from connect import DB_Connection as db

import requests


app = Flask(__name__)

@app.route("/")
def home_view():
    return render_template("index.html")
    
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

@app.route("/ingest", methods=["GET"])
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

@app.route("/observations/<int:observation_id>", methods=['GET'])
def get_observation(observation_id):
    """Fetch weather oservation by ID"""
    results = db().get_observation_by_id(observation_id)
    
    if results:
        observation_dict = {
            "id": results[0],
            "city": results[1],
            "country": results[2],
            "latitude": results[3],
            "longitude": results[4],
            "temperature_c": results[5],
            "windspeed_kmh": results[6],
            "observation_time": results[7],
            "notes": results[8]
        }
        return jsonify(observation_dict)
    else:
        return jsonify({"error": f"No observation found with ID {observation_id}"}), 404

@app.route("/observations/<int:observation_id>", methods=["PUT"])
def update_observation(observation_id):
    """Update an observation by id."""
    data = request.get_json()
    
    city = data.get("city")
    country = data.get("country")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    temperature_c = data.get("temperature_c")
    windspeed_kmh = data.get("windspeed_kmh")

    database = db()
    database.update_observation_by_id(
        observation_id, city, country, latitude, longitude, temperature_c, windspeed_kmh
    )

    return jsonify({"message": f"Observation {observation_id} updated successfully"})

@app.route("/observations", methods=["GET"])
def get_all_observations():
    """Fetch all weather observations."""
    results = db().get_all_observations()

    if results:
        observations_list = []
        for row in results:
            observation_dict = {
                "id": row[0],
                "city": row[1],
                "country": row[2],
                "latitude": row[3],
                "longitude": row[4],
                "temperature_c": row[5],
                "windspeed_kmh": row[6],
                "observation_time": row[7],
                "notes": row[8]
            }
            observations_list.append(observation_dict)

        return jsonify(observations_list)
    else:
        return jsonify({"message": "No observations found"}), 200


@app.route("/observations/<int:observation_id>", methods=["DELETE"])
def delete_observation(observation_id):
    """Delete an observation by ID."""
    database = db()
    database.delete_observation(observation_id)
    return jsonify({"message": f"Observation {observation_id} deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
