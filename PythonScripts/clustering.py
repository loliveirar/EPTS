cd "/UNIVERSIDAD/OneDrive - Universidad de Oviedo"
cd "TESIS/DATOS/RealOviedo/Oviedo Moderno CF_JORNADA 13 - ATHLETIC C_RawData"
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

#configurar pandas para más decimales
pd.set_option('display.float_format', '{:.10f}'.format)

df = pd.read_excel("Todas.xlsx")
#filtro horario. Primero convertimos el campo a formato hora
from datetime import time
df["local_time"] = pd.to_datetime(df.local_time)
filtro = (df.local_time.dt.time >= time(13, 2, 44)) & (df.local_time.dt.time < time(13, 48, 0))
df=df.loc[filtro, ]
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
# Número de clusters que deseas encontrar (puedes ajustar esto según tu caso).
num_clusters = 10

# Crear una matriz de coordenadas para alimentar al algoritmo KMeans.
coordenadas = df[['lon', 'lat']].values

# Aplicar KMeans
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(coordenadas)

# Visualizar los resultados
plt.scatter(df['lon'], df['lat'], c=df['cluster'], cmap='viridis')
plt.title('Clustering de Coordenadas')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.show()



# metodo DBSCAN
import pandas as pd
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt# Aplicar DBSCAN

dbscan = DBSCAN(eps=0.1, min_samples=3)
df['cluster'] = dbscan.fit_predict(coordenadas)

# Visualizar los resultados
fig, ax = plt.subplots()

for cluster_label in coordenadas_df['cluster'].unique():
    if cluster_label == -1:
        # Puntos de ruido
        cluster_data = df[df['cluster'] == cluster_label]
        ax.scatter(cluster_data['lon'], cluster_data['lat'], s=30, label=f'Noise')
    else:
        # Puntos de clúster
        cluster_data = df[df['cluster'] == cluster_label]
        ax.scatter(cluster_data['longitud'], cluster_data['latitud'], label=f'Cluster {cluster_label}')

ax.set_title('Clustering de Coordenadas con DBSCAN')
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')
ax.legend()
plt.show()