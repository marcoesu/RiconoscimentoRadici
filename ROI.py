import cv2 as cv
import numpy as np
import os # utilizzata per effettuare operazioni sulle cartelle
import glob
from skimage.morphology import thin # pip install scikit-image 
import math
import sys
sys.setrecursionlimit(30000)

#(Potrebbe essere necessario aggiungere una cartella al PATH di sistema, vedere output installazione)
#np.set_printoptions(threshold=sys.maxsize)

lato_mm = 5 # lato in mm del quadratino della scacchiera

# Codifica BGR (indici dell'array)
B = 0
G = 1
R = 2

def RimozioneNastro(image):    # Oscuramento della zona del nastro che fissa la pianta al cartoncino
    RN_altezza, RN_larghezza = image.shape[:2]    # Salvataggio delle dimensioni dell'immagine in imput
    r=0     #contatore di riga
    c=0     # indice di taglio
    print("Rimozione nastro...")
    # Definizione dei limiti destro e sinistro per l'operazione di oscuramento
    lim_x1 = int(RN_larghezza*0.25)
    lim_x2= int(RN_larghezza*0.75)
    lim_y = int(RN_altezza*0.25)
    max_val = int(RN_larghezza*0.3) # Valore limite che suggerisce se in un'area vi è del nastro oppure no
    while (r<lim_y):
        area=image[r:(r+1),lim_x1:lim_x2]   #definizione dell'area di lavoro per l'iterazione corrente
        count=np.count_nonzero(area)            # conteggio dei pixel di colore diverso dal nero !=[0]
        if count >= max_val:  # se il numero di pixel calcolato è superiore al massimo valore ammesso
            c = r+1 # si pone l'indice di taglio pari all'indice della riga successiva a quella considerata
        r=r+1 # incremento del contatore di riga
    if c!=0:  # se sono state oscurate parti dell'immagine:
                print("Nastro rimosso.")
                image = image[c+25:RN_altezza,0:RN_larghezza]   # definizione della nuova area contenente le radici
                #cv.imwrite(cartella + r'/' + nomefile +'_ritaglio_radici.jpg', ritaglio_radici) #salvataggio dell'immagine ritagliata su disco
                return image
    elif c==0:  #oppure se c è uguale a 0 significa che non vi è alcun nastro nell'area considerata.
        print("Non è stato trovato alcun nastro.")
        return image
    
def CalcoloCampione(image): # e restituisce il numero di pixel corrispondente a 5 mm

    img_focus = image[(int(altezza/5)):(int(altezza*0.95)),int((larghezza/9)):int((larghezza*0.9))] #parziale ritaglio dell'immagine che facilita il riconoscimento del cartoncino

    hsv=cv.cvtColor(img_focus, cv.COLOR_BGR2HSV) #Conversione di img_focus in HSV

    #Range per selezionare il colore verde con la maschera
    lower_green = np.array([0, 0, 0])          
    upper_green = np.array([150,100,100])

    img = cv.inRange(hsv, lower_green, upper_green) # Applicazione della maschera

    #operazione di closing per rendere i quadratini della scacchiera più definiti

    kernel = np.ones((3,3),np.uint8)
    img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel) #closing
    img_inv=cv.bitwise_not(img)

    size = (2,3) 

    # in corners, abbiamo prima i valori di x e poi i valori di y
    # andiamo a trovare i punti sulla scacchiera in modo da poter poi calcolarne la distanza
    ret, corners_circle = cv.findCirclesGrid(img_inv, size , cv.CALIB_CB_ASYMMETRIC_GRID + cv.CALIB_CB_CLUSTERING) 

    # si crea un array (coord) in cui andiamo a inserire tutti gli elementi presenti in corners e andiamo a calcolare la distanza tra i primi due punti
    # ritorna 0 se non vengono trovati punti sulla scacchiera o se questi sono troppo distanti tra loro
    try :    
        coord = corners_circle.ravel() # inseriamo tutti i valori contetuti nella matrice corners nell'array coord
        #se i punti non sono troppo distanti tra loro
        if((coord[2]-coord[0]) <= 75 and (coord[3]-coord[1])<= 75):
            #calcolo della distanza tra due punti sqrt((x2-x1)^2 + (y2-y1)^2)
            distanza = math.sqrt((coord[2]-coord[0])*(coord[2]-coord[0]) + (coord[3]-coord[1])*(coord[3]-coord[1])) 
            lato_px=float(distanza/math.sqrt(2)).__round__(3) #per trovare il lato in pixel dividiamo la distanza per la radice di 2
            return lato_px,True #ritorna il lato del quadratino in pixel
        else: return 0,True 
    except : return 0,False

