function initMap() {
  const directionsRenderer = new google.maps.DirectionsRenderer();//RENDERS MAP WITH DIRECTIONS
  const directionsService = new google.maps.DirectionsService();//DISPLAYS DIRECTIONS
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 7,
    center: { lat: 26.5629, lng: -81.9495 },//CAPE CORAL,FL DEFAULT STARTING POINT
    disableDefaultUI: false,
  });

  directionsRenderer.setMap(map);
  directionsRenderer.setPanel(document.getElementById("sidebar"));

  const control = document.getElementById("floating-panel");

  map.controls[google.maps.ControlPosition.TOP_CENTER].push(control);

  const onChangeHandler = function () {
    calculateAndDisplayRoute(directionsService, directionsRenderer);
  };

  document.getElementById("start").addEventListener("change", onChangeHandler);
  document.getElementById("end").addEventListener("change", onChangeHandler);
}

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
  const start = document.getElementById("start").value;
  const end = document.getElementById("end").value;

  directionsService
    .route({
      origin: start,
      destination: end,
      travelMode: google.maps.TravelMode.DRIVING,
    })
    .then((response) => {
      directionsRenderer.setDirections(response);
    })
    .catch((e) => window.alert("Directions request failed due to " + status));
}

//WORK IN PROGRESS: CODE FOR USER INPUT DIRECTIONS
// function initMap() {
//   //MAP OPTIONS
//   var myLatLng = { lat: 26.5629, lng: -81.9495 };//CAPE CORAL,FL DEFAULT STARTING POINT
//   var mapOptions = {
//       center: myLatLng,
//       zoom: 8,
//       mapTypeId: google.maps.MapTypeId.ROADMAP
//   }

//   //NEW MAP
//   var map = new google.maps.Map(document.getElementById("map"), mapOptions);

//   //CREATE DIRECTIONS SERVICE OBJECT TO USE THE ROUTE METHOD AND GET A RESULT FOR OUR REQUEST
//   var directionsService = new google.maps.DirectionsService();

//   //CREATE DIRECTIONS RENDERER OBJECT TO DISPLAY THE ROUTE
//   var directionsDisplay = new google.maps.DirectionsRenderer();

//   //BIND DIRECTIONRENDERER() TO THE MAP
//   directionsDisplay.setMap(map);

//   function calcRoute() {
//       //CREATE REQUEST
//       var request = {
//           origin: document.getElementById("starting_point").value,
//           destination: document.getElementById("ending_point").value,
//           travelMode: google.maps.TravelMode.DRIVING,
//           unitSystem: google.maps.UnitSystem.IMPERIAL
//       }

//       //PASS REQUEST TO ROUTE METHOD
//       directionsService.route(request, (result, status) => {
//           if (status == google.maps.DirectionsStatus.OK) {
//               //GET DISTANCE AND TIME
//               const output = document.querySlector('#output');
//               output.innerHTML = "<div>From: " + document.getElementById("starting_point").value + ".<br />To: " + document.getElementById("ending_point").value + ".<br/>Driving Distance: " + result.route.routes[0].legs[0].distance[0].text + "<br />Duration<: " + route.routes[0].legs[0].duration[0].text + ".</div>;"

//               //DISPLAY ROUTE
//               directionsDisplay.setDirections(result);
//           } else {
//               //DELTE ROUTE FROM maps
//               directionsDisplay.setDirections({ routes: [] });
//           }

//           //CENTER MAP IN CAPE CORAL
//           map.setCenter(myLatLng)

//           //SHOW ERROR MESSAGE
//           output.innerHTML = "<div class='alert-danger'>Could not retrieve the distance!</div>";
//       })
//   }

//   var options = {
//       types: ['(cities)']
//   }

//   var input1 = document.getElementById("starting_point")
//   var autocomplete = new google.maps.places.AutoComplete(input1, options)

//   var input2 = document.getElementById("ending_point")
//   var autocomplete2 = new google.maps.places.AutoComplete(input2, options)

//   //ADD MARKER
//   var marker = new google.maps.Marker({
//       position: { lat: 26.4520, lng: -81.9481 },
//       map: map,
//       icon: 'https://i.ibb.co/qgzwqS8/Expedition-Buddy-Marker.png'
//   })
// }
