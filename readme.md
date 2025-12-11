# Local Weather Tracker 

A python application that fetches real-time weather data from Open-Meteo API and stores it in a PostgreSQL database. Perfect for tracking weather patterns and building weather-related applications.

**Key Features:**
- Real-time weather data from 10 cities
- PostgreSQL database storage
- RESTful API endpoints
- Easy-to-use Python interface
- Simple HTML homepage template


## Installation

#### Required software
- Python 3.12.7
- PostgreSQL 16

#### libraries

- psycopg 
- requests
- flask
- dotenv

## Steps
1. Clone the repository

```bash
git clone https://github.com/Tvo34/Local_Weather_Tracker.git
```

2. Install dependencies
```bash
pip install -r requirements.txt 
```
3. Set up database
```bash
createdb weather_observation
```
4. Configure environment variables
```bash
create .env
```
```bash
username=YOUR_USERNAME
password=YOUR_PASSWORD
database=weather_observation
host=localhost
port=5432
```


## Usage

#### Running the App

1. Start with Flask app
```bash
python main.py
```
2. Copy the URL shown in your terminal and paste it into your browser. Or you can use Postman to test the result.

for example: I will paste this URL into my browser/Postman
```bash 
http://127.0.0.1:5000
```
#### Get weather for a city


```bash 
http://127.0.0.1:5000/weather/Chicago
```

#### View all observations
```bash
http://127.0.0.1:5000/observations
```

#### View observation by id
```bash
http://127.0.0.1:5000/observations/1
```








