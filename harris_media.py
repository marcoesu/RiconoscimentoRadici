import numpy as np
import cv2 as cv
import glob
import os
import matplotlib.pyplot as plt
import math
from numpy.core.fromnumeric import ravel
from numpy.core.numeric import count_nonzero
from numpy.lib.function_base import average
from sklearn.cluster import DBSCAN #pip install scikit-learn
file = open("prova.txt","w")

path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
img = cv.imread(r'prova_dbscan.jpg',0) #lettura immagine

#gray = np.float32(img) 
harris = cv.cornerHarris(img,2,3,0.04) #applicazione dell'algoritmo di harris

#result is dilated for marking the corners, not important
#harris = cv.dilate(harris,None) # ingrandisce il corner
#dst = dst.astype(np.uint8)

img = cv.cvtColor(img, cv.COLOR_GRAY2BGR) # conversione da bianco e nero a RGB

# Threshold for an optimal value, it may vary depending on the image.
img[harris>0.02*harris.max()]=[0,0,255] #disegna i cerchi rossi sullo scheletro

altezza, larghezza = harris.shape[:2] #dimensioni dell'immagine ottenuta con harris
nero = np.zeros((altezza,larghezza,1)) #crea un'immagine completamente nera
nero[harris>0.02*harris.max()]=[255] #disegna i punti di interesse trovati con harris su un'immagine nera

nero = nero.astype(np.uint8) #i punti riportati da harris sono in subpixel,
                            # andiamo quindi a convertire l'immagine in un array di interi
                            # approssimando la posizione dei punti ottenuti con l'algoritmo di harris
                            # in pixel
print('----------------------')

cv.imwrite('nero.png', nero)

raggio=5
#definizione zona
#grandezza=np.count
#x= np.ndarray(int(np))

riga = raggio

while (riga < altezza-raggio) : 
    colonna = raggio
    while (colonna < larghezza-raggio) :
        if(nero[riga][colonna] == 255):
            area = nero[int(riga - raggio):int(riga+raggio),int(colonna-raggio):int(colonna+raggio)]
            print(area.shape)
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
                print(media_y)
                print(media_x)
                area[0:9,0:9]=[0]
                print(area)
                area[(media_y),int(media_x)]=[255]
                nero[riga - raggio:riga+raggio,colonna-raggio:colonna+raggio]=area
            
        colonna = colonna+1
    riga = riga+1 

cv.imwrite("arturo.png",nero)

