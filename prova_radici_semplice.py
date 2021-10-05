import numpy as np
import cv2 as cv
import glob
import os
import sys
import math
sys.setrecursionlimit(30000)

def angle_between(p1_y, p1_x, p2_y, p2_x):
    ang1 = np.arctan2(p2_y - p1_y, p2_x - p1_x)
    #return ang1
    return ang1*180/math.pi


def Colorazione(y,x):
    #risultato[y-1:(y+2),x-1:(x+2)]=[255,0,255]
    flag=False
    row_area=y-1
    while (row_area<y+2):
        col_area = x-1
        while (col_area<x+2):
            if (img[row_area,col_area,B] == 255): # quando si incontra un punto bianco, ovvero un punto medio      ==[255]
                flag=True
                img[row_area,col_area,B]=1   # viene riportato, con il colore verde, sullo scheletro iniziale
                risultato[row_area,col_area]=[255,255,255]                
                cv.imshow("a",risultato)
                cv.waitKey()
                #print("riga colonna :" + '['+str(row_area) +" "+ str(col_area)+']'+str(img[row_area,col_area]))
                #print("Passo a Colorazione: "+ str(row_area) +" "+ str(col_area))
                Colorazione(row_area,col_area) 
            col_area+=1
        row_area+=1

    fine_radice_y = y
    fine_radice_x = x

    '''    if (fine_radice_y==inizio_radice_y and fine_radice_x==inizio_radice_x):
        return'''
    '''
    green_found=False

    if (flag==False):
        row_green=y-1
        while (row_area<y+2):
            col_green = x-1
            while (col_area<x+2):
                if (img[row_green,col_green,B] == 0 and img[row_green,col_green,G] == 255 and row_green!=inizio_radice_y and col_green!=inizio_radice_x):
                    print("Punto verde trovato.")
                    fine_radice_y=row_green
                    fine_radice_x=col_green
                    green_found=True
                    data.append([inizio_radice_y,inizio_radice_x,fine_radice_y,fine_radice_x])
                col_green+=1
        row_green+=1'''

    angolo = angle_between(fine_radice_y,fine_radice_x,inizio_radice_y,inizio_radice_x)
    '''
    if (flag==False):
        if(green_found==False):
            #fine_radice_y=y
            #fine_radice_x=x
            risultato[fine_radice_y,fine_radice_x]=[255,0,255]
            #cv.imshow("a",risultato)
            #cv.waitKey()
            #cv.destroyAllWindows()
            data.append([inizio_radice_y,inizio_radice_x,fine_radice_y,fine_radice_x,angolo])
        elif(green_found==True): 
            data.append([inizio_radice_y,inizio_radice_x,fine_radice_y,fine_radice_x,angolo])
    #print("ciao")'''
    
    if (flag==False):
        data.append([inizio_radice_y,inizio_radice_x,fine_radice_y,fine_radice_x,angolo])



path = os.path.abspath(os.path.dirname(__file__)) #salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  #cambio della cartella attuale nella cartella in cui si trova il file .py

B = 0
G = 1
R = 2

img = cv.imread(r'b.png')
altezza, larghezza = img.shape[:2]

risultato = np.zeros((altezza, larghezza,3))


# Dati delle estremità della radice analizzata
inizio_radice_y = 0
inizio_radice_x = 0

data = []
#flag=False

row=0
while (row < altezza):
    col=0
    while (col < larghezza):
        if img[row,col,G] == 255 and img[row,col,R]==0: # quando si incontra un punto bianco, ovvero un punto medio
            print("Punto verde.")
            risultato[row,col]=[0,255,0]
            inizio_radice_y = row
            inizio_radice_x = col
            Colorazione((1 if row==0 else (row)),(1 if col==0 else (col)))
        col+=1  # incremento del contatore della colonna
    row+=1  # incremento del contatore della riga
print(data)


#cv.destroyAllWindows()
cv.imwrite("risultato.png",risultato)
cv.imwrite("scorrimento.png",img)