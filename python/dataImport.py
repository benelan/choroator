# Ben Elan
# Spring 2018
# Python script to insert csv data into a GEOJSON file
# Takes a preformated GEOJSON and a CSV as inputs
# user can create their own CSV with their own data
# CSV Format:
        # Header (first row):
                # Category,Units,Source
                        # ie (Average Income,data.gov)
        # Data (the rest):
                # State,Data
                        # ie (California,53489)
print("RUNNING DATA IMPORT")
print("importing libraries")
import datetime
start = datetime.datetime.now()
import json
import csv
import sys
import pysal as ps # for data classification
import webbrowser, os

def main():
        print("opening csv")
        # to change the dataset
        # just change the csv file below
        with open('../data/csv/data.csv', 'r') as f:
                csvList = [row for row in csv.reader(f.read().splitlines())]
                print("opening json")
                data = json.load(open('../data/json/input.json')) # preset json format to work with the js
                
                print("handling command line arguements")
                # default
                grouping = 'none'
                classification = 'jenks'
                color = 'blue'
                base = 'satellite'
                
                if len(sys.argv) > 1:
                        classification = sys.argv[1]
                        if len(sys.argv) > 2:
                                color = sys.argv[2]
                                if len(sys.argv) > 3:
                                        base = sys.argv[3]
                                        if len(sys.argv) > 4:
                                                grouping = sys.argv[4]
                
                print("inserting data")
                # iterate through the csv
                # inserting number data
                # keeping track of the numbers of the data
                # so that we can determine class breaks
                numbers = []
                for row in csvList:
                        for i, item in enumerate(data["features"]):
                                if item["properties"]["name"] == row[0]:
                                        if grouping == 'density':
                                                # do not add D.C to numbers list for normalization
                                                # because it is so small and skews the classification
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

                
                # setting global info
                if grouping == 'density':
                        data["category"] = csvList[0][0] + ' Density'
                        data["unit"] = csvList[0][1] + '/km<sup>2</sup>'
                else:
                        data["category"] = csvList[0][0]
                        data["unit"] = csvList[0][1]

                data["source"] = csvList[0][2]
                
                # setting color. default is blue
                if (color != 'green') and (color != 'red') and (color != 'gold') and (color != 'purple'):
                        data["color"] = 'blue'
                else:
                        data["color"] = color

                # setting basemap. default is satellite
                if (base != 'dark') and (base != 'light') and (base != 'streets') and (base != 'outdoors'):
                        data["base"] = 'satellite'
                else:
                        data["base"] = base


                # setting data classifications. default is jenks
                if classification == 'quantile': # Quantile
                        classes = ps.esda.mapclassify.Quantiles(numbers, 6).bins
                        c = []
                        for item in classes:
                                c.append(item)
                        data["grade"] = c
                elif classification == 'equal': # Equal Interval
                        classes = ps.esda.mapclassify.Equal_Interval(numbers, 6).bins
                        c = []
                        for item in classes:
                                c.append(item)
                        data["grade"] = c
                elif classification == 'percentiles': # Percentiles
                        classes = ps.esda.mapclassify.Percentiles(numbers, 6).bins
                        c = []
                        for item in classes:
                                c.append(item)
                        data["grade"] = c
                elif classification == 'natural': # Natural Breaks
                        classes = ps.esda.mapclassify.Natural_Breaks(numbers, 6).bins
                        c = []
                        for item in classes:
                                c.append(item)
                        data["grade"] = c
                else:   # Default to Jenks
                        classes = ps.esda.mapclassify.Fisher_Jenks(numbers, 6).bins
                        c = []
                        for item in classes:
                                c.append(item)
                        data["grade"] = c
                        classification = 'jenks'

               
                print("using {} breaks: {}".format(classification, str(data["grade"])))
                
                print("writing output json file")
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
                print("RUN COMPLETED")
                print(str(runtime))
                webbrowser.open('file://' + os.path.realpath('../index.html'))

if __name__ == '__main__':
	main()
