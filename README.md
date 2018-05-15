# README

The United States Choropleth Map Creator was made by Ben Elan for a final project in Spring 2018. The project takes a user's csv file as an input and creates an interactive Leaflet map to be displayed in a web browser.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for use and development purposes.

### Prerequisites

To run the script you must have [Python 3](https://www.python.org/downloads/) installed. You also need [PySal](http://pysal.readthedocs.io/en/latest/) which can be installed from the terminal (once Python is already installed) by typing

```
pip -m install pysal
```
If you are having trouble with pip visit [their website](https://packaging.python.org/tutorials/installing-packages/).

### Creating the CSV

There are some example CSV files included in the package. If you wish to use your own data the format must be the same.

CSV Format:
* Header (first row):
Category,Units,Source (ie. Average Income,Dollars,data.gov)
* Data (the rest):
State,Data (ie. California,53489)

If you have missing data, that is okay. Just do not put the State in the CSV file and the script will handle it properly.

### The Python Scripts

There are three python files located in the python directory:

#### dataImport

This is the command line version. Name the csv file you wish to use 'data.csv' and place it in the cmc/data/csv directory. If one of the command line arguements is misspelled or omitted the default values are chosen. The script takes 4 command line arguments with the following options:
__Data classification__
* 'jenks' (Default)
* 'quantile'
*  'percentile'
*  'equal' (Equal Interval)
*  'natural' (Natural Breaks)

__color palette__
* 'blue' (Default)
* 'green'
*  'red'
*  'gold' 
*  'purple'
*  
__base map__
* 'satellite' (Default)
* 'dark'
*  'light'
*  'streets' 
*  'outdoors'

__data normalization__
* 'none' (Default)
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

#### app

This app is a self explanatory GUI built using TKinter.
````
python3 app.py
````

#### createFolium

I added functionality to bypass the leaflet javscript/html using a python module called folium.
Command line package installation:
```
pip install folium
pip install pandas
```
The CSV header is formated a little bit differently.
* Header (first row):
'State',Title (ie. State,Income)

The rest of the CSV stays the same
* Data (the rest):
State,Data (ie. California,53489)

The data classification is quantile. The output is 'foliumMap.html' 

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