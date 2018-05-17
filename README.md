# Choropleth Map Creator

The United States Choropleth Map Creator was made by Ben Elan for a final project in Spring 2018. The project takes a user's csv file as an input and creates an interactive Leaflet map to be displayed in a web browser.

## Prerequisites

To run the script you must have [Python 3](https://www.python.org/downloads/) installed. You also need a few python modules which can be installed from the terminal (once Python is already installed) by typing

```
pip install pysal
pip install folium
pip install pandas
```
If you are having trouble with pip visit [their website](https://packaging.python.org/tutorials/installing-packages/).

## Creating the CSV

There are some example CSV files included in the package. If you wish to use your own data the format must be the same.

CSV Format:
* Header (first row):
Category,Units,Source (ie. Average Income,Dollars,data.gov)
* Data (the rest):
State,Data (ie. California,53489)

If you have missing data, that is okay. Just do not put the State in the CSV file and the script will handle it properly.

## The Python Scripts

There are two python files located in the python directory:

### __dataImport__

This is the command line version. Name the CSV file you wish to use 'data.csv' and place it in the cmc/data/csv directory. If one of the command line arguements is misspelled or omitted the default values are chosen. The script takes 4 command line arguments with the following options:

__Data classification__
* 'jenks' (Default)
* 'quantile'
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

__data normalization__
* none (Default)
* 'density' (divides by state's area)

**Note: when normalizing by area, 'District of Columbia' is omitted from the pysal classsifaction functions**

example runs:
* defaults to jenks, blue, satellite, no normalization
```
python3 dataImport.py
```
* equal interval, color defaults to blue due to misspelling, light base map, no normalization
```
python3 dataImport.py equal ultraviolet light
```
* quantile classification, gold color scale, dark base map, normalized data based on area
```
python3 dataImport.py quantile gold dark density
```

### __app__

This app is a self explanatory GUI built using TKinter.
````
python3 app.py
````

I added functionality to bypass the leaflet javscript/html using a python module called folium.

The data classification and density options do not currently work for folium. The breaks are set to quantile as default. The output file is 'foliumMap.html' 


## TODO

To do list

### Folium
* add class break support
* add density support
* add folium support to command line script
* scale text doesn't show up on dark base maps

### Other
* let user choose folium/web or both from GUI
* start integrating county GEOJSONs
* clean up and comment code



## Built With

* [Leaflet](http://leafletjs.com/) - web mapping framework
* [Mapbox](https://www.mapbox.com/) - base maps
* [ColorBrewer](http://pysal.readthedocs.io/en/latest/index.html) - color palletes
* [PySal](http://pysal.readthedocs.io/en/latest/index.html) - data classification
* [Folium](http://folium.readthedocs.io/en/latest/) - python leaflet module
* [Tkinter](https://wiki.python.org/moin/TkInter) - GUI

## Data Sources

* [Census](https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?pid=DEC_10_SF1_GCTPH1.US01PR&prodType=table45538) - Area, Population, Housing Units
* [Census](https://factfinder.census.gov/bkmk/table/1.0/en/ACS/11_1YR/R1901.US01PRF) - Average Income
* [Death Penalty Information](https://deathpenaltyinfo.org/murder-rates-nationally-and-state) - Homicide Rates