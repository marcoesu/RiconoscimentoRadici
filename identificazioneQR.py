import cv2 as cv
#import numpy as np
from pyzbar.pyzbar import decode #decodifica del QR     (pip install pyzbar)
import os # utilizzata per effettuare operazioni sulle cartelle
import glob
import shutil #permette di effettuare operazioni su file
import requests #pip install requests
import zipfile

def PresenzaCampioni(path,url):     # Funzione adibita al controllo della presenza del file contenente le immagini campione

    if(os.path.exists(str(path + r'/FotoCampione.zip'))):
        print("Campioni presenti.")
    else:
        try:
            print("Download dei campioni in corso...")
            FotoCampione = requests.get(url)                   
            with open('FotoCampione.zip', 'wb') as local_file: # Salvataggio su disco, nella cartella path, del file .zip
                local_file.write(FotoCampione.content)
            print("Campioni scaricati.")
        except:
            print("Impossibile scaricare i campioni.")         # Errore di download


def EstrazioneCampioni():   # Funzione che si occupa dell'estrazione delle immagini campione dal file .zip

    zip = "FotoCampione.zip"
    try:
        with zipfile.ZipFile(zip) as z:
            z.extractall()
            print("Immagini campione estratte.")
    except:
        print("File non valido.")


path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
url ='https://www.dropbox.com/s/2lourrj1s3wck3q/FotoCampione.zip?dl=1' # File .zip contenente le immagini campione, salvato su DropBox 

PresenzaCampioni(path,url) # Controllo della presenza del file FotoCampione.zip nel path

EstrazioneCampioni() # Estrazione dei campioni dal file FotoCampione.zip

data_path = os.path.join(path,'*.jpg') #lista di tutti gli elementi di estensione jpg nella cartella path
files = glob.glob(data_path) #converte data path in un output Unix-like (ls) (*.jpg -> lista di elementi con estensione jpg)

# Ogni soggetto è identificato dal QR, che viene decodificato ed utilizzato per rinominare le rispettive sottocartelle. 
for f1 in files: # ciclo che scorre le immagini nella cartella path
    image = cv.imread(f1)   #lettura dell'immagine
    altezza, larghezza, colori = image.shape #salva le dimensioni dell'immagine (espresse come una tupla) in dim. quindi altezza = dim[1], lunghezza = dim[2]
    zonaqr=image[(int(altezza/4)):(int(altezza/2)),int((larghezza/10)):int((larghezza/3.5))]    # sezione dell'immagine analizzata contenente il QR identificativo
    for qr in decode(zonaqr):   #ciclo for utilizzato per decodificare il QR di ogni immagine
        codid=qr.data.decode('utf-8')    #codice identificativo estratto dal QR
        #cv.imshow(str(codid),zonaqr)
        #cv.waitKey(0)
        if not os.path.exists(path+r'/'+codid):     # controlla che esista la sottocartella dedicata al soggetto in analisi
            os.makedirs(path+r'/'+codid)            #crea la cartella dedicata
            print(str('Cartella '+codid+' creata.'))
        shutil.move(f1,str(os.path.dirname(f1) + r'/' + codid + r'/' + os.path.basename(f1)))   #sposta il file jpg dalla cartella path alla sottocartella del rispettivo soggetto
print("Processo terminato.")        
