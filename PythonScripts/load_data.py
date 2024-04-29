import pandas as pd

#Set format
pd.set_option('display.float_format', '{:.10f}'.format)

df = pd.read_excel("data.xlsx")
#Filtering by hour
from datetime import time
df["local_time"] = pd.to_datetime(df.local_time)
filtro = (df.local_time.dt.time >= time(12, 5, 0)) & (df.local_time.dt.time < time(12, 50, 0))
df=df.loc[filtro, ]

# Centroids by player
medias_por_jugadora = df.groupby('DEV').mean('lat','lon') 
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

import plotly.express as px
px.set_mapbox_access_token('pk.eyJ1IjoibG9saXZlaXJhciIsImEiOiJjbHFmZ2I4cXcwd2p6Mm9tazI5Z3RybjBwIn0.5QzzXVPTSVGSaF7v7buy2A')
fig = px.density_mapbox(dfx, lat = 'lat', lon = 'lon', z = 'frecuencia',
                        radius = 12,
                        center = dict(lat = 43.276628, lon = -2.83865),
                        zoom = 17,
                        mapbox_style = 'satellite',
                        color_continuous_scale = 'rainbow',
                        opacity=1
                        )
fig.update_layout(
    mapbox=dict(
        bearing=120,
    ),
    uirevision=True,
)
fig.show()

