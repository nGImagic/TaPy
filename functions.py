#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:10:52 2017

@author: harti and valsecchi
"""

import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import gridspec

# Function to read the data and return it as 3D arrays
def read_data(path_im,path_ob,path_dc):
    
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
    
    # Load Projectionss
    filenames_im = os.listdir(path_im)  # Create list of filenames in projection folder
    filenames_im.sort()                 # Sort the lsit (just in case)
    num_im_im = len(filenames_im)      # Get number of projections
    
    stack_im = list()                   # Generate empty list for projections 
    
    for i in filenames_im:              # Iterate through filenames in projection folder
        f_name = path_im + '/' + i
        im = Image.open(f_name)         # Open image
        im_a = np.array(im-im_a1)             # Convert image to array
        stack_im.append(im_a)           # Append array to list
    
    stack_im_ar = np.asarray(stack_im)  # Convert list to numpy array
    
    # Load Open Beams
    filenames_ob = os.listdir(path_ob)
    filenames_ob.sort()
    num_im_ob = len(filenames_ob)
    
    if num_im_im != num_im_ob:
        print('!!!WARNING!!! NUMBERS OF PROJECTIONS AND OPEN BEAMS ARE NOT THE SAME')
    
    stack_ob = list()
    
    for i in filenames_ob:
        f_name = path_ob + '/' + i
        im = Image.open(f_name)
        im_a = np.array(im-im_a1)
        stack_ob.append(im_a)
    
    stack_ob_ar = np.asarray(stack_ob)            
        
    return(stack_im_ar,stack_ob_ar)

    
def roi(im,xROI,yROI,thickROI,heightROI,show=False):
    """
    roi() takes a SINGLE image and crops it 
    (xROI,yROI) is the upper left-hand corner of the cropping rectangle 
    """
    if  (0<=xROI<=im.shape[0] and 0<=xROI+thickROI<=im.shape[0] and 0<=yROI<=im.shape[1] and 0<=yROI+heightROI<=im.shape[1]):
        imROI = im[yROI:yROI+heightROI,xROI:xROI+thickROI]
        if show:
            vmin,vmax=im.min(),im.max()
            cmap='gray'
            fig = plt.figure(figsize=(15,10)) 
            gs = gridspec.GridSpec(1, 2,width_ratios=[4,1],height_ratios=[1,1]) 
            ax = plt.subplot(gs[0])
            ax2 = plt.subplot(gs[1])
#            fig,(ax,ax2) = plt.subplots(1,2,sharex=False,sharey=False,figsize=(15,10))
            ax.imshow(im,vmin=vmin, vmax=vmax,interpolation='nearest',cmap=cmap)
            rectNorm = patches.Rectangle((xROI,yROI),thickROI,heightROI,linewidth=1,edgecolor='m',facecolor='none')
            ax.add_patch(rectNorm)
            ax.set_title('Original image with selected ROI & cropped region')
            ax2.imshow(im,vmin=vmin, vmax=vmax,interpolation='nearest',cmap=cmap)
            ax2.set_title('ROI')
            ax2.set_xlim([xROI,xROI+thickROI])
            ax2.set_ylim([yROI+heightROI,yROI])
            plt.tight_layout()
            plt.show()
            plt.close('all')
        return(imROI)
    else:
        print('!!!WARNING!!! \nROI out of range')