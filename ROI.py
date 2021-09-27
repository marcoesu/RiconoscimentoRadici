import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode #decodifica del QR
import os # utilizzata per effettuare operazioni sulle cartelle
import glob
import shutil #permette di effettuare operazioni su file
from skimage.morphology import thin

def RimozioneNastro(image,nomefile):
    print("Rimozione nastro")
    altezza, larghezza = image.shape[:2]
    c=0 #contatore
    nastro = True
    lim_area1=0
    lim_area2=larghezza
    max_val=int(larghezza*0.35)
    while (nastro==True and (c < altezza)):
        area=image[c:c+1,lim_area1:lim_area2]
        count=np.count_nonzero(area)
        if count > max_val:
            image[c:c+1,lim_area1:lim_area2]=[0]
            #cv.imshow('ciao', image)
            #cv.waitKey(1)
        elif count <=max_val:
            nastro=False
            if c!=0:
                image[(c):(c+3),lim_area1:lim_area2]=[0] # rimozione di 3 righe in più per eliminare eventuali residui di nastro
                ritaglio_radici = image[c+3:altezza,0:larghezza]
                cv.imwrite(nomefile+'ritaglio_radici.jpg', ritaglio_radici)
        c=c+1
    #cv.imwrite(str(nomefile +'_nuovo.jpg'), image)   

path = os.path.abspath(os.path.dirname(__file__)) #salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  #cambio della cartella attuale nella cartella in cui si trova il file .py

scansione = os.scandir() #scansione dei file all'interno della cartella path
for sottocartella in scansione: #ciclo per scansionare le sottocartelle di path
    if sottocartella.is_dir():  #controllo se il file in esame è una cartella
        subpath = str(path + r'/'+ sottocartella.name)
        os.chdir(subpath)   # passaggio alla sottocartella in esame
        #scansubdir = os.scandir()
        data_path = os.path.join(subpath,'*[0-9].jpg')   # I file prodotti dall'esecuzione sono file png, a differenza dei campioni che sono immagini jpg.
                                                    # In questo modo, se il programma viene eseguito più volte, i file salvati su disco da un precedente avvio del programma
                                                    # non vengono utilizzati come input dal programma.                                                    
        files = glob.glob(data_path) #converte data path in un output Unix-like (ls | grep jpg) (*[0-9].jpg -> lista di elementi con estensione jpg che hanno una cifra come ultimo carattere del nome)
        for f1 in files:    #Ciclo per scorrere tutte le immagini delle sottocartelle 
            nomefile = os.path.basename(f1)    #nome dell'immagine in esame, utilizzato poi per rinominare il risultato delle operazioni
            nomefile,ext = os.path.splitext(nomefile) #rimozione dell'estensione ".JPG" dal nome del file
            image = cv.imread(f1)   #lettura dell'immagine dal disco
            altezza, larghezza = image.shape[:2]      # salvataggio delle dimensioni dell'immagine (prende solo i primi 2 valori della tupla shape, il terzo contiene i colori)
            img_focus = image[(int(altezza/5)):(int(altezza*0.95)),int((larghezza/9)):int((larghezza*0.9))] #parziale ritaglio dell'immagine che facilita il riconoscimento del cartoncino
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
            scarto_x = int(larghezza*0.02)
            scarto_y = int(larghezza*0.02)

            cartoncino = img_focus[y:y+h-scarto_y,x+scarto_y:x+w-scarto_y,:] #Ritaglio del cartoncino
          
            mask_inv = cv.bitwise_not(mask) # Inversione della maschera effettuata per trovare le radici
            mask_inv = mask_inv[y:y+h-scarto_y,x+scarto_y:x+w-scarto_y]    # Ritaglio della maschera alle dimensioni del contorno del cartoncino
            
            #Rimozione dell'eventuale nastro che tiene fissata la pianta al cartoncino
            RimozioneNastro(mask_inv,nomefile)

            #aggiungere un margine per eliminare i bordi del cartoncino
            kernel = np.ones((5,5),np.uint8)
            erosion = cv.erode(mask_inv,kernel,iterations = 1) #erosione
            erosion=erosion.astype(bool)

            print('Thinning dell\'immagine')
            thinning = (thin(erosion)*255).astype(np.uint8) #applicazione della funzione thinning

            # Salvataggio delle immagini elaborate su disco
            cv.imwrite(str(nomefile +'_focus.jpg'), img_focus)
            cv.imwrite(str(nomefile +'_maschera_invertita.jpg'), mask_inv)
            cv.imwrite(str(nomefile +'_thinning.jpg'), thinning)
            #cv.imwrite(str(nomefile +'_erosion.jpg'), erosion)
            cv.imwrite(str(nomefile +'_cartoncino.jpg'), cartoncino)

            #stampa nel terminale del file in esame
            print(str('File '+nomefile+' scansionato.'))

        #stampa nel terminale della cartella in esame 

        print(str('Cartella '+sottocartella.name+' scansionata.'))

print(str('Processo terminato'))       