import pandas as pd

#Set format
pd.set_option('display.float_format', '{:.10f}'.format)

df = pd.read_excel("data.xlsx")
#Filtering by hour. Change to match appropiate time
from datetime import time
df["local_time"] = pd.to_datetime(df.local_time)
filtro = (df.local_time.dt.time >= time(12, 5, 0)) & (df.local_time.dt.time < time(12, 50, 0))
df=df.loc[filtro, ]

# Centroids by player
medias_por_jugadora = df.groupby('DEV').mean('lat','lon') 

# Add this section to draw centroids on the satellite map -------------------
import plotly.express as px
px.set_mapbox_access_token('pk.eyJ1IjoibG9saXZlaXJhciIsImEiOiJjbHFmZ2I4cXcwd2p6Mm9tazI5Z3RybjBwIn0.5QzzXVPTSVGSaF7v7buy2A')
# Create graph
fig = px.scatter_mapbox(medias_por_jugadora, lat='lat', lon='lon', zoom=18, color_discrete_sequence=['yellow'], size_max=1)
# Points size
fig.update_traces(marker=dict(size=10))
# Define style
fig.update_layout(mapbox_style="satellite")

# Show map
fig.show()
# ------------ end of section to draw map ------------------------------------

medias_por_jugadora.to_excel("meansbyplayer.xlsx")
# o df.groupby(['DEV'])[["lat","lon"]].mean()

# Add field 'line' depending on the position of each player
primera = {2,4,7,19} #defenders
segunda = {10,12} #pivots
tercera = {6,8,11} #midfielders
cuarta = {18} #forward
df['line']=[1 if s in primera else 2 if s in segunda else 3 if s in tercera else 4 if s in cuarta else 0 for s in df["DEV"]]
# Centroids by lines
medias_por_linea = df.groupby('line').mean('lat','lon') 
medias_por_linea.to_excel("meansbyline.xlsx")

#Filtering to study only a set of players(delete it if you don't need it)
equipo = {2,4,6, 7,8,10,11,12,18,19}
resultado_filtrado = df[df['DEV'].isin(equipo)]
#Show centroid for the whole team
resultado_filtrado.describe()

#-------------------------------------------------
# Calculating centroid for defenders line (registers 0,3,5 y 13 from dataframe)
medias.to_excel("meansdefenders.xlsx")
medias.iloc[['0','3','5','13']].mean()
# lines
primera = "DEV==2 or DEV==5 or DEV==7 or DEV==19"
segunda = "DEV==3 or DEV==10"
tercera = "DEV==8 or DEV==9 or DEV==6"
cuarta = "DEV==18"
(medias.query(primera)).mean()

#--------------------------------------------------
#filter by player id=5 to obtain her heat map
filtroJugadora = df["DEV"]==5
df5=df.loc[filtroJugadora, ]

dfx=df5[['DEV','lat','lon']]
dfx = dfx.groupby(['DEV', 'lat', 'lon']).size().reset_index(name='frecuencia')

#To show heat map
import plotly.express as px
px.set_mapbox_access_token('pk.eyJ1IjoibG9saXZlaXJhciIsImEiOiJjbHFmZ2I4cXcwd2p6Mm9tazI5Z3RybjBwIn0.5QzzXVPTSVGSaF7v7buy2A')
fig = px.density_mapbox(dfx, lat = 'lat', lon = 'lon', z = 'frecuencia',
                        radius = 12,
                        zoom = 17,
                        mapbox_style = 'satellite',
                        color_continuous_scale = 'rainbow',
                        opacity=1
                        )
fig.update_layout(
    mapbox=dict(
        bearing=0,
        coloraxis_colorbar=None
    ),
    uirevision=True,
)
#To hide side colorbar
fig.update(layout_coloraxis_showscale=False)
#To show figure
fig.show()
#To export image as jpg
fig.write_image("imagen.jpg")

#--To calculate distances between two consecutive coordinates-------------------
#Uses external function getDistanceBetweenPointsNew
df2['distance'] = getDistanceBetweenPointsNew(df2['lat'] , df2['lon'] , df2['lat'].shift(1) , df2['lon'].shift(1),unit='meters')
#To eliminate situations in which player stays
filtroDistance = df2["distance"]>0.20
df2=df2.loc[filtroDistance, ]
#--end of section--------------------------------------------------------------


#Section to calculate centroid from heat zones --------------------------------
import pandas as pd
import numpy as np
import plotly.express as px

# Supongamos que tienes un DataFrame llamado df con las columnas 'lat' y 'lon'

# Agrupar por latitud y longitud y contar cuántas veces aparece cada combinación
df_grouped = df2.groupby(['lat', 'lon']).size().reset_index(name='frecuencia')

# Ordenar el DataFrame por frecuencia en orden descendente
df_sorted = df_grouped.sort_values(by='frecuencia', ascending=False)

# Seleccionar las cuatro zonas con más frecuencia
top_zones = df_sorted.head(20)

# Calcular el centroide de las zonas seleccionadas
centroid_lat = np.mean(top_zones['lat'])
centroid_lon = np.mean(top_zones['lon'])

# Añadir una nueva fila al DataFrame con las coordenadas del centroide
df_centroid = pd.DataFrame({'lat': [centroid_lat], 'lon': [centroid_lon]})

# Concatenar el DataFrame original con el DataFrame del centroide
df_with_centroid = pd.concat([df_grouped, df_centroid])

# Crear el mapa de calor
fig = px.density_mapbox(df_with_centroid, lat='lat', lon='lon', z='frecuencia',
                        radius=5, zoom=18,
                        mapbox_style='satellite',
                        color_continuous_scale='Viridis')

# Añadir el punto del centroide al mapa de calor
fig.add_scattermapbox(lat=[centroid_lat], lon=[centroid_lon], mode='markers', marker=dict(size=10, color='yellow'))

# Mostrar el mapa
fig.show()
# end of section ------------------------------------------------------------
