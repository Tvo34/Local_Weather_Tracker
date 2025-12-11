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

class DB_Connection: #this class handles DB conncection & operations

    def __init__(self): #opens a DB connection on initialization
        self.connection = psycopg.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
        self.cursor = self.connection.cursor()


    def create_weather_observation(self, id, city, country, latitude, longitude, temperature_c, windspeed_kmh):
        """Create a new weather observation in the database."""
        try:
            insert_query = """
            INSERT INTO weather_observation (id, city, country, latitude, longitude, temperature_c, windspeed_kmh)
            VALUES (%s, %s, %s, %s, %s, %s, %s);"""

            self.cursor.execute(insert_query, (id, city, country, latitude, longitude, temperature_c, windspeed_kmh))

            self.connection.commit()
            print(f"New observation created with city: {city}")
        #Run SQL INSERT statement -> execute it using placeholder
        # Commits the transaction to save data    

        #self. (this objects stores its own database connection)
        #if no self. -> the variable exists only inside the function

        except (Exception, psycopg.Error) as error:
            print(f"Error while creating observation: {error}")
            if self.connection:
                self.connection.rollback()
        #if error rollback is used to keep the db        
        
        finally:
            if self.connection:
                self.cursor.close()
                # self.connection.close()
        #always run. close cursor to prevent memory leaks

    def get_all_observations(self):
        """Retrieve all weather observations from the database."""
        try:
            # self.connection = psycopg.connect(
            #     dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
            # )
            self.cursor = self.connection.cursor()
            select_query = "SELECT * FROM weather_observation;"
            self.cursor.execute(select_query)
            return self.cursor.fetchall()
        except Exception as error:
            print(f"Error fetching observation by id: {error}")
            return []
        

    def get_observation_by_id(self, observation_id):
        """Retrieve a specific observation by its ID."""
        try:
            self.cursor = self.connection.cursor()

            select_query = "SELECT * FROM weather_observation WHERE id = %s;"
            self.cursor.execute(select_query, (observation_id,))
            observation = self.cursor.fetchone()
            return observation
        except (Exception, psycopg.Error) as error:
            print(f"Error fetching observation by ID: {error}")
            return None
        finally:
            if self.connection:
                self.cursor.close()
                # self.connection.close()

    def update_observation_by_id(self, observation_id, city, country, latitude, longitude, temperature_c, windspeed_kmh):
        """Updates observation by ID."""
        try:
            self.cursor = self.connection.cursor()

            update_query = """
            UPDATE weather_observation
            SET city = %s,
                country = %s,
                latitude = %s,
                longitude = %s,
                temperature_c = %s,
                windspeed_kmh = %s
            WHERE id = %s;
            """
            self.cursor.execute(
                update_query,(city, country, latitude, longitude, temperature_c, windspeed_kmh, observation_id))

            rows_affected = self.cursor.rowcount #check how many rows were affected

            if rows_affected > 0: #at least 1 line is fixed
                print(f"Successfully updated observation with ID {observation_id}.")
                self.connection.commit()
            else:
                print(f"No observation found with ID {observation_id}. No update performed.")

        except (Exception, psycopg.Error) as error:
            print(f"Error updating observation: {error}")
            if self.connection:
                self.connection.rollback()

        finally:
            if self.connection:
                self.cursor.close()
                # self.connection.close()


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
        """Delete a specific observation by its ID."""
        print(observation_id)

        try:            
            self.cursor = self.connection.cursor()
            
            delete_query = "DELETE FROM weather_observation WHERE id = %s;"
            self.cursor.execute(delete_query, (observation_id,))
            rows_affected = self.cursor.rowcount

            if rows_affected > 0:
                print(f"Successfully deleted observation with id: {observation_id}")
                self.connection.commit()
            else:
                print(f"No observation found with ID: {observation_id}. Nothing deleted.")

        except (Exception, psycopg.Error) as error:
            print(f"Error deleting observation: {error}")
            if self.connection:
                self.connection.rollback()

        finally:
            if self.connection:
                self.cursor.close()
                # self.connection.close()

    def close(self):
        if self.connection:
            self.cursor.close()
            # self.connection.close()
                   
