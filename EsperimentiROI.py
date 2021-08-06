#aaaaaaaaaaaaaaa
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
for sottocartella in scansione:
    if sottocartella.is_dir()== True:
        subpath = str(path + r'/'+ sottocartella.name)
        os.chdir(subpath)
        scansubdir = os.scandir()
        data_path = os.path.join(subpath,'*.jpg')
        files = glob.glob(data_path) #converte data path in un output Unix-like (ls) (*.jpg -> lista di elementi con estensione jpg)
        #print(files)
        #Ciclo per scorrere tutte le immagini delle sottocartelle 
        for f1 in files:
            nomefile = os.path.basename(f1)
            image = cv.imread(f1)
            altezza, larghezza, colori = image.shape    
            #dim_scaled = (int(larghezza/altezza*800),800)           # Immagine rimpicciolita per comodità. Le immagini originali sono 6000x4000.
            #img_scaled = cv.resize(image, dim_scaled, interpolation = cv.INTER_AREA)
            #img_to_zero = cv.cvtColor(image, cv.THRESH_TOZERO)     #la radice assume una colorazione tendente al celeste
            
            img_scaledo = image[(int(altezza/4)):(int(altezza)),int((larghezza/9)):int((larghezza))] 

            altezza, larghezza, colori = img_scaledo.shape    
            dim_scaled = (int(larghezza/altezza*800),800)           # Immagine rimpicciolita per comodità. Le immagini originali sono 6000x4000.
            img_scaled = cv.resize(img_scaledo, dim_scaled, interpolation = cv.INTER_AREA)


            img_hsv= cv.cvtColor(img_scaledo, cv.COLOR_BGR2HSV)
            
            #lower_range = np.array([20,15,60])                      #Utilizzando la conversione in HSV in combinazione con la maschera otteniamo buona parte delle radici
            #upper_range = np.array([120,70,250])                    #I limiti della maschera
            #lower_range = np.array([20, 20, 50], dtype=np.uint8)
            #upper_range = np.array([50,255,255], dtype=np.uint8)                    #I limiti della maschera, colore rosso (HSV)
            
            lower_green = np.array([30, 80, 30], dtype=np.uint8)            #range per il colore verde
            upper_green = np.array([150,255,150], dtype=np.uint8)
            
            #lower_green = np.array([57, 63, 100], dtype=np.uint8)            #range per il colore verde
            #upper_green = np.array([53,38,52], dtype=np.uint8)           #per evidenziare il cartoncino blu (nell'immagine convertita in hsv è verde)
            
            mask = cv.inRange(img_hsv, lower_green, upper_green)
            img_gray = cv.cvtColor(img_scaled, cv.COLOR_BGR2GRAY)          #Utilizzando invece TRUNC l'immagine assume una colorazione leggermente più scura di THRESH_TO_ZERO

            #L'immagine viene scalata per essere visibile completamente a schermo
            #ret,thresh1 = cv.threshold(img_scaled,110,250,cv.THRESH_BINARY)
            #imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
            ret, thresh = cv.threshold(mask, 127, 255, cv.THRESH_BINARY)
            contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
            
            c = max(contours, key=cv.contourArea)

            x, y, w, h = cv.boundingRect(c)
            rect = centro, dimensioni, angolo = cv.minAreaRect(c)
            box = cv.boxPoints(rect)
            #box = np.int0(box)
            pts1 = box
            print(pts1)
            pts2 = ([x,y],[x+w,y],[x,y+h],[x+w,y+h])
            print(pts2)
            #M = cv.getPerspectiveTransform(pts1,pts2)
            #imgo=np.array(img_scaledo)
            #dst = cv.warpPerspective(img_scaledo,M,dsize=(larghezza,altezza))
            #box = cv.boxPoints(rect)           
            #box = np.int0(box)

            '''
            altezza_area,larghezza_area=dimensioni
            altezza_area=int(altezza_area)
            larghezza_area=int(larghezza_area)
            #print(box)
            #cv.drawContours(img_scaledo,[box],0,(0,0,255),2)
              # Sommare valori area a punto in alto a sinistra
            if angolo < -45:
                angolo = (90 - angolo)
            else:
                angolo = -90+angolo
            # cols-1 and rows-1 are the coordinate limits.
            M = cv.getRotationMatrix2D((centro),angolo,1)
            #M = cv.getRotationMatrix2D(((altezza_area/2),(larghezza_area)),1,1)
            #dst = cv.warpAffine(img_scaledo,M,(int(larg),int(al)))
            dst = cv.warpAffine(img_scaledo,M,dsize=(larghezza,altezza))
            #dst = cv.warpAffine(img_scaledo,M,(img_scaledo.shape[2],img_scaledo.shape[1]))
            #m_larghezza = 50
            #m_altezza = 40 #non utilizzato perché rovina la maggior parte dei risultati per migliorarne pochi
            img_hsv= cv.cvtColor(dst, cv.COLOR_BGR2HSV)
            mask = cv.inRange(img_hsv, lower_green, upper_green)
            ret, thresh = cv.threshold(mask, 127, 255, cv.THRESH_BINARY)
            contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)        
            c = max(contours, key=cv.contourArea)     
            x, y, w, h = cv.boundingRect(c)
'''


            #prova = dst[y-margine:y+h+margine,x-margine:x+w+margine, :]
            #prova = img_scaledo[y-m_altezza:y+h,x-m_larghezza:x+w+m_larghezza, :]
            
            #prova = dst[y:y+h,x:x+w, :]
            
            #prova = img_scaledo[int(y[1]):int(y[2]),int(x[1]):int(x[2]),:]

            #contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
            #mask = cv.inRange(img_scaled, lower_range, upper_range)
            #mask_scaled = cv.resize(mask, dim_scaled, interpolation = cv.INTER_AREA)
            #cv.imshow('hsv', mask)
            #cv.drawContours(img_hsv, contours, -1, (0,255,0), 2)

            #for c in contours:
            #    if cv.contourArea(c) > 1000:  #  Ignore very small contours
                # Mark triangle with blue line
            #        cv.drawContours(img_hsv, [c], -1, (255, 0, 0), 2)

            #cv.imshow('prova', mask)
            #cv.imshow('to zero', dst)

            #cv.imwrite(str(nomefile +'_area.png'),img_scaledo)
            #cv.imwrite(str(nomefile +'_area2.png'),prova)
            #cv.imwrite(str(nomefile +'_area2.png'),dst)



        # https://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html

            #cv.waitKey(3000)

        #cv.destroyAllWindows()