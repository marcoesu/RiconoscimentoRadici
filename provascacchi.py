import numpy as np
import cv2 as cv
import glob
import os
import math
path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
img = cv.imread(r'a.jpg')
altezza, larghezza = img.shape[:2]      # salvataggio delle dimensioni dell'immagine (prende solo i primi 2 valori della tupla shape, il terzo contiene i colori)
img_focus = img[(int(altezza/5)):(int(altezza*0.95)),int((larghezza/9)):int((larghezza*0.9))] #parziale ritaglio dell'immagine che facilita il riconoscimento del cartoncino
cv.imwrite('ritaglio.jpg', img_focus)

gray = cv.cvtColor(img_focus, cv.COLOR_BGR2GRAY)
print('pippo')
cv.imwrite('grigio.jpg', gray)

hsv=cv.cvtColor(img_focus, cv.COLOR_BGR2HSV)

lower_green = np.array([0, 0, 0])          
upper_green = np.array([150,100,100])
cv.imwrite(path+r'/hsv.jpg', hsv)                       
mask = cv.inRange(hsv, lower_green, upper_green)
cv.imwrite(path+r'/mask.jpg', mask)
contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE) #Ricerca dei contorni utlizzando le informazioni ottenute attraverso il tresholding
c = max(contours, key=cv.contourArea)   #Ricerca del più grande contorno nell'immagine utilizzando come parametro di giudizio l'area del contorno
x, y, w, h = cv.boundingRect(c)
mask=cv.bitwise_not(mask)
scacchiera=mask[y:y+h,x:x+w]

ret, corners = cv.findCirclesGrid(mask, (2,3), cv.CALIB_CB_ASYMMETRIC_GRID + cv.CALIB_CB_CLUSTERING) 
print(corners)

#corners2 = cv.cornerSubPix(gray,corners, (1,2), (-1,-1), (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 60, 0.001))
cv.drawChessboardCorners(img_focus, (1,3), corners, ret)
print("ciao")
cv.imwrite('exit.jpg', img_focus)

'''
CHECKERBOARD = (4,3)
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

gray = cv.cvtColor(img_focus, cv.COLOR_BGR2GRAY)
print('pippo')
cv.imwrite('grigio.jpg', gray)
ret, corners = cv.findChessboardCorners(gray, CHECKERBOARD, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)
print('pluto')

print(ret)
    # If found, add object points, image points (after refining them)
if ret == True:
    objpoints.append(objp)
    corners2 = cv.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
    imgpoints.append(corners2)
    img = cv.drawChessboardCorners(img_focus, CHECKERBOARD, corners2, ret)
    cv.imshow('img', img_focus)
    cv.waitKey(0)
cv.destroyAllWindows()'''
