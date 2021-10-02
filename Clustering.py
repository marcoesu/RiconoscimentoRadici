import numpy as np
import cv2 as cv
import glob
import os

from numpy.core.numeric import count_nonzero

path = os.path.abspath(os.path.dirname(__file__)) #salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  #cambio della cartella attuale nella cartella in cui si trova il file .py

scansione = os.scandir() #scansione dei file all'interno della cartella path
for sottocartella in scansione: #ciclo per scansionare le sottocartelle di path
    if sottocartella.is_dir():  #controllo se il file in esame è una cartella
        subpath = str(path + r'/'+ sottocartella.name) # Percorso della sottocartella
        os.chdir(subpath)   # passaggio alla sottocartella in esame
        data_path = os.path.join(subpath,'*_thinning.jpg')   # I file prodotti dall'esecuzione sono file png, a differenza dei campioni che sono immagini jpg.
                                                    # In questo modo, se il programma viene eseguito più volte, i file salvati su disco da una precedente esecuzione del programma
                                                    # non vengono utilizzati come input dal programma.                                                    
        files = glob.glob(data_path) #converte data path in un output Unix-like (ls | grep jpg) (*[0-9].jpg -> lista di elementi con estensione jpg che hanno una cifra come ultimo carattere del nome)
        for f1 in files:    #Ciclo per scorrere tutte le immagini delle sottocartelle 
            nomefile = os.path.basename(f1)    #nome dell'immagine in esame, utilizzato poi per rinominare il risultato delle operazioni
            nomefile,ext = os.path.splitext(nomefile) #rimozione dell'estensione ".JPG" dal nome del file
            img = cv.imread(f1,0)   #lettura dell'immagine dal disco
            print(str('Scansione del file '+nomefile+' in corso.'))
            # salvataggio delle dimensioni dell'immagine (prende solo i primi 2 valori della tupla shape, il terzo contiene i colori)

            #gray = np.float32(img) 
            harris = cv.cornerHarris(img,2,3,0.04) #applicazione dell'algoritmo di harris

            #result is dilated for marking the corners, not important
            #harris = cv.dilate(harris,None) # ingrandisce il corner
            #dst = dst.astype(np.uint8)

            img = cv.cvtColor(img, cv.COLOR_GRAY2BGR,dstCn=3) # conversione da bianco e nero a RGB

            clustering_rgb=img.copy() # In alternativa clustering_rgb = np.zeros((altezza,larghezza,3)).astype(np.uint8)
            img_harris=img.copy()

            # Threshold for an optimal value, it may vary depending on the image.
            img_harris[harris>0.02*harris.max()]=[0,0,255] #disegna i cerchi rossi sullo scheletro
            cv.imwrite(nomefile+" harris.png", img_harris)

            confronto = img_harris.copy() # creazione di una copia dello scheletro iniziale

            altezza, larghezza = img_harris.shape[:2] #dimensioni dell'immagine ottenuta con harris
            nero = np.zeros((altezza,larghezza,1)) #crea un'immagine completamente nera
            nero[harris>0.02*harris.max()]=[255] #disegna i punti di interesse trovati con harris su un'immagine nera

            nero = nero.astype(np.uint8) #i punti riportati da harris sono in subpixel,
                                        # andiamo quindi a convertire l'immagine in un array di interi
                                        # approssimando la posizione dei punti ottenuti con l'algoritmo di harris
                                        # in pixel

            p=2  # parametro che indica la distanza del punto in esame dal perimetro della sottoarea di lavoro 

            #############
            #     p     #
            #  p  O  p  #
            #     p     #
            #############
            
            # Clustering: si analizzano i punti ottenuti con l'algoritmo di Harris e gli agglomerati costituiti da punti molto vicini vengono sostituiti dal loro punto medio.
            # L'algoritmo definisce una sottoarea di lavoro, utilizzando il parametro p, ogniqualvolta che si incontra un punto bianco.
            # Vengono contati i pixel bianchi e ne vangono salvate le coordinate. Si procede poi a calcolare il punto medio se nell'area vi sono più punti bianchi.
            # Viene colorata di nero l'area sull'immagine di partenza (Harris) corrispondente alla area di lavoro corrente e viene disegnato il punto medio su un'immagine nera.
            clustering = np.zeros((altezza, larghezza, 1)).astype(np.uint8) # creazione di un'immagine nera usata per il salvataggio dei punti medi
            riga = p # il contatore di riga viene posto uguale al parametro per far sì che la sottoarea di lavoro non oltrepassi i bordi dell'immagine.
            while (riga < altezza-p): 
                colonna = p
                while (colonna < larghezza-p):
                    if(nero[riga][colonna] == 255): #definizione
                        area = nero[int(riga - p):int(riga+p),int(colonna-p):int(colonna+p)]
                        n_pixel = np.count_nonzero(area)
                        if (n_pixel>1):
                            media_punti_x=np.ndarray(n_pixel)
                            media_punti_y=np.ndarray(n_pixel)
                            riga_area = 0
                            while (riga_area<area.shape[0]):
                                colonna_area = 0
                                pixel = 0
                                while (colonna_area<area.shape[1] and pixel<n_pixel):
                                    if(area[riga_area,colonna_area]==[255]):
                                        media_punti_y[pixel]=riga_area
                                        media_punti_x[pixel]=colonna_area
                                        pixel+=1
                                    colonna_area+=1
                                riga_area+=1
                            media_x=(sum(media_punti_x)/n_pixel).astype(np.uint8)
                            media_y=(sum(media_punti_y)/n_pixel).astype(np.uint8)
                            area[0:p*2,0:p*2]=[0]                
                            area[(media_y),int(media_x)]=[255]
                            nero[riga - p:riga+p,colonna-p:colonna+p]=area
                            clustering[riga - p:riga+p,colonna-p:colonna+p]=area
                        elif(n_pixel == 1):  #Se è stato trovato un solo pixel nell'area, questo viene salvato direttamente sull'immagine di uscita.
                            clustering[riga][colonna]=[255]

                        
                    colonna = colonna+1
                riga = riga+1 

            # Disegno dei punti ottenuti dal clustering sullo scheletro di partenza e su un'immagine dello scheletro popolata con i punti trovati 
            # con'algoritmo di harris per il confronto fra Harris e il clustering effettuato.
            #Scorrimento dell'immagine in bianco e nero contenente i punti medi ottenuti dall'operazione di clustering
            row=0
            while (row < altezza):
                col=0
                while (col < larghezza):
                    if clustering[row,col] == [255]: # quando si incontra un punto bianco, ovvero un punto medio
                        clustering_rgb[row,col]=[0,255,0]   # viene riportato, con il colore verde, sullo scheletro iniziale
                        confronto[row,col]=[0,255,0]        # e, sempre con il colore verde sull'immagine su cui sono presenti scheletro 
                                                            # e il risultato con l'algoritmo di Harris (punti in rosso)
                    col+=1
                row+=1

            cv.imwrite(nomefile+" clustering_rgb.png",clustering_rgb)
            cv.imwrite(nomefile+" harris_c.png",confronto)




            '''            # Rimozione di punti isolati 
            row=1
            while (row < altezza-1):
                col=1
                while (col < larghezza-1):
                    if clustering_rgb[row,col] == [[0][255][0]]:
                        area=clustering_rgb[row-1:row+1,col-1:col+1]
                        n_pixel=count_nonzero(area)
                        if(n_pixel==1):
                            clustering_rgb[row-1:row+1,col-1:col+1]=[255,0,0]
                col+=1    
            row+=1'''
            



