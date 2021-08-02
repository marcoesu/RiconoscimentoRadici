import cv2 as cv
import numpy as np
import pyzbar.pyzbar
import os
import glob
path = os.path.abspath(os.path.dirname(__file__)) #salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)
print(path)
cwd = os.getcwd()
print(cwd)
data_path = os.path.join(path,'*g') 
files = glob.glob(data_path) 
for f1 in files: 
    image = cv.imread(f1) 
    altezza, larghezza, colori = image.shape #salva le dimensioni dell'immagine (espresse come una tupla) in dim. quindi altezza = dim[1], lunghezza = dim[2]
    zonaqr=image[(int(altezza/4)):(int(altezza/2.5)),int((larghezza/10)):int((larghezza/3.5))]
    dim_scaled = (int(larghezza/altezza*1000),1000)
    for qr in pyzbar.pyzbar.decode(zonaqr):
        codid=qr.data.decode('utf-8')    #codice identificativo estratto dal QR
    img_scaled = cv.resize(image, dim_scaled, interpolation = cv.INTER_AREA) #da sostituire con ROI costituita dall'area che comprende solo il cartoncino blu
    cv.imshow(str(codid),img_scaled)
    cv.waitKey(0)
    cv.destroyAllWindows()  

'''hsv = cv.cvtColor(img1, cv.COLOR_BGR2HSV)
qrCodeDetector = cv.QRCodeDetector()
decodedText, points, _ = qrCodeDetector.detectAndDecode(img)
print('Il contenuto del qr è:'+ decodedText)
#cv.imshow('image',hsv)
cv.waitKey(0)'''

'''original = image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (9,9), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Morph close
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

# Find contours and filter for QR code
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    x,y,w,h = cv2.boundingRect(approx)
    area = cv2.contourArea(c)
    ar = w / float(h)
    if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
        ROI = original[y:y+h, x:x+w]
        cv2.imwrite('ROI.png', ROI)

cv2.imshow('thresh', thresh)
cv2.imshow('close', close)
cv2.imshow('image', image)
cv2.imshow('ROI', ROI)
cv2.waitKey()     '''