# Ben Elan
# Spring 2018
# functions to create leaflet maps
import json
import csv
import pysal as ps     # data classification
import webbrowser, os  # opening files in browser
import folium          # leaflet mapping module
import pandas as pd    # csv/json handling in folium function
import sys

#----------------------------------WEB----------------------------------#
def Web(csv_data, classification, color, base, grouping):
    print ("opening csv")
    try:
        with open(csv_data, 'r') as f:
            # create array of csv rows
            csvList = [row for row in csv.reader(f.read().splitlines())]
            print ("opening json")
            # open json
            data = json.load(open('../data/json/input.json')) # preset json format to work with the js
            print ("inserting data")
            # iterate through the csv
            # inserting value data
            # keeping track of the values of the data
            # so that we can determine class breaks
            numbers = []
            for row in csvList:
                for i, item in enumerate(data["features"]):
                    # matches state names
                    if item["properties"]["name"] == row[0]:
                        # checks if we want to divide by area
                        if grouping == True:
                            area = float(data["features"][i]["properties"]["area"])          # area of state
                            data["features"][i]["properties"]["number"] = float(row[1])/area # divide by area
                            # do not add D.C to numbers list for normalization
                            # because it is so small and skews the classification
                            if (data["features"][i]["properties"]["name"] != 'District of Columbia'):
                                numbers.append(float(row[1])/area)
                        else:
                            data["features"][i]["properties"]["number"] = float(row[1])
                            numbers.append(float(row[1]))
            
            # add info to the GEOJSON
            if grouping == True:
                data["category"] = csvList[0][0] + ' Density'
                data["unit"] = csvList[0][1] + '/km<sup>2</sup>'
            else:
                data["category"] = csvList[0][0]
                data["unit"] = csvList[0][1]

            data["source"] = csvList[0][2]

            # set colors. defaults to blue
            if (color != 'green') and (color != 'red') and (color != 'gold') and (color != 'purple'):
                data["color"] = 'blue'
            else:
                data["color"] = color

            # set basemap. default is satellite
            if (base != 'dark') and (base != 'light') and (base != 'streets') and (base != 'outdoors'):
                data["base"] = 'satellite'
            else:
                data["base"] = base

            # set data classifications. default is quantile
            # data classification from pysal
            if classification == 'jenks':                                   # Jenks
                classes = ps.esda.mapclassify.Fisher_Jenks(numbers, 6).bins
            elif classification == 'equal':                                 # Equal Interval
                classes = ps.esda.mapclassify.Equal_Interval(numbers, 6).bins
                classification = 'equal interval'
            elif classification == 'percentiles':                           # Percentiles
                classes = ps.esda.mapclassify.Percentiles(numbers).bins
            elif classification == 'natural':                               # Natural Breaks
                classes = ps.esda.mapclassify.Natural_Breaks(numbers, 6).bins
                classification = 'natural breaks'
            else:                                                           # default is Quantile
                classes = ps.esda.mapclassify.Quantiles(numbers, 6).bins

            # array from pysal had weird formatting
            # so you need to flatten it
            c = []
            for item in classes:
                    c.append(item)
            data["grade"] = c

            print ("using {} breaks: {}".format(classification, str(data["grade"])))

            print ("writing output json file for web map")
            # dumping json data
            with open('../data/json/output.json', 'w') as original:
                json.dump(data, original)
            
            # editing file so that js can read it
            with open('../data/json/output.json', 'r') as original:
                outfile = original.read()
                outfile = 'var statesData = ' + outfile           # insert varable name
                outfile = outfile + ";"                           # insert semicolon
            
            # writing file
            with open('../data/json/output.json', 'w') as modified:
                modified.write(outfile)

            # open in browser
            webbrowser.open('file://' + os.path.realpath('../mapWeb.html'))
    
    except IOError:
        print("\n#---------------------------------ERROR---------------------------------#")
        print("Try again. Name a file 'data.csv' and put it in the '/..data/csv' directory.")
        sys.exit()
    except Exception as e:
        print("\n#---------------------------------ERROR---------------------------------#")
        print(e)
        sys.exit()



#----------------------------------FOLIUM----------------------------------#
def Folium(csv_data, color, base):
    print("creating Folium map")

    try:
        # read csv
        state_data = pd.read_csv(csv_data)
        columns = list(state_data.columns.values)

        # read json
        state_geo = os.path.join('../data/json', 'input.json')

        # set colors. default is blue
        if color == 'green':
           colorFolium = "Greens"
        elif color == 'red':
           colorFolium = 'OrRd'
        elif color == 'purple':
            colorFolium = 'RdPu'
        elif color == 'gold':
            colorFolium = 'YlOrBr'
        else:
            colorFolium = "GnBu";

        # set basemap. default is satellite
        if (base != 'dark') and (base != 'satellite') and (base != 'light') and (base != 'streets'):
            baseMap = 'outdoors'
        else:
            baseMap = base

        # mapbox access key
        accessToken = 'pk.eyJ1IjoiYmVuZWxhbiIsImEiOiJjamVicTV0MnYwaHFrMnFsYWNpcTBtYms0In0.FI4MYJLQCioc-LmV-zZcpQ';

        # create map
        m = folium.Map(
            location=[40, -96], 
            zoom_start=4, 
            tiles=('http://{s}.tiles.mapbox.com/v4/mapbox.' + baseMap + '/{z}/{x}/{y}.png?access_token=' + accessToken),
            attr='<a href="https://www.mapbox.com/">Mapbox</a> | <a href='+ columns[2] +'>Data Source</a>')

        # add data as choropleth
        m.choropleth(
            geo_data=state_geo,
            name='choropleth',
            data=state_data,
            columns=[columns[0], columns[1]],                    # from csv
            key_on='feature.properties.name',
            #threshold_scale=[5, 6, 7, 8, 9, 10, 15],            # not working
            fill_color=colorFolium,                              # sets colorFolium above
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=columns[0] + ' (' + columns[1] + ')'     # set from csv
        )

        # save and open
        folium.LayerControl().add_to(m)
        m.save(outfile='../mapFolium.html')
        webbrowser.open('file://' + os.path.realpath('../mapFolium.html'))

    # error handling
    except IOError:
        print("\n#---------------------------------ERROR---------------------------------#")
        print("Try again. Name a file 'data.csv' and put it in the '/..data/csv' directory.")
        sys.exit()
    except Exception as e:
        print("\n#---------------------------------ERROR---------------------------------#")
        print(e)
        sys.exit()