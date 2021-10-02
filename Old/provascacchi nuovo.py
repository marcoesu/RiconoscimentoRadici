import numpy as np
import cv2 as cv
import glob
import os
import math
path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
img = cv.imread(r'A_R1 2021-09-03 20-09-04.jpg') #lettura immagine
altezza, larghezza = img.shape[:2]      # salvataggio delle dimensioni dell'immagine (prende solo i primi 2 valori della tupla shape, il terzo contiene i colori)
img_focus = img[(int(altezza/5)):(int(altezza*0.95)),int((larghezza/9)):int((larghezza*0.9))] #parziale ritaglio dell'immagine che facilita il riconoscimento del cartoncino
cv.imwrite('ritaglio.jpg', img_focus)

gray = cv.cvtColor(img_focus, cv.COLOR_BGR2GRAY) #conversione di img_focus da RGB a bianco e nero
cv.imwrite('grigio.jpg', gray)

hsv=cv.cvtColor(img_focus, cv.COLOR_BGR2HSV) #Conversione di img_focus in HSV

#Range per selezionare il colore verde con la maschera
lower_green = np.array([0, 0, 0])          
upper_green = np.array([150,100,100])
cv.imwrite(path+r'/hsv.jpg', hsv)                       
mask = cv.inRange(hsv, lower_green, upper_green) # Applicazione della maschera

#operazione di closing
kernel = np.ones((3,3),np.uint8)
mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel) #closing

cv.imwrite(path+r'/mask.jpg', mask)
mask_inv=cv.bitwise_not(mask)

size = (2,3) #(2,3)

ret, corners = cv.findCirclesGrid(mask_inv, size , cv.CALIB_CB_ASYMMETRIC_GRID + cv.CALIB_CB_CLUSTERING) 
print('corners: ' + str(corners)) 

pinco = corners.ravel()

print("pinco: "+str(pinco))

#corners = np.int0(corners)

x = [] 
y = []

for corner in corners:
    corner_x, corner_y = corner.ravel()
    x.append(corner_x)
    y.append(corner_y)

distanza = math.sqrt((x[1]-x[0])*(x[1]-x[0]) + (y[1]-y[0])*(y[1]-y[0]))
lato_px=int(distanza/math.sqrt(2))
print(lato_px)
#dst = math.sqrt()

cv.drawChessboardCorners(img_focus, size , corners, ret)

cv.imwrite('exit_color.jpg', img_focus)
