import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
matplotlib.use('nbAgg')  # O 'Qt5Agg', 'nbAgg', dependiendo de tu entorno

# Supongamos que el DataFrame se llama df y se carga desde un archivo CSV
# df = pd.read_csv('datos_jugadoras.csv') # Si necesitas cargar el DataFrame desde un archivo CSV

# Crear una figura y un eje
fig, ax = plt.subplots()

# Limitar el área del campo de juego (puedes ajustar estos límites según sea necesario)
ax.set_xlim(-2.8391918333, -2.8378133333)  # Ejemplo: longitud del campo de -100 a 100 (ajusta según tus datos)
ax.set_ylim(43.2762863333, 43.2772301667)    # Ejemplo: latitud del campo de -50 a 50 (ajusta según tus datos)

# Crear un diccionario para guardar los puntos de cada jugadora
jugadoras = df['DEV'].unique()
puntos = {jugadora: ax.plot([], [], 'o', label=jugadora)[0] for jugadora in jugadoras}

# Crear la leyenda
ax.legend()

def init():
    """ Inicializa los puntos de las jugadoras en el gráfico. """
    for punto in puntos.values():
        punto.set_data([], [])
    return puntos.values()

def animate(t):
    """ Actualiza las posiciones de las jugadoras en el tiempo t. """
    tiempo_actual = tiempos[t]
    for jugadora in jugadoras:
        datos = df[(df['DEV'] == jugadora) & (df['local_time'] == tiempo_actual)]
        if not datos.empty:
            x = datos['lon'].values[0]
            y = datos['lat'].values[0]
            puntos[jugadora].set_data(x, y)
    return puntos.values()

# Convertir 'local_time' a datetime para facilitar la ordenación y manejo
#df['local_time'] = pd.to_datetime(df['local_time'])

# Obtener los tiempos únicos en el DataFrame
tiempos = sorted(df['local_time'].unique())
tiempos = tiempos[::5] # Para tomar uno de cada 5 tiempos

# Crear la animación
ani = animation.FuncAnimation(fig, animate, frames=len(tiempos), init_func=init, blit=True, repeat=False)

# Guardar la animación en un archivo de vídeo
# ani.save('jugadoras.mp4', writer='ffmpeg')

# Mostrar la animación en pantalla (opcional)
plt.show()
