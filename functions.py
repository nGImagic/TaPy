#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:10:52 2017

@author: harti and valsecchi

????
kgutdhfjf
"""

import os
from PIL import Image
import numpy as np


# Function to read the data and return it as 3D arrays
def read_data(path_im,path_ob,path_dc):
    
    # Load Projectionss
    filenames_im = os.listdir(path_im)  # Create list of filenames in projection folder
    filenames_im.sort()                 # Sort the lsit (just in case)
    num_im_im = len(filenames_im)      # Get number of projections
    
    stack_im = list()                   # Generate empty list for projections 
    
    for i in filenames_im:              # Iterate through filenames in projection folder
        f_name = path_im + '/' + i
        im = Image.open(f_name)         # Open image
        im_a = np.array(im)             # Convert image to array
        stack_im.append(im_a)           # Append array to list
    
    stack_im_ar = np.asarray(stack_im)  # Convert list to numpy array
    
    # Load Open Beams
    filenames_ob = os.listdir(path_ob)
    filenames_ob.sort()
    num_im_ob = len(filenames_ob)
    
    stack_ob = list()
    
    for i in filenames_ob:
        f_name = path_ob + '/' + i
        im = Image.open(f_name)
        im_a = np.array(im)
        stack_ob.append(im_a)
    
    stack_ob_ar = np.asarray(stack_ob)    
    
    
    # Load DCs and average them
    filenames_dc = os.listdir(path_dc)
    filenames_dc.sort()
    num_im_DC = len(filenames_dc)
    
    f_name = path_dc + '/' + filenames_dc[0]    # Load first DC in folder
    im = Image.open(f_name)
    im_a1 = np.array(im)
    
    for i in filenames_dc:              # Iterate through filenames in DC folder
        f_name = path_dc + '/' + i
        im = Image.open(f_name)
        im_a = np.array(im)
        im_a1 = (im_a1 + im_a)/2        # Add to previous DC and divide by 2 - average
    
    if num_im_im != num_im_ob:
        print('!!!WARNING!!! NUMBERS OF PROJECTIONS AND OPEN BEAMS ARE NOT THE SAME')
        
    return(stack_im_ar,stack_ob_ar,im_a1)
