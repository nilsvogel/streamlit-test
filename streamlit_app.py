import streamlit as st
import pandas as pd
import numpy as np
import folium
from geopy.distance import geodesic
from geopy import Point
from streamlit_folium import folium_static
import pyproj
import math

def get_geodesic_point(start, bearing, distance):
    geod = pyproj.Geod(ellps='WGS84')
    lon, lat, _ = geod.fwd(start[1], start[0], bearing, distance)
    return lat, lon

# Initialize the merged_flight_paths data
data = [
    {'Orig_orig': 'NRT', 'Dest': 'ICN', 'Counts': 16, 'OrigAirpName_orig': 'TOKYO NARITA INTL', 'OrigCity_orig': 'TYO', 'OrigCityNme_orig': 'TOKYO', 'OrigCountry_orig': 'JP', 'OrigCountryName_orig': 'JAPAN', 'OrigCont_orig': 'AP', 'OrigContName_orig': 'ASIA/PACIFIC', 'orig_x_orig': 140.3864, 'orig_y_orig': 35.7647, 'Orig_dest': 'ICN', 'OrigAirpName_dest': 'SEOUL INCHEON INTERNATIONAL AIRPORT', 'OrigCity_dest': 'SEL', 'OrigCityNme_dest': 'SEOUL', 'OrigCountry_dest': 'KR', 'OrigCountryName_dest': 'KOREA REPUBLIC OF', 'OrigCont_dest': 'AP', 'OrigContName_dest': 'ASIA/PACIFIC', 'orig_x_dest': 126.4506, 'orig_y_dest': 37.4692},
    # Add more data as needed...
]

merged_flight_paths = pd.DataFrame(data)

# Initialize map centered at [0, 0] (near coast of Africa)
m = folium.Map(location=[0, 0], zoom_start=2)

# Add lines for each flight path
for idx, row in merged_flight_paths.iterrows():
    orig = (row['orig_y_orig'], row['orig_x_orig'])
    dest = (row['orig_y_dest'], row['orig_x_dest'])

    # Get the great circle distance and initial bearing from orig to dest
    distance = geodesic(orig, dest).miles
    bearing = calculate_initial_compass_bearing(orig, dest)

    # Get points along the great circle path
    line_points = [get_geodesic_point(orig, bearing, d) for d in np.linspace(0, distance, num=50)]
    
    folium.PolyLine(locations=line_points, color="blue", weight=2.5, opacity=1).add_to(m)

# Display the map in the Streamlit app
folium_static(m)
