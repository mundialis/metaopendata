var addOL3 = function() {
    var map = new ol.Map({
    target: 'map',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.TileWMS({
          url: 'https://ows.mundialis.de/osm/service?',
          params: {'LAYERS': 'TOPO-OSM-WMS'},
          serverType: 'geoserver',
          projection: 'EPSG:4326',
          attributions: '©<a href="https://www.openstreetmap.org/copyright"> OpenStreetMap</a> contributors<br>'
        })
      }),
    ],
    view: new ol.View({
      center: [80,20],
      zoom: 4,
      projection: 'EPSG:4326'
    })
  });


  //add draw interaction layer
  var source = new ol.source.Vector({wrapX: false});
  var vector = new ol.layer.Vector({
    source: source
  });
  map.addLayer(vector);

  //find dom elements
  var drawBtn = document.getElementById('drawBtn');
  var mapContainer = document.getElementById('map');
  var oldZ = mapContainer.style.getPropertyValue("z-index");
  var vectorfield = document.getElementById('jsonFile');

  //create draw interaction function
  var draw;
  var addInteraction = function () {
    draw = new ol.interaction.Draw({
      source: source,
      type: "Polygon"
    });
    draw.addEventListener('drawend', function (event) {
      var feat = event.feature;
      var format  = new ol.format.GeoJSON;
      var vector = format.writeFeature(feat);
      mapContainer.style.zIndex=oldZ;
      vectorfield.value = vector;
    });
    map.addInteraction(draw);
  };
  addInteraction();

  //add event listener to draw button
  drawBtn.addEventListener('click', function (event) {
    mapContainer.style.zIndex="100";
    source.clear();
  });


};
