import cv2
import numpy as np

def encontrar_centros_zonas_rojas(imagen, n):
    # Cargar la imagen
    img = cv2.imread(imagen)

    # Convertir la imagen de BGR a RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Definir máscaras para los colores rojos
    lower_red = np.array([255, 0, 0], dtype=np.uint8)
    upper_red = np.array([255, 75, 75], dtype=np.uint8)
    mascara_roja = cv2.inRange(img_rgb, lower_red, upper_red)

    # Encontrar contornos en la máscara
    contornos, _ = cv2.findContours(mascara_roja, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Ordenar los contornos por área (mayor a menor)
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)[:n]

    # Calcular los centros de masa de los contornos
    centros = []
    for contorno in contornos:
        momento = cv2.moments(contorno)
        cx = int(momento['m10'] / momento['m00'])
        cy = int(momento['m01'] / momento['m00'])
        centros.append((cx, cy))

    return centros


# Ejemplo de uso
imagen_path = 'heatmap5solocampo.png'
num_zonas_rojas = 4  # Cambia esto al número deseado de zonas rojas a detectar
centros = encontrar_centros_zonas_rojas(imagen_path, num_zonas_rojas)

# Imprimir los centros de las zonas rojas
for idx, centro in enumerate(centros, start=1):
    print(f'Zona Roja {idx}: x {centro[0]}, y {centro[1]}')