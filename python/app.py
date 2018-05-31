# Ben Elan
# Spring 2018
# A GUI that provides options to create maps
# check the README for more details

print("RUNNING APP")
print("importing libraries")
import datetime                             # timer
start = datetime.datetime.now()
from tkinter import *                       # GUI
from tkinter import ttk
from tkinter import filedialog   
import createMap                            # map creation functions

#----------------------------------BUTTON EVENT----------------------------------#
def clickedWeb():
    csv_data = window.filename

    print ("handling radio parameters")
    grouping = densityVal.get()

    # class breaks
    breaks = classVal.get()
    if breaks == 1: # Jenks
        classification = 'jenks'
    elif breaks == 2: # Quantile
        classification = 'quantile'
    elif breaks == 3: # Equal Interval
        classification = 'equal'
    elif breaks == 4: # Percentiles
        classification = 'percentiles'
    elif breaks == 5: # Natural Breaks
        classification = 'natural'

    # colors
    colorNum = colorVal.get()
    if colorNum == 1:
        color = 'blue'
    elif colorNum == 2:
       color = 'green'
    elif colorNum == 3:
       color = 'red'
    elif colorNum == 4:
        color = 'purple'
    elif colorNum == 5:
        color = 'gold'

    # base maps
    base = baseVal.get()
    if base == 1:               
        baseMap = 'satellite'
    elif base == 2:            
        baseMap = 'streets'
    elif base == 3:             
        baseMap = 'outdoors'
    elif base == 4:             
        baseMap = 'dark'
    elif base == 5:      
        baseMap = 'light'

    try:
        # create map and handle errors
        createMap.Web(csv_data, classification, color, baseMap, grouping)
    except Exception as e:
        print("\n#---------------------------------ERROR---------------------------------#")
        print("Try again. Select a data classification method, color palette, and base map.")
        sys.exit()


    # Done
    runtime = datetime.datetime.now() - start
    print ("RUN COMPLETED")
    print(str(runtime))
    window.destroy()


#----------------------------------FOLIUM BUTTON EVENT----------------------------------#
def clickedFolium():
    csv_data = window.filename

    print ("handling radio parameters")

    # colors
    colorNum = colorVal.get()
    if colorNum == 1:
        color = 'blue'
    elif colorNum == 2:
       color = 'green'
    elif colorNum == 3:
       color = 'red'
    elif colorNum == 4:
        color = 'purple'
    elif colorNum == 5:
        color = 'gold'

    # base maps
    base = baseVal.get()
    if base == 1:               
        baseMap = 'satellite'
    elif base == 2:            
        baseMap = 'streets'
    elif base == 3:             
        baseMap = 'outdoors'
    elif base == 4:             
        baseMap = 'dark'
    elif base == 5:      
        baseMap = 'light'

    # create map and handle errors
    try:
        createMap.Folium(csv_data, color, baseMap)
    except Exception as e:
        print("\n#---------------------------------ERROR---------------------------------#")
        print("Try again. Select a color palette and base map to create a Folium map.")
        sys.exit()
    

    # Done
    runtime = datetime.datetime.now() - start
    print ("RUN COMPLETED")
    print(str(runtime))
    window.destroy()
 
#----------------------------------TKINTER----------------------------------#
window = Tk()
window.title('Choropleth Map Creator')
#window.geometry('500x500')

# grab option values
classVal = IntVar()
colorVal = IntVar()
baseVal = IntVar()
densityVal = BooleanVar()
densityVal.set(False) # set check state (density)

window.update()

# open file selection dialog
window.filename =  filedialog.askopenfilename(
    initialdir = "../data/csv",
    title = "Select file",
    filetypes = (("csv files","*.csv"),("all files","*.*"))
)
 
# gives weight to the cells in the grid
rows = 0
while rows < 50:
    window.rowconfigure(rows, weight=1)
    window.columnconfigure(rows, weight=1)
    rows += 1
 
# Defines and places the notebook widget
nb = ttk.Notebook(window)
nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')
 

#----------------------------------WEB TAB----------------------------------#
# Adds tab 1 of the notebook
page1 = Frame(nb, bg='white')
nb.add(page1, text='Web')

# classification options
title1 = Label(page1, text="Select a data classification method")
jenks = Radiobutton(page1,text='Jenks', value=1, variable=classVal)
quantile = Radiobutton(page1,text='Quantile', value=2, variable=classVal)
equal = Radiobutton(page1,text='Equal Interval', value=3, variable=classVal)
percentile = Radiobutton(page1,text='Percentile', value=4, variable=classVal)
natural = Radiobutton(page1,text='Natural Breaks', value=5, variable=classVal)

