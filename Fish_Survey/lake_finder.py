import json
import requests
import pprint
import csv

def main():
    lake_id = "08004500"
    lake_info = get_lake_info(lake_id)
    
    fish_catch_data = get_fish_catch_summary_data(lake_info)
    fish_length_data = get_fish_length_summary_data(lake_info)

    fish_length_summary_csv(fish_length_data,lake_id)
    fish_catch_summary_csv(fish_catch_data,lake_id)

#JSON response for MN lake id number.
def get_lake_info(lake_id):
    response = requests.get("https://maps2.dnr.state.mn.us/cgi-bin/lakefinder/detail.cgi?type=lake_survey&id="+lake_id)
    return response.json()

#pretty print the json so I know what I'm looking at
def fish_data(d):
    pprint.pprint(d.keys())
    pprint.pprint(d["result"].keys())
    pprint.pprint(d["result"]["surveys"][0].keys())
    pprint.pprint(d["result"]["surveys"][1]["lengths"])

def get_survey_dates(lake_info):
    survey_dates = [lake_info["result"]["surveys"][_]["surveyDate"] for _ in range(len(lake_info["result"]["surveys"]))]
    print(survey_dates)

def get_species_summary_data(d,species):
    species_list = []
    for i in range(len(d["result"]["surveys"])): 
        survey_date = d["result"]["surveys"][i]["surveyDate"]
        survey_id = d["result"]["surveys"][i]["surveyID"]
        for j in range(len(d["result"]["surveys"][i]["fishCatchSummaries"])):
            fish_catch_summary = d["result"]["surveys"][i]["fishCatchSummaries"][j]
            if fish_catch_summary["species"] == species:
                fish_catch_summary["survey_date"] = survey_date
                fish_catch_summary["survey_ID"] = survey_id
                species_list.append(fish_catch_summary)
    pprint.pprint(species_list)

#lake_info is .json() from requests.get
def get_fish_catch_summary_data(lake_info):
    fish_catch_list = []
    for i in range(len(lake_info["result"]["surveys"])): 
        survey_date = lake_info["result"]["surveys"][i]["surveyDate"]
        survey_id = lake_info["result"]["surveys"][i]["surveyID"]
        for j in range(len(lake_info["result"]["surveys"][i]["fishCatchSummaries"])):
            fish_catch_summary = lake_info["result"]["surveys"][i]["fishCatchSummaries"][j]
            fish_catch_summary["survey_date"] = survey_date
            fish_catch_summary["survey_ID"] = survey_id
            fish_catch_list.append(fish_catch_summary)
    return fish_catch_list

def get_fish_length_summary_data(lake_info):
    fish_length_list = []
    for i in range(len(lake_info["result"]["surveys"])): 
        survey_date = lake_info["result"]["surveys"][i]["surveyDate"]
        survey_id = lake_info["result"]["surveys"][i]["surveyID"]
        for j in lake_info["result"]["surveys"][i]["lengths"].keys():
            fish_length_summary = {}
            fish_length_summary["species"] = j
            fish_length_summary["fish_count"] = lake_info["result"]["surveys"][i]["lengths"][j]["fishCount"]
            fish_length_summary["maximum_length"] = lake_info["result"]["surveys"][i]["lengths"][j]["maximum_length"]
            fish_length_summary["minimum_length"] = lake_info["result"]["surveys"][i]["lengths"][j]["minimum_length"]
            fish_length_summary["survey_date"] = survey_date
            fish_length_summary["survey_ID"] = survey_id
            fish_length_list.append(fish_length_summary)
    return fish_length_list

#create .csv of fish catch survey summary
#fish_catch_data = get_fish_catch_summary_data(get_lake_info("lake_id"))
#example: fish_catch_data = get_fish_catch_summary_data(get_lake_info("08004500"))
#lake_id = "08004500"
def fish_catch_summary_csv(fish_catch_data, lake_id):
    with open(f'Resources/{lake_id}_catch.csv', 'w', newline='') as csvfile:
        fieldnames = [
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
        for _ in fish_catch_data:
            writer.writerow(_)
            
def fish_length_summary_csv(fish_length_data, lake_id):
    with open(f'Resources/{lake_id}_lengths.csv', 'w', newline='') as csvfile:
        fieldnames = [
            'species',
            'fish_count',
            'maximum_length',
            'minimum_length',
            'survey_ID',
            'survey_date',
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for _ in fish_length_data:
            writer.writerow(_)

if __name__ == "__main__":
    main()