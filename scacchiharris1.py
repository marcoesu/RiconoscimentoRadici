import numpy as np
import cv2 as cv
import glob
import os
import matplotlib.pyplot as plt
import math
from numpy.core.fromnumeric import ravel
from numpy.lib.function_base import average
from sklearn.cluster import DBSCAN #pip install scikit-learn
path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
img = cv.imread(r'prova_dbscan.jpg',0) #lettura immagine

gray = np.float32(img)
dst = cv.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv.dilate(dst,None) # ingrandisce il corner
#dst = dst.astype(np.uint8)

img = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.02*dst.max()]=[0,0,255]

altezza, larghezza = dst.shape[:2]
nero = np.zeros((altezza,larghezza,1))
nero[dst>0.02*dst.max()]=[255]
#bianco = nero.astype(np.uint8)
nero = nero.astype(np.uint8)

grandezza = np.count_nonzero(nero)

x= np.ndarray(int(grandezza*2)) #grandezza per due perchè salviamo le coordinate di ogni pixel (x,y)

riga = 0
contatore = 0

while (riga < altezza) :
    colonna = 0
    while (colonna < larghezza) :
        if(nero[riga][colonna] == 255) :
            x[contatore] = colonna
            x[contatore+1] = riga
            contatore = contatore+2
        colonna = colonna+1
    riga = riga+1        

x = x.reshape(grandezza,2)
print(x)

print('------------------')

cv.imwrite('exit_float.jpg', img)

cv.imwrite('nero.png', nero)

db = DBSCAN(eps=5, min_samples=100).fit(x)

labels = db.labels_
labels
print(db.labels_)
np.set_printoptions(threshold=labels.size)
file = open("prova.txt","w")
file.write(str(db.labels_))
cont = 0


for l in labels:    
    if (l != -1):
        if (l == cont) : #scorrimento
            file.write('ciao')
        elif(l != cont) :
            file.write(str(l))
            file.write('#######')
            cont += 1
            file.write(str(cont))
            file.write('-------')   
print(cont)    

'''
cv.imwrite('output.png', db.labels_)

dbscan = np.zeros((altezza, larghezza,3))
#dbscan = cv.cvtColor(dbscan,cv.COLOR_GRAY2BGR)
contatore = 0
n_cluster = 0
grandezza_p_medi = (db.labels_[grandezza-1]+1) #ultimo cluster presente in db 
print('grandezza '+ str(grandezza_p_medi))
p_medi = np.ndarray(grandezza_p_medi*2)
puntatore = 0



while (contatore < grandezza and n_cluster < grandezza_p_medi):
    n_elementi_cluster = 0
    #while (n_cluster <= grandezza_p_medi): #contare quanti elementi ci sono nel cluster
    while(db.labels_[contatore] == n_cluster):
        n_elementi_cluster += 1
        contatore += 1      
    #elif((db.labels_[contatore] == (n_cluster+1)) or db.labels_[contatore] == -1):
    #print(str(n_elementi_cluster) + ' elementi nel cluster' + str(n_cluster))
    copia_corners = 0
    #media_punti = np.ndarray(n_elementi_cluster*2).reshape(n_elementi_cluster,2)
    media_punti = np.ndarray(n_elementi_cluster*2).reshape(n_elementi_cluster,2)
    #print('------------')
    #print(media_punti.shape)
    #print(x.shape)
    #print('-------------')
    #print(n_elementi_cluster)
    while(copia_corners < (n_elementi_cluster)):
        #print('ciao')
        media_punti[copia_corners] = x[int(puntatore+copia_corners)]
<<<<<<< HEAD
        print(x[int(puntatore+copia_corners)])
        print('media punti' + str(media_punti))
        
=======
        #print(x[int(puntatore+copia_corners)])
        #print('media punti' + str(media_punti))
        '''
>>>>>>> 5ced20c05ef0347f7f625e7aaf751c4dd5a24cb5
        p_medi[n_cluster] = average(media_punti)
        print(p_medi[n_cluster])
        copia_corners +=1
    
    media_punti_x = np.ndarray(n_elementi_cluster)
    media_punti_y = np.ndarray(n_elementi_cluster)
    media_punti = media_punti.ravel()
    c=0
    c_xy=0
    dim_media_punti = n_elementi_cluster
    while c<n_elementi_cluster:
        media_punti_x[c_xy] = media_punti[c]
        c=c+1
        media_punti_y[c_xy] = media_punti[c]
        c=c+1
        c_xy=c_xy+1
    media_x=(average(media_punti_x)).astype(np.uint8)
    media_y=(average(media_punti_y)).astype(np.uint8)
#   tmp=np.ndarray([[media_x][media_y]]).reshape(2,2) #errore
    print(p_medi.shape)
    print("Siamo al cluster "+str(n_cluster))
    print('grandezza_p_medi'+str(grandezza_p_medi))
    print('grandezza '+ str(db.labels_[grandezza-1]))
    print(db.labels_)
    p_medi[n_cluster*2-1]=media_y #=[int(average(media_punti_x))int(average(media_punti_x))]
    p_medi[n_cluster*2]=media_x

    n_cluster += 1
    contatore += 1
    puntatore = contatore



c = 0

while(c < p_medi.size):
    dbscan[int(p_medi[c+1])][int(p_medi[c])] = [0,255,0]
    c = c+2

cv.imwrite('dbscan.png',dbscan)

#p_medi[n_cluster]

    

p_medi = p_medi.astype(np.uint8)
print(p_medi)



riga = 0
contatore = 0

while (riga < altezza) :
    colonna = 0
    while (colonna < larghezza) :
        if(nero[riga][colonna] == 255) :
            x[contatore] = colonna
            x[contatore+1] = riga
            contatore = contatore+2
        colonna = colonna+1
    riga = riga+1
'''
#cv.imwrite('bianco.png', bianco)