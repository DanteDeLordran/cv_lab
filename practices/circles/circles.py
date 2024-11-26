import csv
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import math

# Se importa la matriz con los bordes señalados
matrix_borders_pd = pd.read_csv("matriz_bordes_aux.csv")

matrix_borders = np.array(matrix_borders_pd)

height = len(matrix_borders)
width = len(matrix_borders[0])

print("ancho ", width)
print("alto ", height)

def is_cut_pixel(x,y):
    global matrix_borders
    global matrix_votes_circle
    
    cutPixelRecta1 = False
    cutPixelRecta2 = False
    cutPixelRecta3 = False
    cutPixelRecta4 = False

    cutPixelDiagonal1 = False
    cutPixelDiagonal2 = False
    cutPixelDiagonal3 = False
    cutPixelDiagonal4 = False

    matrix_borders_copy = matrix_borders.copy()

    i = x
    j = y+1    
    while j < width - 1:
        pixel = matrix_borders[i][j]
        if pixel == 1:
            cutPixelRecta1 = True
            break
        # matrix_borders[i][j] = 0.75
        j += 1    

    if not cutPixelRecta1 :
        matrix_borders = matrix_borders_copy.copy()
    else:
        iPositionVote = int(round((i+x)/2))
        jPositionVote = int(round((j+y)/2))
        matrix_votes_circle[iPositionVote,jPositionVote] += 1

    matrix_borders_copy = matrix_borders.copy()

    i = x+1
    j = y
    while i < height - 1:
        pixel = matrix_borders[i][j]
        if pixel == 1:
            cutPixelRecta2 = True
            break
        # matrix_borders[i][j] = 0.75
        i += 1    
    if not cutPixelRecta2 :
        matrix_borders = matrix_borders_copy.copy()
    else:
        iPositionVote = int(round((i+x)/2))
        jPositionVote = int(round((j+y)/2))
        matrix_votes_circle[iPositionVote,jPositionVote] += 1

    matrix_borders_copy = matrix_borders.copy()

    i = x+1
    j = y+1
    while j < width - 1  and i < height - 1:
        pixel = matrix_borders[i][j]
        if pixel == 1:
            cutPixelDiagonal1 = True
            break
        # matrix_borders[i][j] = 0.75
        i += 1    
        j += 1
    if not cutPixelDiagonal1 :
        matrix_borders = matrix_borders_copy.copy()
    else:
        iPositionVote = int(round((i+x)/2))
        jPositionVote = int(round((j+y)/2))
        matrix_votes_circle[iPositionVote,jPositionVote] += 1

    matrix_borders_copy = matrix_borders.copy()

    i = x+1
    j = y-1
    while i < height - 1 and j > 0:
        pixel = matrix_borders[i][j]
        if pixel == 1:
            cutPixelDiagonal2 = True
            break
        # matrix_borders[i][j] = 0.25
        i += 1
        j -= 1
    if not cutPixelDiagonal2 :
        matrix_borders = matrix_borders_copy.copy()
    else:
        iPositionVote = int(round((i+x)/2))
        jPositionVote = int(round((j+y)/2))
        matrix_votes_circle[iPositionVote,jPositionVote] += 1

    matrix_borders_copy = matrix_borders.copy()

    i = x
    j = y-1    
    while j > 0:
        pixel = matrix_borders[i][j]
        if pixel == 1:
            cutPixelRecta3 = True
            break
        # matrix_borders[i][j] = 0.5
        j -= 1    
    if not cutPixelRecta3 :
        matrix_borders = matrix_borders_copy.copy()
    else:
        iPositionVote = int(round((i+x)/2))
        jPositionVote = int(round((j+y)/2))
        matrix_votes_circle[iPositionVote,jPositionVote] += 1

    matrix_borders_copy = matrix_borders.copy()

    i = x-1
    j = y
    while i > 0:
        pixel = matrix_borders[i][j]
        if pixel == 1:
            cutPixelRecta4 = True
            break
        # matrix_borders[i][j] = 0.25
        i -= 1    
    if not cutPixelRecta4 :
        matrix_borders = matrix_borders_copy.copy()
    else:
        iPositionVote = int(round((i+x)/2))
        jPositionVote = int(round((j+y)/2))
        matrix_votes_circle[iPositionVote,jPositionVote] += 1

    matrix_borders_copy = matrix_borders.copy()

    i = x-1
    j = y-1
    while i > 0 and j > 0:
        pixel = matrix_borders[i][j]
        if pixel == 1:
            cutPixelDiagonal3 = True
            break
        # matrix_borders[i][j] = 0.25
        i -= 1    
        j -= 1
    if not cutPixelDiagonal3 :
        matrix_borders = matrix_borders_copy.copy()
    else:
        iPositionVote = int(round((i+x)/2))
        jPositionVote = int(round((j+y)/2))
        matrix_votes_circle[iPositionVote,jPositionVote] += 1

    matrix_borders_copy = matrix_borders.copy()

    i = x-1
    j = y+1
    while i > 0 and j < width - 1:
        pixel = matrix_borders[i][j]
        if pixel == 1:
            cutPixelDiagonal4 = True
            break
        matrix_borders[i][j] = 0.25
        i -= 1    
        j += 1
    if not cutPixelDiagonal4 :
        matrix_borders = matrix_borders_copy.copy()
    else:
        iPositionVote = int(round((i+x)/2))
        jPositionVote = int(round((j+y)/2))
        matrix_votes_circle[iPositionVote,jPositionVote] += 1

    return [cutPixelDiagonal1, cutPixelDiagonal2, cutPixelDiagonal3, cutPixelDiagonal4, cutPixelRecta1, cutPixelRecta2, cutPixelRecta3, cutPixelRecta4]

