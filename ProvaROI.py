import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode #decodifica del QR
import os # utilizzata per effettuare operazioni sulle cartelle
import glob
import shutil #permette di effettuare operazioni su file

path = os.path.abspath(os.path.dirname(__file__)) #salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  #cambio della cartella attuale nella cartella in cui si trova il file .py

scanpath = os.scandir()
 
print('Files and Directories in ' + path)
scansione = os.scandir()
print(scansione)
for pino in scansione:
    if pino.is_dir()== True:
        #print(pino.name)
        subpath = str(path + r'/'+ pino.name)
        os.chdir(subpath)
        scansubdir = os.scandir()
        data_path = os.path.join(subpath,'*.jpg')
        files = glob.glob(data_path) #converte data path in un output Unix-like (ls) (*.jpg -> lista di elementi con estensione jpg)
        #print(files)
# Ogni soggetto è identificato dal QR, che viene decodificato ed utilizzato per rinominare le rispettive sottocartelle. 
        for f1 in files:
            pippo = os.path.basename(f1)
            image = cv.imread(f1)
            altezza, larghezza, colori = image.shape
            dim_scaled = (int(larghezza/altezza*800),800)
            #img_scaled = cv.resize(image, dim_scaled, interpolation = cv.INTER_AREA)
            img_to_zero = cv.cvtColor(image, cv.THRESH_TOZERO_INV)
            img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)      #Truncated viene meglio
            lower_range = np.array([20,15,60])
            upper_range = np.array([120,70,250])
            img_scaled = cv.resize(img_hsv, dim_scaled, interpolation = cv.INTER_AREA)
            #ret,thresh1 = cv.threshold(img_scaled,110,250,cv.THRESH_BINARY)
            mask = cv.inRange(img_scaled, lower_range, upper_range)
            #mask_scaled = cv.resize(mask, dim_scaled, interpolation = cv.INTER_AREA)
            cv.imshow('hsv', mask)
            cv.imshow('to zero', img_scaled)
            #cv.imwrite(str(pippo +'_HSV.jpg'), img_trunc)


            cv.waitKey(3000)

        cv.destroyAllWindows()


#print("Files and Directories in '% s':" % path)
#scansione = os.scandir()
#print(scansione)
#for pino in scansione:
#    print(pino.name)
#    if pino.name == 'SBP_140_R3':
#        os.chdir(r'C:\Users\esu7z\Desktop\GitHub\IdentificazioneQR\SBP_140_R3')
#        print(os.getcwd)
 #       img = cv.imread('DSC00406.JPG')
 #       cv.imshow('pino', img)
 #       cv.waitKey(0)   '''