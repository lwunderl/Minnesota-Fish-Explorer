
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
    let distanceMenuLabels = ["5 Miles", "10 Miles", "20 Miles", "30 Miles"]
    let distanceMenuValues = [5,10,20,30];
    for (let i = 0; i < distanceMenuLabels.length; i++) {
        distanceDropDown.append("option").text(distanceMenuLabels[i]).property("value", distanceMenuValues[i]);
    }
};

function loadDataAgeDropDown() {
    //populate data age drop down menu
    let dataAgeDropDown = d3.select("#selAge");
    let dataAgeMenuValues = [5,10,20,30,100];
    let dataAgeMenuLabels = ["less than 5 Years", "less than 10 Years", "less than 20 Years", "less than 30 Years", "All time"]
    for (let i = 0; i < dataAgeMenuLabels.length; i++) {
        dataAgeDropDown.append("option").text(dataAgeMenuLabels[i]).property("value", dataAgeMenuValues[i]);
    }
};

function loadSamplingGearDropDown() {
    //populate sampling gear choices
    let gearDropDown = d3.select("#selGear");
    let gearMenu = ["Standard Gill Nets", "Standard Trap Nets"];
    for (let i = 0; i < gearMenu.length; i++) {
        gearDropDown.append("option").text(gearMenu[i]);
    }
};

function loadNumberOfResultsDropDown() {
    //populate number of results preferred choices
    let resultsDropDown = d3.select("#selResults");
    let resultsMenu = [5,10,20,30,40,50];
    for (let i = 0; i < resultsMenu.length; i++) {
        resultsDropDown.append("option").text(resultsMenu[i]);
    }
};

function loadAllDropDowns() {
    //load all drop down menus
    d3.json(cityUrl).then(function (data){
        loadCityDropDown(data)
    });
    
    d3.json(fishUrl).then(function (data){
        loadFishDropDown(data)
    });
    
    loadDistanceDropDown()
    loadDataAgeDropDown()
    loadSamplingGearDropDown()
    loadNumberOfResultsDropDown()
}

function getSpeciesCode(currentSpecies) {
    return d3.json(fishUrl).then(function(data) {
        let speciesCode = Object.keys(data).find(key => data[key] == currentSpecies);
        return speciesCode;
    })
}

function getLakeData(lakeResultUrl) {
    return d3.json(lakeResultUrl).then(function(data) {
        return data
    })
}

