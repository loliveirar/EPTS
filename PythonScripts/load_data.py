import pandas as pd

#configurar pandas para más decimales
pd.set_option('display.float_format', '{:.10f}'.format)

df = pd.read_excel("Todas.xlsx")
#filtro horario. Primero convertimos el campo a formato hora
from datetime import time
df["local_time"] = pd.to_datetime(df.local_time)
filtro = (df.local_time.dt.time >= time(12, 5, 0)) & (df.local_time.dt.time < time(12, 50, 0))
df=df.loc[filtro, ]

# Cálculo de posiciones medias por jugadora
medias_por_jugadora = df.groupby('DEV').mean('lat','lon') 
medias_por_jugadora.to_excel("medias_por_jugadora.xlsx")
# o df.groupby(['DEV'])[["lat","lon"]].mean()

# Añadir un campo nuevo por línea
primera = {2,4,7,19}
segunda = {10,12}
tercera = {6,8,11}
cuarta = {18}
df['line']=[1 if s in primera else 2 if s in segunda else 3 if s in tercera else 4 if s in cuarta else 0 for s in df["DEV"]]
# Cálculo de posiciones medias por línea
medias_por_linea = df.groupby('line').mean('lat','lon') 
medias_por_linea.to_excel("medias_por_linea.xlsx")

#filtrar datos dejando solo a las titulares
equipo = {2,4,6, 7,8,10,11,12,18,19}
resultado_filtrado = df[df['DEV'].isin(equipo)]
#para ver media del equipo
resultado_filtrado.describe()

#-------------------------------------------------
# Cálculo de media de la línea defensiva (registros 0,3,5 y 13 del dataframe)
medias.to_excel("nombrefichero.xlsx")
medias.iloc[['0','3','5','13']].mean()
# líneas
primera = "DEV==2 or DEV==5 or DEV==7 or DEV==19"
segunda = "DEV==3 or DEV==10"
tercera = "DEV==8 or DEV==9 or DEV==6"
cuarta = "DEV==18"
(medias.query(primera)).mean()

#--------------------------------------------------
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

