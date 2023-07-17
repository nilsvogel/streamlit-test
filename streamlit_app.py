import streamlit as st
import pandas as pd
import numpy as np
import folium
from geopy.distance import great_circle
from geopy import Point
from streamlit_folium import folium_static
import math

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formula used to calculate bearing is:
        θ = atan2(sin(Δlong).cos(lat2), cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :param pointA: tuple of (latitude, longitude)
    :param pointB: tuple of (latitude, longitude)
    :returns: initial compass bearing in degrees, as a float
    """

    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2() returns values from -π to + π so we need to normalize the result
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

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
    distance = great_circle(orig, dest).miles
    initial_bearing = calculate_initial_compass_bearing(orig, dest)

    # Get points along the great circle path
    line_points = [(great_circle(orig, distance_fraction * distance).destination.latitude, great_circle(orig, distance_fraction * distance).destination.longitude) for distance_fraction in np.linspace(0, 1, num=50)]
    
    folium.PolyLine(locations=line_points, color="blue", weight=2.5, opacity=1).add_to(m)

# Display the map in the Streamlit app
folium_static(m)
