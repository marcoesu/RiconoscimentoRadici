import numpy as np
import cv2
import matplotlib.pyplot as plt
from fil_finder import FilFinder2D

skeleton = cv2.imread(r"C:\Users\esu7z\Desktop\RiconoscimentoRadici\a.png", 0) #in numpy array format

fil = FilFinder2D(skeleton, distance=250, mask=skeleton)
fil.preprocess_image(flatten_percent=85)
fil.create_mask(border_masking=True, verbose=False,
use_existing_mask=True)
fil.medskel(verbose=False)
fil.analyze_skeletons(branch_thresh=40, skel_thresh=10, prune_criteria='length')

# Show the longest path
plt.imshow(fil.skeleton, cmap='gray')
plt.contour(fil.skeleton_longpath, colors='r')
plt.axis('off')
plt.show()