import streamlit as st
import pandas as pd
import numpy as np
import folium
from geopy.distance import geodesic
from geopy import Point
from streamlit_folium import folium_static
import pyproj
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

def get_geodesic_point(start, bearing, distance):
    geod = pyproj.Geod(ellps='WGS84')
    lon, lat, _ = geod.fwd(start[1], start[0], bearing, distance)
    return lat, lon

# Initialize the merged_flight_paths data
data = [
    {'Orig_orig': 'NRT', 'Dest': 'ICN', 'Counts': 16, 'OrigAirpName_orig': 'TOKYO NARITA INTL', 'OrigCity_orig': 'TYO', 'OrigCityNme_orig': 'TOKYO', 'OrigCountry_orig': 'JP', 'OrigCountryName_orig': 'JAPAN', 'OrigCont_orig': 'AP', 'OrigContName_orig': 'ASIA/PACIFIC', 'orig_x_orig': 140.3864, 'orig_y_orig': 35.7647, 'Orig_dest': 'ICN', 'OrigAirpName_dest': 'SEOUL INCHEON INTERNATIONAL AIRPORT', 'OrigCity_dest': 'SEL', 'OrigCityNme_dest': 'SEOUL', 'OrigCountry_dest': 'KR', 'OrigCountryName_dest': 'KOREA REPUBLIC OF', 'OrigCont_dest': 'AP', 'OrigContName_dest': 'ASIA/PACIFIC', 'orig_x_dest': 126.4506, 'orig_y_dest': 37.4692},
    {'Orig_orig': 'LHR', 'Dest': 'JFK', 'Counts': 14, 'OrigAirpName_orig': 'LONDON HEATHROW', 'OrigCity_orig': 'LON', 'OrigCityNme_orig': 'LONDON', 'OrigCountry_orig': 'GB', 'OrigCountryName_orig': 'UNITED KINGDOM', 'OrigCont_orig': 'EU', 'OrigContName_orig': 'EUROPE', 'orig_x_orig': -0.461389, 'orig_y_orig': 51.4775, 'Orig_dest': 'JFK', 'OrigAirpName_dest': 'NEW YORK J F KENNEDY INTERNATIONAL AIRPORT', 'OrigCity_dest': 'NYC', 'OrigCityNme_dest': 'NEW YORK', 'OrigCountry_dest': 'US', 'OrigCountryName_dest': 'UNITED STATES', 'OrigCont_dest': 'NA', 'OrigContName_dest': 'NORTH AMERICA', 'orig_x_dest': -73.7781, 'orig_y_dest': 40.6398},
    {'Orig_orig': 'SFO', 'Dest': 'LAX', 'Counts': 13, 'OrigAirpName_orig': 'SAN FRANCISCO INTERNATIONAL AIRPORT', 'OrigCity_orig': 'SFO', 'OrigCityNme_orig': 'SAN FRANCISCO', 'OrigCountry_orig': 'US', 'OrigCountryName_orig': 'UNITED STATES', 'OrigCont_orig': 'NA', 'OrigContName_orig': 'NORTH AMERICA', 'orig_x_orig': -122.375, 'orig_y_orig': 37.6189, 'Orig_dest': 'LAX', 'OrigAirpName_dest': 'LOS ANGELES INTERNATIONAL AIRPORT', 'OrigCity_dest': 'LAX', 'OrigCityNme_dest': 'LOS ANGELES', 'OrigCountry_dest': 'US', 'OrigCountryName_dest': 'UNITED STATES', 'OrigCont_dest': 'NA', 'OrigContName_dest': 'NORTH AMERICA', 'orig_x_dest': -118.4081, 'orig_y_dest': 33.9425},
    {'Orig_orig': 'SYD', 'Dest': 'MEL', 'Counts': 11, 'OrigAirpName_orig': 'SYDNEY KINGSFORD SMITH', 'OrigCity_orig': 'SYD', 'OrigCityNme_orig': 'SYDNEY', 'OrigCountry_orig': 'AU', 'OrigCountryName_orig': 'AUSTRALIA', 'OrigCont_orig': 'AP', 'OrigContName_orig': 'ASIA/PACIFIC', 'orig_x_orig': 151.1772, 'orig_y_orig': -33.9461, 'Orig_dest': 'MEL', 'OrigAirpName_dest': 'MELBOURNE TULLAMARINE', 'OrigCity_dest': 'MEL', 'OrigCityNme_dest': 'MELBOURNE', 'OrigCountry_dest': 'AU', 'OrigCountryName_dest': 'AUSTRALIA', 'OrigCont_dest': 'AP', 'OrigContName_dest': 'ASIA/PACIFIC', 'orig_x_dest': 144.8433, 'orig_y_dest': -37.6733},
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
    line_points = [get_geodesic_point(orig, bearing, fraction * distance) for fraction in np.linspace(0, 1, num=1000)]
    
    folium.PolyLine(locations=line_points, color="blue", weight=2.5, opacity=1).add_to(m)

# Display the map in the Streamlit app
folium_static(m)
