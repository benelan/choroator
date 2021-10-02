# Choropleth Map Creator

The United States Choropleth Map Creator was made by Ben Elan for a final undergraduate project in Spring 2018. The project takes a user's CSV file as an input and creates an interactive Leaflet map to be displayed in a web browser.

## Prerequisites

To run the script you must have [Python 3](https://www.python.org/downloads/) installed. You also need a few Python packages which can be installed from the terminal (once Python is already installed) by typing:

```
python3 -m pip install pysal==1.14.4
python3 -m pip install pandas==1.3.3
python3 -m pip install folium==0.7.0
```
If you are having trouble with pip visit [their website](https://packaging.python.org/tutorials/installing-packages/).

## Creating the CSV

There are some example CSV files included in the repo. If you wish to use your own data the format must be the same.

CSV Format:
* __Header (first row):__
`Category,Units,Source` (ie. Average Income,Dollars,data.gov)
* __Data (the rest):__
`State,Data` (ie. California,53489)

It is okay if you don't have data for every state. Leaving out state rows in the CSV will be handled properly.

## The Python Scripts

There are three python files located in the python directory:

### __dataImport.py__

This is the command line version. Name the CSV file you wish to use `data.csv` and place it in the `data/csv` directory. Alternatively, change the file path in the script. If one of the command line arguements is misspelled or omitted the default values are chosen. The script takes 5 command line arguments with the following options:

__Data classification__ (web only)
* 'quantile' (Default)
* 'jenks'
* 'percentile'
* 'equal' (Equal Interval)
* 'natural' (Natural Breaks)

__Color palette__
* 'blue' (Default)
* 'green'
* 'red'
* 'gold' 
* 'purple'

__Basemap__
* 'satellite' (Default)
* 'dark'
* 'light'
* 'streets' 
* 'outdoors'

__Map type__
* both (Default)
* 'folium'
* 'web'

__Data normalization__ (web only)
* none (Default)
* 'density' (divides by state's area)

> Note: when normalizing by area, 'District of Columbia' is omitted from the pysal classsifaction functions

#### Example runs
Defaults to quantile, blue, satellite, no normalization, creates both maps:
```
python3 dataImport.py
```
Equal interval, color defaults to blue due to misspelling, light basemap, no normalization, creates both maps:
```
python3 dataImport.py equal ultraviolet light
```
Jenks classification, gold color scale, dark basemap, normalized data based on area, only creates a web map:
```
python3 dataImport.py jenks gold dark density web
```

### __app.py__

This GUI is built using TKinter. The app first prompts you to choose a CSV file. The path defaults to the choropleth/data/csv directory but you can chose a file from anywhere on the computer. There are two tabs to chose from, Web and Folium. You are then given the same options described above in GUI format.
````
python3 app.py
````

### __createMap.py__
This script contains two functions. 

__Web__

Creates an output GEOJSON to be used with a web version of the Leaflet map. The GEOJSON is used in the `index.html` and `map.js` files. This option has the most functionality.

__Folium__

This uses a Python package called Folium to create a Leaflet map which bypasses the need for creating a new GEOJSON and using HTML or JavaScript. 

The Folium map does not have interactivity and the data classification and density options do not currently work. The breaks are set to quantile by default. 


## TODO
To do list
* add iframe support
* scale text doesn't show up on dark basemaps for folium (somehow change css class to 'leaflet-bar')
* add class break support to folium
* add density support to folium
* use pandas for the web function
* add a population normalization option
* start integrating county GEOJSONs


## Built With

* [PySal](https://pysal.org/pysal/) - Data classification
* [Pandas](https://pandas.pydata.org/) - Data management
* [Folium](https://python-visualization.github.io/folium/) - Python Leaflet package
* [Tkinter](https://wiki.python.org/moin/TkInter) - GUI
* [Leaflet](http://leafletjs.com/) - Web mapping library
* [Mapbox](https://www.mapbox.com/maps/) - Basemaps
* [ColorBrewer](https://colorbrewer2.org) - Color palletes


## Data Sources

* [Census](https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?pid=DEC_10_SF1_GCTPH1.US01PR&prodType=table45538) - Area, Population, Housing Units
* [Census](https://factfinder.census.gov/bkmk/table/1.0/en/ACS/11_1YR/R1901.US01PRF) - Average Income
* [Death Penalty Information](https://deathpenaltyinfo.org/murder-rates-nationally-and-state) - Homicide Rates