def search_radio_circle(x, y, umbral):

    radio = 0

    radios = [0,0,0,0,0,0,0,0]

    global matrix_borders
    global matrix_circles
    
    i = x
    j = y+1    
    while j < width - 1:
        pixel = matrix_circles[i][j]
        if pixel == 1:
            radio = int(round(((i-x)**2+(j-y)**2)**0.5))
            break
        j += 1    

    if radio != 0:
        radios[0] = radio

    radio = 0

    i = x+1
    j = y
    while i < height - 1:
        pixel = matrix_circles[i][j]
        if pixel == 1:
            radio = int(round(((i-x)**2+(j-y)**2)**0.5))
            break
        i += 1    
  
    if radio != 0:
        radios[1] = radio

    radio = 0

    i = x+1
    j = y+1
    while j < width - 1  and i < height - 1:
        pixel = matrix_circles[i][j]
        if pixel == 1:
            radio = int(round(((i-x)**2+(j-y)**2)**0.5))
            break
        i += 1    
        j += 1
   
   
    if radio != 0:
        radios[2] = radio

    radio = 0

    i = x+1
    j = y-1
    while i < height - 1 and j > 0:
        pixel = matrix_circles[i][j]
        if pixel == 1:
            radio = int(round(((i-x)**2+(j-y)**2)**0.5))
            break
        i += 1
        j -= 1
    
    
    if radio != 0:
        radios[3] = radio

    radio = 0

    j = y-1    
    while j > 0:
        pixel = matrix_circles[i][j]
        if pixel == 1:
            radio = int(round(((i-x)**2+(j-y)**2)**0.5))
            break
        j -= 1    
    
    if radio != 0:
        radios[4] = radio

    radio = 0

    i = x-1
    j = y
    while i > 0:
        pixel = matrix_circles[i][j]
        if pixel == 1:
            radio = int(round(((i-x)**2+(j-y)**2)**0.5))
            break
        i -= 1    
    
   
    if radio != 0:
        radios[5] = radio

    radio = 0

    i = x-1
    j = y-1
    while i > 0 and j > 0:
        pixel = matrix_circles[i][j]
        if pixel == 1:
            radio = int(round(((i-x)**2+(j-y)**2)**0.5))
            break
        i -= 1    
        j -= 1
    
   
    if radio != 0:
        radios[6] = radio

    radio = 0

    i = x-1
    j = y+1
    while i > 0 and j < width - 1:
        pixel = matrix_circles[i][j]
        if pixel == 1:
            radio = int(round(((i-x)**2+(j-y)**2)**0.5))
            break
        i -= 1    
        j += 1
   
   
    if radio != 0:
        radios[7] = radio

    radio = 0

    return radios

def is_within_bounds(x, y, width, height):
    return 0 <= x < height and 0 <= y < width

matrix_lines = np.zeros((height, width))
matrix_votes_circle = np.zeros((height, width))
matrix_marked_circles = np.zeros((height, width))
matrix_walked_lines = np.zeros((height, width))
matrix_centers = np.zeros((height, width))

for x in matrix_walked_lines:
    for y in x:
        y = False

matrix_borders_aux = matrix_borders.copy()

for i, row in enumerate(matrix_borders):
    print(i)
    for j, pixel in enumerate(row):
        if pixel == 1:
            is_cut_pixel(i,j)

nVal = 0
suma = 0

for i in matrix_votes_circle:
    for j in i:
        if j > 0:
            nVal += 1
            suma += j

umbral = suma/nVal
umbral = umbral + umbral*0.35

print('umbral: ', umbral)

