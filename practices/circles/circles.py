import csv
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import math

# Se importa la matriz con los bordes señalados
# Matriz binaria de bordes
matrix_borders_pd = pd.read_csv("matriz_borders.csv")

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
        matrix_borders[i][j] = 0.75
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
        matrix_borders[i][j] = 0.75
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
        matrix_borders[i][j] = 0.75
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
        matrix_borders[i][j] = 0.25
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
        matrix_borders[i][j] = 0.5
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
        matrix_borders[i][j] = 0.25
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
        matrix_borders[i][j] = 0.25
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

# votos_flat = matrix_votes_circle.flatten()

# umbral = np.percentile(votos_flat, 95)  # Cambia 95 al percentil deseado

# max_votes = np.max(votes_flat)
# mean_votes = np.mean(votes_flat)
# std_votes = np.std(votes_flat)

# umbral = mean_votes + std_votes

nVal = 0
suma = 0

for i in matrix_votes_circle:
    for j in i:
        if j > 0:
            nVal += 1
            suma += j

umbral = suma/nVal
umbral = umbral + umbral*0.25

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
            if pixel == 1 and (i+1>=height or matrix_circles[i+1][j] == 0) and (i+1>=height or j+1>=width or matrix_circles[i+1][j+1] == 0) and (i-1 <= -1 or matrix_circles[i-1][j] == 0)  and (i-1 <= -1 or j+1 >= width or matrix_circles[i-1][j+1] == 0) and (i-1 <= -1 or j-1 <= -1 or matrix_circles[i-1][j-1] == 0) and (j+1 >= height or matrix_circles[i][j+1] == 0) and (j-1 <= -1 or matrix_circles[i][j-1]) == 0 and (i+1>= height or j-1 <= width or matrix_circles[i+1][j-1] == 0) and (i+2 >= height or matrix_circles[i+2][j] == 0) and (i+2 >= height or j+2 >= height or matrix_circles[i+2][j+2] == 0) and (i-2 <= -1 or matrix_circles[i-2][j] == 0) and (i-2 <= -1 or j+2 >= width or matrix_circles[i-2][j+2] == 0) and (i-2 <= -1 or j-2 <= -1 or matrix_circles[i-2][j-2] == 0) and (j+2 >= width or matrix_circles[i][j+2] == 0) and (j-2 <= -1 or matrix_circles[i][j-2] == 0) and (i+2 >= height or j-2 <= -1 or matrix_circles[i+2][j-2] == 0): 
                # radios = search_radio_circle(i,j, umbral)

                # isValidRadio = True
                # previousRadio = radios[0]

                # for item in radios:
                #     isValidRadio = isValidRadio and (item <= previousRadio + previousRadio*.10 and item >= previousRadio - previousRadio*.10)

                # if not isValidRadio:
                #     break
                
                # radio = radios[0]

                # radios = search_radio_circle(i,y, umbral)

                # radiosRep = []
                # savedRadios = []

                # print('hola')

                # for item in radios:
                #     if not item in savedRadios:
                #         savedRadios.append(item)
                #         radiosRep.append([item, 1])
                #     else:
                #         index = None
                #         for i,r in enumerate(radiosRep):
                #             if r[0] == item:
                #                 index = i
                #                 break
                #         radiosRep[index][1] += 1
                
                # maxRadiosRepIndex = 0

                # for i, r in enumerate(radiosRep):
                #     if r > radiosRep[maxRadiosRepIndex][1]:
                #         maxRadiosRepIndex = i
                
                # print(radios)

                # radio = radiosRep[maxRadiosRepIndex][0]

                # isValidRadios = [True]*8
                # validRadios = []

                # for i,item in enumerate(radiosRep):
                #     isValidRadios[i] = item[0] <= radio+radio*0.1 and item[0] >= radio-radio*0.1
                #     if isValidRadios[i]:
                #         validRadios.append(item[0])

                # if len(validRadios) > 2:
                matrix_centers[i][j] = 1

                # if radio is not None and radio > 0:
                #     validations = [False,False,False,False,False,False,False,False]
                    
                #     # for dx in [-1, 0, 1]:
                #     #     for dy in [-1, 0, 1]:

                #     #         if is_within_bounds(i, j + radio - 1 + dy, width, height):
                #     #             validations[0] = validations[0] or matrix_circles[i + dx][j + radio - 1 + dy] == 1
                            
                #     #         if is_within_bounds(i + radio - 1 + dx, j + radio - 1 + dy, width, height):
                #     #             validations[1] = validations[1] or matrix_circles[i + radio - 1 + dx][j + radio - 1 + dy] == 1
                            
                #     #         if is_within_bounds(i - radio + 1 + dx, j - radio + 1 + dy, width, height):
                #     #             validations[2] = validations[2] or matrix_circles[i - radio + 1 + dx][j - radio + 1 + dy] == 1
                            
                #     #         if is_within_bounds(i + dx, j - radio + 1 + dy, width, height):
                #     #             validations[3] = validations[3] or matrix_circles[i + dx][j - radio + 1 + dy] == 1
                            
                #     #         if is_within_bounds(i - radio + 1 + dx, j + dy, width, height):
                #     #             validations[4] = validations[4] or matrix_circles[i - radio + 1 + dx][j + dy] == 1
                            
                #     #         if is_within_bounds(i + radio - 1 + dx, j + dy, width, height):
                #     #             validations[5] = validations[5] or matrix_circles[i + radio - 1 + dx][j + dy] == 1
                            
                #     #         if is_within_bounds(i - radio + 1 + dx, j + dy, width, height):
                #     #             validations[6] = validations[6] or matrix_circles[i - radio + 1 + dx][j + dy] == 1
                            
                #     #         if is_within_bounds(i + radio - 1 + dx, j + radio - 1 + dy, width, height):
                #     #             validations[7] = validations[7] or matrix_circles[i + radio - 1 + dx][j + radio - 1 + dy] == 1
                    
                #     # if sum(validations) == 8:
                #     #     print(validations)
                #     matrix_centers[i][j] = 1
except:
    print("Error al crear matriz de centros")

print("Dibujar circulos")

try:
    for i, row in enumerate(matrix_centers):
        for j, pixel in enumerate(row):
            if pixel == 1: 
                # print(i,',',j)
                radios = search_radio_circle(i,j, umbral)
                radio = radios[0]
                
                isValidCenter = True

                for r in radios:
                    isValidCenter = isValidCenter and r >= radio-radio*.10 and r <= radio+radio*.10

                
                if radio > 0 and isValidCenter:
                    print(radios)
                    for angulo in range(360):
                        radianes = math.radians(angulo)
                        x = int(round(i + radio * math.cos(radianes)))
                        y = int(round(j + radio * math.sin(radianes))) 
                        if x < height and y < width and x >= 0 and y >= 0:
                            if matrix_borders_aux[x][y] == 1:#or matrix_borders_aux[x+1][y] == 1 or matrix_borders_aux[x+1][y+1] == 1  or matrix_borders_aux[x-1][y] == 1  or matrix_borders_aux[x-1][y+1] == 1  or matrix_borders_aux[x-1][y-1] == 1  or matrix_borders_aux[x][y+1] == 1  or matrix_borders_aux[x][y-1] == 1 or matrix_borders_aux[x+1][y-1] == 1:
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