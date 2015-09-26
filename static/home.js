
function initialize(dest,listOfOrigin) {
  var mapProp = {
    center:new google.maps.LatLng(-33.9,151),
    zoom:9,
    mapTypeId:google.maps.MapTypeId.ROADMAP
  };
  
  var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);

  var image='DestPin.png';

  var marker=new google.maps.Marker({
    position:{lat:dest[1], lng:dest[2]},
    icon:image,
    map:map
  });

  for (var i = 0; i < listOfOrigin.length; i++) {
    var origin = listOfOrigin[i];
    var marker = new google.maps.Marker({
      position: {lat: origin[1], lng: origin[2]},
      map: map
    });
  }
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendPosition);
    }
}

var cLat;
var cLon;
function sendPosition(position) {
    var cLat= position.coords.latitude;
    var cLon= position.coords.longitude;
 }   



google.maps.event.addDomListener(window, 'load', initialize);