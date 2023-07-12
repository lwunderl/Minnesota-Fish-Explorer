import csv
import requests
#import key from geoapify
from config import key
import time

def main():

    #write header list to csv
    with open("MN_cities_coordinates.csv", "a", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(["city_name", "city_longitude", "city_latitude"])

    #open csv list of cities to attach coordinates and append to list
    with open("MN_cities_list.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            #store coordinates for writing to csv
            city_coordinates = []
            time.sleep(1)
            print(f"Currently retrieving coordinates for {row}")
            lon_lat = get_city_coordinates(row[0], key)
            lon = lon_lat[0]
            lat = lon_lat[1]
            city_coordinates.append([row[0], lon, lat])

            #write coordinates list to csv
            with open("MN_cities_info.csv", "a", newline="") as file:
                writer = csv.writer(file, delimiter=",")
                for _ in range(len(city_coordinates)):
                    writer.writerow(city_coordinates[_])

#get the coordinates from geoapify
def get_city_coordinates(city, key):
    params = {
        "city": city,
        "state": "MN",
        "country": "United States of America",
        "apiKey": key
    }

    base_url = "https://api.geoapify.com/v1/geocode/search"

    response = requests.get(base_url, params=params).json()

    lon = response["features"][0]["geometry"]["coordinates"][0]
    lat = response["features"][0]["geometry"]["coordinates"][1]

    return [lon, lat]

if __name__ == "__main__":
    main()