/*
Ben Elan
Spring 2018

HTML and JavaScript was adapted from:
http://leafletjs.com/examples/choropleth/
*/

// access key
mapboxgl.accessToken = 'pk.eyJ1IjoiYmVuZWxhbiIsImEiOiJjamVicTV0MnYwaHFrMnFsYWNpcTBtYms0In0.FI4MYJLQCioc-LmV-zZcpQ';
var map = L.map('map').setView([37.8, -96], 4);

// set map
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    maxZoom: 18,
    accessToken: mapboxgl.accessToken,
    attribution: '<a href="http://mapbox.com">Mapbox</a>',
    id: 'mapbox.' + statesData.base
}).addTo(map);

// grab variables from json
var grades = statesData.grade;
var category = statesData.category;
var unit = statesData.unit;
var geojson;

// get color depending classification values
function getColor(d) {
    if (statesData.color == 'red') {
        return  d >= grades[5] ? '#b30000' :
                d >= grades[4] ? '#e34a33' :
                d >= grades[3] ? '#fc8d59' :
                d >= grades[2] ? '#fdbb84' :
                d >= grades[1] ? '#fdd49e' :
                d >= grades[0] ? '#fef0d9' :
                d == -1        ? 'transparent':
                                '#fef0d9';
    }

    if (statesData.color == 'green') {
        return  d >= grades[5] ? '#006d2c' :
                d >= grades[4] ? '#31a354' :
                d >= grades[3] ? '#74c476' :
                d >= grades[2] ? '#a1d99b' :
                d >= grades[1] ? '#c7e9c0' :
                d >= grades[0] ? '#edf8e9' :
                d == -1        ? 'transparent':
                                '#edf8e9';
    }

    if (statesData.color == 'purple') {
        return  d >= grades[5] ? '#7a0177' :
                d >= grades[4] ? '#c51b8a' :
                d >= grades[3] ? '#f768a1' :
                d >= grades[2] ? '#fa9fb5' :
                d >= grades[1] ? '#fcc5c0' :
                d >= grades[0] ? '#feebe2' :
                d == -1        ? 'transparent':
                                '#feebe2';
    }

    if (statesData.color == 'gold') {
        return  d >= grades[5] ? '#993404' :
                d >= grades[4] ? '#d95f0e' :
                d >= grades[3] ? '#fe9929' :
                d >= grades[2] ? '#fec44f' :
                d >= grades[1] ? '#fee391' :
                d >= grades[0] ? '#ffffd4' :
                d == -1        ? 'transparent':
                                '#ffffd4';
    }

    else {
        return  d >= grades[5] ? '#0868ac' :
                d >= grades[4] ? '#43a2ca' :
                d >= grades[3] ? '#7bccc4' :
                d >= grades[2] ? '#a8ddb5' :
                d >= grades[1] ? '#ccebc5' :
                d >= grades[0] ? '#f0f9e8' :
                d == -1        ? 'transparent':
                                '#f0f9e8';
    }
}

function style(feature) {
    return {
        weight: 2,
        opacity: 1,
        color: 'grey',
        dashArray: '3',
        fillOpacity: 0.8,
        fillColor: getColor(feature.properties.number)
    };
}

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 3,
        color: 'white',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }

    info.update(layer.feature.properties);
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}

geojson = L.geoJson(statesData, {
    style: style,
    onEachFeature: onEachFeature
}).addTo(map);

// control that shows state info on hover
var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info');
    this.update();
    return this._div;
};

info.update = function (props) {
    this._div.innerHTML = '<h4>' + category + '</h4>' +  (props ?
        '<b>' + props.name + '</b><br/>' + 
        props.number.toFixed(2) + ' ' + unit
        //+ '<i><br/></br>' + "Area: " + props.area + ' km<sup>2</sup>' + '</i>'
        : 'Hover over a state');
};

info.addTo(map);

map.attributionControl.addAttribution('<a href='+statesData.source+'>Data Source</a>');

var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        labels = [],
        from, to;

    for (var i = 0; i < grades.length; i++) {
        from = grades[i];
        to = grades[i + 1];

        labels.push(
            '<i style="background:' + getColor(from + 1) + '"></i> ' +
            from.toFixed(2) + (to ? '&ndash;' + to.toFixed(2) : '+')); // toFixed(2) cuts off extra decimal places
    }

    div.innerHTML = labels.join('<br>');
    return div;
};

legend.addTo(map);