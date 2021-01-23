import numpy as np

def hist(im):
   counts, bins = np.histogram(im)
   return counts
   