matrix_borders_umbral_applied = matrix_votes_circle.copy()

for i, row in enumerate(matrix_borders_umbral_applied):
    for j, pixel in enumerate(row):
        if pixel < umbral:
            matrix_borders_umbral_applied[i][j] = 0
        else:
            matrix_borders_umbral_applied[i][j] = 1

matrix_circles = matrix_borders_umbral_applied.copy()

try:
     for i, row in enumerate(matrix_circles):
        for j, pixel in enumerate(row):
                if (
                    pixel == 1 and  # Pixel central
                    # Chequeo de píxeles a distancia 1
                    (i+1 >= height or matrix_circles[i+1][j] == 0) and  # Abajo
                    (i+1 >= height or j+1 >= width or matrix_circles[i+1][j+1] == 0) and  # Abajo-derecha
                    (i-1 < 0 or matrix_circles[i-1][j] == 0) and  # Arriba
                    (i-1 < 0 or j+1 >= width or matrix_circles[i-1][j+1] == 0) and  # Arriba-derecha
                    (i-1 < 0 or j-1 < 0 or matrix_circles[i-1][j-1] == 0) and  # Arriba-izquierda
                    (j+1 >= width or matrix_circles[i][j+1] == 0) and  # Derecha
                    (j-1 < 0 or matrix_circles[i][j-1] == 0) and  # Izquierda
                    (i+1 >= height or j-1 < 0 or matrix_circles[i+1][j-1] == 0)  # Abajo-izquierda

                    # Chequeo de píxeles a distancia 2
                    # (i+2 >= height or matrix_circles[i+2][j] == 0) and  # Dos posiciones abajo
                    # (i+2 >= height or j+2 >= width or matrix_circles[i+2][j+2] == 0) and  # Abajo-derecha
                    # (i-2 < 0 or matrix_circles[i-2][j] == 0) and  # Dos posiciones arriba
                    # (i-2 < 0 or j+2 >= width or matrix_circles[i-2][j+2] == 0) and  # Arriba-derecha
                    # (i-2 < 0 or j-2 < 0 or matrix_circles[i-2][j-2] == 0) and  # Arriba-izquierda
                    # (j+2 >= width or matrix_circles[i][j+2] == 0) and  # Dos posiciones a la derecha
                    # (j-2 < 0 or matrix_circles[i][j-2] == 0) and  # Dos posiciones a la izquierda
                    # (i+2 >= height or j-2 < 0 or matrix_circles[i+2][j-2] == 0)  # Abajo-izquierda
                ):
                    matrix_centers[i][j] = 1
except:
    print("Error al crear matriz de centros")

print("Dibujar circulos")

try:
    for i, row in enumerate(matrix_centers):
        for j, pixel in enumerate(row):
            if pixel == 1: 
                radios = search_radio_circle(i,j, umbral)
                radio = radios[0]
                
                isValidCenter = True

                nValidRadios = 0

                for r in radios:
                    if r >= radio-radio*.2 and r <= radio+radio*.2:
                        nValidRadios = nValidRadios + 1

                isValidCenter = nValidRadios >= 5
                
                if radio > 0 and isValidCenter:
                    print(radios)
                    for angulo in range(360):
                        radianes = math.radians(angulo)
                        x = int(round(i + radio * math.cos(radianes)))
                        y = int(round(j + radio * math.sin(radianes))) 
                        for i in range(round(x-x*.2), round(x+x*.2)):
                            for j in range(round(y-y*.2), round(y+y*.2)):
                                if i < height and j < width and i >= 0 and j >= 0:
                                    if matrix_borders_aux[i][j] == 1 :
                                        matrix_marked_circles[x][y] = 1

except: 
    print("ocurrio un error")

decimal_matrix = np.zeros((height, width))

with open("matriz_votes_circle.csv", mode="w", newline="") as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerows(matrix_votes_circle)

with open("matriz_circulos_marcados.csv", mode="w", newline="") as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerows(matrix_marked_circles)

with open("matriz_borders.csv", mode="w", newline="") as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerows(matrix_borders_aux)

with open("matriz_centros.csv", mode="w", newline="") as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerows(matrix_circles)

cv2.imshow('Imagen Votos', matrix_votes_circle)
cv2.imshow('Imagen Bordes 1', matrix_borders_umbral_applied)
cv2.imshow('Imagen Bordes 2', matrix_borders_aux)
cv2.imshow('Imagen Circulos con umbral', matrix_circles)
cv2.imshow('Imagen Circulos', matrix_marked_circles)
cv2.imshow('Imagen Centros', matrix_centers)
cv2.waitKey(0)
cv2.destroyAllWindows()