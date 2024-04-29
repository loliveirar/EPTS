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



