const slideshowImages = document.querySelectorAll(".intro-slideshow img");

const nextImageDelay = 5000;
let currentImageCounter = 0; // setting a variable to keep track of the current image (slide)

// slideshowImages[currentImageCounter].style.display = "block";
slideshowImages[currentImageCounter].style.opacity = 1;

setInterval(nextImage, nextImageDelay);

function nextImage() {
  // slideshowImages[currentImageCounter].style.display = "none";
  slideshowImages[currentImageCounter].style.opacity = 0;

  currentImageCounter = (currentImageCounter+1) % slideshowImages.length;

  // slideshowImages[currentImageCounter].style.display = "block";
  slideshowImages[currentImageCounter].style.opacity = 1;
}

let mapPlacementLat= 42.3601 
let mapPlacementLng =-71.0598;
let address;
let dataPretty;

//MAP VIEWING
function initMap(){
  //map options
  
  // let options_map= {
  //   zoom: 14,
  //   center:{lat: mapPlacementLat, lng: mapPlacementLng}
  // }
  // //new map 
  // let map = new google.maps.Map(document.getElementById('map'),options_map);

  //Adding a marker 
  // let marker = new google.maps.Map({
  //   position:{lat:42.4668,lng:-70.9695},
  //   map:map
  // });
  
  
  initAutocomplete();
  
}

// AUTOCOMPLETE FUNCTIONALITY
let autocomplete;
function initAutocomplete(){
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('autocomplete'),
    {
      types: ['establishment'],
      componentRestrictions: {'country':['CA','USA']},
      fields: ['place_id','name','geometry','adr_address']
  
    }
  )
  autocomplete.addListener('place_changed', onPlaceClick);
  
}


function onPlaceClick(){
  let place = autocomplete.getPlace()
  
  if(!place.geometry){
    // No prediction was selected
    document.getElementById('autocomplete').placeholder = "Search";
  } else {
    //Show details of the valid place
    // document.getElementById('details').innerHTML = place.adr_address;
    address = place.adr_address;
    geocode(address)
  }

}

function geocode(location){
  // let location = ' 22 Main st Bostan MA';
  axios.get('https://maps.googleapis.com/maps/api/geocode/json',{
    params:{
      address:location,
      key: 'AIzaSyANso2rcGXQQY850G3SgTWtBc5Vs26C1Pg'
    }
  })
  .then(function(result){
    // console.log(result);
  
    mapPlacementLat = (result.data.results[0].geometry.location['lat']);
    mapPlacementLng = (result.data.results[0].geometry.location['lng']);
    console.log("Latitude: " + mapPlacementLat + " Longi: " + mapPlacementLng)
    let options_map= {
        zoom: 14,
        center:{lat: mapPlacementLat, lng: mapPlacementLng}
      }
      //new map 
    let map = new google.maps.Map(document.getElementById('map'),options_map);
    weatherJSONCoordinates(mapPlacementLat, mapPlacementLng);
    solarRadiationCurrentJSONCoordinates(mapPlacementLat, mapPlacementLng);

  })
  .catch(function(error){
    console.log(error);
  })
}


// WEATHER API

const API_KEY = "ed8b789eecee129309891dfe30f9a4c6"

// weather by city
function weatherJSONLocation(city, stateCode = null, countryCode = null) {
    var url;

    if (stateCode == null) {
        url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&APPID=${API_KEY}`;
    } else if (countryCode == null) {
        url = `https://api.openweathermap.org/data/2.5/weather?q=${city},${stateCode}&APPID=${API_KEY}`;
    } else {
        url = `https://api.openweathermap.org/data/2.5/weather?q=${city},${stateCode},${countryCode}&APPID=${API_KEY}`;
    }

    fetch(url)
    .then(response => response.json())
    .then(data => {
                    console.log(data);
                    const body = document.querySelector("body");
                    const dataPretty = JSON.stringify(data, null, 2); 
                    body.insertAdjacentHTML("beforeend", `<h1> ${dataPretty} <\h1>`);
                  });
}

