import numpy as np
import cv2 as cv
import glob
import os
import sys
sys.setrecursionlimit(10000)


def Colorazione(y,x):
    #risultato[y-1:(y+2),x-1:(x+2)]=[255,0,255]
    row_area=y-1
    print(row_area)
    while (row_area<y+2):
        col_area = x-1
        print(col_area)
        while (col_area<x+2):
            if (img[row_area,col_area,B] == 255): # quando si incontra un punto bianco, ovvero un punto medio      ==[255]
                img[row_area,col_area,B]=127   # viene riportato, con il colore verde, sullo scheletro iniziale
                risultato[row_area,col_area]=[255,255,255]
                cv.imshow("a",risultato)
                cv.waitKey(1)
                #print("riga colonna :" + '['+str(row_area) +" "+ str(col_area)+']'+str(img[row_area,col_area]))
                #print("Passo a Colorazione: "+ str(row_area) +" "+ str(col_area))
                flag = Colorazione(row_area,col_area)
                print(flag)
               # e, sempre con il colore verde sull'immagine su cui sono presenti scheletro                                                    
            col_area+=1
        row_area+=1
    return True
    #print("ciao")
    




path = os.path.abspath(os.path.dirname(__file__)) #salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  #cambio della cartella attuale nella cartella in cui si trova il file .py

B = 0
G = 1
R = 2

img = cv.imread(r'f.png')#.astype(np.uint16)
altezza, larghezza = img.shape[:2]
#n_nodi = count_nonzero(img)
#nodi = []
risultato = np.zeros((altezza, larghezza,3))#.astype(np.uint16)
row=0
#print(altezza)
#print(larghezza)
while (row < altezza):
    col=0
    while (col < larghezza):
        #print("riga colonna :" + '['+str(row) +" "+ str(col)+']'+str(img[row,col]))
        if img[row,col,G] == 255 and img[row,col,R]==0: # quando si incontra un punto bianco, ovvero un punto medio
            print("punto verde")
            risultato[row,col]=[0,255,0]
            Colorazione((1 if row==0 else (row)),(1 if col==0 else (col)))
            '''
            #cv.imwrite("aoooo.png",risultato)
            coord_y = 0 if row==0 else (row-1)
            coord_x = 0 if col==0 else (col-1)
            #area = img[coord_y:(coord_y+2),coord_x:(coord_x+2)]
            row_area=coord_y
            while (row_area<=coord_y+2):
                col_area = coord_x
                while (col_area<=coord_x+2):
                    if (img[row_area,col_area,B] >= 250): # quando si incontra un punto bianco, ovvero un punto medio      ==[255]
                        print("ciao")
                        img[row_area,col_area]=[127,255,255]   # viene riportato, con il colore verde, sullo scheletro iniziale
                        risultato[row_area,col_area]=[255,255,255]
                        Colorazione(row_area,col_area)
                        #cv.imshow("a",risultato)
                        #cv.waitKey()        # e, sempre con il colore verde sull'immagine su cui sono presenti scheletro                                                    
                    col_area+=1
                row_area+=1
                '''



        col+=1  # incremento del contatore della colonna
    row+=1  # incremento del contatore della riga
#print(nodi)
cv.destroyAllWindows()
cv.imwrite("aoooo.png",risultato)
cv.imwrite("ciaooo.png",img)