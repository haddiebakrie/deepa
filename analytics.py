from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
import folium
import geopandas as gpd

pytrends = TrendReq(hl='en-US', tz=360, geo="NG")
kw_list = ["face cream"]


def get_related_queries(queries):
    pytrends.build_payload(queries, cat=0, timeframe='today 5-y', geo='NG', gprop='')
    df = pytrends.related_queries()
    return df

def get_interest_by_region(queries):
    pytrends.build_payload(queries, cat=0, timeframe='today 5-y', geo='NG', gprop='')
    df = pytrends.interest_by_region()
    return df

df = get_interest_by_region(["face cream"])
# Reset index to get regions in a column
df = df.reset_index()

# Load Nigeria's geospatial data
nigeria = gpd.read_file('gdms/gadm41_NGA_0.shp')

# Inspect the first few rows of the geospatial data to ensure correct loading
print(nigeria.head())

# Merge the interest data with the geospatial data
# Ensure the column names used for merging are correct
nigeria_map = nigeria.merge(df, how='left', left_on='COUNTRY', right_on='geoName')

# Check the merged data
print(nigeria_map.head())

# Create a base map
m = folium.Map(location=[9.0820, 8.6753], zoom_start=6)

# Add choropleth layer to the map
folium.Choropleth(
    geo_data=nigeria_map,
    name='choropleth',
    data=nigeria_map,
    columns=['COUNTRY', 'face cream'],
    key_on='feature.properties.COUNTRY',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Interest in "face cream"'
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save('nigeria_face_cream_interest_map.html')

# Display the map
m.show_in_browser()