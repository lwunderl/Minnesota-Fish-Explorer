from splinter import Browser
from bs4 import BeautifulSoup as soup
import csv

#set browser
browser = Browser("chrome")

#wikipedia list of cities in Minnesota
url = "https://en.wikipedia.org/wiki/List_of_cities_in_Minnesota"

#visit browser and scrape city names
browser.visit(url)
browser.is_element_present_by_css("td", wait_time=1)
html = browser.html
city_page = soup(html, "html.parser")
city_table = city_page.find("tbody")
city_places = city_table.find_all("a")

minnesota_places = [place["title"] for place in city_places if "County" not in place["title"]]

minnesota_city_list = []

for place in minnesota_places:
    if "," in place:
        city, state = place.split(",")
        minnesota_city_list.append(city)
    else:
        minnesota_city_list.append(place)

with open("MN_cities_list.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter="\n")
    writer.writerow(minnesota_city_list)

#close browser
browser.quit()