import numpy as np
import cv2 as cv
import glob
import os
from numpy.core.numeric import count_nonzero
def PippoBaudo(y,x):
    #print("ciao")
    coord_y = 0 if y==0 else (y-1)
    coord_x = 0 if x==0 else (x-1)
    #area = img[coord_y:(coord_y+2),coord_x:(coord_x+2)]
    row_area=coord_y
    while (row<coord_y+2):
        col_area = coord_x
        while (col_area<coord_x+2):
            cv.imshow("a",risultato)
            cv.waitKey(10)
            #if (img[row,col,B]==[255]):
            #    img[row,col,B]=0
            risultato[row_area,col_area]=255
            cv.imwrite("aoooo.png",risultato)
            #    PippoBaudo(row,col)
            col_area+=1
        row_area+=1

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













path = os.path.abspath(os.path.dirname(__file__)) #salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  #cambio della cartella attuale nella cartella in cui si trova il file .py

B = 0
G = 1
R = 2

img = cv.imread('a.png')
altezza, larghezza = img.shape[:2]
#n_nodi = count_nonzero(img)
#nodi = []
risultato = np.zeros((altezza, larghezza,1)).astype(np.uint16)
row=0
while (row < altezza):
    col=0
    while (col < larghezza):
        if img[row,col,G] == 255 and img[row,col,R]==0: # quando si incontra un punto bianco, ovvero un punto medio
            #nodi.append((row,col))
            #coord = 
            risultato[row][col]=255
            cv.imshow("a",risultato)
            cv.waitKey(10)
            PippoBaudo(row,col)
        col+=1  # incremento del contatore della colonna
    row+=1  # incremento del contatore della riga
#print(nodi)
cv.destroyAllWindows()
cv.imwrite("aoooo.png",risultato)