'''
print(nero)
file.write(str(nero))

grandezza = np.count_nonzero(nero) #cerchiamo il numero di pixel non neri nell'immagine nero

x= np.ndarray(int(grandezza*2)) #grandezza per due perchè salviamo le coordinate di ogni pixel (x,y)

#andiamo a popolare l'array x con le coordinate dei punti bianchi dell'immagine nero
riga = 0
contatore = 0

while (riga < altezza) : 
    colonna = 0
    while (colonna < larghezza) :
        if(nero[riga][colonna] == 255) :
            x[contatore] = riga
            x[contatore+1] = colonna
            contatore = contatore+2
        colonna = colonna+1
    riga = riga+1        

x = x.reshape(grandezza,2) #effettuiamo un reshape per accorpare le coordinate x e y in un singolo elemento dell'array (matrice mx2)

cv.imwrite('harris.jpg', img)

cv.imwrite('nero.png', nero)

db = DBSCAN(eps=20, min_samples=3).fit(x) #utilizziamo l'array x con dbscan per trovare i cluster di punti

labels = db.labels_ #array contenente le etichette(cluster di appartenenza) di ogni punto dell'array x

np.set_printoptions(threshold=labels.size)

cont = 0 


cv.imwrite('output.png', db.labels_)

dbscan = np.zeros((altezza, larghezza,3)) #crea un'immagine nera in RGB con le dimensioni di altezza e larghezza
contatore = 0
n_cluster = 0
grandezza_p_medi = (labels[labels.size-1]+1) #prendiamo il valore dell'ultimo cluster presente in labels e aggiungiamo un elemento in più
                                            #così da avere valori che vanno da zero a labels.size-1
#print('grandezza '+ str(grandezza_p_medi))

# conteggio elementi isolati
#controllo della presenza di punti isolati
n_elementi_isolati = 0
for l in labels:
    #n_elementi_cluster = 0
    if(l == -1): # se ci sono punti isolati (con labels == -1)
        n_elementi_isolati += 1 
print(n_elementi_isolati)

p_medi = np.ndarray((grandezza_p_medi+n_elementi_isolati)*2) #creazione dell'array p_medi di dimensione pari al numero delle label
                                                            # che vanno da zero al numero massimo di label presenti + numero di punti isolati
print('-------------------')
print(p_medi.size)
print('-------------------')
puntatore = 0

#print('grandezza_p_medi'+str(grandezza_p_medi))

#ciclo che scorre labels per cercare gli elementi appartenenenti allo stesso cluster (appartenenti alle stesse labels), 
#trovare il punto medio e salvare le sue coordinate in un array (p_medi)
#manca il caso del -1
while (contatore < labels.size) and n_cluster < grandezza_p_medi:     #while (contatore < grandezza):
    n_elementi_cluster = 0

   #ciclo che conta il numero di elementi per ogni cluster
    for l in labels:
        #n_elementi_cluster = 0
        if(l == n_cluster): 
            n_elementi_cluster += 1        
    #print('n_elementi_cluster '+str(n_elementi_cluster) + ' nel cluster ' + str(n_cluster)) 

    copia_corners = 0

    media_punti = np.ndarray(n_elementi_cluster*2).reshape(n_elementi_cluster,2)     #array in cui andiamo a salvare le coordinate dei punti appartenenti al cluster esaminato
                                                                                    #il reshape viene effettuato affinchè sia possibile effettuare le operazioni di assegnamento
                                                                                    #sugli elementi di media_punti dei valori dei punti di x

    #assegnazione delle coordinate dei punti da x a media_punti
    while(copia_corners < (n_elementi_cluster)):

        media_punti[copia_corners] = x[int(puntatore+copia_corners)]
        
        copia_corners +=1

    #definizione degli array che conterranno le coordinate x e y dei punti appartenenti al cluster analizzato
    media_punti_x = np.ndarray(n_elementi_cluster)
    media_punti_y = np.ndarray(n_elementi_cluster)
    media_punti = media_punti.ravel() #trasformazione di media_punti da matrice mx2 a un array 

    #il ciclo divide l'array media_punti in due array contenenti uno solo le ascisse e uno solo le ordinate dei punti
    c=0
    c_xy=0

    while c<n_elementi_cluster:
        media_punti_y[c_xy] = media_punti[c]
        media_punti_x[c_xy] = media_punti[c+1]
        c=c+2
        c_xy=c_xy+1

    #variabili contententi rispettivamente la media delle ascisse e delle ordinate dei punti (convertiti in int)    
    media_x=(np.average(media_punti_x))#.astype(np.uint8)
    media_y=(np.average(media_punti_y))#.astype(np.uint8)


    media_x=(sum(media_punti_x)/n_elementi_cluster).astype(np.uint32)
    media_y=(sum(media_punti_y)/n_elementi_cluster).astype(np.uint32)

    print('media_x_intera '+ str(media_x))
    print('media_y_intera '+ str(media_y))

    print('---------------')

    #salvataggio coordinate in p_medi
    p_medi[n_cluster*2]=media_y
    p_medi[n_cluster*2+1]=media_x

    n_cluster += 1
    contatore += 1
    puntatore = contatore


#ciclo che viene utilizzato per colorare di verde i punti medi trovati
c = 0
nero=cv.cvtColor(nero,cv.COLOR_GRAY2RGB,dstCn=3)

while(c < p_medi.size):
    nero[int(p_medi[c])][int(p_medi[c+1])]= [0,255,0]
    c = c+2

cv.imwrite('dbscan.png',nero)   

#print(img.shape)
print(nero.shape)
#print(harris.shape)
print(dbscan.shape)'''
