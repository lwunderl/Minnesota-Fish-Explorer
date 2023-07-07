//create a variable for the API
const lakeUrl = "http://127.0.0.1:5000/api/v1.0/lakes";

const cityUrl = "http://127.0.0.1:5000/api/v1.0/cities";

const fishUrl = "http://127.0.0.1:5000/api/v1.0/fish";

const wasUrl = "http://127.0.0.1:5000/api/v1.0/wateraccess";

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

function loadFishDropDown(data) {
    //populate species drop down menu
    let speciesMenu = Object.values(data)
    for (let i = 0; i < data.length; i++) {
        speciesMenu.push(data[i]);
    }
    speciesMenu.sort()
    
    let fishDropDown = d3.select("#selSpecies");
    for (let i = 0; i < speciesMenu.length; i++) {
        fishDropDown.append("option").text(speciesMenu[i]);
    }
};

function loadDistanceDropDown() {
    //populate distance drop down menu
    let distanceDropDown = d3.select("#selDistance");
    let distanceMenu = [5,10,20,30];
    for (let i = 0; i < distanceMenu.length; i++) {
        distanceDropDown.append("option").text(distanceMenu[i]);
    }
};

function getSpeciesCode(currentSpecies) {
    return d3.json(fishUrl).then(function(data) {
        let speciesCode = Object.keys(data).find(key => data[key] == currentSpecies);
        return speciesCode;
    })
}

function getMedianCPUE(data, lakeID, speciesCode) {
    for (let i = 0; i < data[0].lake_results.length; i++) {
        let medianCPUEArray = []
        for (let i = 0; i < data[1].cpue_results.length; i++) {
            if (data[1].cpue_results[i].lake_ID == lakeID && data[1].cpue_results[i].species == speciesCode) {
                medianCPUEArray.push(Number(data[1].cpue_results[i].CPUE))
            }
        }
        
        if(medianCPUEArray.length > 0); {

            medianCPUEArray.sort(function(a,b){
            return a-b;
            });
        
            let half = Math.floor(medianCPUEArray.length / 2);
            
            if (medianCPUEArray.length % 2) {
                let medianCPUE = Math.round((medianCPUEArray[half] + Number.EPSILON) * 100) / 100
                return medianCPUE
            }
            else{
                let medianCPUE = Math.round((((medianCPUEArray[half - 1] + medianCPUEArray[half]) / 2) + Number.EPSILON) * 100) / 100
                return medianCPUE
            }
        }
    }
}

function getAverageLength(data, lakeID, speciesCode) {
    let averageLengthArray = []
    for (let i = 0; i < data[2].length_results.length; i++) {
        if (data[2].length_results[i].lake_ID == lakeID && data[2].length_results[i].species == speciesCode) {
            averageLengthArray.push(...data[2].length_results[i].fish_count)
        }
    }
    
    if(averageLengthArray.length > 0); {

        let total = 0;
        for(let i = 0; i < averageLengthArray.length; i++) {
            total += averageLengthArray[i];
        }
        let avg = Math.round((((total / averageLengthArray.length) + Number.EPSILON) * 100)) / 100;

        return avg

    }
}

function getColor(d) {
    return d > 11 ? "#1BFF00" :
           d > 9  ? "#93FF00" :
           d > 7  ? "#D8FF00" :
           d > 5  ? "#FFFF00" :
           d > 3   ? "#FFB200" :
           d > 2   ? "#FF8300" :
           d > 1   ? "#FF5500" :
                      "#FF0000";
     }

