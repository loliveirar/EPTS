#KMeans method
#Replace next line with your work folder
#cd "/UNIVERSIDAD/OneDrive - Universidad de Oviedo" <

import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

#Set format
pd.set_option('display.float_format', '{:.10f}'.format)

df = pd.read_excel("Todas.xlsx")
#Filter 
from datetime import time
df["local_time"] = pd.to_datetime(df.local_time)
filtro = (df.local_time.dt.time >= time(13, 2, 44)) & (df.local_time.dt.time < time(13, 48, 0))
df=df.loc[filtro, ]
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
# Number of clusters
num_clusters = 10

# Creating matrix to input KMeans
coordenadas = df[['lon', 'lat']].values

# KMeans algorithm
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(coordenadas)

# Showing results
plt.scatter(df['lon'], df['lat'], c=df['cluster'], cmap='viridis')
plt.title('Clustering de Coordenadas')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.show()

#Add this section to show cluster centroids
centroides = kmeans.cluster_centers_

# Draw graph with centroids
plt.scatter(df['lon'], df['lat'], c=df['cluster'], cmap='viridis', label='Puntos')
plt.scatter(centroides[:, 0], centroides[:, 1], marker='x', s=100, color='red', label='Centroides')
plt.title('Clustering de Coordenadas con Centroides')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.legend()
plt.show()

# Show centroids numeric value
print("Valores numéricos de los centroides:")
for i, centroide in enumerate(centroides):
    print("Centroide {}: Longitud = {:.6f}, Latitud = {:.6f}".format(i+1, centroide[0], centroide[1]))
