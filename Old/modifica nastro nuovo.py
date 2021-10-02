import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode #decodifica del QR
import os # utilizzata per effettuare operazioni sulle cartelle
import glob
import shutil #permette di effettuare operazioni su file
from skimage.morphology import thin # pip install scikit-image 
#(Potrebbe essere necessario aggiungere una cartella al PATH di sistema, vedere output installazione)

def RimozioneNastro(image, cartella, nomefile):    # Oscuramento della zona del nastro che fissa la pianta al cartoncino
    altezza, larghezza = image.shape[:2]    # Salvataggio delle dimensioni dell'immagine in imput
    r=0     #contatore di riga
    c=0     # indice di taglio


    never_found = False
    inizio_nastro = 0



    nastro = True   # booleano che indica la presenza di nastro in cima al cartoncino
    print("Rimozione nastro...")
    # Definizione dei limiti destro e sinistro per l'operazione di oscuramento
    lim_x1 = int(larghezza/4)
    print("larghezza/4 =" + str(larghezza/4))
    lim_x2= int(larghezza/4*3)
    print(lim_x1)
    lim_y = int(altezza/4)
    max_val = int(larghezza*0.3) # Valore limite che suggerisce se in un'area vi è del nastro oppure no
    while (r<lim_y):
        area=image[r:(r+1),lim_x1:lim_x2]   #definizione dell'area di lavoro per l'iterazione corrente
        count=np.count_nonzero(area)            # conteggio dei pixel di colore diverso dal nero !=[0]
        if count >= max_val:  # se il numero di pixel calcolato è superiore al massimo valore ammesso
            if (never_found==False):
                never_found=True
                inizio_nastro=r
            c = r+1 # si pone l'indice di taglio pari all'indice della riga successiva a quella considerata
        r=r+1 # incremento del contatore di riga
    if c!=0:  # se sono state oscurate parti dell'immagine:
                print("Nastro rimosso.")
                 #salvataggio su disco dell'immagine prima della rimozione del nastro
                image_bgr=cv.cvtColor(image,cv.COLOR_GRAY2BGR)
                print(image_bgr.shape[2])
                image_bgr[c:c+1,lim_x1:lim_x2]=[0,0,255]
                zona = image_bgr[c+25:c+630,lim_x1:lim_x2]   # definizione della nuova area contenente le radici
                image_bgr[inizio_nastro:inizio_nastro+1,lim_x1:lim_x2]=[0,255,0]
                image_bgr[inizio_nastro:c,lim_x1:lim_x1+1]=[0,255,0]
                image_bgr[inizio_nastro:c,lim_x2-1:lim_x2]=[0,255,0]
                image_bgr[c:c+1,lim_x1:lim_x2]=[0,255,0]
                image_bgr[c+25:c+26,lim_x1:lim_x2]=[0,0,255]
                nastro = image_bgr[inizio_nastro:inizio_nastro+600,lim_x1:lim_x2]
                cv.imwrite(str(nomefile +' zona.jpg'), zona)
                cv.imwrite(str(nomefile +' nastro.jpg'), nastro)
                #cv.imwrite(cartella + r'/' + nomefile +'_ritaglio_radici.jpg', ritaglio_radici) #salvataggio dell'immagine ritagliata su disco
                return image
    elif c==0:  #oppure se c è uguale a 0 significa che non vi è alcun nastro nell'area considerata.
        print("Non è stato trovato alcun nastro.")
        return image

path = os.path.abspath(os.path.dirname(__file__)) #salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  #cambio della cartella attuale nella cartella in cui si trova il file .py

scansione = os.scandir() #scansione dei file all'interno della cartella path
for sottocartella in scansione: #ciclo per scansionare le sottocartelle di path
    if sottocartella.is_dir():  #controllo se il file in esame è una cartella
        subpath = str(path + r'/'+ sottocartella.name) # Percorso della sottocartella
        os.chdir(subpath)   # passaggio alla sottocartella in esame
        data_path = os.path.join(subpath,'*[0-9].jpg')   # I file prodotti dall'esecuzione sono file png, a differenza dei campioni che sono immagini jpg.
                                                    # In questo modo, se il programma viene eseguito più volte, i file salvati su disco da una precedente esecuzione del programma
                                                    # non vengono utilizzati come input dal programma.                                                    
        files = glob.glob(data_path) #converte data path in un output Unix-like (ls | grep jpg) (*[0-9].jpg -> lista di elementi con estensione jpg che hanno una cifra come ultimo carattere del nome)
        for f1 in files:    #Ciclo per scorrere tutte le immagini delle sottocartelle 
            nomefile = os.path.basename(f1)    #nome dell'immagine in esame, utilizzato poi per rinominare il risultato delle operazioni
            nomefile,ext = os.path.splitext(nomefile) #rimozione dell'estensione ".JPG" dal nome del file
            image = cv.imread(f1)   #lettura dell'immagine dal disco
            print(str('Scansione del file '+nomefile+' in corso.'))
            altezza, larghezza = image.shape[:2]      # salvataggio delle dimensioni dell'immagine (prende solo i primi 2 valori della tupla shape, il terzo contiene i colori)
            #img_focus = image[(int(altezza/5)):(int(altezza*0.95)),int((larghezza/9)):int((larghezza*0.9))] #parziale ritaglio dell'immagine che facilita il riconoscimento del cartoncino
            img_focus = image[1200:5700,450:3600] #parziale ritaglio dell'immagine che facilita il riconoscimento del cartoncino
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
            scarto_x = int(larghezza*0.03) #margine per eliminare i bordi del cartoncino a destra e sinistra
            scarto_y = int(altezza*0.02) #margine per eliminare i bordi del cartoncino in fondo all'immagine

            cartoncino = img_focus[y:y+h-scarto_y,x+scarto_x:x+w-scarto_x,:] #Ritaglio del cartoncino
          
            mask_inv = cv.bitwise_not(mask) # Inversione della maschera effettuata per evidenziare le radici
            mask_inv = mask_inv[y:y+h-scarto_y,x+scarto_x:x+w-scarto_x]    # Ritaglio della maschera alle dimensioni del contorno del cartoncino

            #Rimozione dell'eventuale nastro che tiene fissata la pianta al cartoncino
            mask_inv = RimozioneNastro(mask_inv,subpath,nomefile)

            kernel = np.ones((5,5),np.uint8) # definizione del kernel
            erosion = cv.erode(mask_inv,kernel,iterations = 1) #erosione
            erosion=erosion.astype(bool) # Conversione in binario in modo da avere
                                         # 1 per valori > 0 in BGR, 0 per valori uguali a zero in BGR

            #Thinning
            print('Thinning dell\'immagine...')
            #thinning = (thin(erosion)*255).astype(np.uint8) #applicazione della funzione thinning
            print('Thinning eseguito.')

            # Salvataggio delle immagini elaborate su disco
            #cv.imwrite(str(nomefile +'_focus.jpg'), img_focus)
            #cv.imwrite(str(nomefile +'_maschera_invertita.jpg'), mask_inv)
            #cv.imwrite(str(nomefile +'_thinning.jpg'), thinning)
            #cv.imwrite(str(nomefile +'_erosion.jpg'), erosion)
            #cv.imwrite(str(nomefile +'_cartoncino.jpg'), cartoncino)

            #stampa nel terminale del file in esame
            print(str('File '+nomefile+' scansionato.'))

        #stampa nel terminale della cartella in esame 

        print(str('Cartella '+sottocartella.name+' scansionata.'))

print(str('Processo terminato'))       