import psycopg2
import numpy as np
from flask import Flask
from flask_cors import CORS
import requests
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

#default YYYY-MM-DD format, datetime64
start_date = "2000-01-01"
#default gear from gear list, string, optional
gear = "Standard gill nets"

#convert coordinate lat or lon from degrees to radians; coordinate = -94.728528
def get_radians(coordinate):
    radian = coordinate*np.pi/180
    return radian

#calculate distance between 2 geographic degree points; lon1 = -94.728528 , lat1 = 44.308025
def get_distance(lat1, lon1, lat2, lon2):
    distance = np.arccos(np.sin(get_radians(lat1))*np.sin(get_radians(lat2)) + np.cos(get_radians(lat1))*np.cos(get_radians(lat2)) * np.cos(get_radians(lon2)-get_radians(lon1)))*3958.8
    return distance

#JSON response for MN lake id number.
def get_catch_info(lake_id):
    response = requests.get("https://maps2.dnr.state.mn.us/cgi-bin/lakefinder/detail.cgi?type=lake_survey&id="+lake_id)
    return response.json()

#fish catch summary returns a list of dictionaries cpue by species by survey ID using API response
def get_fish_catch_summary_data(catch_info):
    fish_catch_list = []
    for i in range(len(catch_info["result"]["surveys"])): 
        survey_date = catch_info["result"]["surveys"][i]["surveyDate"]
        survey_id = catch_info["result"]["surveys"][i]["surveyID"]
        for j in range(len(catch_info["result"]["surveys"][i]["fishCatchSummaries"])):
            fish_catch_summary = catch_info["result"]["surveys"][i]["fishCatchSummaries"][j]
            fish_catch_summary["lake_ID"] = catch_info["result"]["DOWNumber"]
            fish_catch_summary["survey_date"] = survey_date
            fish_catch_summary["survey_ID"] = survey_id
            fish_catch_list.append(fish_catch_summary)
    return fish_catch_list

#fish length summary returns a list of dictionaries lengths and counts by species by survey ID using API response
def get_fish_length_summary_data(lake_info):
    fish_length_list = []
    for i in range(len(lake_info["result"]["surveys"])): 
        survey_date = lake_info["result"]["surveys"][i]["surveyDate"]
        survey_id = lake_info["result"]["surveys"][i]["surveyID"]
        for j in lake_info["result"]["surveys"][i]["lengths"].keys():
            fish_length_summary = {}
            fish_length_summary["lake_ID"] = lake_info["result"]["DOWNumber"]
            fish_length_summary["species"] = j
            fish_length_summary["fish_count"] = lake_info["result"]["surveys"][i]["lengths"][j]["fishCount"]
            fish_length_summary["maximum_length"] = lake_info["result"]["surveys"][i]["lengths"][j]["maximum_length"]
            fish_length_summary["minimum_length"] = lake_info["result"]["surveys"][i]["lengths"][j]["minimum_length"]
            fish_length_summary["survey_date"] = survey_date
            fish_length_summary["survey_ID"] = survey_id
            fish_length_list.append(fish_length_summary)
    return fish_length_list

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
        f"/api/v1.0/lake_results/city_name/distance_in_miles<br/>"
        f"/api/v1.0/survey_results/city_name/distance_in_miles/species_code"
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

@app.route("/api/v1.0/lake_results/<city>/<distance>")
def get_lake_results(city, distance):
    lake_list = get_lake_list(city, distance)
    return [{"lake_results": len(lake_list)},lake_list]

@app.route("/api/v1.0/survey_results/<city>/<distance>/<species>")
def get_survey_results(city, distance, species):
    #set species variable to uppercase
    species = species.upper()

    #variable for species name to be used in dictionary for return
    species_name = fish_info.get(species)

    #get nearby lakes
    lake_list = get_lake_list(city, distance)

    #get fish cpue data from outside api
    fish_data = [get_catch_info(x["lake_id"]) for x in lake_list if get_catch_info(x["lake_id"])["status"] == "SUCCESS"]

    cpue_list = []
    for _ in range(len(fish_data)):
        catch = get_fish_catch_summary_data(fish_data[_])
        for _ in range(len(catch)):
            sample = catch[_]
            if sample["species"] == species and sample["survey_date"] > start_date and sample["gear"] == gear:
                cpue_list.append(sample)

    #get fish length data from same api
    length_list = []
    for _ in range(len(fish_data)):
        catch = get_fish_length_summary_data(fish_data[_])
        for _ in range(len(catch)):
            sample = catch[_]
            if sample["species"] == species and sample["survey_date"] > start_date:
                fish_count = []
                for _ in sample["fish_count"]:
                    fish_count.extend([_[0]]*_[1])
                fish_count_clean = [x for x in fish_count if x > 2]
                sample["fish_count"] = fish_count_clean
                length_list.append(sample)
    
    cpue_statistics = []
    for lake in lake_list:
        cpue_hist = []
        cpue_median = 0
        for cpue in cpue_list:
            if lake["lake_id"] == cpue["lake_ID"]:
                cpue_hist.append(float(cpue["CPUE"]))
        if cpue_hist:
            cpue_median = np.median(np.array(cpue_hist))
            cpue_statistics.append({"lake_name": lake["lake_name"], 
                                "cpue_median": cpue_median,
                                "cpue_histogram": cpue_hist,
                                "species": species,
                                "lake_id": lake["lake_id"],
                                "species_name": species_name})

    length_statistics = []
    for lake in lake_list:
        lake_hist = []
        for length in length_list:
            if lake["lake_id"] == length["lake_ID"]:
                lake_hist.extend(length["fish_count"])
        if lake_hist:
            lake_ave = round(np.average(lake_hist),2)
            length_statistics.append({"length_histogram": lake_hist,
                                      "length_average": lake_ave,
                                      "lake_id": lake["lake_id"],
                                      "lake_name": lake["lake_name"],
                                      "species": species,
                                      "species_name": species_name})

    return [{"total_cpue_results": len(cpue_list), "cpue_results": cpue_list}, 
            {"total_length_results": len(length_list), "length_results": length_list}, 
            {"cpue_statistics_results": len(cpue_statistics), "cpue_statisitcs": cpue_statistics},
            {"length_statistics_results": len(length_statistics), "length_statistics": length_statistics}]

if __name__ == "__main__":
    app.run(debug=True)