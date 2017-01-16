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
import pyfits
from os import listdir,rename, makedirs
from os.path import isfile, join, exists, isdir
# Function to read the data and return it as 3D arrays
def read_data(path_im,path_ob,path_dc):
    """
    read()
    """
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
    
    stack_ob = list()
    
    for i in filenames_ob:
        f_name = path_ob + '/' + i
        im = Image.open(f_name)
        im_a = np.array(im-im_a1)
        stack_ob.append(im_a)
    
    stack_ob_ar = np.asarray(stack_ob)            
    if  stack_im_ar.shape != stack_ob_ar.shape:
        print('!!!WARNING!!! SHAPE OF PROJECTIONS AND OPEN BEAMS ARE NOT THE SAME')
    return(stack_im_ar,stack_ob_ar)

xROI,yROI,thickROI,heightROI=10,10,35,35 #parameter for roi
   
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


def cropped(stack_im,stack_ob,xROI=xROI,yROI=yROI,thickROI=thickROI,heightROI=heightROI):
    """
    cropped() takes a stack of data,ob and dark currenr and crops them 
    (xROI,yROI) is the upper left-hand corner of the cropping rectangle 
    """
    stack_im_ar = [roi(im=stack_im[0],xROI=xROI,yROI=yROI,thickROI=thickROI,heightROI=heightROI,show=True)]
    for i in stack_im[1:]:
        stack_im_ar.append(roi(im=i,xROI=xROI,yROI=yROI,thickROI=thickROI,heightROI=heightROI,show=False))
#    stack_im_ar = [roi(im=i,xROI=xROI,yROI=yROI,thickROI=thickROI,heightROI=heightROI,show=True) for i in stack_im]
    
    stack_ob_ar = [roi(im=i,xROI=xROI,yROI=yROI,thickROI=thickROI,heightROI=heightROI,show=False) for i in stack_ob]
    
    
    return(np.asarray(stack_im_ar),np.asarray(stack_ob_ar))

    
def normalization(stack_im,stack_ob,xROI=xROI,yROI=yROI,thickROI=thickROI,heightROI=heightROI,show=False):
    """
    normalization()
    """
    Area = abs(thickROI*heightROI)  
    
    stack_im_ar = []    

    stack_im_ar = [l/(l[yROI:yROI+heightROI+1,xROI:xROI+thickROI+1].sum()/Area) for l in stack_im]   
    for i in stack_im_ar:
        print(i.mean())
        
    stack_ob_ar = [l/(l[yROI:yROI+heightROI+1,xROI:xROI+thickROI+1].sum()/Area) for l in stack_ob] 
        
    return(np.asarray(stack_im_ar),np.asarray(stack_ob_ar))

def matrix(stack_im):
    """
    """
    shapeStack = np.shape(stack_im)
    B = np.zeros((shapeStack[0],3))  
    numberPeriods = 1
    ###TODO: function for number of periods
    
    stack_imReshaped = np.reshape(stack_im,[shapeStack[0],shapeStack[1]*shapeStack[2]])
    rangeStack = range(shapeStack[0])
    
    for j in rangeStack:
        B[j][0] = 1.0
        B[j][1] = np.cos(2*np.pi*rangeStack[j]*numberPeriods/(shapeStack[0]-1))
        B[j][2] = np.sin(2*np.pi*rangeStack[j]*numberPeriods/(shapeStack[0]-1))
    B = np.matrix(B)
    
    G = (B.T * B).I * B.T
    print(np.shape(G),np.shape(stack_imReshaped))
    A = (G*stack_imReshaped)
    offSet,absoluteAmpl,absPhase = A[0,:],A[1,:],A[2,:]
    a0 = np.reshape(np.asarray(offSet),[shapeStack[1],shapeStack[2]])
    a1 = np.reshape(np.sqrt(np.asarray(absoluteAmpl)**2+np.asarray(absPhase)**2),[shapeStack[1],shapeStack[2]])
    phi = np.reshape(np.arctan((np.asarray(absPhase)/np.asarray(absoluteAmpl))),[shapeStack[1],shapeStack[2]])
    return a0,a1,phi
     
def reductionMatrix(stack_im,stack_ob):
    """
    reductionMatrix(): it applies matrix() to both stacks im and ob
    """
    return (matrix(stack_im),matrix(stack_ob))
    
def createIm(stack_im,stack_ob):
    """
    """
    imParam,obParam = reductionMatrix(stack_im,stack_ob)
    
    TI = np.divide(imParam[0],obParam[0])
    DPCI = imParam[2]-obParam[2]
    DFI = np.divide(np.divide(imParam[1],imParam[0]),np.divide(obParam[1],obParam[0]))
    return TI, DPCI, DFI
    
def saveIm(ti,dpci,dfi,name='name',folder='folder',overWrite=False):
    """
    """
    if not exists('data/'+folder):
        makedirs('data/'+folder) 
        print('files saved in folder: ','data/'+folder)

    pyfits.writeto('data/'+folder+'/ti_'+str(name)+'.fits',ti,clobber=overWrite)
    pyfits.writeto('data/'+folder+'/dpci_'+str(name)+'.fits',dpci,clobber=overWrite)
    pyfits.writeto('data/'+folder+'/dfi_'+str(name)+'.fits',dfi,clobber=overWrite)
    
#    fits.writeto('out.fits', ti, 96)
    return