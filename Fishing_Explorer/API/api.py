import psycopg2
import numpy as np
from flask import Flask
from flask_cors import CORS
import json
#you'll need a config.py file in this same folder that has 2 variables, password = "your_password" and fish_db = "your_database_name"
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
#fetch the column headers to make a dictionary for json display; your table_schema name may be named something other than "public"
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'lake_info'")
lake_headers = cur.fetchall()
lake_headers = [x[0] for x in lake_headers]
cur.execute("SELECT * FROM lake_info")
lake_info = cur.fetchall()
lake_info = list(lake_info)
lake_api = [{lake_headers[x]: lake_info[y][x] for x in range(len(lake_info[y]))} for y in range(len(lake_info))]
for _ in lake_api:
    _["water_access_sites"] = json.loads(_["water_access_sites"].replace("\'",'\"'))

#query city data for api
#fetch the column headers to make a dictionary for json display; your table_schema name may be named something other than "public"
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'city_info'")
city_headers = cur.fetchall()
city_headers = [x[0] for x in city_headers]
cur.execute("SELECT * FROM city_info")
city_info = cur.fetchall()
city_info = list(city_info)
city_api = [{city_headers[x]: city_info[y][x] for x in range(len(city_info[y]))} for y in range(len(city_info))]

#query was data for api
#fetch the column headers to make a dictionary for json display; your table_schema name may be named something other than "public"
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'water_access_info'")
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

#query survey gear data for api
cur.execute("SELECT gear FROM gear_info")
gear_info = cur.fetchall()
gear_info = [x[0] for x in gear_info]

#close connection
print("Closing PostgreSQL connection.")
cur.close()
conn.close()
print("PostgreSQL connection now closed.")

#convert coordinate lat or lon from degrees to radians; coordinate = -94.728528
def get_radians(coordinate):
    radian = coordinate*np.pi/180
    return radian

#calculate distance between 2 geographic degree points; lon1 = -94.728528 , lat1 = 44.308025
def get_distance(lat1, lon1, lat2, lon2):
    distance = np.arccos(np.sin(get_radians(lat1))*np.sin(get_radians(lat2)) + np.cos(get_radians(lat1))*np.cos(get_radians(lat2)) * np.cos(get_radians(lon2)-get_radians(lon1)))*3958.8
    return distance

#create list of lakes by distance from chosen city
def get_lake_list(city, distance):
    lake_list = []
    for row in city_api:
        if row["city_name"] == city.title():
            city_longitude = float(row["city_longitude"])
            city_latitude = float(row["city_latitude"])
            for lake in lake_api:
                lake_latitude = float(lake["lake_latitude"])
                lake_longitude = float(lake["lake_longitude"])
                if get_distance(city_latitude, city_longitude, lake_latitude, lake_longitude) < float(distance):
                    lake_list.append(lake)
    return lake_list

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
        f"/api/v1.0/gear<br/>"
        f"/api/v1.0/lake_results/city_name/distance_in_miles<br/>"
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

@app.route("/api/v1.0/gear")
def get_gear():
    return gear_info

@app.route("/api/v1.0/lake_results/<city>/<distance>")
def get_lake_results(city, distance):

    #get lake data 
    lake_list = get_lake_list(city, distance)
    #get string list of lake ID's to pass into SQL query
    lake_ids = str([x["lake_id"] for x in lake_list]).replace("[","(").replace("]",")")

    #connect to fish database
    conn = connect_db(fish_db)
    cur = conn.cursor()

    #get cpue headers
    #fetch the column headers to make a dictionary for json display; your table_schema name may be named something other than "public"
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'cpue_info'")
    cpue_headers = cur.fetchall()
    cpue_headers = [x[0] for x in cpue_headers]

    #get length headers
    #fetch the column headers to make a dictionary for json display; your table_schema name may be named something other than "public"
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'length_info'")
    length_headers = cur.fetchall()
    length_headers = [x[0] for x in length_headers]

    #retrieve cpue and length data
    if lake_list:

        cpue_api = []
        cur.execute(f"SELECT * FROM cpue_info WHERE lake_id IN {lake_ids}")
        while True:
            cpue_info = cur.fetchmany(500)
            if cpue_info:
                cpue_info = list(cpue_info)
                cpue_info_list = [{cpue_headers[x]: cpue_info[y][x] for x in range(len(cpue_info[y]))} for y in range(len(cpue_info))] 
                cpue_api.extend(cpue_info_list)
            else:
                break

        length_api = []
        cur.execute(f"SELECT * FROM length_info WHERE lake_id IN {lake_ids}")
        while True:
            length_info = cur.fetchmany(500)
            if length_info:
                length_info = list(length_info)
                length_info_list = [{length_headers[x]: length_info[y][x] for x in range(len(length_info[y]))} for y in range(len(length_info))]
                for _ in length_info_list:
                    _["fish_count"] = json.loads(_["fish_count"])
                length_api.extend(length_info_list)
            else:
                break

        return [{"total_lake_results": len(lake_list), "lake_results": lake_list},
                {"total_cpue_results": len(cpue_api), "cpue_results": cpue_api},
                {"total_length_results": len(length_api), "length_results": length_api}
                ]

    #close connection to fish database
    print("Closing PostgreSQL connection.")
    cur.close()
    conn.close()
    print("PostgreSQL connection now closed.")

    return [{"total_lake_results": 0, "lake_results": "No results"},
            {"total_cpue_results": 0, "cpue_results": "No results"},
            {"total_length_results": 0, "length_results": "No results"}]

if __name__ == "__main__":
    app.run(debug=True)