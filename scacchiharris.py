import numpy as np
import cv2 as cv
import glob
import os
import matplotlib.pyplot as plt
import math
from sklearn.cluster import DBSCAN #pip install scikit-learn
path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
img = cv.imread(r'a.jpg',0) #lettura immagine

gray = np.float32(img)
dst = cv.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv.dilate(dst,None) # ingrandisce il corner
#dst = dst.astype(np.uint8)

print(dst)

img = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.02*dst.max()]=[0,0,255]

altezza, larghezza = dst.shape[:2]
nero = np.zeros((altezza,larghezza,1))
nero[dst>0.02*dst.max()]=[255]
#bianco = nero.astype(np.uint8)
nero = nero.astype(np.uint8)

grandezza = np.count_nonzero(nero)

print(grandezza)

x= np.ndarray(int(grandezza*2)) #grandezza per due perchè salviamo le coordinate di ogni pixel (x,y)

riga = 0
contatore = 0

while (riga < altezza) :
    colonna = 0
    while (colonna < larghezza) :
        if(nero[riga][colonna] == 255) :
            x[contatore] = colonna
            x[contatore+1] = riga
            contatore = contatore+2
        colonna = colonna+1
    riga = riga+1        

x = x.reshape(grandezza,2)
print(x)

cv.imwrite('exit_float.jpg', img)

cv.imwrite('nero.png', nero)

db = DBSCAN(eps=0.3, min_samples=100).fit(x)

print(db.labels_)

#cv.imwrite('bianco.png', bianco)