from flask import Flask, jsonify, request, redirect, render_template
from connect import DB_Connection
import requests
from datetime import datetime

app = Flask(__name__)

# ===== DB INIT =====
db = DB_Connection()
db.init_table()
# ==================

@app.route("/")
def home_view():
    return render_template("index.html")

@app.route("/about")
def about_view():
    return render_template("about.html")

# ================= WEATHER =================
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

    formatted_time = datetime.fromisoformat(weather["time"]).strftime(
        "%b %d, %Y — %I:%M %p"
    )

    return render_template(
        "result.html",
        city=city.title(),
        temperature=weather["temperature"],
        windspeed=weather["windspeed"],
        latitude=lat,
        longitude=lon,
        observation_time=formatted_time
    )

# ================= OBSERVATIONS =================
@app.route("/observations")
def get_all_observations():
    try:
        rows = db.get_all_observations()
    except Exception as e:
        print("DB ERROR:", e)
        return render_template("observations.html", observations=[])

    observations = []
    for r in rows:
        observations.append({
            "id": r[0],
            "city": r[1],
            "country": r[2],
            "latitude": r[3],
            "longitude": r[4],
            "temperature_c": r[5],
            "windspeed_kmh": r[6],
        })

    return render_template("observations.html", observations=observations)

@app.route("/observations/<int:id>", methods=["PUT"])
def update_observation(id):
    data = request.get_json()
    success = db.update_observation_by_id(
        id,
        data["city"],
        data["country"],
        data["latitude"],
        data["longitude"],
        data["temperature_c"],
        data["windspeed_kmh"]
    )
    return jsonify({"message": "Updated successfully"}) if success else jsonify({"error": "Not found"}), 404

@app.route("/observations/<int:id>", methods=["DELETE"])
def delete_observation(id):
    success = db.delete_observation(id)
    return jsonify({"message": "Deleted successfully"}) if success else jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)