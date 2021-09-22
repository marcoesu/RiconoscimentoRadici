import numpy as np
import cv2 as cv
import glob
import os
path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
img = cv.imread(r'a.jpg')
hsv=cv.cvtColor(img, cv.COLOR_BGR2HSV)
#aaa, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)
#CALIB_CB_FAST_CHECK saves a lot of time on images
#that do not contain any chessboard corners
lower_green = np.array([0, 0, 0])          
upper_green = np.array([150,100,100])
cv.imwrite(r'C:\Users\esu7z\Desktop\GitHub\IdentificazioneQR\ciao.jpg', hsv)                       
mask = cv.inRange(hsv, lower_green, upper_green)
contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE) #Ricerca dei contorni utlizzando le informazioni ottenute attraverso il tresholding
c = max(contours, key=cv.contourArea)   #Ricerca del più grande contorno nell'immagine utilizzando come parametro di giudizio l'area del contorno
x, y, w, h = cv.boundingRect(c)
mask=cv.bitwise_not(mask)
scacchiera=mask[y:y+h,x:x+w]
#scacchiera=img[y:y+h,x:x+w,:]
# mask=cv.bitwise_not(mask)

gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
pino = cv.bitwise_or(gray, mask)
#pino= cv.morphologyEx(pino, cv.MORPH_OPEN, (1,1))
#pino= cv.morphologyEx(pino, cv.MORPH_OPEN, (1,1))
#pino = cv.dilate(pino,(1,1),iterations = 5)
#pino = cv.bilateralFilter(pino,9,75,75)
#params = cv.SimpleBlobDetector_Params()
#params.maxArea = 100000
#detector = cv.SimpleBlobDetector_create(params)
ret, corners = cv.findCirclesGrid(scacchiera, (1,30), cv.CALIB_CB_ASYMMETRIC_GRID + cv.CALIB_CB_CLUSTERING) #,  blobDetector=detector)
print(corners)
cv.imwrite(r'C:\Users\esu7z\Desktop\GitHub\IdentificazioneQR\ciaoo.jpg', scacchiera)
#cv.waitKey(2000)
if(ret==True):
    corners2 = cv.cornerSubPix(pino,corners, (1,1), (-1,-1), (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 60, 0.001))
    cv.drawChessboardCorners(img, (2,1), corners2, ret)
    print("ciao")
    cv.imwrite(str(r'C:\Users\esu7z\Desktop\GitHub\IdentificazioneQR\b.jpg'+'exit.jpg'), img)