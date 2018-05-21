# Choropleth Map Creator

The United States Choropleth Map Creator was made by Ben Elan for a final project in Spring 2018. The project takes a user's CSV file as an input and creates an interactive Leaflet map to be displayed in a web browser.

## Prerequisites

To run the script you must have [Python 3](https://www.python.org/downloads/) installed. You also need a few Python modules which can be installed from the terminal (once Python is already installed) by typing

```
python3 -m pip install pysal
python3 -m pip install pandas
python3 -m pip install folium
```
If you are having trouble with pip visit [their website](https://packaging.python.org/tutorials/installing-packages/).

## Creating the CSV

There are some example CSV files included in the package. If you wish to use your own data the format must be the same.

CSV Format:
* Header (first row):
Category,Units,Source (ie. Average Income,Dollars,data.gov)
* Data (the rest):
State,Data (ie. California,53489)

It is okay if you don't have data for every state. Leaving out State rows in the CSV will be handled properly.

## The Python Scripts

There are three python files located in the python directory:

### __dataImport.py__

This is the command line version. Name the CSV file you wish to use 'data.csv' and place it in the choropleth/data/csv directory. If one of the command line arguements is misspelled or omitted the default values are chosen. The script takes 5 command line arguments with the following options:

__Data classification__ (web only)
* 'quantile' (Default)
* 'jenks'
* 'percentile'
* 'equal' (Equal Interval)
* 'natural' (Natural Breaks)

__color palette__
* 'blue' (Default)
* 'green'
* 'red'
* 'gold' 
* 'purple'

__base map__
* 'satellite' (Default)
* 'dark'
* 'light'
* 'streets' 
* 'outdoors'

__data normalization__ (web only)
* none (Default)
* 'density' (divides by state's area)

__map type__
* both (Default)
* 'folium' (creates both web and folium maps)
* 'web' (creates both web and folium maps)

**Note: when normalizing by area, 'District of Columbia' is omitted from the pysal classsifaction functions**

example runs:
* defaults to quantile, blue, satellite, no normalization, creates both maps
```
python3 dataImport.py
```
* equal interval, color defaults to blue due to misspelling, light base map, no normalization, creates both maps
```
python3 dataImport.py equal ultraviolet light
```
* jenks classification, gold color scale, dark base map, normalized data based on area, only creates a web map
```
python3 dataImport.py jenks gold dark density web
```

### __app.py__

This GUI is built using TKinter. The app first prompts you to choose a CSV file. The path defaults to the choropleth/data/csv directory but you can chose a file from anywhere in your operating system. There are two tabs to chose from, Web and Folium. You are then given the same options described above in GUI format.
````
python3 app.py
````

### __createMap.py__
This script contains two functions. 

__Web__

Creates an output GEOJSON to be used with a web version of the Leaflet map. The GEOJSON is used in the index.html and map.js files included in the package. 

This option has the most functionality, but is more robust.

__Folium__

This uses a Python module called Folium to create a Leaflet map. This bypasses the need for creating a new GEOJSON and using HTML or Javascript. 

The Folium map does not have interactivity and the data classification and density options do not currently work. The breaks are set to quantile by default. 


## TODO
To do list

* scale text doesn't show up on dark base maps for folium (somehow change css class to 'leaflet-bar')
* add class break support to folium
* add density support to folium
* use pandas for the web function
* add a population normalization option (framework already in place with density)
* start integrating county GEOJSONs


## Built With

* [PySal](http://pysal.readthedocs.io/en/latest/index.html) - data classification
* [Pandas](https://pandas.pydata.org/) - data management
* [Folium](http://folium.readthedocs.io/en/latest/) - python leaflet module
* [Tkinter](https://wiki.python.org/moin/TkInter) - GUI
* [Leaflet](http://leafletjs.com/) - web mapping framework
* [Mapbox](https://www.mapbox.com/) - base maps
* [ColorBrewer](http://pysal.readthedocs.io/en/latest/index.html) - color palletes


## Data Sources

* [Census](https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?pid=DEC_10_SF1_GCTPH1.US01PR&prodType=table45538) - Area, Population, Housing Units
* [Census](https://factfinder.census.gov/bkmk/table/1.0/en/ACS/11_1YR/R1901.US01PRF) - Average Income
* [Death Penalty Information](https://deathpenaltyinfo.org/murder-rates-nationally-and-state) - Homicide Rates