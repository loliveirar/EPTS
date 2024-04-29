# finding hot zones in a given image
import cv2
import numpy as np

def encontrar_centros_zonas_rojas(imagen, n):
    # Load sample image
    img = cv2.imread(imagen)

    # Convertin BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Mask to detect red points
    lower_red = np.array([255, 0, 0], dtype=np.uint8)
    upper_red = np.array([255, 75, 75], dtype=np.uint8)
    mascara_roja = cv2.inRange(img_rgb, lower_red, upper_red)

    # Finding contours
    contornos, _ = cv2.findContours(mascara_roja, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Ordering founded zones (bigger to smaller)
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)[:n]

    # Calculating centroids of detected zones
    centros = []
    for contorno in contornos:
        momento = cv2.moments(contorno)
        cx = int(momento['m10'] / momento['m00'])
        cy = int(momento['m01'] / momento['m00'])
        centros.append((cx, cy))

    return centros


# Example
imagen_path = 'image.png'
num_zonas_rojas = 4  # Number of hot zones to detect
centros = encontrar_centros_zonas_rojas(imagen_path, num_zonas_rojas)

# Showing centers of detected zones
for idx, centro in enumerate(centros, start=1):
    print(f'Zona Roja {idx}: x {centro[0]}, y {centro[1]}')