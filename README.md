# Minnesota-Fish-Explorer
![image](https://user-images.githubusercontent.com/116906733/221359723-5307fb87-2246-4305-911e-d5ff28991c40.png)

## Technologies Required
Python 3.8 or later<br>
PostgreSQL<br>
pgAdmin4

## How to Install and Set-Up
Download the Fishing_Explorer folder.<br>
This readme describes how to host this application on your local machine.

### Create SQL database
<ol type="1">
<li>Using pgAdmin4, create a database by right-clicking PostgreSQL in the tree and "Create > Database". Name the database whatever you'd like.</li>
<li>Open the "Tools > Query Tool" and copy and paste the fish_finder_db_schema.sql into the query tool.</li>
<li>Highlight the create tables and execute using "F5" or the "play" button. Your tables should be created. Highlight SELECT * FROM table and execute using "F5"/"play" button to see the "Data Output" below which will only contain empty columns at this time.</li>
<li>To enter data into the tables using .csv files from the accompanying "Data" folder, expand the tree to Schemas > public > Tables, then right-click each table and select "import/export data". Choose the appropriate .csv file from the "Data" folder for each table in "General" and choose header in "Options". NOTE: Be sure to import data in the order the tables are listed in the SQL. This will prevent foreign key errors.</li>
</ol>

![image](https://github.com/lwunderl/Minnesota-Fish-Explorer/assets/116906733/b86bf770-cace-4814-82a9-9f95f04e0727)
<br>

### Create config.py for db connection
<ol type="1">
<li>In the "API" folder, create a file named config.py and within the file create a variable named password = "your_db_password" and create a variable named fish_db = "your_db_name" (api.py uses this to connect to postgreSQL)</li>
<li>In your terminal, run "python api.py" (you may need to pip install psycopg2, numpy, flask, flask_cors, and json)</li>
</ol>

### Open web page and use
<ol type="1">
<li>Copy the path of the index.html into your browser(preferrably chrome)</li>
<li>The web page should load select menus and a gray placeholder for a map</li>
</ol>

## User Tutorial
Use the drop down menus to explore the fishing opportunities in the area of your choice.
<ol type="1">
<li>City: choose a city in Minnesota</li>
<li>Species: choose a species for data analysis</li>
<li>Distance: choose a distance from the city chosen</li>
<li>Data Age: choose how old you want the data to be</li>
<li>Sampling Gear: choose what sampling gear used to collect metrics for abundance (standard gill nets is a good start)</li>
<li>Number of Results: choose how many results you want returned</li>
</ol>

Circles will appear on the map in the location of the lakes with the size of the circle representing fish length and the color of the circle representing most abundance (green) to least abundance (red).<br><br>
NOTE: If you are not getting many results, choose a different sampling gear, an older data age, or further distance. It is possible that lakes will return data, but not for your criteria. Some lakes may only contain information about the lake and not the fish, hence the lake results will return with data, but no display.

![image](https://github.com/lwunderl/Minnesota-Fish-Explorer/assets/116906733/56b02f4f-a9a4-4831-a5a4-50bedd93f7e4)


## Data Resources and Citations
Lake and fish survey data retrieved from various api endpoints at https://www.dnr.state.mn.us/<br>
City information retrieved from https://en.wikipedia.org/wiki/List_of_cities_in_Minnesota<br>
City location information retrieved from https://www.geoapify.com/
