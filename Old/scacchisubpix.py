import numpy as np
import cv2 as cv
import glob
import os
import math
path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
img = cv.imread(r'a.jpg',0) #lettura immagine

# find Harris corners
gray = np.float32(img)
#dst = cv.cornerHarris(gray,2,3,0.04)
dst = cv.cornerHarris(gray,6,3,0.04)
dst = cv.dilate(dst,None)
ret, dst = cv.threshold(dst,0.01*dst.max(),255,0)
dst = np.uint8(dst)

# find centroids
ret, labels, stats, centroids = cv.connectedComponentsWithStats(dst)
print(centroids)

# define the criteria to stop and refine the corners
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)
print(corners)

# Now draw them
res = np.hstack((centroids,corners)) #lavora su due colonne: la prima contiene i centri e l'altra gli spigoli
res = np.int0(res)
print('-----------------------')
print(res)
img = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
img[res[:,1],res[:,0]]=[0,0,255]#centri (0 colonna, 1 riga)
img[res[:,3],res[:,2]] = [0,255,0]#angoli (2 colonna, 3 riga)

cv.imwrite('subpixel.jpg',img)