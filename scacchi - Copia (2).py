import numpy as np
import cv2 as cv
import glob
import os
path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
#img = cv.imread(path+r'/'+'a.jpg')
'''
hsv=cv.cvtColor(img, cv.COLOR_BGR2HSV)
#aaa, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)
#CALIB_CB_FAST_CHECK saves a lot of time on images
#that do not contain any chessboard corners
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
ret, corners = cv.findCirclesGrid(img, (1,60), cv.CALIB_CB_ASYMMETRIC_GRID + cv.CALIB_CB_CLUSTERING) #,  blobDetector=detector)
print(corners)
cv.drawChessboardCorners(img, (2,3), corners, ret)
cv.imwrite(path+r'/scacchiera.jpg', img)
#cv.waitKey(2000)
if(ret==True):
    corners2 = cv.cornerSubPix(pino,corners, (1,1), (-1,-1), (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 60, 0.001))
    cv.drawChessboardCorners(img, (2,1), corners2, ret)
    print("ciao")
    cv.imwrite(str(path+r'/exit.jpg'), img)
    '''
# Arrays to store object points and image points from all the images.
img = cv.imread(str(path+r'/a.jpg'))
print('ciao')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imwrite(str(path+r'/gray.jpg'),gray)
print('ciao')
# Find the chess board corners
#ret, corners = cv.findChessboardCorners(gray, (7,6), None)
ret, corners = cv.findCirclesGrid(gray, (2,2), None)
#corners.reshape((2,2))
rawpoints = corners.ravel()
print(len(rawpoints))
#Generazione array delle coordinate iniziali (pre-trasformazione)
points=np.zeros(6) #[x_0, y_0, x_1, y_1, x_2, y_2, x_3, y_3]
#Passaggio coordinate da corners a points
i=0
while (i<len(rawpoints)):
    points[i]=rawpoints[i]
    i=i+1
print('---------')
print(points)
print('---------')
cv.drawChessboardCorners(img, (2,2), corners, ret)
cv.imwrite(str(path+r'/ciaooo.jpg'),img)

cv.circle(img, (int(points[0]),int(points[1])), 2, (255,255,0), -1)
cv.circle(img, (int(points[2]),int(points[3])), 2, (255,255,0), -1)
#Generazione punti per effetturare la trasformazione
points[4]=points[0]
points[5]=points[3]
cv.circle(img, (int(points[4]),int(points[5])), 2, (255,255,0), -1)
# Generazione punti del secondo vettore per effetturare la trasformazione
points_t=np.zeros(6)
points_t[0]=points[0]
points_t[1]=points[1]
points_t[2]=points[2] #x_1t = x_1
points_t[3]=points_t[1]-points_t[2]+points_t[0] #y_1t = y_0t-(x_1t-x_0t)
points_t[4]=points_t[0]
points_t[5]=points_t[3]
cv.circle(img, (int(points_t[0]),int(points_t[1])), 2, (0,255,255), -1)
cv.circle(img, (int(points_t[2]),int(points_t[3])), 2, (0,255,255), -1)
cv.circle(img, (int(points_t[4]),int(points_t[5])), 2, (0,255,255), -1)

cv.imwrite(str(path+r'/ciaooo.jpg'),img)

rows,cols,ch = img.shape
pts1=np.float32([[points[0],points[1]],[points[2],points[3]],[points[4],points[5]]])
pts2=np.float32([[points_t[0],points_t[1]],[points_t[2],points_t[3]],[points_t[4],points_t[5]]])
M = cv.getAffineTransform(pts1,pts2)
dst = cv.warpAffine(img,M,(cols,rows))
cv.imwrite(str(path+r'/exit.jpg'),dst)

