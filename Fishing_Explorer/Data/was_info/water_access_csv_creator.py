import requests
import csv
import time

def main():
    i = 0
    was_summary_csv_header()
    with open('was_id_list.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            time.sleep(10)
            i += 1
            was_id = row[0]
            was_info = get_was_info(was_id)
            try:
                was_list = []
                was_summary = get_was_summary_data(was_info)
                was_list.append(was_summary)
                was_summary_csv(was_list)
            except TypeError:
                pass
            if i % 50 == 0 and i >= 50:
                print(f"Processing {i}, {was_id}")
    
def get_was_info(was_id):
    response = requests.get("https://maps1.dnr.state.mn.us/cgi-bin/compass/feature_detail.cgi?id="+was_id)
    return response.json()

def get_was_summary_data(was_info):
    was_summary = {}
    was_summary["was_site_id"] = was_info["result"]["id"]
    was_summary["was_site_name"] = was_info["result"]["name"]
    was_summary["directions_to_was_site"] = was_info["result"]["directions"]
    was_summary["was_site_coordinates"] = was_info["result"]["point"]["epsg:4326"]
    was_summary["was_site_administrator"] = was_info["result"]["administrator"]
    was_summary["number_of_docks"] = was_info["result"]["facilities"]["num_docks"]
    was_summary["number_of_restrooms"] = was_info["result"]["facilities"]["num_restrooms"]
    was_summary["number_of_parking_lots"] = was_info["result"]["facilities"]["parking"]["num_lots"]
    was_summary["number_of_handicap_accessible_spaces"] = was_info["result"]["facilities"]["parking"]["num_accessible"]
    was_summary["number_of_trailer_spaces"] = was_info["result"]["facilities"]["parking"]["num_trailer"]
    was_summary["number_of_vehicle_spaces"] = was_info["result"]["facilities"]["parking"]["num_vehicle"]
    was_summary["parking_lot_surface_type"] = was_info["result"]["facilities"]["parking"]["lot_surface"]
    was_summary["number_of_launch_ramps"] = was_info["result"]["facilities"]["launch"]["num_ramps"]
    was_summary["launch_ramp_surface_type"] = was_info["result"]["facilities"]["launch"]["ramp_surface"]
    return was_summary

def was_summary_csv_header():
    with open(f'water_access_information.csv', 'a', newline='') as csvfile:
        fieldnames = [
            "was_site_id",
            "was_site_name",
            "directions_to_was_site",
            "was_site_coordinates",
            "was_site_administrator",
            "number_of_docks",
            "number_of_restrooms",
            "number_of_parking_lots",
            "number_of_handicap_accessible_spaces",
            "number_of_trailer_spaces",
            "number_of_vehicle_spaces",
            "parking_lot_surface_type",
            "number_of_launch_ramps",
            "launch_ramp_surface_type"
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def was_summary_csv(was_list):
    with open(f'water_access_information.csv', 'a', newline='') as csvfile:
        fieldnames = [
            "was_site_id",
            "was_site_name",
            "directions_to_was_site",
            "was_site_coordinates",
            "was_site_administrator",
            "number_of_docks",
            "number_of_restrooms",
            "number_of_parking_lots",
            "number_of_handicap_accessible_spaces",
            "number_of_trailer_spaces",
            "number_of_vehicle_spaces",
            "parking_lot_surface_type",
            "number_of_launch_ramps",
            "launch_ramp_surface_type"
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for _ in was_list:
            writer.writerow(_)

if __name__ == "__main__":
    main()