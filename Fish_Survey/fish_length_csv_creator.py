import json
import requests
import csv
import time

def main():
    i = 0
    with open('Resources/lake_id_info/lake_id_list.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            time.sleep(10)
            i += 1
            lake_id = row[1]
            lake_info = get_lake_info(lake_id)
            try:
                length_list = []
                length_summary_list = get_fish_length_summary_data(lake_info)
                for length in length_summary_list:
                    length_list.append(length)
                fish_length_summary_csv(length_list)
                if i % 100 == 0 and i >= 100:
                    print(f"Processing {i}")
            except TypeError:
                pass

#JSON response for MN lake id number.
def get_lake_info(lake_id):
    response = requests.get("https://maps2.dnr.state.mn.us/cgi-bin/lakefinder/detail.cgi?type=lake_survey&id="+lake_id)
    return response.json()

def get_fish_length_summary_data(lake_info):
    fish_length_list = []
    for i in range(len(lake_info["result"]["surveys"])): 
        survey_date = lake_info["result"]["surveys"][i]["surveyDate"]
        survey_id = lake_info["result"]["surveys"][i]["surveyID"]
        for j in lake_info["result"]["surveys"][i]["lengths"].keys():
            fish_length_summary = {}
            fish_length_summary["lake_ID"] = lake_info["result"]["DOWNumber"]
            fish_length_summary["lake_name"] = lake_info["result"]["lakeName"]
            fish_length_summary["species"] = j
            fish_length_summary["fish_count"] = lake_info["result"]["surveys"][i]["lengths"][j]["fishCount"]
            fish_length_summary["maximum_length"] = lake_info["result"]["surveys"][i]["lengths"][j]["maximum_length"]
            fish_length_summary["minimum_length"] = lake_info["result"]["surveys"][i]["lengths"][j]["minimum_length"]
            fish_length_summary["survey_date"] = survey_date
            fish_length_summary["survey_ID"] = survey_id
            fish_length_list.append(fish_length_summary)
    return fish_length_list
            
def fish_length_summary_csv(length_list):
    with open(f'Resources/fish_lengths.csv', 'a', newline='') as csvfile:
        fieldnames = [
            'lake_ID',
            'lake_name',
            'species',
            'fish_count',
            'maximum_length',
            'minimum_length',
            'survey_ID',
            'survey_date',
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for _ in length_list:
            writer.writerow(_)

if __name__ == "__main__":
    main()