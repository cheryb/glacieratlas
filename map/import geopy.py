import geopy 
import pandas as pd
import folium
#import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
#from folium.vector_layers import Rectangle
from folium.plugins import MarkerCluster
from geopy.distance import geodesic
# Read excel file with just coordinates
twila = pd.read_csv('Map_python.csv')
# Read csv file with names
names = pd.read_csv('Map_names.csv')
group_name = names.groupby('NAMES')
# defined distance in kilmeters
distance_threshold = 5
subset_size = 100
twila_subset = twila.head(subset_size)
names_subset = names.head(subset_size)
# Creates a map centered on the first location
center_lat = twila_subset['LAT'].iloc[0]
center_long = twila_subset['LONG'].iloc[0]
my_map = folium.Map(location=[center_lat, center_long], zoom_start = 10)
geolocator = Nominatim(user_agent="email@email.com", timeout=20)
locations = []
marker_cluster = MarkerCluster().add_to(my_map)
for index, row in names_subset.iterrows():
    latitude = row['LAT']
    longitude = row['LONG']
    name = row['NAMES']
    #folium.Marker([latitude, longitude], popup = name, icon=folium.Icon(color='red')).add_to(marker_cluster)
    # Add markers for points in csv file with just coordinates
for index, row in twila_subset.iterrows():
    # Get the longitude and latitude values
    twila_latitude = row['LAT']
    twila_longitude = row['LONG']
    popup_text = f"LAT: {twila_latitude}<br>LONG: {twila_longitude}"
    #folium.Marker([twila_latitude, twila_longitude], popup = popup_text, icon=folium.Icon(color='blue')).add_to(marker_cluster)
    box_size = 0.1
    box = bounds = [(twila_latitude - box_size/2, twila_longitude - box_size/2), (twila_latitude + box_size/2, twila_longitude + box_size/2), (twila_latitude - box_size/2, twila_longitude + box_size), (twila_latitude + box_size/2, twila_longitude - box_size/2)]
for name, group in group_name:
    name_lat = group['LAT'].iloc[0]
    name_long = group['LONG'].iloc[0]
    # Filter database based on the distance threshold from named point
    filter_group = group[group.apply(lambda row: geodesic((row['LAT'], row['LONG']), (name_lat,name_long)).kilometers <= distance_threshold, axis = 1)]
    # Average of Latitude and Longitude
    avg_lat = filter_group['LAT'].mean()
    avg_long = filter_group['LONG'].mean()
    popup_text = f"{name}<br>LAT: {avg_lat}<br>LONG: {avg_long}"
    folium.Marker([avg_lat, avg_long], popup=popup_text, icon=folium.Icon(color='red')).add_to(marker_cluster)
# Add url to map
# Define the link URL and text
link_url = 'https://greenland-glacier-atlas.webnode.page/?_ga=2.50092334.963773679.1689862140-131486709.1689267035'
link_text = 'Click here for more information'
# Create a marker with a clickable link
marker = folium.Marker(
    location=[latitude, longitude],
    popup=folium.Popup(f'<a href="{link_url}">{link_text}</a>'),
    icon=folium.Icon(color='blue')
)
# Add the marker to the map
marker.add_to(my_map)
# Add a satellite tile layer with attribution
satellite_layer = folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr='Google Satellite',
    name='Satellite'
).add_to(my_map)
# Add layer control to toggle between map and satellite layers
folium.LayerControl().add_to(my_map)
my_map
my_map.save('map.html')