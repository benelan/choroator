# Ben Elan
# Spring 2018
# GUI version of DataImport.py

print("RUNNING APP")
print("importing libraries")
import datetime
start = datetime.datetime.now()
from tkinter import filedialog
from tkinter import *
import json
import csv
import sys
import pysal as ps # for data classification
import webbrowser, os
import folium
import pandas as pd

# -- BUTTON EVENT -- #
def clicked():
        print ("opening csv")
        # to change the dataset
        # just change the csv file below
        with open(window.filename, 'r') as f:
                csvList = [row for row in csv.reader(f.read().splitlines())]
                print ("opening json")
                data = json.load(open('../data/json/input.json')) # preset json format to work with the js
                
                print ("handling command line arguements")
                grouping = chk_state.get()
                classification = classVal.get()
                color = colorVal.get()
                base = baseVal.get()
                colorFolium = '';
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
                                                        area = float(data["features"][i]["properties"]["area"]) # area of state
                                                        data["features"][i]["properties"]["number"] = float(row[1])/area
                                                else:
                                                        area = float(data["features"][i]["properties"]["area"]) # area of state
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

                # set colors
                if color == 1: # blue
                        data["color"] = 'blue'
                        colorFolium = "GnBu";
                elif color == 2: # green
                       data["color"] = 'green'
                       colorFolium = "Greens"
                elif color == 3: # red
                       data["color"] = 'red'
                       colorFolium = 'OrRd'
                elif color == 4: # purple
                        data["color"] = 'purple'
                        colorFolium = 'RdPu'
                elif color == 5: # gold
                        data["color"] = 'gold'
                        colorFolium = 'YlOrBr'

                # base maps
                if base == 1: # blue
                        data["base"] = 'satellite'
                elif base == 2: # green
                       data["base"] = 'streets'
                elif base == 3: # red
                       data["base"] = 'outdoors'
                elif base == 4: # purple
                        data["base"] = 'dark'
                elif base == 5: # gold
                        data["base"] = 'light'

                # set data classifications
                if classification == 1: # Jenks
                        classes = ps.esda.mapclassify.Fisher_Jenks(numbers, 6).bins
                        c = []
                        for item in classes:
                                c.append(item)
                        data["grade"] = c
                        classification = 'jenks'
                elif classification == 2: # Quantile
                        classes = ps.esda.mapclassify.Quantiles(numbers, 6).bins
                        c = []
                        for item in classes:
                                c.append(item)
                        data["grade"] = c
                        classification = 'quantile'
                elif classification == 3: # Equal Interval
                        classes = ps.esda.mapclassify.Equal_Interval(numbers, 6).bins
                        c = []
                        for item in classes:
                                c.append(item)
                        data["grade"] = c
                        classification = 'equal interval'
                elif classification == 4: # Percentiles
                        classes = ps.esda.mapclassify.Percentiles(numbers, 6).bins
                        c = []
                        for item in classes:
                                c.append(item)
                        data["grade"] = c
                        classification = 'percentiles'
                elif classification == 5: # Natural Breaks
                        classes = ps.esda.mapclassify.Natural_Breaks(numbers, 6).bins
                        c = []
                        for item in classes:
                                c.append(item)
                        data["grade"] = c
                        classification = 'natural breaks'

               
                print ("using {} breaks: {}".format(classification, str(data["grade"])))
                
                print ("writing output json file")
                # dumping json data
                with open('../data/json/output.json', 'w') as original:
                        json.dump(data, original)
                
                # editing file so that js can read it
                with open('../data/json/output.json', 'r') as original:
                        outfile = original.read()
                        outfile = 'var statesData = ' + outfile  # insert varable name
                        outfile = outfile + ";" # insert semicolon
                
                # writing file
                with open('../data/json/output.json', 'w') as modified:
                        modified.write(outfile)

                # Done
                runtime = datetime.datetime.now() - start
                print ("RUN COMPLETED")
                print(str(runtime))
                webbrowser.open('file://' + os.path.realpath('../index.html'))
                window.destroy()


                # ---FOLIUM--- #
                # read json
                state_geo = os.path.join('../data/json', 'input.json')

                # ready csv
                state_csv = os.path.join('../data/csv', window.filename)
                state_data = pd.read_csv(state_csv)
                
                # mapbox access key
                accessToken = 'pk.eyJ1IjoiYmVuZWxhbiIsImEiOiJjamVicTV0MnYwaHFrMnFsYWNpcTBtYms0In0.FI4MYJLQCioc-LmV-zZcpQ';
                
                # create map
                print(base)
                m = folium.Map(
                    location=[37.8, -96], 
                    zoom_start=4, 
                    tiles=('http://{s}.tiles.mapbox.com/v4/mapbox.' + data["base"] + '/{z}/{x}/{y}.png?access_token=' + accessToken),
                    attr='Mapbox Basemaps')
                
                # add data as choropleth
                m.choropleth(
                    geo_data=state_geo,
                    name='choropleth',
                    data=state_data,
                    columns=[csvList[0][0], csvList[0][1]],         # from csv
                    key_on='feature.properties.name',
                    #threshold_scale= data["grade"],                # not working
                    fill_color=colorFolium,                         # sets color above
                    fill_opacity=0.7,
                    line_opacity=0.2,
                    legend_name=csvList[0][0] + ' (' + csvList[0][1] + ')'    # set from csv
                )

                # save and open
                folium.LayerControl().add_to(m)
                m.save(outfile='../foliumMap.html')
                webbrowser.open('file://' + os.path.realpath('../foliumMap.html'))


