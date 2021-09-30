import numpy as np
import cv2 as cv
import glob
import os
import math
from matplotlib import pyplot as plt

path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
img = cv.imread(r'a.jpg', 0) #lettura immagine

corners = cv.goodFeaturesToTrack(img,25,0.01,10)
corners = np.int0(corners)
print(corners)

for i in corners:
    x,y = i.ravel()
    cv.circle(img,(x,y),3,255,-1)

cv.imwrite('shitomasi.jpg',img)