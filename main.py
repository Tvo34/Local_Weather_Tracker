from flask import Flask, jsonify, request, redirect, render_template
from connect import DB_Connection as db
import requests, os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home_view():
    return render_template("index.html")

@app.route("/about")
def about_view():
    return render_template("about.html")


@app.route("/weather/<city>")
def show_weather(city):


    geo_resp = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1}
    ).json()

    if not geo_resp.get("results"):
        return "City not found", 404

    lat = geo_resp["results"][0]["latitude"]
    lon = geo_resp["results"][0]["longitude"]

    weather_resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "timezone": "auto"
        }
    ).json()

    weather = weather_resp["current_weather"]

    temperature = weather["temperature"]
    windspeed = weather["windspeed"]
    time_iso = weather["time"]

    temperature_f = (temperature * 9/5) + 32    


    formatted_time = datetime.fromisoformat(time_iso).strftime("%b %d, %Y — %I:%M %p")

    return render_template(
        "result.html",
        city=city.title(),
        temperature=temperature,
        temperature_f=temperature_f,
        windspeed=windspeed,
        latitude=lat,
        longitude=lon,
        observation_time=formatted_time
    )



@app.route("/weather", methods=["GET"])
def weather_search():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "No city provided"}), 400

    return redirect(f"/weather/{city}")


@app.route("/ingest", methods=["GET"])
def create_observation():
    city = request.args.get("city")
    country = request.args.get("country")

    if not city or not country:
        return jsonify({"error": "Please provide both city and country"}), 400

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


@app.route("/observations/<int:observation_id>", methods=["GET"])
def get_observation(observation_id):
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
    data = request.get_json()

    db().update_observation_by_id(
        observation_id,
        data.get("city"),
        data.get("country"),
        data.get("latitude"),
        data.get("longitude"),
        data.get("temperature_c"),
        data.get("windspeed_kmh")
    )

    return jsonify({"message": f"Observation {observation_id} updated successfully"})


@app.route("/observations", methods=["GET"])
def get_all_observations():
    results = db().get_all_observations()

    observations_list = []
    if results:
        for row in results:
            observations_list.append({
                "id": row[0],
                "city": row[1],
                "country": row[2],
                "latitude": row[3],
                "longitude": row[4],
                "temperature_c": row[5],
                "windspeed_kmh": row[6],
                "observation_time": row[7],
                "notes": row[8]
            })

    return render_template("observations.html", observations=observations_list)


@app.route("/observations/<int:observation_id>", methods=["DELETE"])
def delete_observation(observation_id):
    db().delete_observation(observation_id)
    return jsonify({"message": f"Observation {observation_id} deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