// weather by coordinates
function weatherJSONCoordinates(lat, lon) {
    var url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&APPID=${API_KEY}&units=imperial&exclude=hourly`;

    fetch(url)
    .then(response => response.json())
    .then(data => {
                    console.log(data);
                    const weather = document.querySelector("#weather");
                    const status = document.querySelector('#status')
                    // const icon = document.querySelector(".img")
                    //  console.log(icon)
                    // let weather_icon = data['weather'][0]['icon']
                    // console.log(weather_icon)

                    //Getting image of the weather of that day
                    // let img = document.createElement("img")
                    // icon.src = `https://openweathermap.org/img/wn/${weather_icon}@2x.png`
          
                    // console.log(img)
                    // icon.appendChild(img);

                    //defining what a good or a bad day is in terms of weather
                    if(data['main']['temp'] >= 75 && data['main']['temp'] <= 95){
                      status.innerHTML = "Perfect!"
                    } else if(data['main']['temp'] < 75 ){
                      status.innerHTML = "Too Cold"
                    } else if(data['main']['temp']  > 95 ){
                      status.innerHTML = "Too Warm"
                    }
                    console.log(data['main']['temp'])
                    weather.innerHTML = data['main']['temp'] + "˚F"
                    // status.innerHTML = data['main']['temp']
                    dataPretty = JSON.stringify(data, null, 2);

                    // weather.innerHTML = dataPretty.main.feels_like
                    // console.log(dataPretty.main[0].feels_like)
                    // body.insertAdjacentHTML("beforeend", `<h1> ${dataPretty} <\h1>`);
                  });
}
// weather by zipcode
function weatherJSONZipCode(zipCode, countryCode) {
    var url = `https://api.openweathermap.org/data/2.5/weather?zip=${zipCode},${countryCode}&APPID=${API_KEY}`;

    fetch(url)
    .then(response => response.json())
    .then(data => {
                    console.log(data);
                    const body = document.querySelector("body");
                    dataPretty = JSON.stringify(data, null, 2); 
                    body.insertAdjacentHTML("beforeend", `<h1> ${dataPretty} <\h1>`);
                  });
}

const solar_API_KEY = "ed8b789eecee129309891dfe30f9a4c6"

// current solar radiation by coordinates
function solarRadiationCurrentJSONCoordinates(lat, lon) {
    var url = `https://api.openweathermap.org/data/2.5/solar_radiation?lat=${lat}&lon=${lon}&appid=${solar_API_KEY}`;

    fetch(url)
    .then(response => response.json())
    .then(data => {
                    console.log(data);
                    const solarRadGHI = document.querySelector("#ghi");
                    let ghi = data['list'][0]['radiation']['ghi'];
                    console.log(ghi);
                    if(ghi < 1000){
                      solarRadGHI.innerHTML = "Radiation: " + "Great";
                    } else {
                      solarRadGHI.innerHTML = "Radiation: " + "Stay Home";
                    }
        
                    // solarRadGHI.innerHTML = "Radiation: " + ghi;
                    // const solarRadDNI = document.querySelector("dni");




                    // const dataPretty = JSON.stringify(data, null, 2); 
                    // body.insertAdjacentHTML("beforeend", `<h1> ${dataPretty} <\h1>`);
                  });
}

// forecast solar radiation by coordinates
function solarRadiationForecastJSONCoordinates(lat, lon) {
    var url = `https://api.openweathermap.org/data/2.5/solar_radiation/forecast?lat=${lat}&lon=${lon}&appid=${API_KEY}`;

    fetch(url)
    .then(response => response.json())
    .then(data => {
                    console.log(data);
                    const body = document.querySelector("body");
                    const dataPretty = JSON.stringify(data, null, 2); 
                    body.insertAdjacentHTML("beforeend", `<h1> ${dataPretty} <\h1>`);
                  });
}

// demo
// solarRadiationCurrentJSONCoordinates(0, 0);
// solarRadiationForecastJSONCoordinates(0, 0);

 

