import requests
import csv
import re

class Lakes():
    def __init__(self, name):
        self.name = name

    def get_lakes(self, user_input):
        self.input = user_input
        lakes_list =[]
        with open("Resources/lake_id_list.csv") as file:
            for line in file:
                if matches := re.search(rf"^.*{user_input}.*$", line, re.IGNORECASE):
                    county, lake_id, other_info = line.strip().split(",")
                    lakes_list.append({"County":county, "Lake ID": lake_id, "Other Info": other_info})
        return lakes_list

    def lake_map(self, name):
        self.name = name
        lake_id = input("Enter Lake ID: ")
        #https://maps1.dnr.state.mn.us/cgi-bin/mapserv?map=LAKEFINDER_KML_MAPFILE&mode=nquery&lake={lake_id}

class Species():
    def __init__(self, name):
        self.name = name

    def get_species(self, user_input):
        self.input = user_input
        species_list =[]
        with open("Resources/fish_codes.csv") as file:
            for line in file:
                if matches := re.search(rf"^.*{user_input}.*$", line, re.IGNORECASE):
                    desc, fcode = line.strip().split(",")
                    species_list.append({fcode:desc})
        return species_list
