import numpy as np
import cv2 as cv
import glob
import os
import math
path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
img = cv.imread(r'a.jpg') #lettura immagine
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

size = (1,29)
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
points = np.zeros((size[0] * size[1], 3), np.float32)
points[:,:2] = np.indices(size).T.reshape(-1, 2)

obj_points = []
img_points = []

ret, corners = cv.findCirclesGrid(mask_inv, size , cv.CALIB_CB_ASYMMETRIC_GRID + cv.CALIB_CB_CLUSTERING) 
print(ret)
print(corners)

img_points.append(corners)
obj_points.append(points)
print(img_points)
print(obj_points)

cv.drawChessboardCorners(img_focus, size , corners, ret)
cv.drawChessboardCorners(mask, size , corners, ret)
cv.drawChessboardCorners(mask_inv, size , corners, ret)

cv.imwrite('exit_color.jpg', img_focus)
cv.imwrite('exit_mask.jpg', mask)
cv.imwrite('exit_mask_inv.jpg', mask_inv)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None) # necessita di 4 punti
h,  w = img_focus.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
# undistort
dst = cv.undistort(img_focus, mtx, dist, None, newcameramtx)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('calibresult.jpg', dst)






'''

try:
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, gray.shape[:2], None, None) # necessita di 4 punti
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    # undistort
    dst = cv.undistort(img_focus, mtx, dist, None, newcameramtx)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imwrite('calibresult.jpg', dst)

except:
    print("Errore")



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
