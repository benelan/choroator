# Ben Elan
# Spring 2018
# Python script to create a choropleth map using folium
# quantile class breaks
# Takes a GEOJSON of states and a CSV as inputs
# user can create their own CSV with their own data
# CSV Format:
        # Header (first row):
                # 'State',Title
                        # ie (State,Income)
        # Data (the rest):
                # State Name,Data
                        # ie (California,53489)

# import libraries
import os
import pandas as pd
import json
import folium

# read json
state_geo = os.path.join('../data/json', 'input.json')

# ready csv
state_csv = os.path.join('../data/csv', 'folium_income.csv')
state_data = pd.read_csv(state_csv)

# create map
m = folium.Map(location=[48, -102], zoom_start=3) #, tiles="Mapbox Control room")

# add data as choropleth
m.choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=state_data,
    columns=['State','Income'],		# change the second column name to use your own data
    key_on='feature.properties.name',
    fill_color='BuGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Average Income ($)'	# change the legend name to use your own data
)

# save
folium.LayerControl().add_to(m)
m.save(outfile='../foliumMap.html')