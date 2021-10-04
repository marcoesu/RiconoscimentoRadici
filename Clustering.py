import numpy as np
import cv2 as cv
import glob
import os

path = os.path.abspath(os.path.dirname(__file__)) #salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  #cambio della cartella attuale nella cartella in cui si trova il file .py

scansione = os.scandir() #scansione dei file all'interno della cartella path
for sottocartella in scansione: #ciclo per scansionare le sottocartelle di path
    if sottocartella.is_dir():  #controllo se il file in esame è una cartella
        subpath = str(path + r'/'+ sottocartella.name) # Percorso della sottocartella
        os.chdir(subpath)   # passaggio alla sottocartella in esame
        data_path = os.path.join(subpath,'*thinning.[j|p][p|n]g')   # I file prodotti dall'esecuzione sono file png, a differenza dei campioni che sono immagini jpg.
                                                    # In questo modo, se il programma viene eseguito più volte, i file salvati su disco da una precedente esecuzione del programma
                                                    # non vengono utilizzati come input dal programma.                                                    
        files = glob.glob(data_path) #converte data path in un output Unix-like (ls | grep jpg) (*[0-9].jpg -> lista di elementi con estensione jpg che hanno una cifra come ultimo carattere del nome)
        for f1 in files:    #Ciclo per scorrere tutte le immagini delle sottocartelle 
            nomefile = os.path.basename(f1)    #nome dell'immagine in esame, utilizzato poi per rinominare il risultato delle operazioni
            nomefile = (nomefile.rsplit(" ",1))[0] # nome del file
            img = cv.imread(f1,0)   #lettura dell'immagine contenente lo scheletro dal disco
            print(str('Analisi dello scheletro di '+nomefile+' in corso...'))
            
            scheletro=img.copy() # copia dell'immagine contentente lo scheletro
            

            # applicazione dell'algoritmo di Harris per l'individuazione delle giunzioni e le terminazioni delle radici
            # L'algoritmo prende in ingresso come parametri: l'immagine su cui effettuiamo l'operazione, la dimensione dell'intorno per il rilevamento degli angoli,
            # il parametro di apertura della derivata di Sobel utilizzato e il parametro libero nell'equazione dell'Harris detector
            harris = cv.cornerHarris(img,2,3,0.08) 
            #harris = cv.cornerHarris(img,2,3,0.04) # applicazione dell'algoritmo di Harris

            img = cv.cvtColor(img, cv.COLOR_GRAY2BGR,dstCn=3) # conversione da bianco e nero a RGB

            img_harris=img.copy() #creazione di una copia dello scheletro su cui verrà disegnato l'output dell'algoritmo di Harris
            clustering_rgb=img.copy() #creazione di una copia dello scheletro su cui verrà disegnato il risultato del clustering

            img_harris[harris>0.02*harris.max()]=[0,0,255] # disegna i punti rossi, ottenuti con l'algoritmo di Harris, sullo scheletro
            cv.imwrite(nomefile+" harris.png", img_harris) # salvataggio su disco

            confronto = img_harris.copy() # creazione di una copia dello scheletro iniziale

            altezza, larghezza = img_harris.shape[:2] #dimensioni dell'immagine ottenuta con harris
            nero = np.zeros((altezza,larghezza,1)) #crea un'immagine completamente nera
            nero[harris>0.02*harris.max()]=[255] #disegna i punti di interesse trovati con harris su un'immagine nera

            p=5  # parametro che indica la distanza del punto in esame dal perimetro della sottoarea di lavoro 

            #############
            #     p     #
            #  p  O  p  #
            #     p     #
            #############
            
            # Clustering: si analizzano i punti ottenuti con l'algoritmo di Harris e gli agglomerati costituiti da punti molto vicini vengono sostituiti dal loro punto medio.
            # L'algoritmo definisce una sottoarea di lavoro, utilizzando il parametro p, ogniqualvolta che si incontra un punto bianco.
            # Vengono contati i pixel bianchi e ne vangono salvate le coordinate. Si procede poi a calcolare il punto medio se nell'area vi sono più punti bianchi.
            # Viene colorata di nero l'area sull'immagine di partenza (Harris) corrispondente alla area di lavoro corrente e viene disegnato il punto medio su un'immagine nera.
            clustering = np.zeros((altezza, larghezza, 1)).astype(np.int16)#uint16 # creazione di un'immagine nera usata per il salvataggio dei punti medi
            print("Clustering...")
            riga = 0 # il contatore di riga viene posto uguale al parametro per far sì che la sottoarea di lavoro non oltrepassi i bordi dell'immagine.
            while (riga < altezza-p): 
                colonna = p
                y = riga if (riga>=p) else p
                while (colonna < larghezza-p):
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
                            clustering[riga][colonna]=[255]    
                    colonna = colonna+1
                riga = riga+1
            print("Clustering completato.")
            # Disegno dei punti ottenuti dal clustering sullo scheletro di partenza e su un'immagine dello scheletro popolata con i punti trovati 
            # con'algoritmo di harris per il confronto fra Harris e il clustering effettuato.
            #Scorrimento dell'immagine in bianco e nero contenente i punti medi ottenuti dall'operazione di clustering
            print("Disegno i punti...")          
            row=0
            while (row < altezza):
                col=0
                while (col < larghezza):
                    if clustering[row,col] == 255: # quando si incontra un punto bianco, ovvero un punto medio      ==[255]
                        clustering_rgb[row,col]=[0,255,0]   # viene riportato, con il colore verde, sullo scheletro iniziale
                        confronto[row,col]=[0,255,0]        # e, sempre con il colore verde sull'immagine su cui sono presenti scheletro 
                                                            # e il risultato con l'algoritmo di Harris (punti in rosso)
                    col+=1  # incremento del contatore della colonna
                row+=1  # incremento del contatore della riga

             #Salvataggio su disco
            print("Salvataggio su disco...")
            cv.imwrite(nomefile+" clustering.png",clustering_rgb)
            cv.imwrite(nomefile+" harris_c.png",confronto)
            print(str('Analisi dello scheletro di '+nomefile+' completata.'))
            print('---------------------------------------------------------------')




            



