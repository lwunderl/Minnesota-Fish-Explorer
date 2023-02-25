import json
import requests
import pprint
import csv

#JSON response formatted in a list of dictionaries
def noniterated_JSON_response():
    response = requests.get("https://maps2.dnr.state.mn.us/cgi-bin/lakefinder/detail.cgi?type=lake_survey&id=08004500")
    print(json.dumps(response.json(), indent=2))

#JSON response iterated and filtered for key

def get_lake_info(lake_id):
    response = requests.get("https://maps2.dnr.state.mn.us/cgi-bin/lakefinder/detail.cgi?type=lake_survey&id="+lake_id)
    return response.json()

lake_info = get_lake_info("08004500")

def fish_data(d):
    pprint.pprint(d.keys())
    pprint.pprint(d["result"].keys())
    pprint.pprint(d["result"]["surveys"][0].keys())
    pprint.pprint(d["result"]["surveys"][1]["lengths"])

def get_survey_dates(d):
    survey_dates = [d["result"]["surveys"][_]["surveyDate"] for _ in range(len(d["result"]["surveys"]))]
    print(survey_dates)

def get_fish_catch_summaries(d):
    fish_catch_summaries = [{d["result"]["surveys"][_]["surveyDate"]: d["result"]["surveys"][_]["fishCatchSummaries"]} for _ in range(len(d["result"]["surveys"]))]
    pprint.pprint(fish_catch_summaries)

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
    
def get_survey_summary_data(d):
    survey_list = []
    for i in range(len(d["result"]["surveys"])): 
        survey_date = d["result"]["surveys"][i]["surveyDate"]
        survey_id = d["result"]["surveys"][i]["surveyID"]
        for j in range(len(d["result"]["surveys"][i]["fishCatchSummaries"])):
            fish_catch_summary = d["result"]["surveys"][i]["fishCatchSummaries"][j]
            fish_catch_summary["survey_date"] = survey_date
            fish_catch_summary["survey_ID"] = survey_id
            survey_list.append(fish_catch_summary)
    return survey_list

def export_csv(survey_data, lake_id):
    #lake_data = get_survey_summary_data()
    with open(f'Resources/{lake_id}.csv', 'w', newline='') as csvfile:
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
        for _ in survey_data:
            writer.writerow(_)

fish_data(lake_info)