'''

if(points[3]<points[1]): # Se il secondo punto (x_1,y_1) si trova più in alto rispetto al primo punto (x_0,y_0)
    #P(x_2,y_2)
    points[4]=points[2] # x_2=x_1
    points[5]=(2*points[1]-points[3]) # y_2=y_0+(y_0-y_1)=2*y_0-y_1
    #P(x_3,y_3)
    points[6]=2*points[2]-points[0] #x_3=x_1+(x_1-x_0)=2*x_1-x_0
    points[1]=points[7] #y_3=y_0
    print("prova")
    print(points)
    # Generazione punti del secondo vettore per effetturare la trasformazione
    points_t=np.zeros(8)
    points_t[0]=points[0]
    points_t[1]=points[1]
    points_t[2]=points[2] #x_1t = x_1
    points_t[3]=points_t[1]-points_t[2]+points_t[0] #y_1t = y_0t-(x_1t-x_0t)   ?
     #P(x_2t,y_2t)
    points_t[4]=points_t[2] # x_2t=x_1t
    points_t[5]=(2*points_t[1]-points_t[3]) # y_2=y_0+(y_0-y_1)=2*y_0-y_1
    #P(x_3,y_3)
    points_t[6]=2*points_t[2]-points_t[0] #x_3=x_1+(x_1-x_0)=2*x_1-x_0
    points_t[1]=points_t[7] #y_3=y_0
    print(points_t)

    pts1=np.float32([[points[0],points[1]],[points[2],points[3]],[points[4],points[5]],[points[6],points[7]]])
    pts2=np.float32([[points_t[0],points_t[1]],[points_t[2],points_t[3]],[points_t[4],points_t[5]],[points_t[6],points_t[7]]])  
    M = cv.getPerspectiveTransform(pts1,pts2)
    dst = cv.warpPerspective(img,M,(int(points[0]),int(points[1])))
    cv.imwrite(str(path+r'/ciaooo.jpg'),img)


#P(x_3,y_3)
print(points)
points_t=np.zeros(8)

points_t[:2]=points[:2]
print(points_t)
points_t[2]=points[2]
points_t[3]=points[2]-points[0]+points[1]
points_t[4]=(points_t[0]+points_t[2])/2
points_t[5]=(points_t[1]+points_t[3])/2
cv.drawChessboardCorners(img, (2,2), corners, ret)
pts1=np.float32([[points[0],points[1]],[points[2],points[3]],[points[4],points[5]],[points[6],points[7]]])
pts2=np.float32([[points_t[0],points_t[1]],[points_t[2],points_t[3]],[points_t[4],points_t[5]]])  
#M = cv.getPerspectiveTransform(pts1,pts2)
#dst = cv.warpPerspective(img,M,(300,300))
cv.imwrite(str(path+r'/ciaooo.jpg'),img)
#    elif (points[0]<points[2]):
if (points[0]<points[2]):  # se il primo punto si trova dopo al secondo punto rispetto all'asse x
    points_t[0]=points[0]
    points_t[1]=points[1]
    points_t[2]=points[2]
    points_t[3]=points[2]-points[0]+points[1]
    points_t[4]=(points_t[0]+points_t[2])/2
    points_t[5]=(points_t[1]+points_t[3])/2
    cv.drawChessboardCorners(img, (2,2), corners, ret)
    pts1=np.float32([[points[0],points[1]],[points[2],points[3]],[points[4],points[5]]])
    pts2=np.float32([[points_t[0],points_t[1]],[points_t[2],points_t[3]],[points_t[4],points_t[5]]])  
    #M = cv.getPerspectiveTransform(pts1,pts2)
    #dst = cv.warpPerspective(img,M,(300,300))
    cv.imwrite(str(path+r'/ciaooo.jpg'),img)
#    elif (points[0]<points[2]):
       

#pts1 = np.float32(points[0],points[1])
#pts2 = np.float32()

pts1 = np.float32(points[0],points[1])
pts2 = np.float32()

print(ret)
#cv.imwrite(str(path+r'/ciaooo.jpg'),dst)


# If found, add object points, image points (after refining them)
if ret == True:
    print('boh')
    objpoints.append(objp)
    #corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
    # Draw and display the corners
    cv.drawChessboardCorners(img, (2,2), corners, ret)
    #cv.imshow('img', img)
    #cv.waitKey()
    cv.imwrite(str(path+r'/ciaooo.jpg'),img)
cv.destroyAllWindows()
'''