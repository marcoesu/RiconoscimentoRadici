import cv2 as cv
#import numpy as np
from pyzbar.pyzbar import decode #decodifica del QR     (pip install pyzbar)
import os # utilizzata per effettuare operazioni sulle cartelle
import glob
import shutil #permette di effettuare operazioni su file
import requests #pip install requests
import zipfile
import exifread

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

def Archiviazione(path,file,immagine,codice): # Spostamento file campione nella sottocartella dedicata
    if not os.path.exists(path+r'/'+codice):  # controlla che esista la sottocartella dedicata al soggetto in analisi
            os.makedirs(path+r'/'+codice)     # crea la cartella dedicata
            print(str('Cartella '+codice +' creata.'))
    nomefile = os.path.basename(file)    #nome dell'immagine in esame, utilizzato poi per rinominare il risultato delle operazioni
    with open(nomefile, 'rb') as fh: #apre il file e lo restituisce come oggetto
        tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal") #viene preso solamente il tag contenente la data e l'ora dello scatto originale
        DataScatto = str(tags['EXIF DateTimeOriginal']) #viene assegnato il valore alla variabile
        anno, mese, giornoora, minuti, secondi = DataScatto.split(":", 5) #viene suddivisa l'informazione in più campi, separati da :
        giorno, ora = giornoora.split(" ",1) #scomposizione giorno e ora tramite uno spazio
        fh.close() #chiude il file aperto
    shutil.move(file,str(path + r'/' + codice + r'/' + codice +' '+anno+'-'+mese+'-'+giorno+' '+ora+'-'+minuti+'-'+secondi+'.jpg')) 
    #sposta il file jpg dalla cartella path alla sottocartella del rispettivo soggetto, rinominandolo utilizzando il codice del soggetto estratto dal QR, la data e l'ora

path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
url ='https://www.dropbox.com/s/opu3e8kpoujio1t/FotoCampione.zip?dl=1' # File .zip contenente le immagini campione, salvato su DropBox 

PresenzaCampioni(path,url) # Controllo della presenza del file FotoCampione.zip nel path

EstrazioneCampioni() # Estrazione dei campioni dal file FotoCampione.zip

data_path = os.path.join(path,'*[0-9].jpg') #lista di tutti gli elementi di estensione jpg nella cartella path
files = glob.glob(data_path) #converte data path in un output Unix-like (ls) (*.jpg -> lista di elementi con estensione jpg)

# Ogni soggetto è identificato dal QR, che viene decodificato ed utilizzato per rinominare le rispettive sottocartelle. 
for f1 in files: # ciclo che scorre le immagini nella cartella path
    
    image = cv.imread(f1)   #lettura dell'immagine
    altezza, larghezza = image.shape[:2] #salva le dimensioni dell'immagine (espresse come una tupla) in dim. quindi altezza = dim[1], lunghezza = dim[2]
    zonaqrsx=image[(int(altezza/6)):(int(altezza*0.3)),int((larghezza/10)):int((larghezza/5))]    # sezione dell'immagine analizzata contenente il QR identificativo
    zonaqrdx=image[(int(altezza*0.15)):(int(altezza*0.3)),int((larghezza*0.8)):int((larghezza*0.9))]
    for qrsx in decode(zonaqrsx):  # ciclo for utilizzato per decodificare il QR di ogni immagine
        codid=qrsx.data.decode('utf-8')    # codice identificativo estratto dal QR
        Archiviazione(path,f1,image,codid) # Spostamento file campione nella sottocartella dedicata
        print("Decodifica riuscita: QR a sinistra per "+ str(os.path.basename(f1)))
    if os.path.exists(f1):
        for qrdx in decode(zonaqrdx):   # ciclo for utilizzato per decodificare il QR di ogni immagine
            codid=qrdx.data.decode('utf-8')    # codice identificativo estratto dal QR
            Archiviazione(path,f1,image,codid) # Spostamento file campione nella sottocartella dedicata
            print("Decodifica riuscita: QR a destra per "+ str(os.path.basename(f1)))
    if os.path.exists(f1):
       cv.imwrite(str(os.path.basename(f1)+'qrsx.jpg'), zonaqrsx) # Salvataggio su disco del QR sinistro non riconosciuto
       cv.imwrite(str(os.path.basename(f1)+'qrdx.jpg'), zonaqrdx) # # Salvataggio su disco del QR destro non riconosciuto
print("Processo terminato.")      