(manageForm = function(cfg) {

  var fileuploadUrl = "http://127.0.0.1:5000/files";
  // var fileuploadUrl = "https://bmvimetadaten.mundialis.de/api/files";

  var catalogBaseUrl = 'https://bmvimetadaten.mundialis.de/geonetwork';
  var catalogPath = 'srv/ger/catalog.search#/metadata';

  var form = document.getElementById('geodataform');
  var geodataFileField = document.getElementById('geodataFile');
  var loadingMask = document.getElementById('loading-mask');
  var warnBox = document.getElementById('warning');
  var error;

  warnBox.style.visibility="hidden";

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    loadingMask.style.visibility="visible";
    chkdata();
    if (error) return;
    var data = new FormData(form);
    upload(data);
  });

  var warn = function(msg) {
    warnBox.style.color="red"
    warnBox.innerHTML = msg;
    warnBox.style.visibility="visible";
    loadingMask.style.visibility="hidden";
    return true
  };

  var chkdata = function() {
    var geodata;
    var zip;
    var json;
    var selection;
    var empty = 0;

    //check if only exactly one vector file is selected
    geodata = form.elements[name="geodataFile"].value;
    json = form.elements[name="jsonFile"].value;
    error = (!geodata && !json)? warn("WARNING:<br>Please upload or draw geodata!"):false;
    if (error) return;
    error = (geodata && json)? warn("WARNING:<br>Please choose only one data source!"):false;
    if (error) return;

    // TODO: check file format
    // if geodata, check if it is a zip file
    // zip = geodata.split(".")[1];
    // error = (geodata && zip!=="zip")? warn("WARNING:<br>File is not a valid zip file!"):false;
    // if (error) return;

  };

  var upload = function(data) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      var html;
      var now;
      var timestamp;
      if (xhttp.readyState == 4) {
        if (xhttp.status == 200) {
          warnBox.style.color="inherit"
          name = JSON.parse(xhttp.responseText).name;
          uuid = JSON.parse(xhttp.responseText).record;
          url = catalogBaseUrl + '/' + catalogPath + '/' + uuid;
          html = 'Your data will be enriched with metadata! See status here:'
               + '<br><br><a href="' + url + '">' + url + '</a><br>'
               + '<pre><code>' + xhttp.responseText + '</code></pre>';
        } else if (xhttp.status == 500) {
          warnBox.style.color="red";
          html = '500 Internal Server Error<br>' + xhttp.response;
        }
        setTimeout(function(){
          // show loading mask at least 1 second
          warnBox.innerHTML = html;
          warnBox.style.visibility="visible";
          loadingMask.style.visibility="hidden";
        }, 1000);

      }
    };
    xhttp.open("POST", fileuploadUrl, true);
    xhttp.send(data);
  };

})
