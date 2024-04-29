# Add here lines to load data in df dataframe!
# DBSCAN Method
import pandas as pd
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

#Apply DBSCAN
dbscan = DBSCAN(eps=0.1, min_samples=3)
df['cluster'] = dbscan.fit_predict(coordenadas)

# Showing results
fig, ax = plt.subplots()

for cluster_label in coordenadas_df['cluster'].unique():
    if cluster_label == -1:
        # Noise points
        cluster_data = df[df['cluster'] == cluster_label]
        ax.scatter(cluster_data['lon'], cluster_data['lat'], s=30, label=f'Noise')
    else:
        # Cluster points
        cluster_data = df[df['cluster'] == cluster_label]
        ax.scatter(cluster_data['longitud'], cluster_data['latitud'], label=f'Cluster {cluster_label}')

ax.set_title('Clustering de Coordenadas con DBSCAN')
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')
ax.legend()
plt.show()