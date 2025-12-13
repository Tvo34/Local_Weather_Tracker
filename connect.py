import psycopg
from psycopg import OperationalError
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

print("DEBUG DB_NAME =", DB_NAME)


#local DB config-> move to .env for security

class DB_Connection:
    def __init__(self):
        self.connection = psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
          

    def init_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS weather_observation (
            id SERIAL PRIMARY KEY,
            city TEXT,
            country TEXT,
            latitude FLOAT,
            longitude FLOAT,
            temperature_c FLOAT,
            windspeed_kmh FLOAT,
            observation_time TIMESTAMP,
            notes TEXT
        );
        """
        with self.connection.cursor() as cur:
            cur.execute(query)
            self.connection.commit()

    def create_weather_observation(
        self, city, country, latitude, longitude,
        temperature_c, windspeed_kmh, observation_time=None, notes=None
    ):
        try:
            query = """
            INSERT INTO weather_observation
            (city, country, latitude, longitude, temperature_c, windspeed_kmh, observation_time, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            with self.connection.cursor() as cur:
                cur.execute(query, (
                    city, country, latitude, longitude,
                    temperature_c, windspeed_kmh, observation_time, notes
                ))
                self.connection.commit()

        except Exception as e:
            self.connection.rollback()
            print("Error creating observation:", e)

    def get_all_observations(self):
        try:
            query = "SELECT * FROM weather_observation ORDER BY id;"
            with self.connection.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()
        except Exception as e:
            print("Error fetching observations:", e)
            return []
        

    def get_observation_by_id(self, observation_id):
        try:
            query = "SELECT * FROM weather_observation WHERE id = %s;"
            with self.connection.cursor() as cur:
                cur.execute(query, (observation_id,))
                return cur.fetchone()
        except Exception as e:
            print("Error fetching observation:", e)
            return None

    def update_observation_by_id(
        self, observation_id, city, country,
        latitude, longitude, temperature_c, windspeed_kmh
    ):
        try:
            query = """
            UPDATE weather_observation
            SET city=%s,
                country=%s,
                latitude=%s,
                longitude=%s,
                temperature_c=%s,
                windspeed_kmh=%s
            WHERE id=%s;
            """
            with self.connection.cursor() as cur:
                cur.execute(query, (
                    city, country, latitude, longitude,
                    temperature_c, windspeed_kmh, observation_id
                ))
                self.connection.commit()
                return cur.rowcount > 0

        except Exception as e:
            self.connection.rollback()
            print("Error updating observation:", e)
            return False


    def update_latitude_and_longitude(self, id, latitude, longitude):
        """Update latitude and longitude for a specific observation."""
        try:
            self.cursor = self.connection.cursor()

            update_query = "UPDATE weather_observation SET latitude = %s, longitude = %s WHERE id = %s;"
            self.cursor.execute(update_query, (latitude, longitude, id))
            self.connection.commit()
            print(f"Updated observation ID {id} with new latitude and longitude.")

        except (Exception, psycopg.Error) as error:
            print(f"Error updating observation: {error}")
            if self.connection:
                self.connection.rollback()

        finally:
            if self.connection:
                self.cursor.close()
                # self.connection.close()


    def delete_observation(self, observation_id):
        try:
            query = "DELETE FROM weather_observation WHERE id = %s;"
            with self.connection.cursor() as cur:
                cur.execute(query, (observation_id,))
                self.connection.commit()
                return cur.rowcount > 0

        except Exception as e:
            self.connection.rollback()
            print("Error deleting observation:", e)
            return False

    