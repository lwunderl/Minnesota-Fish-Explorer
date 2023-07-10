--Drop Tables
DROP TABLE if EXISTS water_access_info, lake_info, fish_info, city_info;

--Create Fish ID table
CREATE TABLE fish_info (
    fish_id VARCHAR(3) PRIMARY KEY,
    fish_description VARCHAR(30)
);

--Create WAS table
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
    was_site_latitude DECIMAL
);

--Create Lake ID table
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

--Create Fish Length table
CREATE TABLE city_info (
	city_name VARCHAR(50) PRIMARY KEY,
	city_longitude DECIMAL,
	city_latitude DECIMAL
);

SELECT * FROM fish_info;
SELECT * FROM lake_info;
SELECT * FROM water_access_info;
SELECT * FROM city_info;