def angle_between(p1_y, p1_x, p2_y, p2_x):
    ang = np.arctan2(p2_y - p1_y, p2_x - p1_x)
    return ang*180/math.pi


def CalcoloParametri(y,x,l_radice):
    #if l_radice==0: risultato[row,col]=[0,0,255]
    flag=False
    green_found=False
    global fine_radice_y
    global fine_radice_x
    global ultimo_p_verde_y
    global ultimo_p_verde_x
    fine_radice_y = y
    fine_radice_x = x
    
    row_area=y-1
    while (row_area<y+2 and row_area<H_altezza):
        col_area = x-1
        while (col_area<x+2 and col_area<H_larghezza):
            if (clustering_rgb[row_area,col_area,G] == 255 and (row_area!=inizio_radice_y or col_area!=inizio_radice_x)): 
                if clustering_rgb[row_area,col_area,B] == 255:
                    flag=True
                    l_radice+=1 # incremento del contatore della lunghezza del tratto (in pixel) 
                    # Modifica del pixel in clustering_rgb, affinché non venga considerato da successive iterazioni
                    clustering_rgb[row_area,col_area,B]=150
                    clustering_rgb[row_area,col_area,G]=150

                    #risultato[row_area,col_area]=[255,255,255]
                    
                    # Richiamo alla funzione che parte da un pixel bianco o verde trovato nelle prossimità del pixel attualmente in esame
                    CalcoloParametri(row_area,col_area,l_radice)

                elif(clustering_rgb[row_area,col_area,B] == 0 and clustering_rgb[row_area,col_area,R] == 0):
                    l_radice+=1
                    green_found=True
                    clustering_rgb[row_area,col_area,R] = 50 # Colorazione del punto verde (solo componente rossa)
                    fine_radice_y = row_area
                    fine_radice_x = col_area
                    ultimo_p_verde_y = row_area
                    ultimo_p_verde_x = col_area
                    #risultato[row_area,col_area]=[200,200,20] 
                    angolo = angle_between(fine_radice_y,fine_radice_x,inizio_radice_y,inizio_radice_x)
                    
                    l_radice_cm = 0.0 # inizializzazione del parametro che indica lunghezza radice in cm
                    if(lato_pixel != 0):
                        l_radice_cm = (((float(l_radice)/float(lato_pixel))*float(lato_mm))*0.1).__round__(3)
                    
                    file_radici.write(str(inizio_radice_y) + ";" + str(inizio_radice_x) + ";" + str(fine_radice_y) + ";" + str(fine_radice_x) + ";" + str(green_found) + ";" + str(ultimo_p_verde_y)+ ";" + str(ultimo_p_verde_x)+ ";" + str(l_radice) + ";" + str(l_radice_cm) + ";" + str(angolo.__round__(3)) + "\n")

                    data.append([inizio_radice_y,inizio_radice_x,fine_radice_y,fine_radice_x,green_found,ultimo_p_verde_y,ultimo_p_verde_x,l_radice,l_radice_cm,angolo])
            col_area+=1
        row_area+=1


    if (fine_radice_y==inizio_radice_y and fine_radice_x==inizio_radice_x): # se il punto iniziale coincide con il punto finale, non viene considerata come radice
        return 

    if (flag==False and green_found==False): # se non è stato trovato alcun punto attorno a quello considerato
        #risultato[y,x]=[0,0,200]
        angolo = angle_between(fine_radice_y,fine_radice_x,inizio_radice_y,inizio_radice_x)

        l_radice_cm = 0.0
        if(lato_pixel != 0):
            l_radice_cm = (((float(l_radice)/float(lato_pixel))*float(lato_mm))*0.1).__round__(3)

        file_radici.write(str(inizio_radice_y) + ";" + str(inizio_radice_x) + ";" + str(fine_radice_y) + ";" + str(fine_radice_x) + ";" + str(green_found) + ";" + str(ultimo_p_verde_y)+ ";" + str(ultimo_p_verde_x)+ ";" + str(l_radice) + ";" + str(l_radice_cm) + ";" + str(angolo.__round__(3)) + "\n")

        data.append([inizio_radice_y,inizio_radice_x,fine_radice_y,fine_radice_x,green_found,ultimo_p_verde_y,ultimo_p_verde_x,l_radice,l_radice_cm,angolo])       