//prepare data for info panel
function infoPanel(currentCity, currentDistance) {
    let tableInfo = d3.select("#lakeResults");
    let tableHeader = d3.select("#tableHeader");
    let lakeResultUrl = `http://127.0.0.1:5000/api/v1.0/lake_results/${currentCity}/${currentDistance}`;
    tableHeader.text("")
    tableInfo.text("")
    d3.json(lakeResultUrl).then(function (data){
        console.log(data)
        let search_results = 0;
        for (let i = 0; i < data[0].lake_results.length; i++) {
            if (data[0].lake_results[i].lake_depth > 0) {
                tableInfo.append("tr");
                tableInfo.append("td").text(`${data[0].lake_results[i].lake_name}`);
                tableInfo.append("td").text(`${data[0].lake_results[i].lake_depth} feet`);
                tableInfo.append("td").text(`${data[0].lake_results[i].lake_area} acres`);
                search_results += 1
            }
        }
        tableHeader.append("tr").text(`Lake Search Results = ${search_results} Total Lakes Found`);
        tableHeader.append("th").attr("scope", "col").text("Lake Name")
        tableHeader.append("th").attr("scope", "col").text("Lake Depth")
        tableHeader.append("th").attr("scope", "col").text("Lake Area")
    });
}

async function createFishingMap(currentCity, currentDistance, currentSpecies) {
    let lakeResultUrl = `http://127.0.0.1:5000/api/v1.0/lake_results/${currentCity}/${currentDistance}`;
    let speciesCode = await getSpeciesCode(currentSpecies)

    //loop through dataFeatures and set variables for lat, lon, depth, and area
    d3.json(lakeResultUrl).then(function(data){
        myMap.remove()
        //create layer for street map
        let streetMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        });
    
        // create array variable to store circles
        let fishingLakes = [];

        for (let i = 0; i < data[0].lake_results.length; i++) {
            if (data[0].lake_results[i].lake_depth > 0) {
                let lakeLat = data[0].lake_results[i].lake_latitude
                let lakeLon = data[0].lake_results[i].lake_longitude
                let lakeID = data[0].lake_results[i].lake_id
                let lakeName = data[0].lake_results[i].lake_name
                let lakeDepth = data[0].lake_results[i].lake_depth
                let lakeArea = data[0].lake_results[i].lake_area
                let medianCPUE = getMedianCPUE(data, lakeID, speciesCode)
                let averageLength = getAverageLength(data, lakeID, speciesCode)
                if (averageLength && medianCPUE){
                    fishingLakes.push(
                        L.circle([lakeLat, lakeLon], {
                            color: getColor(medianCPUE),
                            fillColor: getColor(medianCPUE),
                            fillOpacity: .75,
                            radius: averageLength * 35
                        }).bindPopup(
                            `<h4>Lake ID: ${lakeID}</h4>
                            <h6>Fish Species: ${currentSpecies}</h6>
                            <li>Lake Name: ${lakeName}</li>
                            <li>Lake Depth: ${lakeDepth}</li>
                            <li>Lake Area: ${lakeArea}</li>
                            <li>Average Length: ${averageLength}</li>
                            <li>Median CPUE: ${medianCPUE}</li>`
                            )
                        )
                    }
                }
            }
        
        //turn port values array into a layer
        lakes = L.layerGroup(fishingLakes);
        d3.json(cityUrl).then(function(data) {
            let mapCenter = []
            for (let i = 0; i < data.length; i++) {
                if (data[i].city_name == currentCity) {
                    mapCenter.push(data[i].city_latitude, data[i].city_longitude);
                }
            }
            //create myMap variable
            myMap = L.map("map", {
                center: mapCenter,
                zoom: 12,
                layers: [streetMap, lakes]
                });
            });
        });

};

function cpueChart(currentSpecies) {};

d3.json(cityUrl).then(function (data){
    loadCityDropDown(data)
});

d3.json(fishUrl).then(function (data){
    loadFishDropDown(data)
});

loadDistanceDropDown()

let myMap = L.map("map");

function speciesChanged() {
    let currentCity = d3.select("#selCity option:checked").text();
    let currentSpecies = d3.select("#selSpecies option:checked").text();
    let currentDistance = d3.select("#selDistance option:checked").text();
    createFishingMap(currentCity, currentDistance, currentSpecies)
}

function cityChanged() {
    let currentCity = d3.select("#selCity option:checked").text();
    let currentSpecies = d3.select("#selSpecies option:checked").text();
    let currentDistance = d3.select("#selDistance option:checked").text();
    infoPanel(currentCity, currentDistance)
    createFishingMap(currentCity, currentDistance, currentSpecies)
}

