import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN #pip install scikit-learn
import os

path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
img = cv2.imread(r'exit.jpg') #lettura immagine

labimg = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

n = 0
while(n<8):
    labimg = cv2.pyrDown(labimg)
    n = n+1

feature_image=np.reshape(labimg, [-1, 3])
rows, cols, chs = labimg.shape

db = DBSCAN(eps=5, min_samples=50, metric = 'euclidean',algorithm ='auto')
db.fit(feature_image)
labels = db.labels_

indices = np.dstack(np.indices(labimg.shape[:2]))
xycolors = np.concatenate((labimg, indices), axis=-1) 
feature_image2 = np.reshape(xycolors, [-1,5])
db.fit(feature_image2)
labels2 = db.labels_

plt.imshow(img)
plt.axis('off')
plt.show()

# plt.subplot(2, 1, 2)
# plt.imshow(np.reshape(labels, [rows, cols]))
# plt.axis('off')
'''
Z = np.float32(img.reshape((-1,3)))
db = DBSCAN(eps=0.3, min_samples=100).fit(Z[:,:2])

plt.imshow(np.uint8(db.labels_.reshape(img.shape[:2])))
plt.show()'''