path = os.path.abspath(os.path.dirname(__file__)) #salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  #cambio della cartella attuale nella cartella in cui si trova il file .py

file = open("misurazioni.csv","w") #apertura del file per scrivere al suo interno il nome del file, perimetro e area
file.write("soggetto;data_ora_scatto;perimetro_px;perimetro_cm;area_pixel;area_cm;lato_pixel" + "\n") # definizione del'intestazione delle colonne

scansione = os.scandir() #scansione dei file all'interno della cartella path
for sottocartella in scansione: #ciclo per scansionare le sottocartelle di path
    if sottocartella.is_dir():  #controllo se il file in esame è una cartella
        subpath = str(path + r'/'+ sottocartella.name) # Percorso della sottocartella
        os.chdir(subpath)   # passaggio alla sottocartella in esame
        data_path = os.path.join(subpath,'[A-Z]_*[0-9].[j|p][p|n]g') # Il programma prende in ingresso solamente i file campione, ignorando i file prodotti da precedenti esecuzioni.
                                                                                                    
        files = glob.glob(data_path) #converte data path in un output Unix-like (ls | grep jpg) (*[0-9].jpg -> lista di elementi con estensione jpg che hanno una cifra come ultimo carattere del nome)
        for f1 in files:    #Ciclo per scorrere tutte le immagini delle sottocartelle 
            nomefile = os.path.basename(f1)    #nome dell'immagine in esame, utilizzato poi per rinominare il risultato delle operazioni
            nomefile,ext = os.path.splitext(nomefile) #rimozione dell'estensione ".JPG" dal nome del file
            image = cv.imread(f1)   #lettura dell'immagine dal disco
            print(str('Scansione del file '+nomefile+' in corso.'))
            altezza, larghezza = image.shape[:2]    # salvataggio delle dimensioni dell'immagine (prende solo i primi 2 valori della tupla shape, il terzo contiene i colori)
        
            # assegnazione del valore in pixel relativo al lato del quadrato nella scacchiera e 
            # del valore booleano utilizzato per verificare la presenza o meno dei punti
            lato_pixel, flag = CalcoloCampione(image)

            #Zona di ritaglio per escludere la zona delle luci e altri elementi di disturbo
            ritaglio_y1 = 1200      #(int(altezza/5)
            ritaglio_x1 = 450       #int((larghezza/9)
            ritaglio_y2 = 5700      #(int(altezza*0.95)
            ritaglio_x2 = 3600      #(int(larghezza*0.9))
            img_focus = image[ritaglio_y1:ritaglio_y2,ritaglio_x1:ritaglio_x2] #parziale ritaglio dell'immagine che facilita il riconoscimento del cartoncino
            cv.imwrite(str(nomefile +' focus.png'), img_focus) #Salvataggio su disco

            altezza, larghezza = img_focus.shape[:2]    # dimensioni dell'immagine leggermente ritagliata

            img_hsv = cv.cvtColor(img_focus, cv.COLOR_BGR2HSV) #conversione da BGR (Blu, Verde, Rosso) ad HSV
            #Hue Saturation Brightness (HSB), in inglese "tonalità, saturazione e luminosità", indica sia un metodo additivo di composizione dei colori,
            # sia un modo per rappresentarli in un sistema digitale. Viene anche chiamato HSV da Hue Saturation Value (tonalità, saturazione e valore).
            cv.imwrite(str(nomefile +' hsv.png'), img_hsv) #Salvataggio su disco       

            #Range per selezionare il colore verde con la maschera
            lower_green = np.array([30, 80, 30])          
            upper_green = np.array([150,255,150])                       
            mask = cv.inRange(img_hsv, lower_green, upper_green) # Applicazione della maschera
            cv.imwrite(str(nomefile +' maschera.png'), mask)

            #Ricerca dei contorni utlizzando la maschera
            #ret, thresh = cv.threshold(mask, 127, 255, cv.THRESH_BINARY) # necessita di un'immagine in scala di grigi che viene convertita in un'immagine binaria
            contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE) #Ricerca dei contorni utlizzando le informazioni ottenute attraverso il tresholding
            c = max(contours, key=cv.contourArea)   #Ricerca del più grande contorno nell'immagine utilizzando come parametro di giudizio l'area del contorno

            x, y, w, h = cv.boundingRect(c) #Restituisce le coordinate dell'area che contiene il contorno 
                                            #(le coordinate di un rettangolo, più precisamente le coordinate del vertice sinistro superiore e le dimensioni del rettangolo)
            scarto_x = int(larghezza*0.03) #margine per eliminare i bordi del cartoncino a destra e sinistra
            scarto_y = int(altezza*0.02) #margine per eliminare i bordi del cartoncino in fondo all'immagine

            cartoncino = img_focus[y:y+h-scarto_y,x+scarto_x:x+w-scarto_x,:] #Ritaglio del cartoncino
            cv.imwrite(str(nomefile +' cartoncino.png'), cartoncino) #Salvataggio su disco

            mask_inv = cv.bitwise_not(mask) # Inversione della maschera effettuata per evidenziare le radici

            mask_inv = mask_inv[y:y+h-scarto_y,x+scarto_x:x+w-scarto_x]    # Ritaglio della maschera alle dimensioni del contorno del cartoncino
            cv.imwrite(str(nomefile +' maschera_invertita_pre_rim_nastro.png'), mask_inv)
            #Rimozione dell'eventuale nastro che tiene fissata la pianta al cartoncino
            mask_inv = RimozioneNastro(mask_inv)

            # Inizializzazione dei parametri in cm
            area_cm = 0 
            perimetro_cm = 0

            area_pixel = np.count_nonzero(mask_inv) # calcolo dell'area in pixel contando il numero di punti bianchi 
               
            # Erosione
            kernel = np.ones((5,5),np.uint8) # definizione del kernel
            erosion = cv.erode(mask_inv,kernel,iterations = 1) #erosione
            cv.imwrite(str(nomefile +' erosione_pre_thinning.png'), erosion)

            #Thinning
            print('Thinning dell\'immagine...')
            thinning = (thin(erosion)*255).astype(np.uint8) #applicazione della funzione thinning
            print('Thinning eseguito.')

            perimetro_pixel = np.count_nonzero(thinning) #calcolo del perimetro in pixel contando il numero di punti bianchi

            # se il valore del lato del quadratino è diverso da zero allora calcoliamo perimetro e area in millimetri
            if(lato_pixel != 0):
                perimetro_cm = (((float(perimetro_pixel)/float(lato_pixel))*float(lato_mm))*0.1).__round__(3) #calcolo del perimetro in millimetri
                area_cm = (((float(area_pixel)/float(lato_pixel*lato_pixel))*float(lato_mm))*0.01).__round__(3) #calcolo dell'area in millimetri
            elif(lato_pixel == 0 and flag == True):
                print("I punti trovati non sono adatti per la conversione in millimetri.") #punti troppo distanti
            else:
                print("Non sono stati trovati punti per la conversione in millimetri.") #punti non trovati

            cartella, data = nomefile.split(" ",1) #divisione del nome del file in cartella e data

            #Scrittura su file csv
            file.write(str(cartella) + ";" + str(data) + ";" + str(perimetro_pixel) + ";" + str(perimetro_cm) + ";" + str(area_pixel) + ";" + str(area_cm) + ";" + str(lato_pixel) + "\n") 

            # Salvataggio delle immagini elaborate su disco
            cv.imwrite(str(nomefile +' maschera_invertita.png'), mask_inv)
            cv.imwrite(str(nomefile +' thinning.png'), thinning)
            
            img = thinning.copy()
            scheletro=thinning.copy() # copia dell'immagine contentente lo scheletro
            
            print(str('Analisi dello scheletro di '+nomefile+' in corso...'))
            img = img.astype(np.float32) #conversione di img in float32

            # applicazione dell'algoritmo di Harris per l'individuazione delle giunzioni e le terminazioni delle radici
            # L'algoritmo prende in ingresso come parametri: l'immagine su cui effettuiamo l'operazione, la dimensione dell'intorno per il rilevamento degli angoli,
            # il parametro di apertura della derivata di Sobel utilizzato e il parametro libero nell'equazione dell'Harris detector
            harris = cv.cornerHarris(img,2,3,0.08)

            img = cv.cvtColor(img, cv.COLOR_GRAY2BGR,dstCn=3) # conversione da bianco e nero a RGB

            img_harris=img.copy() #creazione di una copia dello scheletro su cui verrà disegnato l'output dell'algoritmo di Harris
            clustering_rgb=img.copy() #creazione di una copia dello scheletro su cui verrà disegnato il risultato del clustering

            img_harris[harris>0.02*harris.max()]=[0,0,255] # disegna i punti rossi, ottenuti con l'algoritmo di Harris, sullo scheletro
            cv.imwrite(nomefile+" harris.png", img_harris) # salvataggio su disco

            confronto = img_harris.copy() # creazione di una copia dello scheletro iniziale

            H_altezza, H_larghezza = img_harris.shape[:2] #dimensioni dell'immagine ottenuta con harris
            nero = np.zeros((H_altezza,H_larghezza,1)) #crea un'immagine completamente nera
            nero[harris>0.02*harris.max()]=[255] #disegna i punti di interesse trovati con harris su un'immagine nera

            p=4  # parametro che indica la distanza del punto in esame dal perimetro della sottoarea di lavoro 

            #############
            #     p     #
            #  p  O  p  #
            #     p     #
            #############
            
            # Clustering: si analizzano i punti ottenuti con l'algoritmo di Harris e gli agglomerati costituiti da punti molto vicini vengono sostituiti dal loro punto medio.
            # L'algoritmo definisce una sottoarea di lavoro, utilizzando il parametro p, ogniqualvolta che si incontra un punto bianco.
            # Vengono contati i pixel bianchi e ne vangono salvate le coordinate. Si procede poi a calcolare il punto medio se nell'area vi sono più punti bianchi.
            # Viene colorata di nero l'area sull'immagine di partenza (Harris) corrispondente alla area di lavoro corrente e viene disegnato il punto medio su un'immagine nera.
            clustering = np.zeros((H_altezza, H_larghezza, 1)).astype(np.uint16)#uint16 # creazione di un'immagine nera usata per il salvataggio dei punti medi
            print("Clustering...")
            riga = 0 # il contatore di riga viene posto uguale al parametro per far sì che la sottoarea di lavoro non oltrepassi i bordi dell'immagine.
            while (riga < H_altezza-p): 
                colonna = p
                y = riga if (riga>=p) else p
                while (colonna < H_larghezza-p):
                    if(nero[riga][colonna] == 255):
                        area = nero[int(y - p):int(y+p+1),int(colonna-p):int(colonna+p+1)]
                        n_pixel = np.count_nonzero(area)
                        #Calcolo del punto medio
                        if (n_pixel>1):
                            # allocazione degli array che conterranno rispettivamente ascisse e ordinate dei punti dell'area di lavoro
                            media_punti_x=np.zeros((n_pixel,1),dtype=np.uint32)
                            media_punti_y=np.zeros((n_pixel,1),dtype=np.uint32)
                            # Scorrimento dell'area di lavoro
                            pixel = 0
                            riga_area = y-p
                            while (riga_area<y+p+1):
                                colonna_area = colonna-p
                                while (colonna_area<colonna+p+1 and pixel<n_pixel):
                                    if(int(nero[riga_area,colonna_area])==255):
                                        # Salva le coordinate del punto bianco
                                        media_punti_y[pixel]=riga_area
                                        media_punti_x[pixel]=colonna_area
                                        pixel+=1 # incremento del contatore di pixel
                                    colonna_area+=1 # incremento del contatore delle colonne
                                riga_area+=1 # incremento del contatore delle righe
                            media_x=(sum(media_punti_x)/n_pixel).astype(np.uint32) # media delle ascisse
                            media_y=(sum(media_punti_y)/n_pixel).astype(np.uint32) # media delle ascisse
                            # Cancellazione dell'area analizzata
                            nero[y - p:y+p+1,colonna-p:colonna+p+1]=0
                            clustering[(media_y),(media_x)]=[255]
                        elif(n_pixel == 1):  #Se è stato trovato un solo pixel nell'area, questo viene salvato direttamente sull'immagine di uscita.
                            nero[riga][colonna] = [0]
                            clustering[riga, colonna]=[255]    
                    colonna = colonna+1
                riga = riga+1
            print("Clustering completato.")
            # Disegno dei punti ottenuti dal clustering sullo scheletro di partenza e su un'immagine dello scheletro popolata con i punti trovati 
            # con'algoritmo di harris per il confronto fra Harris e il clustering effettuato.
            #Scorrimento dell'immagine in bianco e nero contenente i punti medi ottenuti dall'operazione di clustering
            print("Disegno i punti...")          
            row=0
            while (row < H_altezza):
                col=0
                while (col < H_larghezza):
                    if clustering[row,col] == 255: # quando si incontra un punto bianco, ovvero un punto medio      ==[255]
                        clustering_rgb[row,col]=[0,255,0]   # viene riportato, con il colore verde, sullo scheletro iniziale
                        confronto[row,col]=[0,255,0]        # e, sempre con il colore verde sull'immagine su cui sono presenti scheletro 
                                                            # e il risultato con l'algoritmo di Harris (punti in rosso)
                    col+=1  # incremento del contatore della colonna
                row+=1  # incremento del contatore della riga

             #Salvataggio su disco
            print("Salvataggio su disco...")
            cv.imwrite(nomefile+" clustering.png",clustering_rgb)
            cv.imwrite(nomefile+" harris_clustering.png",confronto)
            print(str('Analisi dello scheletro di '+nomefile+' completata.')) 
            
            #Apertura del file .csv su cui vengono salvati i dati ottenuti
            file_radici = open(str(nomefile+'.csv'),'w')
            # Scrittura su file .csv
            file_radici.write("inizio della radice (y);inizio della radice (x);fine della radice (y);fine della radice (x);punto verde finale;ultimo punto verde incontrato (y);ultimo punto verde incontrato (x);lunghezza (px);lunghezza (cm);angolo"+"\n")

            #C_altezza, C_larghezza = clustering_rgb.shape[:2]

            #risultato = np.zeros((C_altezza, C_larghezza,3))


            # Dati delle estremità della radice analizzata
            inizio_radice_y = 0
            inizio_radice_x = 0
            ultimo_p_verde_y = 0
            ultimo_p_verde_x = 0
            fine_radice_y = 0
            fine_radice_x = 0            

            data = [] # inizializzazione di una lista vuota

            # Scorrimento immagine ottenuta dall'operazione di clustering
            row=0
            while (row < H_altezza):
                col=0
                while (col < H_larghezza):
                    if clustering_rgb[row,col,G] == 255 and clustering_rgb[row,col,B]==0: # quando si incontra un punto verde
                        count=0 # viene posto il contatore a zero, utilizzato per settare a 0 la lunghezza del segmento che verrà analizzato da CalcoloParametri
                        print("Punto verde.")
                        inizio_radice_y = row
                        inizio_radice_x = col
                        ultimo_p_verde_y = row
                        ultimo_p_verde_x = col
                        CalcoloParametri(row,col,count)
                    col+=1  # incremento del contatore della colonna
                row+=1  # incremento del contatore della riga
            print(data)

            #cv.imwrite(str(nomefile + "risultato.png"),risultato)
            #cv.imwrite(str(nomefile+"scorrimento.png"),clustering_rgb)


            # Chiusura del file .csv
            file_radici.close()

            # Stampa nel terminale del file in esame
            print(str('File '+nomefile+' scansionato.'))
            print('---------------------------------------------------------------')

        #Stampa nel terminale della cartella in esame 
        print(str('Cartella '+sottocartella.name+' scansionata.'))
        print('---------------------------------------------------------------')

file.close()        

print(str('Processo terminato'))       