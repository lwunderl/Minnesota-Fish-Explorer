import requests
import csv
import time

def main():
    i = 0
    was_summary_csv_header()
    with open('Resources/was_id_info/was_id_list.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            i += 1
            was_id = row[0]
            was_info = get_was_info(was_id)
            try:
                was_list = []
                was_summary = get_was_summary_data(was_info)
                was_summary["Site ID"] = was_id
                was_list.append(was_summary)
                was_summary_csv(was_list)
                if i % 50 == 0 and i >= 50:
                    print(f"Processing {i}, {was_id}")
            except TypeError:
                pass
    
def get_was_info(was_id):
    response = requests.get("https://maps1.dnr.state.mn.us/cgi-bin/compass/feature_detail.cgi?id="+was_id)
    return response.json()

def get_was_summary_data(was_info):
    was_summary = {}
    was_summary["Site Name"] = was_info["result"]["name"]
    was_summary["Directions to Site"] = was_info["result"]["directions"]
    was_summary["Site Coordinates"] = was_info["result"]["point"]["epsg:4326"]
    was_summary["Administrator of Site"] = was_info["result"]["administrator"]
    was_summary["Number of Docks"] = was_info["result"]["facilities"]["num_docks"]
    was_summary["Number of Restrooms"] = was_info["result"]["facilities"]["num_restrooms"]
    was_summary["Number of Parking Lots"] = was_info["result"]["facilities"]["parking"]["num_lots"]
    was_summary["Number of Accessible Spaces"] = was_info["result"]["facilities"]["parking"]["num_accessible"]
    was_summary["Number of Trailer Spaces"] = was_info["result"]["facilities"]["parking"]["num_trailer"]
    was_summary["Number of Vehicle Spaces"] = was_info["result"]["facilities"]["parking"]["num_vehicle"]
    was_summary["Parking Lot Surface"] = was_info["result"]["facilities"]["parking"]["lot_surface"]
    was_summary["Number of Ramps"] = was_info["result"]["facilities"]["launch"]["num_ramps"]
    was_summary["Ramp Surface"] = was_info["result"]["facilities"]["launch"]["ramp_surface"]
    return was_summary

def was_summary_csv_header():
    with open(f'Resources/was_id_info/water_access_information.csv', 'a', newline='') as csvfile:
        fieldnames = [
            "Site ID",
            "Site Name",
            "Directions to Site",
            "Site Coordinates",
            "Administrator of Site",
            "Number of Docks",
            "Number of Restrooms",
            "Number of Parking Lots",
            "Number of Accessible Spaces",
            "Number of Trailer Spaces",
            "Number of Vehicle Spaces",
            "Parking Lot Surface",
            "Number of Ramps",
            "Ramp Surface"
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def was_summary_csv(was_list):
    with open(f'Resources/was_id_info/water_access_information.csv', 'a', newline='') as csvfile:
        fieldnames = [
            "Site ID",
            "Site Name",
            "Directions to Site",
            "Site Coordinates",
            "Administrator of Site",
            "Number of Docks",
            "Number of Restrooms",
            "Number of Parking Lots",
            "Number of Accessible Spaces",
            "Number of Trailer Spaces",
            "Number of Vehicle Spaces",
            "Parking Lot Surface",
            "Number of Ramps",
            "Ramp Surface"
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for _ in was_list:
            writer.writerow(_)

if __name__ == "__main__":
    main()