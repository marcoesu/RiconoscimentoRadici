import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode #decodifica del QR
import os # utilizzata per effettuare operazioni sulle cartelle
import glob
import shutil #permette di effettuare operazioni su file
import exiftool
import json
from PIL import Image
import exifread

path = os.path.abspath(os.path.dirname(__file__)) #salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  #cambio della cartella attuale nella cartella in cui si trova il file .py

scansione = os.scandir() #scansione dei file all'interno della cartella path
for sottocartella in scansione: #ciclo per scansionare le sottocartelle di path 
    if sottocartella.is_dir():  #controllo se il file in esame è una cartella
        subpath = str(path + r'/'+ sottocartella.name)
        os.chdir(subpath)   # passaggio alla sottocartella in esame
        scansubdir = os.scandir()
        data_path = os.path.join(subpath,'*[0-9].jpg')   # I file prodotti dall'esecuzione sono file png, a differenza dei campioni che sono immagini jpg.
                                                    # In questo modo, se il programma viene eseguito più volte, i file salvati su disco da un precedente avvio del programma
                                                    # non vengono utilizzati come input dal programma.                                                    
        files = glob.glob(data_path) #converte data path in un output Unix-like (ls | grep jpg) (*[0-9].jpg -> lista di elementi con estensione jpg che hanno una cifra come ultimo carattere del nome)
        for f1 in files:    #Ciclo per scorrere tutte le immagini delle sottocartelle 
            nomefile = os.path.basename(f1)    #nome dell'immagine in esame, utilizzato poi per rinominare il risultato delle operazioni
            image = cv.imread(f1)   #lettura dell'immagine dal disco
            with open(nomefile, 'rb') as fh:
                tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
                dateTaken = tags["EXIF DateTimeOriginal"]
                print(dateTaken)
            '''
            im = Image.open(nomefile)
            im.load
            print(im.info['meta_to_read'])
            
            tags = ["File Name", "CreateDate"]
            log_file = f1
            with exiftool.ExifTool() as et:
                metadata = et.get_tags_batch(tags,nomefile)
            f = open(log_file, "w")
            f.write(str(metadata))
            f.close()    
            with open(log_file, 'w') as fd:
                json.dump(metadata, log_file)
            with open(log_file, 'r') as fd:
                metadata = json.load(fd)    
            for imageinfo in metadata:
                print('CreateDate:', imageinfo.get('EXIF:CreateDate', 'unknown'))'''