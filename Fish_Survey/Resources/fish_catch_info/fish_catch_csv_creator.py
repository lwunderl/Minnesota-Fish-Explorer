import json
import requests
import csv
import time

def main():
    fish_catch_summary_csv_header()
    i = 0
    with open('../lake_id_info/lake_id_list.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            time.sleep(10)
            i += 1
            lake_id = row[1]
            lake_info = get_lake_info(lake_id)
            try:
                catch_list = []
                catch_summary_list = get_fish_catch_summary_data(lake_info)
                for catch in catch_summary_list:
                    catch_list.append(catch)
                fish_catch_summary_csv(catch_list)
                if i % 100 == 0 and i >= 100:
                    print(f"Processing {i}")
            except TypeError:
                print(f"{row[1]} not found...")
                pass

#JSON response for MN lake id number.
def get_lake_info(lake_id):
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
    with open(f'fish_catch.csv', 'a', newline='') as csvfile:
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
    with open(f'fish_catch.csv', 'a', newline='') as csvfile:
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

if __name__ == "__main__":
    main()