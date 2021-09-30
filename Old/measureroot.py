import numpy as np
import cv2 as cv
import glob
import os
import math
from matplotlib import pyplot as plt
from fil_finder import FilFinder2D #pip install fil_finder
import astropy.units as u
import pandas as pd #pip install pandas
from IPython.display import display #pip install IPython

path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
skeleton = cv.imread(r'f.jpg', 0) #lettura immagine
print(type(skeleton))

fil = FilFinder2D(skeleton, distance=250 * u.pc, mask=skeleton)
fil.preprocess_image(flatten_percent=85)
print('pippo')
fil.create_mask(border_masking=True, verbose=False, use_existing_mask=True)
print('pippo3')
fil.medskel(verbose=False)
print('pippo4')
fil.analyze_skeletons(branch_thresh=40*u.pix, skel_thresh=10*u.pix, prune_criteria='length')
plt.imshow(fil.skeleton, cmap='gray')

# this also works for multiple filaments/skeletons in the image: here only one
for idx, filament in enumerate(fil.filaments): 

    data = filament.branch_properties.copy()
    data_df = pd.DataFrame(data)
    data_df['offset_pixels'] = data_df['pixels'].apply(lambda x: x+filament.pixel_extents[0])

    print(f"Filament: {idx}")
    display(data_df.head())

    longest_branch_idx = data_df.length.idxmax()
    longest_branch_pix = data_df.offset_pixels.iloc[longest_branch_idx]

    y,x = longest_branch_pix[:,0],longest_branch_pix[:,1]

    plt.scatter(x,y , color='r')

plt.axis('off')
plt.show()