function getMedianCPUE(data, lakeID, speciesCode, currentDataAge, currentGear) {
    let today = new Date()
    let medianCPUEArray = []
    for (let i = 0; i < data[1].cpue_results.length; i++) {
        surveyDate = new Date(data[1].cpue_results[i].survey_date)
        ageCutOff = today.getFullYear() - surveyDate.getFullYear()
        if (data[1].cpue_results[i].lake_id == lakeID && data[1].cpue_results[i].species == speciesCode && ageCutOff <= currentDataAge) {
            medianCPUEArray.push(Number(data[1].cpue_results[i].cpue))
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

function getAverageLength(data, lakeID, speciesCode, currentDataAge) {
    let averageLengthArray = []
    let today = new Date()
    for (let i = 0; i < data[2].length_results.length; i++) {
        surveyDate = new Date(data[2].length_results[i].survey_date)
        ageCutOff = today.getFullYear() - surveyDate.getFullYear()
        if (data[2].length_results[i].lake_id == lakeID && data[2].length_results[i].species == speciesCode && ageCutOff <= currentDataAge) {
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
async function infoPanel(data, currentSpecies, currentNumberResults, currentDataAge) {
    let speciesCode = await getSpeciesCode(currentSpecies);
    let search_results = 0;
    let medianCPUE = 0;
    let averageLength = 0;
    let medianList = [];
    for (let i = 0; i < data[0].lake_results.length; i++) {
        if (data[0].lake_results[i].lake_depth > 0) {
            search_results += 1
            lakeID = data[0].lake_results[i].lake_id;
            medianCPUE = getMedianCPUE(data, lakeID, speciesCode, currentDataAge);
            averageLength = getAverageLength(data, lakeID, speciesCode, currentDataAge);
            medianList.push(
                {
                "lakeName": data[0].lake_results[i].lake_name,
                "lakeDepth": data[0].lake_results[i].lake_depth,
                "lakeArea": data[0].lake_results[i].lake_area,
                "abundance": medianCPUE,
                "averageLength": averageLength
            }
            )
        }
    }
    medianList.sort(function(a,b) {
        if (isNaN(b.abundance)) {
            return -1
        }
        if (isNaN(a.abundance)) {
            return 1
        }
        else {
            return b.abundance - a.abundance
        }
    })

    let tableInfo = d3.select("#lakeResults");
    let tableHeader = d3.select("#tableHeader");
    tableHeader.text("");
    tableInfo.text("");

    resultsLimit = medianList.slice(0,currentNumberResults);

    for (let i = 0; i < resultsLimit.length; i++) {
        tableInfo.append("tr");
        tableInfo.append("td").text(`${medianList[i].lakeName}`);
        tableInfo.append("td").text(`${medianList[i].lakeDepth} feet`);
        tableInfo.append("td").text(`${medianList[i].lakeArea} acres`);
        tableInfo.append("td").text(`${medianList[i].abundance}`);
        tableInfo.append("td").text(`${medianList[i].averageLength} inches`);
        }

    tableHeader.append("tr").text(`Lake Search Results = ${search_results} Total Lakes Found with Data`);
    tableHeader.append("th").attr("scope", "col").text("Lake Name")
    tableHeader.append("th").attr("scope", "col").text("Lake Depth")
    tableHeader.append("th").attr("scope", "col").text("Lake Area")
    tableHeader.append("th").attr("scope", "col").text("Abundance")
    tableHeader.append("th").attr("scope", "col").text("Average Length")
}

async function createFishingMap(data, currentSpecies, currentNumberResults, currentDataAge) {
    //remove old map
    myMap.remove()
    //get code for current species
    let speciesCode = await getSpeciesCode(currentSpecies)
    //create layer for street map
    let streetMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    // create array variable to store info circles
    let fishingLakes = [];

    let lakeResults = [];

    //loop through each lake
    for (let i = 0; i < data[0].lake_results.length; i++) {
        if (data[0].lake_results[i].lake_depth > 0) {
            let lakeLat = data[0].lake_results[i].lake_latitude
            let lakeLon = data[0].lake_results[i].lake_longitude
            let lakeID = data[0].lake_results[i].lake_id
            let lakeName = data[0].lake_results[i].lake_name
            let lakeDepth = data[0].lake_results[i].lake_depth
            let lakeArea = data[0].lake_results[i].lake_area
            let medianCPUE = getMedianCPUE(data, lakeID, speciesCode, currentDataAge)
            let averageLength = getAverageLength(data, lakeID, speciesCode, currentDataAge)
            let circleSize = 100
            if (averageLength) {circleSize = averageLength * 50}
            lakeResults.push(
                {
                    "lakeLat": lakeLat,
                    "lakeLon": lakeLon,
                    "lakeID": lakeID,
                    "lakeName": lakeName,
                    "lakeDepth": lakeDepth,
                    "lakeArea": lakeArea,
                    "abundance": medianCPUE,
                    "averageLength": averageLength,
                    "circleSize": circleSize
                }
                )
        }   
    }
    lakeResults.sort(function(a,b) {
        if (isNaN(b.abundance)) {
            return -1
        }
        if (isNaN(a.abundance)) {
            return 1
        }
        else {
            return b.abundance - a.abundance
        }
    })

// create results list here then make map layer
    resultsLimit = lakeResults.slice(0,currentNumberResults)

    for (let i = 0; i < resultsLimit.length; i++) {
        if (lakeResults[i].abundance){
            fishingLakes.push(
                L.circle([lakeResults[i].lakeLat, lakeResults[i].lakeLon], {
                    color: getColor(lakeResults[i].abundance),
                    fillColor: getColor(lakeResults[i].abundance),
                    fillOpacity: .75,
                    radius: lakeResults[i].circleSize
                }).bindPopup(
                    `<h5>Lake ID: ${lakeResults[i].lakeID}</h5>
                    <li style="font-size:11px">Lake Name: ${lakeResults[i].lakeName}</li>
                    <li style="font-size:11px">Lake Depth: ${lakeResults[i].lakeDepth}</li>
                    <li style="font-size:11px">Lake Area: ${lakeResults[i].lakeArea}</li>
                    <li style="font-size:11px">Fish Species: ${currentSpecies}</li>
                    <li style="font-size:11px">Average Length: ${lakeResults[i].averageLength}</li>
                    <li style="font-size:11px">Abundance: ${lakeResults[i].abundance}</li>`
                    )
                )
            }
        }

    //create lakes layer
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
};

function cpueChart(currentSpecies) {};

//load drop downs
loadAllDropDowns()

//initialize variables
let myMap = L.map("map");
let currentCity = "Ada"
let currentSpecies = "No Particular Species"
let currentDistance = 5
let currentGear = "Standard Gill Nets"
let currentDataAge = 5
let currentNumberResults = 5
let lakeResultUrl = ""
let lakeData = ""

//function for changing data choices without retrieving new data from API
function choicesChanged() {
    currentSpecies = d3.select("#selSpecies option:checked").text();
    currentGear = d3.select("#selGear option:checked").text();
    currentNumberResults = d3.select("#selResults option:checked").text();
    if (lakeData){
        createFishingMap(lakeData, currentSpecies, currentNumberResults, currentDataAge)
        infoPanel(lakeData, currentSpecies, currentNumberResults, currentDataAge)
    }
}

//function for changing data and retrieving new data from API
async function dataChanged() {
    currentCity = d3.select("#selCity option:checked").text();
    currentSpecies = d3.select("#selSpecies option:checked").text();
    currentDistance = d3.select("#selDistance option:checked").property("value");
    currentGear = d3.select("#selGear option:checked").text();
    currentDataAge = d3.select("#selAge option:checked").property("value");
    currentNumberResults = d3.select("#selResults option:checked").text();

    lakeResultUrl = `http://127.0.0.1:5000/api/v1.0/lake_results/${currentCity}/${currentDistance}`;
    lakeData = await getLakeData(lakeResultUrl);

    infoPanel(lakeData, currentSpecies, currentNumberResults, currentDataAge);
    createFishingMap(lakeData, currentSpecies, currentNumberResults, currentDataAge);
}


