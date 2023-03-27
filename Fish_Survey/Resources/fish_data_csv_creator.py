import json
import requests
import csv
import time

def main():
    fish_catch_summary_csv_header()
    fish_length_summary_csv_header()
    i = 0
    with open("lake_info/lake_id_info/most_accurate_lake_list.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            time.sleep(10)
            i += 1
            lake_id = row[1]
            lake_info = get_fish_info(lake_id)
            try:
                catch_list = []
                catch_summary_list = get_fish_catch_summary_data(lake_info)
                for catch in catch_summary_list:
                    catch_list.append(catch)
                fish_catch_summary_csv(catch_list)
            except TypeError:
                print(f"{row[1]} CPUE not found...")
                pass

            try:
                length_list = []
                length_summary_list = get_fish_length_summary_data(lake_info)
                for length in length_summary_list:
                    length_list.append(length)
                fish_length_summary_csv(length_list)
            except TypeError:
                print(f"{row[1]} Length not found...")
                pass
            if i % 100 == 0 and i >= 100:
                print(f"Processing {i}")
    print("Process Complete")

#JSON response for MN lake id number.
def get_fish_info(lake_id):
    response = requests.get("https://maps2.dnr.state.mn.us/cgi-bin/lakefinder/detail.cgi?type=lake_survey&id="+lake_id)
    return response.json()

#catch summary data returns a list of dictionaries CPUE's by species by survey ID
def get_fish_catch_summary_data(lake_info):
    fish_catch_list = []
    for i in range(len(lake_info["result"]["surveys"])): 
        survey_date = lake_info["result"]["surveys"][i]["surveyDate"]
        survey_id = lake_info["result"]["surveys"][i]["surveyID"]
        for j in range(len(lake_info["result"]["surveys"][i]["fishCatchSummaries"])):
            fish_catch_summary = lake_info["result"]["surveys"][i]["fishCatchSummaries"][j]
            fish_catch_summary["lake_ID"] = lake_info["result"]["DOWNumber"]
            fish_catch_summary["survey_date"] = survey_date
            fish_catch_summary["survey_ID"] = survey_id
            fish_catch_list.append(fish_catch_summary)
    return fish_catch_list

#write the header of the .csv file
def fish_catch_summary_csv_header():
    with open(f'fish_catch_info/fish_catch.csv', 'a', newline='') as csvfile:
        fieldnames = [
            'lake_ID',
            'CPUE',
            'averageWeight',
            'gear',
            'gearCount',
            'quartileCount',
            'quartileWeight',
            'species',
            'survey_ID',
            'survey_date',
            'totalCatch',
            'totalWeight'
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

#write the rows of the .csv file
def fish_catch_summary_csv(catch_list):
    with open(f'fish_catch_info/fish_catch.csv', 'a', newline='') as csvfile:
        fieldnames = [
            'lake_ID',
            'CPUE',
            'averageWeight',
            'gear',
            'gearCount',
            'quartileCount',
            'quartileWeight',
            'species',
            'survey_ID',
            'survey_date',
            'totalCatch',
            'totalWeight'
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for _ in catch_list:
            writer.writerow(_)

#fish length summary returns a list of dictionaries lengths and counts by species by survey ID
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

#write header for .csv file
def fish_length_summary_csv_header():
    with open(f'fish_length_info/fish_length.csv', 'a', newline='') as csvfile:
        fieldnames = [
            'lake_ID',
            'species',
            'fish_count',
            'maximum_length',
            'minimum_length',
            'survey_ID',
            'survey_date',
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

#write row for .csv file
def fish_length_summary_csv(length_list):
    with open(f'fish_length_info/fish_length.csv', 'a', newline='') as csvfile:
        fieldnames = [
            'lake_ID',
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