# color options
title2 = Label(page1, text="Select a color palette")
blue = Radiobutton(page1,text='Blue', value=1, variable=colorVal)
green = Radiobutton(page1,text='Green', value=2, variable=colorVal)
red = Radiobutton(page1,text='Red', value=3, variable=colorVal)
purple = Radiobutton(page1,text='Purple', value=4, variable=colorVal)
gold = Radiobutton(page1,text='Gold', value=5, variable=colorVal)

# base map options
title4 = Label(page1, text="Select a base map")
satellite = Radiobutton(page1,text='Satellite', value=1, variable=baseVal)
streets = Radiobutton(page1,text='Streets', value=2, variable=baseVal)
outdoors = Radiobutton(page1,text='Outdoors', value=3, variable=baseVal)
dark = Radiobutton(page1,text='Dark', value=4, variable=baseVal)
light = Radiobutton(page1,text='Light', value=5, variable=baseVal)

# density option
title3 = Label(page1, text="Enable Density")
density = Checkbutton(page1, text="Divide by the state's area", var=densityVal)
 
# send it
btn = Button(page1, text="Create Map", command=clickedWeb)


#----------------------------------GUI GRID POSITIONING----------------------------------#
# classifications
title1.grid(column=0, row=0, columnspan=5, sticky=W)
quantile.grid(column=0, row=4, sticky=W)
jenks.grid(column=1, row=4, sticky=W)
percentile.grid(column=2, row=4, sticky=W)
equal.grid(column=3, row=4, sticky=W)
natural.grid(column=4, row=4, sticky=W)

# colors
title2.grid(column=0, row=7, columnspan=5, sticky=W)
blue.grid(column=0, row=8, sticky=W)
gold.grid(column=1, row=8, sticky=W)
green.grid(column=2, row=8, sticky=W)
red.grid(column=3, row=8, sticky=W)
purple.grid(column=4, row=8, sticky=W)

# base maps
title4.grid(column=0, row=9, columnspan=5, sticky=W)
light.grid(column=0, row=10, sticky=W)
dark.grid(column=1, row=10, sticky=W)
satellite.grid(column=2, row=10, sticky=W)
streets.grid(column=3, row=10, sticky=W)
outdoors.grid(column=4, row=10, sticky=W)

# density and submit button
title3.grid(column=0, row=11, columnspan=5, sticky=W)
density.grid (column=0, row=12, columnspan=5, sticky=W)
btn.grid(column=0, row=13, columnspan=5, sticky=W)


#----------------------------------FOLIUM TAB----------------------------------#
page2 = Frame(nb, bg='white')
nb.add(page2, text='Folium')
 
# color options
foliumTitle = Label(page2, text="Select a color palette")
foliumBlue = Radiobutton(page2,text='Blue', value=1, variable=colorVal)
foliumGreen = Radiobutton(page2,text='Green', value=2, variable=colorVal)
foliumRed = Radiobutton(page2,text='Red', value=3, variable=colorVal)
foliumPurple = Radiobutton(page2,text='Purple', value=4, variable=colorVal)
foliumGold = Radiobutton(page2,text='Gold', value=5, variable=colorVal)

# base map options
foliumTitle2 = Label(page2, text="Select a base map")
foliumSatellite = Radiobutton(page2,text='Satellite', value=1, variable=baseVal)
foliumStreets = Radiobutton(page2,text='Streets', value=2, variable=baseVal)
foliumOutdoors = Radiobutton(page2,text='Outdoors', value=3, variable=baseVal)
foliumDark = Radiobutton(page2,text='Dark', value=4, variable=baseVal)
foliumLight = Radiobutton(page2,text='Light', value=5, variable=baseVal)

foliumTitle3 = Label(page2, text="Data classification is quantile")
foliumBtn = Button(page2, text="Create Map", command=clickedFolium)

#----------------------------------GUI GRID POSITIONING----------------------------------#
# colors
foliumTitle.grid(column=0, row=1, columnspan=5, sticky=W)
foliumBlue.grid(column=0, row=3, sticky=W)
foliumGold.grid(column=1, row=3, sticky=W)
foliumGreen.grid(column=2, row=3, sticky=W)
foliumRed.grid(column=3, row=3, sticky=W)
foliumPurple.grid(column=4, row=3, sticky=W)

# base maps
foliumTitle2.grid(column=0, row=5, columnspan=5, sticky=W)
foliumLight.grid(column=0, row=7, sticky=W)
foliumDark.grid(column=1, row=7, sticky=W)
foliumSatellite.grid(column=2, row=7, sticky=W)
foliumStreets.grid(column=3, row=7, sticky=W)
foliumOutdoors.grid(column=4, row=7, sticky=W)

foliumTitle3.grid(column=0, row=11, columnspan=5, sticky=W)

# submit button
foliumBtn.grid(column=0, row=13, columnspan=5, sticky=W)
 
window.mainloop()