# -- TKINTER -- #
window = Tk()

window.title("Choropleth Map Creator")

classVal = IntVar()
colorVal = IntVar()
baseVal = IntVar()
chk_state = BooleanVar()
chk_state.set(False) #set check state

window.update()

window.filename =  filedialog.askopenfilename(initialdir = "../data/csv",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))

title1 = Label(window, text="Select a data classification method")
jenks = Radiobutton(window,text='Jenks', value=1, variable=classVal)
quantile = Radiobutton(window,text='Quantile', value=2, variable=classVal)
equal = Radiobutton(window,text='Equal Interval', value=3, variable=classVal)
percentile = Radiobutton(window,text='Percentile', value=4, variable=classVal)
natural = Radiobutton(window,text='Natural Breaks', value=5, variable=classVal)

title2 = Label(window, text="Select a color palette")
blue = Radiobutton(window,text='Blue', value=1, variable=colorVal)
green = Radiobutton(window,text='Green', value=2, variable=colorVal)
red = Radiobutton(window,text='Red', value=3, variable=colorVal)
purple = Radiobutton(window,text='Purple', value=4, variable=colorVal)
gold = Radiobutton(window,text='Gold', value=5, variable=colorVal)

title4 = Label(window, text="Select a base map")
satellite = Radiobutton(window,text='Satellite', value=1, variable=baseVal)
streets = Radiobutton(window,text='Streets', value=2, variable=baseVal)
outdoors = Radiobutton(window,text='Outdoors', value=3, variable=baseVal)
dark = Radiobutton(window,text='Dark', value=4, variable=baseVal)
light = Radiobutton(window,text='Light', value=5, variable=baseVal)

title3 = Label(window, text="Enable Density")
density = Checkbutton(window, text="Divide by the state's area", var=chk_state)
 
btn = Button(window, text="Create Map", command=clicked)

title1.grid(column=0, row=0, columnspan=5, sticky=W)
jenks.grid(column=0, row=4, sticky=W)
quantile.grid(column=1, row=4, sticky=W)
percentile.grid(column=2, row=4, sticky=W)
equal.grid(column=3, row=4, sticky=W)
natural.grid(column=4, row=4, sticky=W)


title2.grid(column=0, row=7, columnspan=5, sticky=W)
blue.grid(column=0, row=8, sticky=W)
green.grid(column=1, row=8, sticky=W)
gold.grid(column=2, row=8, sticky=W)
red.grid(column=3, row=8, sticky=W)
purple.grid(column=4, row=8, sticky=W)

title4.grid(column=0, row=9, columnspan=5, sticky=W)
dark.grid(column=0, row=10, sticky=W)
light.grid(column=1, row=10, sticky=W)
satellite.grid(column=2, row=10, sticky=W)
streets.grid(column=3, row=10, sticky=W)
outdoors.grid(column=4, row=10, sticky=W)

title3.grid(column=0, row=11, columnspan=5, sticky=W)
density.grid (column=0, row=12, columnspan=5, sticky=W)
btn.grid(column=0, row=13, columnspan=5, sticky=W)

window.mainloop()