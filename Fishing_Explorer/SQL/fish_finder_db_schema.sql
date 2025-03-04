--Drop Tables
DROP TABLE if EXISTS length_info, cpue_info, water_access_info, lake_info, city_info, gear_info, fish_info;

--Create fish info table
CREATE TABLE fish_info (
    fish_id VARCHAR(3) PRIMARY KEY,
    fish_description VARCHAR(30)
);

--Create gear info table
CREATE TABLE gear_info (
    gear_id SERIAL PRIMARY KEY,
    gear VARCHAR(50) UNIQUE
);

--Create city info table
CREATE TABLE city_info (
	city_name VARCHAR(50) PRIMARY KEY,
	city_longitude DECIMAL,
	city_latitude DECIMAL
);

--Create lake info table
CREATE TABLE lake_info (
    lake_id VARCHAR(10) PRIMARY KEY,
    lake_name VARCHAR(50),
    lake_county VARCHAR(30),
    nearest_town VARCHAR(40),
    lake_area DECIMAL,
    littoral_area DECIMAL,
    lake_depth DECIMAL,
    mean_depth DECIMAL,
    water_access_sites VARCHAR(800),
    lake_longitude DECIMAL,
    lake_latitude DECIMAL
);

--Create water access info table
CREATE TABLE water_access_info (
    was_site_id VARCHAR(8) PRIMARY KEY,
    was_site_name VARCHAR(100),
    directions_to_was_site VARCHAR(800),
    was_site_administrator VARCHAR(500),
    number_of_docks INTEGER,
    number_of_restrooms INTEGER,
    number_of_parking_lots INTEGER,
    number_of_handicap_accessible_spaces INTEGER,
    number_of_trailer_spaces INTEGER,
    number_of_vehicle_spaces INTEGER,
    parking_lot_surface_type VARCHAR(30),
    number_of_launch_ramps INTEGER,
    launch_ramp_surface_type VARCHAR(30),
    was_site_longitude DECIMAL,
    was_site_latitude DECIMAL,
    lake_id VARCHAR(10),
    lake_name VARCHAR(50)
);

--Create cpue info table
CREATE TABLE cpue_info (
    cpue_id SERIAL PRIMARY KEY,
    lake_id VARCHAR(10),
    cpue DECIMAL,
    average_weight DECIMAL,
    gear VARCHAR(50),
    gear_count INTEGER,
    species VARCHAR(3),
    survey_id VARCHAR(20),
    survey_date DATE,
    total_catch INTEGER,
    total_weight DECIMAL,
    count_lower_quartile DECIMAL,
    count_upper_quartile DECIMAL,
    weight_lower_quartile DECIMAL,
    weight_upper_quartile DECIMAL,
    FOREIGN KEY (lake_id) REFERENCES lake_info(lake_id),
    FOREIGN KEY (species) REFERENCES fish_info(fish_id),
    FOREIGN KEY (gear) REFERENCES gear_info(gear)
);

--Create length info table
CREATE TABLE length_info (
    length_id SERIAL PRIMARY KEY,
    lake_id VARCHAR(10),
    species VARCHAR(3),
    fish_count VARCHAR,
    maximum_length INTEGER,
    minimum_length INTEGER,
    survey_id VARCHAR(20),
    survey_date DATE,
    average_length DECIMAL,
    FOREIGN KEY (lake_id) REFERENCES lake_info(lake_id),
    FOREIGN KEY (species) REFERENCES fish_info(fish_id)
);

SELECT * FROM fish_info;
SELECT * FROM gear_info;
SELECT * FROM lake_info;
SELECT * FROM water_access_info;
SELECT * FROM city_info;
SELECT * FROM cpue_info;
SELECT * FROM length_info;