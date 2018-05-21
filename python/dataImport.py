# Ben Elan
# Spring 2018
# handles command line arguements for creating leaflet maps
# check the README for more details
print("RUNNING COMMAND LINE MAP CREATION")
print("importing libraries")

import datetime                     # timer
start = datetime.datetime.now()
import sys                          # comand line 
import createMap                    # map creation functions

def main():
    print("handling command line arguements")
    # set default
    grouping = 'none'
    classification = 'quantile'
    color = 'blue'
    base = 'satellite'
    mapType = 'both'
    csv_data = "../data/csv/data.csv"

    # change defaults based on command line arguements
    if len(sys.argv) > 1:
        classification = sys.argv[1]
        if len(sys.argv) > 2:
            color = sys.argv[2]
            if len(sys.argv) > 3:
                base = sys.argv[3]
                if len(sys.argv) > 4:
                    grouping = sys.argv[4]
                    if len(sys.argv) > 5:
                        mapType = sys.argv[5]

    # create maps
    if mapType == 'folium':
        createMap.Folium(csv_data, color, base)
    elif mapType == 'web':
        createMap.Web(csv_data, classification, color, base, grouping)
    else:
        createMap.Web(csv_data, classification, color, base, grouping)
        createMap.Folium(csv_data, color, base)

    # Done
    runtime = datetime.datetime.now() - start
    print ("RUN COMPLETED")
    print(str(runtime))

if __name__ == '__main__':
	main()