import cv2 as cv
import numpy as np

#path = r'C:\Users\chiar\OneDrive\Desktop\1.jpg'
# Load imgae, grayscale, Gaussian blur, Otsu's threshold
img = cv.imread(r'C:\Users\chiar\OneDrive\Desktop\progetto\IdentificazioneQR\1.jpg')
img1 = cv.resize(img,None,fx=0.13,fy=0.13, interpolation = cv.INTER_CUBIC)
dim = img.shape #salva le dimensioni dell'immagine (espresse come una tupla) in dim. quindi altezza = dim[1], lunghezza = dim[2]

hsv = cv.cvtColor(img1, cv.COLOR_BGR2HSV)
qr = cv.QRCodeDetector.detect(img,int())
cv.imshow('image',hsv)
cv.waitKey(0)
cv.destroyAllWindows()

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