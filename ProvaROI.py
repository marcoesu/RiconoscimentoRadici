import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode #decodifica del QR
import os # utilizzata per effettuare operazioni sulle cartelle
import glob
import shutil #permette di effettuare operazioni su file

path = os.path.abspath(os.path.dirname(__file__)) #salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  #cambio della cartella attuale nella cartella in cui si trova il file .py

scansione = os.scandir() #scansione dei file all'interno della cartella path
for sottocartella in scansione: #ciclo per scansionare le sottocartelle di path 
    if sottocartella.is_dir():  #controllo se il file in esame è una cartella
        subpath = str(path + r'/'+ sottocartella.name)
        os.chdir(subpath)   # passaggio alla sottocartella in esame
        scansubdir = os.scandir()
        data_path = os.path.join(subpath,'*[0-9].jpg')   # I file prodotti dall'esecuzione sono file png, a differenza dei campioni che sono immagini jpg.
                                                    # In questo modo, se il programma viene eseguito più volte, i file salvati su disco da un precedente avvio del programma
                                                    # non vengono utilizzati come input dal programma.                                                    
        files = glob.glob(data_path) #converte data path in un output Unix-like (ls | grep jpg) (*[0-9].jpg -> lista di elementi con estensione jpg che hanno una cifra come ultimo carattere del nome)
        for f1 in files:    #Ciclo per scorrere tutte le immagini delle sottocartelle 
            nomefile = os.path.basename(f1)    #nome dell'immagine in esame, utilizzato poi per rinominare il risultato delle operazioni
            nomefile,ext = os.path.splitext(nomefile) #rimozione dell'estensione ".JPG" dal nome del file
            image = cv.imread(f1)   #lettura dell'immagine dal disco
            altezza, larghezza = image.shape[:2]      # salvataggio delle dimensioni dell'immagine (prende solo i primi 2 valori della tupla shape, il terzo contiene i colori)
            img_focus = image[(int(altezza/4)):(int(altezza)),int((larghezza/9)):int((larghezza))] #parziale ritaglio dell'immagine che facilita il riconoscimento del cartoncino
            altezza, larghezza = img_focus.shape[:2]    # dimensioni dell'immagine leggermente ritagliata

            img_hsv = cv.cvtColor(img_focus, cv.COLOR_BGR2HSV) #conversione da BGR (Blu, Verde, Rosso) ad HSV
            #Hue Saturation Brightness (HSB), in inglese "tonalità, saturazione e luminosità", indica sia un metodo additivo di composizione dei colori,
            # sia un modo per rappresentarli in un sistema digitale. Viene anche chiamato HSV da Hue Saturation Value (tonalità, saturazione e valore).
                        
            #Range per selezionare il colore verde con la maschera
            lower_green = np.array([30, 80, 30])          
            upper_green = np.array([150,255,150])                       
            mask = cv.inRange(img_hsv, lower_green, upper_green) # Applicazione della maschera

            #Ricerca dei contorni utlizzando la maschera
            ret, thresh = cv.threshold(mask, 127, 255, cv.THRESH_BINARY) # necessita di un'immagine in scala di grigi che viene convertita in un'immagine binaria
            contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE) #Ricerca dei contorni utlizzando le informazioni ottenute attraverso il tresholding
            c = max(contours, key=cv.contourArea)   #Ricerca del più grande contorno nell'immagine utilizzando come parametro di giudizio l'area del contorno

            x, y, w, h = cv.boundingRect(c) #Restituisce le coordinate dell'area che contiene il contorno 
                                            #(le coordinate di un rettangolo, più precisamente le coordinate del vertice sinistro superiore e le dimensioni del rettangolo)

            cartoncino = img_focus[y:y+h,x:x+w,:] #Ritaglio del cartoncino
            cartoncino_hsv = cv.cvtColor(cartoncino, cv.COLOR_BGR2HSV)   #Conversione di cartoncino in HSV
            for c in contours:  #ciclo per disegnare i contorni
                if cv.arcLength(c, True) > 5000:  # Ignora i contorni più piccoli
                #if cv.contourArea(c) > 2000:  # Ignora i contorni più piccoli (non utilizzato perché restituiva altri contorni non rilevanti)
                    cv.drawContours(img_hsv, [c], -1, (255, 255, 255), 2)   #disegno dei contorni sull'immagine in HSV (colore bianco)

          
            mask_inv = cv.bitwise_not(mask) # Inversione della maschera effettuata per trovare le radici
            mask_inv = mask_inv[y:y+h,x:x+w]    # Ritaglio della maschera alle dimensioni del contorno del cartoncino

            # Applicazione del Thresholding adattivo (Gaussian)
            #mask_inv = cv.medianBlur(mask_inv,5) #meglio 3
            ThresholdAdattivo = cv.adaptiveThreshold(mask_inv,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)

            # Generazione dell'immagine ottenuta prendendo solo le parti in comune di cartoncino e maschera invertita
            radici = cv.bitwise_and(cartoncino, cartoncino, mask= mask_inv) 

            #utilizzo dell'immagine bitwise per l'adaptiveThreshold 
            radici_gray = cv.cvtColor(radici, cv.COLOR_BGR2GRAY) #conversione dell'immagine radici in scala di grigi
            # Applicazione del Thresholding adattivo (Gaussian)
            ThresholdAdattivoBitwise = cv.adaptiveThreshold(radici_gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)
        
            
            # Salvataggio delle immagini elaborate su disco
            cv.imwrite(str(nomefile +'_focus.jpg'), img_focus)
            cv.imwrite(str(nomefile +'_hsv.jpg'), img_hsv)
            cv.imwrite(str(nomefile +'_radici.jpg'), radici)
            cv.imwrite(str(nomefile +'_cartoncino_hsv.jpg'), cartoncino_hsv)
            cv.imwrite(str(nomefile +'_maschera.jpg'), mask)
            cv.imwrite(str(nomefile +'_maschera_invertita.jpg'), mask_inv)
            cv.imwrite(str(nomefile +'_ThresholdAdattivo.jpg'), ThresholdAdattivo)
            cv.imwrite(str(nomefile +'_ThresholdAdattivoBitwise.jpg'), ThresholdAdattivoBitwise)
            cv.imwrite(str(nomefile +'_cartoncino.jpg'), cartoncino)

    #        cv.imshow('Immagine', cartoncino)
    #        cv.waitKey(1500)

    #    cv.destroyAllWindows()