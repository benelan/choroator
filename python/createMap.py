# Ben Elan
# Spring 2018
# functions to create leaflet maps
import json
import csv
import pysal as ps     # data classification
import webbrowser, os  # opening files
import folium
import pandas as pd

#----------------------------------WEB----------------------------------#
def Web(csv_data, classification, color, base, grouping):
    print ("opening csv")
    with open(csv_data, 'r') as f:
        csvList = [row for row in csv.reader(f.read().splitlines())]
        print ("opening json")
        data = json.load(open('../data/json/input.json')) # preset json format to work with the js
        print ("inserting data")
        # iterate through the csv
        # inserting number data
        # keeping track of the numbers of the data
        # so that we can determine class breaks
        numbers = []
        for row in csvList:
            for i, item in enumerate(data["features"]):
                if item["properties"]["name"] == row[0]:
                    if grouping == True:
                        # do not add D.C to numbers list for normalization
                        # because it is so small and skew the classification
                        if (data["features"][i]["properties"]["name"] == 'District of Columbia'):
                            area = float(data["features"][i]["properties"]["area"])          # area of state
                            data["features"][i]["properties"]["number"] = float(row[1])/area
                        else:
                            area = float(data["features"][i]["properties"]["area"])          # area of state
                            # to find density you can divide by area
                            data["features"][i]["properties"]["number"] = float(row[1])/area # density
                            numbers.append(float(row[1])/area)
                    else:
                        data["features"][i]["properties"]["number"] = float(row[1])
                        numbers.append(float(row[1]))
        
        # set global info
        if grouping == True:
            data["category"] = csvList[0][0] + ' Density'
            data["unit"] = csvList[0][1] + '/km<sup>2</sup>'
        else:
            data["category"] = csvList[0][0]
            data["unit"] = csvList[0][1]

        data["source"] = csvList[0][2]

        # set colors. default to blue
        if (color != 'green') and (color != 'red') and (color != 'gold') and (color != 'purple'):
            data["color"] = 'blue'
        else:
            data["color"] = color

        # setting basemap. default is satellite
        if (base != 'dark') and (base != 'light') and (base != 'streets') and (base != 'outdoors'):
            data["base"] = 'satellite'
        else:
            data["base"] = base

        # setting data classifications. default is quantile
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

        # array had weird formatting
        c = []
        for item in classes:
                c.append(item)
        data["grade"] = c
        print ("using {} breaks: {}".format(classification, str(data["grade"])))
        

        print ("writing output json file")
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

        # open
        webbrowser.open('file://' + os.path.realpath('../mapWeb.html'))



#----------------------------------FOLIUM----------------------------------#
def Folium(csv_data, color, base):
    print("creating Folium map")
    # read json
    state_geo = os.path.join('../data/json', 'input.json')

    # ready csv
    state_data = pd.read_csv(csv_data)
    columns = list(state_data.columns.values)

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

    # setting basemap. default is satellite
    if (base != 'dark') and (base != 'light') and (base != 'streets') and (base != 'outdoors'):
        baseMap = 'satellite'
    else:
        baseMap = base

    # mapbox access key
    accessToken = 'pk.eyJ1IjoiYmVuZWxhbiIsImEiOiJjamVicTV0MnYwaHFrMnFsYWNpcTBtYms0In0.FI4MYJLQCioc-LmV-zZcpQ';

    # create map
    m = folium.Map(
        location=[40, -96], 
        zoom_start=4, 
        tiles=('http://{s}.tiles.mapbox.com/v4/mapbox.' + baseMap + '/{z}/{x}/{y}.png?access_token=' + accessToken),
        attr='<a href="https://www.mapbox.com/">Mapbox</a>')

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