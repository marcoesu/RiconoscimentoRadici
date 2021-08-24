import numpy as np
import cv2 as cv
import glob
 #interior number of corners
img = cv.imread(r'C:\Users\esu7z\Desktop\GitHub\IdentificazioneQR\a.jpg')
hsv=cv.cvtColor(img, cv.COLOR_BGR2HSV)
#aaa, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)
#CALIB_CB_FAST_CHECK saves a lot of time on images
#that do not contain any chessboard corners
lower_green = np.array([0, 0, 0])          
upper_green = np.array([150,100,100])
cv.imwrite(r'C:\Users\esu7z\Desktop\GitHub\IdentificazioneQR\ciao.jpg', hsv)                       
mask = cv.inRange(hsv, lower_green, upper_green)
mask=cv.bitwise_not(mask)
gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
pino = cv.bitwise_and(gray, gray, mask= mask)
ret, corners = cv.findCirclesGrid(pino, (2,1), None)
cv.imwrite(r'C:\Users\esu7z\Desktop\GitHub\IdentificazioneQR\ciaoo.jpg', pino)
#cv.waitKey(2000)
if(ret==True):
    corners2 = cv.cornerSubPix(pino,corners, (1,1), (-1,-1), (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001))
    cv.drawChessboardCorners(img, (2,1), corners, ret)
    print("ciao")
    cv.imwrite(str(r'C:\Users\esu7z\Desktop\GitHub\IdentificazioneQR\b.jpg'+'exit.jpg'), img)