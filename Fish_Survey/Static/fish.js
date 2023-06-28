//create a variable for the API
const lakeUrl = "http://127.0.0.1:5000/api/v1.0/lakes";

const cityUrl = "http://127.0.0.1:5000/api/v1.0/cities";

const fishUrl = "http://127.0.0.1:5000/api/v1.0/fish";

const wasUrl = "http://127.0.0.1:5000/api/v1.0/wateraccess";

let city = "Adrian"
let distance = 20
let lakeResultUrl = `http://127.0.0.1:5000/api/v1.0/lake_results/${city}/${distance}`;

d3.json(lakeResultUrl).then(function (data){
    console.log(data)
});

function loadCityDropDown(data) {
    //populate city drop down menu 
    let cityMenu = []
    for (let i = 0; i < data.length; i++) {
        cityMenu.push(data[i].city_name);
    }
    cityMenu.sort()
    
    let cityDropDown = d3.select("#selCity");
    for (let i = 0; i < cityMenu.length; i++) {
        cityDropDown.append("option").text(cityMenu[i]);
    }
};

function loadFishDropDown(data){
    //populate species drop down menu
    let speciesMenu = Object.keys(data)
    for (let i = 0; i < data.length; i++) {
        speciesMenu.push(data[i]);
    }
    speciesMenu.sort()
    
    let fishDropDown = d3.select("#selSpecies");
    for (let i = 0; i < speciesMenu.length; i++) {
        fishDropDown.append("option").text(speciesMenu[i]);
    }
};

function loadDistanceDropDown(){
    //populate distance drop down menu
    let distanceDropDown = d3.select("#selDistance");
    let distanceMenu = [5,10,20,30,45];
    for (let i = 0; i < distanceMenu.length; i++) {
        distanceDropDown.append("option").text(distanceMenu[i]);
    }
};

//prepare data for info panel
function infoPanel(currentCity, currentDistance) {
    let tableInfo = d3.select("#lakeResults");
    let tableHeader = d3.select("#tableHeader");
    let lakeResultUrl = `http://127.0.0.1:5000/api/v1.0/lake_results/${currentCity}/${currentDistance}`;
    tableHeader.text("")
    tableInfo.text("")
    d3.json(lakeResultUrl).then(function (data){
        let search_results = 0;
        for (let i = 0; i < data[1].length; i++) {
            if (data[1][i].lake_depth > 1) {
                tableInfo.append("tr");
                tableInfo.append("td").text(`${data[1][i].lake_name}`);
                tableInfo.append("td").text(`${data[1][i].lake_depth} feet`);
                tableInfo.append("td").text(`${data[1][i].lake_area} acres`);
                search_results += 1
            }
        }
        tableHeader.append("tr").text(`Lake Search Results = ${search_results} Total Lakes Found`);
        tableHeader.append("th").attr("scope", "col").text("Lake Name")
        tableHeader.append("th").attr("scope", "col").text("Lake Depth")
        tableHeader.append("th").attr("scope", "col").text("Lake Area")
    });
}

function createFishingMap(currentCity, currentDistance) {
    let lakeResultUrl = `http://127.0.0.1:5000/api/v1.0/lake_results/${currentCity}/${currentDistance}`;

    //loop through dataFeatures and set variables for lat, lon, depth, and area
    d3.json(lakeResultUrl).then(function(data){
        myMap.remove()
        //create layer for street map
        let streetMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        });
    
        // create array variable to store circles
        let fishingLakes = [];

        for (let i = 0; i < data[1].length; i++) {
            if (data[1][i].lake_depth > 1) {
                let lakeLat = data[1][i].lake_latitude
                let lakeLon = data[1][i].lake_longitude
                let lakeID = data[1][i].lake_id
                let lakeName = data[1][i].lake_name
                let lakeDepth = data[1][i].lake_depth
                let lakeArea = data[1][i].lake_area   
                fishingLakes.push(
                    L.circle([lakeLat, lakeLon], {
                        color: "red",
                        fillColor: "red",
                        fillOpacity: .75,
                        radius: 400
                    }).bindPopup(
                        `<h4>Lake ID: ${lakeID}</h4>
                        <li>Lake Name: ${lakeName}</li>
                        <li>Lake Depth: ${lakeDepth}</li>
                        <li>Lake Area: ${lakeArea}</li>`
                        )
                    )}
                }
        
        //turn port values array into a layer
        lakes = L.layerGroup(fishingLakes);
        d3.json(cityUrl).then(function(data) {
            let mapCenter = []
            for (let i = 0; i < data.length; i++) {
                if (data[i].city_name == currentCity) {
                    mapCenter.push(data[i].city_latitude, data[i].city_longitude)
                }
            }
        //create myMap variable
        myMap = L.map("map", {
            center: mapCenter,
            zoom: 12,
            layers: [streetMap, lakes]
            });
        })

        })

};

d3.json(cityUrl).then(function (data){
    loadCityDropDown(data)
});

d3.json(fishUrl).then(function (data){
    loadFishDropDown(data)
});

loadDistanceDropDown()

let myMap = L.map("map");

function optionChanged() {
    let currentCity = d3.select("#selCity option:checked").text();
    let currentSpecies = d3.select("#selSpecies option:checked").text();
    let currentDistance = d3.select("#selDistance option:checked").text();
    infoPanel(currentCity, currentDistance)
    createFishingMap(currentCity, currentDistance)
}

