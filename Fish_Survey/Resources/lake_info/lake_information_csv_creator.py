import json
import requests
import csv
import time

def main():
    i = 0
    lake_summary_csv_header()
    with open('lake_id_list.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            time.sleep(10)
            i += 1
            lake_id = row[1]
            lake_info = get_lake_info(lake_id)
            was_info = get_was_info(lake_id)
            try:
                lake_list = []
                lake_summary = get_lake_summary_data(lake_info, was_info)
                lake_list.append(lake_summary)
                lake_summary_csv(lake_list)
            except TypeError:
                print(f"{row[1]} not found...")
                pass
            if i % 100 == 0 and i >= 100:
                print(f"Processing {i}")

def get_lake_info(lake_id):
    response = requests.get("https://maps1.dnr.state.mn.us/cgi-bin/lakefinder_json.cgi?id="+lake_id)
    return response.json()

def get_was_info(lake_id):
    response = requests.get("https://maps2.dnr.state.mn.us/cgi-bin/lakefinder/detail.cgi?type=was&id="+lake_id)
    return response.json()
    
def get_lake_summary_data(lake_info, was_info):
    lake_summary = {}
    lake_summary["lake_ID"] = lake_info["results"][0]["id"]
    lake_summary["Lake Name"] = lake_info["results"][0]["name"]
    lake_summary["Lake County"] = lake_info["results"][0]["county"]
    lake_summary["Nearest Town"] = lake_info["results"][0]["nearest_town"]
    lake_summary["Lake Coordinates"] = lake_info["results"][0]["point"]["epsg:4326"]
    lake_summary["Lake Area"] = lake_info["results"][0]["morphology"]["area"]
    lake_summary["Littoral Area"] = lake_info["results"][0]["morphology"]["littoral_area"]
    lake_summary["Lake Depth"] = lake_info["results"][0]["morphology"]["max_depth"]
    lake_summary["Mean Depth"] = lake_info["results"][0]["morphology"]["mean_depth"]
    try:
        lake_summary["Water Access Sites"] = [was_info["result"]["sites"][_]["id"] for _ in range(len(was_info["result"]["sites"]))]
    except TypeError:
        lake_summary["Water Access Sites"] = []
    return lake_summary

def lake_summary_csv_header():
    with open(f'lake_information.csv', 'a', newline='') as csvfile:
        fieldnames = [
            "lake_ID",
            "Lake Name",
            "Lake County",
            "Nearest Town",
            "Lake Coordinates",
            "Lake Area",
            "Littoral Area",
            "Lake Depth",
            "Mean Depth",
            "Water Access Sites"
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def lake_summary_csv(lake_list):
    with open(f'lake_information.csv', 'a', newline='') as csvfile:
        fieldnames = [
            "lake_ID",
            "Lake Name",
            "Lake County",
            "Nearest Town",
            "Lake Coordinates",
            "Lake Area",
            "Littoral Area",
            "Lake Depth",
            "Mean Depth",
            "Water Access Sites"
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for _ in lake_list:
            writer.writerow(_)

if __name__ == "__main__":
    main()