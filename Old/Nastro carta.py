import cv2 as cv
import numpy as np
import exifread
import os
path = os.path.abspath(os.path.dirname(__file__)) #salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  #cambio della cartella attuale nella cartella in cui si trova il file .py

img=cv.imread('a.jpg')

altezza,larghezza = img.shape[:2]
print('-------')
c=0 #contatore
nastro = True
lim_area1=int(larghezza*0.25)
lim_area2=int(larghezza*0.75)
max_val=int(larghezza*0.5)
while (nastro==True and c < altezza):
    area=img[c:c+1,lim_area1:lim_area2]
    count=np.count_nonzero(area)
    if count > max_val:
        img[c:c+1,lim_area1:lim_area2]=[0,0,0]
        cv.imshow('ciao', img)
        cv.waitKey(5)
    elif count <=max_val:
        nastro=False
        if c!=0:
            img[(c):(c+3),lim_area1:lim_area2]=[0,0,0] # rimozione di 3 righe in più per eliminare eventuali residui di nastro
            ritaglio_radici = img[c+3:altezza,0:larghezza]
            cv.imwrite('ritaglio_radici.jpg', ritaglio_radici)
            cv.imshow('ciao', img)
            cv.waitKey(0)
    c=c+1
cv.imwrite('a_nuovo.jpg', img)    
