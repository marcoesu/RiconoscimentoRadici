import numpy as np
import cv2 as cv
import glob
import os
import matplotlib.pyplot as plt
import math
from numpy.core.fromnumeric import ravel
from numpy.core.numeric import count_nonzero
from numpy.lib.function_base import average
from sklearn.cluster import DBSCAN #pip install scikit-learn
file = open("prova.txt","w")

path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
img = cv.imread(r'prova_dbscan.jpg',0) #lettura immagine

#gray = np.float32(img) 
harris = cv.cornerHarris(img,2,3,0.04) #applicazione dell'algoritmo di harris

#result is dilated for marking the corners, not important
#harris = cv.dilate(harris,None) # ingrandisce il corner
#dst = dst.astype(np.uint8)

img = cv.cvtColor(img, cv.COLOR_GRAY2BGR) # conversione da bianco e nero a RGB

# Threshold for an optimal value, it may vary depending on the image.
img[harris>0.02*harris.max()]=[0,0,255] #disegna i cerchi rossi sullo scheletro

altezza, larghezza = harris.shape[:2] #dimensioni dell'immagine ottenuta con harris
nero = np.zeros((altezza,larghezza,1)) #crea un'immagine completamente nera
nero[harris>0.02*harris.max()]=[255] #disegna i punti di interesse trovati con harris su un'immagine nera

nero = nero.astype(np.uint8) #i punti riportati da harris sono in subpixel,
                            # andiamo quindi a convertire l'immagine in un array di interi
                            # approssimando la posizione dei punti ottenuti con l'algoritmo di harris
                            # in pixel

cv.imwrite('nero.png', nero)

raggio=3        # definizione del raggio dell'area di lavoro
#definizione zona
#grandezza=np.count
#x= np.ndarray(int(np))
bianco = np.zeros(nero.shape)
riga = raggio

while (riga < altezza-raggio) : 
    colonna = raggio
    while (colonna < larghezza-raggio) :
        if(nero[riga][colonna] == 255):
            area = nero[int(riga - raggio):int(riga+raggio),int(colonna-raggio):int(colonna+raggio)]
            n_pixel = np.count_nonzero(area)
            if (n_pixel>1):
                media_punti_x=np.ndarray(n_pixel)
                media_punti_y=np.ndarray(n_pixel)
                riga_area = 0
                while (riga_area<area.shape[0]):
                    colonna_area = 0
                    pixel = 0
                    while (colonna_area<area.shape[1] and pixel<n_pixel):
                        if(area[riga_area,colonna_area]==[255]):
                            media_punti_y[pixel]=riga_area
                            media_punti_x[pixel]=colonna_area
                            pixel+=1
                        colonna_area+=1
                    riga_area+=1
                media_x=(sum(media_punti_x)/n_pixel).astype(np.uint8)
                media_y=(sum(media_punti_y)/n_pixel).astype(np.uint8)
                area[0:raggio*2+1,0:raggio*2+1]=[0]
                
                area[(media_y),int(media_x)]=[255]
                nero[riga - raggio:riga+raggio,colonna-raggio:colonna+raggio]=area
                bianco[riga - raggio:riga+raggio,colonna-raggio:colonna+raggio]=area
            
        colonna = colonna+1
    riga = riga+1 

cv.imwrite("nuovi_punti.png",nero)
cv.imwrite("bianco.png",bianco)



