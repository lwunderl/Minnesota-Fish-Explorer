import csv
import re

def main():
    file_location = "lake_id_list.txt"
    lake_list = txt_filter(file_location)
    lake_list_csv(lake_list, "lake_id_list")

#write csv
def lake_list_csv(lake_list, file_name):
    with open(f'{file_name}.csv', 'w', newline='') as csvfile:
        fieldnames = [
            'county',
            'lake_id',
            'other_info'
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for _ in lake_list:
            writer.writerow(_)

#from https://files.dnr.state.mn.us/waters/watermgmt_section/shoreland/basins_shoreland_classifications.pdf
def txt_filter(txt):
    lake_info = []
    replacement_words = ["Natural", "Environment", "Recreational", "Development", "General"]
    with open(txt, "r") as file:
        for line in file:
            if matches := re.search(r"^(\w*\s?\w*)\s(\d{8})\s(.*)$", line, re.IGNORECASE):
                gr3 = matches.group(3)
                for word in replacement_words:
                    gr3 = gr3.replace(word,"")
                lake_id = {}
                lake_id["county"] = matches.group(1)
                lake_id["lake_id"] = matches.group(2)
                lake_id["other_info"] = gr3
                lake_info.append(lake_id)
    return lake_info

if __name__ == "__main__":
    main()