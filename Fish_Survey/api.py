import psycopg2
from flask import Flask
from flask_cors import CORS
from config import password, fish_db

# method to connect to local postgres
def connect_db(database):
    print("Connecting to the PostgreSQL")
    conn = psycopg2.connect(host="localhost",
                            port=5432,
                            database=database,
                            user="postgres",
                            password=password)
    cur = conn.cursor()
    cur.execute("SELECT version()")
    db_version = cur.fetchone()
    print(f"PostgreSQL database version: {db_version}")
    cur.close()
    return conn

#connect to fish database
conn = connect_db(fish_db)
cur = conn.cursor()

#query lake data for api
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name   = 'lake_info'")
lake_headers = cur.fetchall()
lake_headers = [x[0] for x in lake_headers]
cur.execute("SELECT * FROM lake_info")
lake_info = cur.fetchall()
lake_info = list(lake_info)
lake_api = [{lake_headers[x]: lake_info[y][x] for x in range(len(lake_info[y]))} for y in range(len(lake_info))]

#query city data for api
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name   = 'city_info'")
city_headers = cur.fetchall()
city_headers = [x[0] for x in city_headers]
cur.execute("SELECT * FROM city_info")
city_info = cur.fetchall()
city_info = list(city_info)
city_api = [{city_headers[x]: city_info[y][x] for x in range(len(city_info[y]))} for y in range(len(city_info))]

#query was data for api
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name   = 'water_access_info'")
was_headers = cur.fetchall()
was_headers = [x[0] for x in was_headers]
cur.execute("SELECT * FROM water_access_info")
was_info = cur.fetchall()
was_info = list(was_info)
was_api = [{was_headers[x]: was_info[y][x] for x in range(len(was_info[y]))} for y in range(len(was_info))]

#query fish data for api
cur.execute("SELECT * FROM fish_info")
fish_info = cur.fetchall()
fish_info = dict(fish_info)

#close connection
cur.close()
conn.close()

#create variable for the Flask
app = Flask(__name__)
CORS(app)

@app.route("/")
def welcome():
    #List all available api routes.
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/lakes<br/>"
        f"/api/v1.0/cities<br/>"
        f"/api/v1.0/wateraccess<br/>"
        f"/api/v1.0/fish<br/>"
    )

@app.route("/api/v1.0/lakes")
def get_lakes():
    return lake_api

@app.route("/api/v1.0/cities")
def get_cities():
    return city_api

@app.route("/api/v1.0/wateraccess")
def get_was():
    return was_api

@app.route("/api/v1.0/fish")
def get_fish():
    return fish_info

if __name__ == "__main__":
    app.run(debug=True)