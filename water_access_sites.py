import requests

def main():
    lake_id = "08004500"

def get_lake_info(lake_id):
    response = requests.get("https://www.dnr.state.mn.us/lakefind/was/report.html?id="+lake_id)
    return response.json()

if __name__ == "__main__":
    main()