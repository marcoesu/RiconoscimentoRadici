import numpy as np
import cv2 as cv
import glob
import os
import math
path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
img = cv.imread(r'a.jpg',0) #lettura immagine

gray = np.float32(img)
dst = cv.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv.dilate(dst,None)

print(dst)

img = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.02*dst.max()]=[0,0,255]

cv.imwrite('exit.jpg', img)
