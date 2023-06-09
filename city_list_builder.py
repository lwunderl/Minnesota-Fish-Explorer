from splinter import Browser
from bs4 import BeautifulSoup as soup
import csv

browser = Browser("chrome")

url = "https://en.wikipedia.org/wiki/List_of_cities_in_Minnesota"

browser.visit(url)
browser.is_element_present_by_css("td", wait_time=1)
html = browser.html
city_page = soup(html, "html.parser")
city_table = city_page.find("tbody")
city_places = city_table.find_all("a")

place_titles = [place["title"] for place in city_places]

with open("MN_cities.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(place_titles)

browser.quit()

