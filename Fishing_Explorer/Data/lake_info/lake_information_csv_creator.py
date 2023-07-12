import requests
import csv
import time

def main():
    i = 0
    lake_summary_csv_header()
    with open("lake_id_info/lake_id_list.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            time.sleep(2)
            i += 1
            lake_id = row[0]
            lake_info = get_lake_info(lake_id)
            was_info = get_was_info(lake_id)
            try:
                lake_list = []
                lake_summary = get_lake_summary_data(lake_info, was_info)
                lake_list.append(lake_summary)
                lake_summary_csv(lake_list)
            except TypeError:
                print(f"{row[0]} not found...")
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
    lake_summary["lake_id"] = lake_info["results"][0]["id"]
    lake_summary["lake_name"] = lake_info["results"][0]["name"]
    lake_summary["lake_county"] = lake_info["results"][0]["county"]
    lake_summary["nearest_town"] = lake_info["results"][0]["nearest_town"]
    lake_summary["lake_coordinates"] = lake_info["results"][0]["point"]["epsg:4326"]
    lake_summary["lake_area"] = lake_info["results"][0]["morphology"]["area"]
    lake_summary["littoral_area"] = lake_info["results"][0]["morphology"]["littoral_area"]
    lake_summary["lake_depth"] = lake_info["results"][0]["morphology"]["max_depth"]
    lake_summary["mean_depth"] = lake_info["results"][0]["morphology"]["mean_depth"]
    try:
        lake_summary["water_access_sites"] = [was_info["result"]["sites"][_]["id"] for _ in range(len(was_info["result"]["sites"]))]
    except TypeError:
        lake_summary["water_access_sites"] = []
    return lake_summary

def lake_summary_csv_header():
    with open(f'lake_information.csv', 'a', newline='') as csvfile:
        fieldnames = [
            "lake_id",
            "lake_name",
            "lake_county",
            "nearest_town",
            "lake_coordinates",
            "lake_area",
            "littoral_area",
            "lake_depth",
            "mean_depth",
            "water_access_sites"
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def lake_summary_csv(lake_list):
    with open(f'lake_information.csv', 'a', newline='') as csvfile:
        fieldnames = [
            "lake_id",
            "lake_name",
            "lake_county",
            "nearest_town",
            "lake_coordinates",
            "lake_area",
            "littoral_area",
            "lake_depth",
            "mean_depth",
            "water_access_sites"
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for _ in lake_list:
            writer.writerow(_)

if __name__ == "__main__":
    main()