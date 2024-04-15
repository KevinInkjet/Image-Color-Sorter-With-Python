import cv2
import numpy as np
from skimage import io
import colorsys
import os
import tkinter as tk
from tkinter import filedialog

# Variable global para almacenar la ruta seleccionada
ruta_seleccionada = ""
archivos_en_carpeta = []

# Función para abrir el diálogo de selección de carpeta
def seleccionar_carpeta():
    global ruta_seleccionada
    carpeta_seleccionada = filedialog.askdirectory()
    if carpeta_seleccionada:
        ruta_seleccionada = carpeta_seleccionada
        label_ruta.config(text="Ruta: " + ruta_seleccionada)
        print("Carpeta seleccionada:", ruta_seleccionada)
        global archivos_en_carpeta
        archivos_en_carpeta = os.listdir(ruta_seleccionada)
        #print("Archivos en la carpeta:")
        #for archivo in archivos_en_carpeta:
        #    print(archivo)

def ordenar():
    global archivos_en_carpeta
    global ruta_seleccionada
    print("Ordenando...")
    #for image in archivos_en_carpeta:
    #    print(image)
    print("Ruta seleccionada: ", ruta_seleccionada)
    print(archivos_en_carpeta)
    for image in archivos_en_carpeta:
        image = os.path.join(ruta_seleccionada, image)
        img = io.imread(image)[:, :, :-1]

        pixels = np.float32(img.reshape(-1, 3))

        n_colors = 5
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)

        dominant_index = np.argmax(counts)
        dominant = palette[dominant_index]

        dominant_rgb = tuple(map(int, dominant))
        #print("Dominant Color (RGB):", dominant_rgb)
        #print(list(dominant_rgb))


        #CAMBIAR NOMBRES
        nuevo_nombre = str(colorsys.rgb_to_hsv(list(dominant_rgb)[0], list(dominant_rgb)[1], list(dominant_rgb)[2]))
        #ruta_seleccionada_temp = ruta_seleccionada + "/"
        ruta_antigua = os.path.join(ruta_seleccionada, image)
        ruta_nueva = os.path.join(ruta_seleccionada, nuevo_nombre)
        os.rename(ruta_antigua, ruta_nueva)  # Cambiar el nombre del archivo

    #OBTENER OTRA VEZ LISTA DE ARCHIVOS
    archivos_en_carpeta = os.listdir(ruta_seleccionada)
    print("Nuevos nombres: ")
    for imagen in archivos_en_carpeta:
        print(imagen)
        
    #ORDENAR
    # Función de comparación personalizada para ordenar los colores en función de su valor HSV
    def comparar_colores(color):
        hsv_values = color.strip("()").split(", ")
        h, s, v = map(float, hsv_values)
        return (h, s, v)

    # Ordenar la lista de nombres de colores en función de su valor HSV
    nombres_colores_hsv_ordenados = sorted(archivos_en_carpeta, key=comparar_colores)

    # Imprimir la lista ordenada y renombrar de 0-n
    count = 0
    print("Lista ordenada: ")
    for color in nombres_colores_hsv_ordenados:
        print(color)
        nuevo_nombre = str(count) + ".jpg"
        ruta_antigua = os.path.join(ruta_seleccionada, color)
        ruta_nueva = os.path.join(ruta_seleccionada, nuevo_nombre)
        os.rename(ruta_antigua, ruta_nueva)

        count = count + 1

    print("LISTO!")

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Seleccionar Carpeta")

# Botón para abrir el diálogo de selección de carpeta
boton_seleccionar = tk.Button(root, text="Seleccionar Carpeta", command=seleccionar_carpeta)
boton_seleccionar.pack(padx=20, pady=10)

# Label para mostrar la ruta seleccionada
label_ruta = tk.Label(root, text="Ruta: ")
label_ruta.pack(pady=5)

#Boton para ordenar
boton_ordenar = tk.Button(root, text="Ordenar", command=ordenar)
boton_ordenar.pack(padx=20, pady=10)

# Ejecutar el bucle principal de la aplicación
root.mainloop()
