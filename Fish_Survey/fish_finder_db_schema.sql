--Drop Tables
DROP TABLE if EXISTS water_access_sites, median_cpue, fish_catch, fish_length, lake_id, fish_id, city_info;

--Create Fish ID table
CREATE TABLE fish_info (
    fish_description VARCHAR(30),
	fish_id VARCHAR(3) PRIMARY KEY
);

--Create WAS table
CREATE TABLE water_access_sites (
    site_id VARCHAR(7) PRIMARY KEY,
    site_name VARCHAR(30),
    directions_to_site VARCHAR(250),
    administrator_of_site VARCHAR(100),
    number_of_docks INTEGER,
    number_of_restrooms INTEGER,
    number_of_parking_lots INTEGER,
    number_of_accessible_spaces INTEGER,
    number_of_trailer_spaces INTEGER,
    number_of_vehicle_spaces INTEGER,
    parking_lot_surface VARCHAR(12),
    number_of_ramps INTEGER,
    ramp_surface VARCHAR(12),
    longitude DECIMAL,
    latitude DECIMAL
);

--Create Lake ID table
CREATE TABLE lake_info (
    lake_id VARCHAR(10) PRIMARY KEY,
    lake_name VARCHAR(30),
    county VARCHAR(25),
    nearest_town VARCHAR(30),
    lake_area DECIMAL,
    littoral_area DECIMAL,
    lake_depth INTEGER,
    mean_depth DECIMAL,
    water_access_sites VARCHAR(7),
    longitude DECIMAL,
    latitude DECIMAL,
    FOREIGN KEY (water_access_sites) REFERENCES water_access_sites(site_id)
);

--Create Fish Length table
CREATE TABLE fish_length (
    lake_id VARCHAR(10),
    species VARCHAR(3),
    fish_count VARCHAR(250),
    max_length INTEGER,
    min_length INTEGER,
    survey_id VARCHAR(30) PRIMARY KEY,
    survey_date DATE,
    average_length DECIMAL,
    FOREIGN KEY (lake_id) REFERENCES lake_info(lake_id),
    FOREIGN KEY (fish_id) REFERENCES fish_info(fish_id)
);

--Create Fish Catch table
CREATE TABLE fish_catch (
    lake_id VARCHAR(10),
    survey_cpue DECIMAL,
    average_weight DECIMAL,
    gear VARCHAR(30),
    gear_count INTEGER,
    species VARCHAR(3),
    survey_id VARCHAR(30) PRIMARY KEY,
    survey_date DATE,
    total_catch INTEGER,
    total_weight DECIMAL,
    lower_quartile_count DECIMAL,
    upper_quartile_count DECIMAL,
    lower_quartile_weight DECIMAL,
    upper_quartile_weight DECIMAL,
    FOREIGN KEY (lake_id) REFERENCES lake_info(lake_id),
    FOREIGN KEY (fish_id) REFERENCES fish_info(fish_id)
);

--Create Median CPUE table
CREATE TABLE median_cpue(
    lake_id VARCHAR(10),
    species VARCHAR(3),
    lake_cpue DECIMAL,
    PRIMARY KEY (lake_id, species),
    FOREIGN KEY (lake_id) REFERENCES lake_info(lake_id),
    FOREIGN KEY (fish_id) REFERENCES fish_info(fish_id)
);

SELECT * FROM fish_info;
SELECT * FROM lake_info;
SELECT * FROM fish_length;
SELECT * FROM fish_catch;
SELECT * FROM median_cpue;
SELECT * FROM water_access_sites;
SELECT * FROM city_info;
