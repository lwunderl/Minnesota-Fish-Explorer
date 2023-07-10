import csv
import requests
from config import key
import time

def main():
    city_coordinates = []
    with open("MN_cities_list.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row[0])
            time.sleep(1)
            lon_lat = get_city_coordinates(row[0], key)
            print(lon_lat)
            lon = lon_lat[0]
            lat = lon_lat[1]
            city_coordinates.append([row[0], lon, lat])
    with open("MN_cities_coordinates.csv", "a", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(["city_name", "city_longitude", "city_latitude"])
        for _ in range(len(city_coordinates)):
            writer.writerow(city_coordinates[_])

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