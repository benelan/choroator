# Ben Elan
# Spring 2018
# A GUI that provides options to create maps
# check the README for more details

print("RUNNING APP")
print("importing libraries")
import datetime                             # timer
start = datetime.datetime.now()
from tkinter import filedialog              # gui file opener
from tkinter import *                       # gui
import createMap                            # map creation functions

#----------------------------------BUTTON EVENT----------------------------------#
def clicked():
    csv_data = window.filename

    print ("handling radio parameters")
    grouping = chk_state.get()

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

    # create maps
    createMap.Web(csv_data, classification, color, baseMap, grouping)
    createMap.Folium(csv_data, color, baseMap)
     
    # Done
    runtime = datetime.datetime.now() - start
    print ("RUN COMPLETED")
    print(str(runtime))
    window.destroy()

#----------------------------------TKINTER----------------------------------#
window = Tk()

window.title("Choropleth Map Creator")

classVal = IntVar()
colorVal = IntVar()
baseVal = IntVar()
chk_state = BooleanVar()
chk_state.set(False) # set check state

window.update()

window.filename =  filedialog.askopenfilename(
    initialdir = "../data/csv",
    title = "Select file",
    filetypes = (("csv files","*.csv"),("all files","*.*"))
)

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