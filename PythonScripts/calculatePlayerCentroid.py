#!/usr/bin/env python
# coding: utf-8

# This snippet calculates a player centroid from her geopositioning data.
# It executes the following steps:
# - Load original data
# - Filter with match time
# - Filter for a given player
# - Clean data to delete coordinates in which player stays
# - Calculate n most density zones
# - Calculate centroid from previously calculated n zones
# - Show heatmap
# - Show calculated centroid

# Move to working folder
cd "/UNIVERSIDAD/OneDrive - Universidad de Oviedo"


# In[1]:


import pandas as pd
#Set format
pd.set_option('display.float_format', '{:.10f}'.format)

df = pd.read_excel("todas.xlsx")
#Filtering by hour
from datetime import time
df["local_time"] = pd.to_datetime(df.local_time)
filtro = (df.local_time.dt.time >= time(12, 2, 12)) & (df.local_time.dt.time < time(12, 49, 50))
df=df.loc[filtro, ]


# In[2]:
#filter by player id=4 to obtain her heat map
filtroJugadora = df["DEV"]==4
df4=df.loc[filtroJugadora, ]

dfx=df4[['DEV','lat','lon']]
dfx = dfx.groupby(['DEV', 'lat', 'lon']).size().reset_index(name='frecuencia')

import plotly.express as px
px.set_mapbox_access_token('pk.eyJ1IjoibG9saXZlaXJhciIsImEiOiJjbHFmZ2I4cXcwd2p6Mm9tazI5Z3RybjBwIn0.5QzzXVPTSVGSaF7v7buy2A')
fig = px.density_mapbox(dfx, lat = 'lat', lon = 'lon', z = 'frecuencia',
                        radius = 5,
                        zoom = 17,
                        mapbox_style = 'satellite',
                        color_continuous_scale = 'rainbow',
                        opacity=1
                        )
fig.update_layout(
    mapbox=dict(
        bearing=0       
    ),
    uirevision=True,
)
fig.update(layout_coloraxis_showscale=False)

fig.show()


# In[3]:


#To eliminate situations in which player stays
df4['distance'] = getDistanceBetweenPointsNew(df4['lat'] , df4['lon'] , df4['lat'].shift(1) , df4['lon'].shift(1),unit='meters')
#To eliminate situations in which player stays
filtroDistance = df4["distance"]>0.20
df4=df4.loc[filtroDistance, ]


# In[4]:


df4


# In[5]:


import pandas as pd
import numpy as np
import plotly.express as px

# We assume that we have a dataframe df with 'lat' y 'lon' columns

# Group by lat and long. Count number of times.
df_grouped = df4.groupby(['lat', 'lon']).size().reset_index(name='frecuencia')

# To order dataframe
df_sorted = df_grouped.sort_values(by='frecuencia', ascending=False)

# To select 4 most density zones
top_zones = df_sorted.head(4)

# With selected zones, calculate centroids
centroid_lat = np.mean(top_zones['lat'])
centroid_lon = np.mean(top_zones['lon'])

# Add new row with calculated centroid
df_centroid = pd.DataFrame({'lat': [centroid_lat], 'lon': [centroid_lon]})

# Concat calculated df_centroid with original dataframe
df_with_centroid = pd.concat([df_grouped, df_centroid])

# Show heatmap (most density zones and its centroid)
fig = px.density_mapbox(df_with_centroid, lat='lat', lon='lon', z='frecuencia',
                        radius=5, zoom=18,
                        mapbox_style='satellite',
                        color_continuous_scale='Viridis')

# Add centroid calculated from most frequent zones
fig.add_scattermapbox(lat=[centroid_lat], lon=[centroid_lon], mode='markers', marker=dict(size=10, color='yellow'))

# Show map
fig.show()



# In[6]:
# To show actual dataframe

df4 

# To show calculated centroid (using coordinates)
df_centroid







