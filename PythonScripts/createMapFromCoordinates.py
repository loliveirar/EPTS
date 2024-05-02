import pandas as pd
# Create map from a set of given coordinates
# Datos
data = {
    'DEV': [2, 4, 6, 7, 8, 10, 11, 12, 18, 19],
    'LAT': [43.3552793500, 43.3555372083, 43.3554537917, 43.3554595000, 43.3553385000, 
            43.3553719583, 43.3556621667, 43.3554924167, 43.3553941250, 43.3553482083],
    'LON': [-5.9227981500, -5.9228211667, -5.9225615417, -5.9229905000, -5.9226570833,
            -5.9227041250, -5.9225802500, -5.9227469167, -5.9225585417, -5.9228889167]
}

# Crear DataFrame
dfnew = pd.DataFrame(data)

import plotly.graph_objects as go

# Mapbox token

mapbox_access_token='pk.eyJ1IjoibG9saXZlaXJhciIsImEiOiJjbHFmZ2I4cXcwd2p6Mm9tazI5Z3RybjBwIn0.5QzzXVPTSVGSaF7v7buy2A'


# Def figure
fig = go.Figure()

# Add points to the map
fig.add_trace(go.Scattermapbox(
    lat=dfnew['LAT'],
    lon=dfnew['LON'],
    mode='markers',  # Mode marker to show points
    marker=go.scattermapbox.Marker(
        size=8,  # Size of markers
        color='yellow',  # Markers colors
        opacity=1  
    ),
    text=df['DEV'],  # Tooltips text
    hoverinfo='text'  # Only show text in tooltips
))

# Other configurations
fig.update_layout(
    mapbox_style="satellite",  
    mapbox_accesstoken=mapbox_access_token,
    mapbox_center_lon=dfnew['LON'].mean(),
    mapbox_center_lat=dfnew['LAT'].mean(),
    mapbox_zoom=18
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})  

# Show map
fig.show()