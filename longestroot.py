import numpy as np
import cv2 as cv
import glob
import os
import math
from matplotlib import pyplot as plt
from fil_finder import FilFinder2D
import astropy.units as u

path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
skeleton = cv.imread(r'f.jpg', 0) #lettura immagine
skeleton = skeleton[0:2000,0:int(skeleton.shape[1])]
print(type(skeleton))

fil = FilFinder2D(skeleton, distance=250 * u.pc, mask=skeleton)
fil.preprocess_image(flatten_percent=85)
print('pippo')
fil.create_mask(border_masking=True, verbose=False, use_existing_mask=True)
print('pippo3')
fil.medskel(verbose=False)
print('pippo4')
fil.analyze_skeletons(branch_thresh=40*u.pix, skel_thresh=10*u.pix, prune_criteria='length')

# Show the longest path
plt.imshow(fil.skeleton, cmap='gray')
plt.contour(fil.skeleton_longpath, colors='r')
plt.axis('off')
plt.show()