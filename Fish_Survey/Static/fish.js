//create a variable for the API
const lakeUrl = "http://127.0.0.1:5000/api/v1.0/lakes";

const cityUrl = "http://127.0.0.1:5000/api/v1.0/cities";

const fishUrl = "http://127.0.0.1:5000/api/v1.0/fish";

const wasUrl = "http://127.0.0.1:5000/api/v1.0/wateraccess";

let city = "Minneapolis"
let distance = 12
let lakeResultUrl = `http://127.0.0.1:5000/api/v1.0/lake_results/${city}/${distance}`;

d3.json(lakeResultUrl).then(function (data){
    console.log(data)
});
