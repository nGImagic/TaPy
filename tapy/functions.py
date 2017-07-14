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
from os import makedirs
from astropy.io import fits 
import h5py
from pathlib import Path
from scipy.signal import medfilt,wiener



def readRead(path,dc=0):
    """
    Function to read data from the specified path, it can read FITS, TIFF and HDF.
    
    Parameters
    ----------
    path : string_like
            Path of the input file with his extention.
    dc : array_like
            An array containing the dark current data.
    
    Returns
    -------
    im_a1 : array_like
            An array containing the read data.
    
    Notes
    -----
    In case of corrupted header it skips the header and reads the raw data.
    For the HDF format you need to specify the hierarchy.
    """
    my_file = Path(path)
    if my_file.is_file():
        im_a1 = []
        if path.lower().endswith('.fits'):
            try:
                temp = fits.open(path,ignore_missing_end=True)[0].data
                if len(temp.shape) == 3:
                    temp = temp.reshape(temp.shape[1:])                
                im_a1.append(temp)  
            except OSError:
                import fitsio
                im_a1.append(fitsio.read(path))
        elif path.lower().endswith(('.tiff','.tif')) :
            im_a1.append(np.asarray(Image.open(path)))
        elif path.lower().endswith(('.hdf','.h4','.hdf4','.he2','h5','.hdf5','.he5')): 
            # change here the hierarchy 
            hdf = h5py.File(path,'r')['entry']['data']['data'].value    
            for iScan in hdf:
                im_a1.append(iScan)
        else:
            raise OSError('file extension not yet implemented....Do it your own way!')     
        im_a1 = np.asarray(im_a1)-dc
        return im_a1
    else:
        raise OSError('the path does not exist')
    
def read_data(path_im,path_ob,path_dc):
    """
    Function to read data from the specified folders, it can read FITS, TIFF and HDF.

    Parameters
    ----------
    path_im : string_like
            Path of the projection folder.
            
    path_ob : string_like
            Path of the open beam folder.
            
    path_dc : string_like
            Path of the dark current folder.
            
    Returns
    -------
    stack_im_ar : array_like
            A stack containing all the projections.
    
    stack_ob : array_like
            A stack containing all the references.
    
    Notes
    -----   
    File format supported: ['.fits','.tiff','.tif','.hdf','.h4','.hdf4','.he2','h5','.hdf5','.he5']
    """
#    Dark current
    imExt = ['.fits','.tiff','.tif','.hdf','.h4','.hdf4','.he2','h5','.hdf5','.he5']
    if path_dc:
        im_a1 = []
        filenames_dc = [name for name in os.listdir(path_dc) if name.lower().endswith(tuple(imExt))]
        filenames_dc.sort()
        for name in filenames_dc:
            full_path_name = path_dc+'/'+name
#            print(full_path_name)
            im_a1.append(readRead(full_path_name))
        im_a1 = np.asarray(im_a1)
        im_a1 = np.sum(im_a1,axis=0)/np.shape(im_a1)[0]
    
#    Open beam
    filenames_ob = [name for name in os.listdir(path_ob) if name.lower().endswith(tuple(imExt))]
    filenames_ob.sort()
    stack_ob = []
    for name in filenames_ob:
        full_path_name = path_ob+'/'+name
        if path_dc:
            stack_ob.append(readRead(full_path_name,im_a1)) #with dc
        else:
            stack_ob.append(readRead(full_path_name))   #without dc
    stack_ob = np.concatenate(stack_ob)

#    Projections
    filenames_im = [name for name in os.listdir(path_im) if name.lower().endswith(tuple(imExt))]
    filenames_im.sort()
    stack_im_ar = []
    for name in filenames_im:
        full_path_name = path_im+'/'+name
        if path_dc:
            stack_im_ar.append(readRead(full_path_name,im_a1)) #with dc
        else:
            stack_im_ar.append(readRead(full_path_name))   #without dc
    stack_im_ar = np.concatenate(stack_im_ar)
    if np.shape(stack_im_ar) != np.shape(stack_ob):
            raise ValueError('Data and open beam have different shapes')
        
    return stack_im_ar,stack_ob


xROI,yROI,widthROI,heightROI=10,10,35,35 #parameter for roi
   
def roi(im,xROI,yROI,widthROI,heightROI,show=False,titleOne='Original image with selected ROI',titleTwo='ROI',shape=False):
    """
    roi() takes a single image and crops it, (xROI,yROI) is the upper left-hand corner of the rectangle in pixel units.
    
    Parameters
    ----------
    im : array_like
        Input image.
        
    xROI : int_like
        x position of the upper left-hand corner in pixel units.
    
    yROI : int_like
        y position of the upper left-hand corner in pixel units.
    
    widthROI : int_like
        width of the recangle in pixel units.
    
    heightROI : int_like
        height of the recangle in pixel units.
    
    show : boolean
        If True it shows the ROI and its position.
        
    titleOne : string_like
        Title of the ROI position.
        
    titleTwo : string_like
        Title of the ROI.
        
    shape : boolean
        If True it shows the size of the image.
        
    Returns
    -------
    imROI : array_like
        Return the ROI.
    
    Notes
    -----
    """
    if shape:
        print(im.shape)
    if (0<=xROI<=im.shape[1] and 0<=xROI+widthROI<=im.shape[1] and 0<=yROI<=im.shape[0] and 0<=yROI+heightROI<=im.shape[0]):
        imROI = im[yROI:yROI+heightROI,xROI:xROI+widthROI]
        if show:
            vmin,vmax=np.mean(im)-2*np.std(im),np.mean(im)+2*np.std(im)
            print(vmax, vmin)
            cmap='gray'
            fig = plt.figure(figsize=(15,10)) 
            gs = gridspec.GridSpec(1, 2,width_ratios=[4,1],height_ratios=[1,1]) 
            ax = plt.subplot(gs[0])
            ax2 = plt.subplot(gs[1])
            ax.imshow(im,vmin=vmin, vmax=vmax,interpolation='nearest',cmap=cmap)
            rectNorm = patches.Rectangle((xROI,yROI),widthROI,heightROI,linewidth=1,edgecolor='m',facecolor='none')
            ax.add_patch(rectNorm)
            ax.set_title(titleOne)
            ax2.imshow(im,vmin=vmin, vmax=vmax,interpolation='nearest',cmap=cmap)
            ax2.set_title(titleTwo)
            ax2.set_xlim([xROI,xROI+widthROI])
            ax2.set_ylim([yROI+heightROI,yROI])
            plt.tight_layout()
            plt.show()
            plt.close('all')
      
        return(imROI)
    else:
        print('!!!WARNING!!! \nROI out of range')


def cropped(stack_im,stack_ob,xROI=xROI,yROI=yROI,widthROI=widthROI,heightROI=heightROI,show=True):
    """
    Crop the stacks to the selected ROI 
   
    Parameters
    ----------
    stack_im : array_like
        Input stack of projections.
    
    stack_ob : array_like
        Input stack of open beam.
        
    xROI : int_like
        x position of the upper left-hand corner in pixel units.
    
    yROI : int_like
        y position of the upper left-hand corner in pixel units.
    
    widthROI : int_like
        width of the recangle in pixel units.
    
    heightROI : int_like
        height of the recangle in pixel units.
    
    show : boolean
        If True it shows the ROI and its position.
    
    Returns
    -------
    stack_im_ar : array_like
            A stack containing all the cropped projections.
    
    stack_ob_ar : array_like
            A stack containing all the cropped references.  
            
    Notes
    -----
    
    """
    stack_im_ar = [roi(im=stack_im[0],xROI=xROI,yROI=yROI,widthROI=widthROI,heightROI=heightROI,show=show,titleTwo='Cropped region',shape=True)]
    for i in stack_im[1:]:
        stack_im_ar.append(roi(im=i,xROI=xROI,yROI=yROI,widthROI=widthROI,heightROI=heightROI,show=False))    
    stack_ob_ar = [roi(im=i,xROI=xROI,yROI=yROI,widthROI=widthROI,heightROI=heightROI,show=False) for i in stack_ob]
    
    return(np.asarray(stack_im_ar),np.asarray(stack_ob_ar))

    
def normalization(stack_im,stack_ob,xROI=xROI,yROI=yROI,widthROI=widthROI,heightROI=heightROI,show=True):
    """
    Normalize the stacks to the selected ROI 
   
    Parameters
    ----------
    stack_im : array_like
        Input stack of projections.
    
    stack_ob : array_like
        Input stack of open beam.
        
    xROI : int_like
        x position of the upper left-hand corner in pixel units.
    
    yROI : int_like 
        y position of the upper left-hand corner in pixel units.
    
    widthROI : int_like
        width of the recangle in pixel units.
    
    heightROI : int_like
        height of the recangle in pixel units.
    
    show : boolean
        If True it shows the ROI and its position.
    
    Returns
    -------
    stack_im_ar : array_like
            A stack containing all the normalized projections.
    
    stack_ob_ar : array_like
            A stack containing all the normalized references.  
            
    Notes
    -----
    
    """
    area = abs(widthROI*heightROI)  
    stack_im_ar = []    
    roi(stack_im[0],xROI,yROI,widthROI,heightROI,show,titleTwo='Area for normalization')
    stack_im_ar = [l/(l[yROI:yROI+heightROI+1,xROI:xROI+widthROI+1].sum()/area) for l in stack_im]   
    stack_ob_ar = [l/(l[yROI:yROI+heightROI+1,xROI:xROI+widthROI+1].sum()/area) for l in stack_ob] 
    
    return(np.asarray(stack_im_ar),np.asarray(stack_ob_ar))

def oscillation(stack_im,stack_ob,xROI=xROI,yROI=yROI,widthROI=widthROI,heightROI=heightROI,repeatedPeriod=False,folder=False,show=True):
    """
    Oscillation plot analysis of the selected ROI.
   
    Parameters
    ----------
    stack_im : array_like
        Input stack of projections.
    
    stack_ob : array_like
        Input stack of open beam.
        
    xROI : int_like
        x position of the upper left-hand corner in pixel units.
    
    yROI : int_like
        y position of the upper left-hand corner in pixel units.
    
    widthROI : int_like
        width of the recangle in pixel units.
    
    heightROI : int_like
        height of the recangle in pixel units.
    
    repeatedPeriod : boolean
        If True it plots the oscillation twice.
        
    folder : string_like or False
        Path of the folder where to save the oscillation plot, if False it doesn't save the plot.
    
    show : boolean
        If True it shows the ROI and its position.
    
    Returns
    -------
    Oscillation plot.  
            
    Notes
    -----  
    """
    titleOne='Area for oscillation'
    titleTwo='Oscillation plot'
    stack_ob_ar = [l[yROI:yROI+heightROI,xROI:xROI+widthROI].mean() for l in stack_ob] 
    stack_im_ar = [l[yROI:yROI+heightROI,xROI:xROI+widthROI].mean() for l in stack_im] 

    if repeatedPeriod:
        stack_ob_ar += stack_ob_ar
        stack_im_ar += stack_im_ar
        titleTwo += ' repetead period'
#    PLOT oscillation
    im = stack_im[0]
    if (0<=xROI<=im.shape[1] and 0<=xROI+widthROI<=im.shape[1] and 
        0<=yROI<=im.shape[0] and 0<=yROI+heightROI<=im.shape[0]):
        vmin,vmax=im.min(),im.max()
        cmap='gray'
        fig = plt.figure(figsize=(15,10)) 
        gs = gridspec.GridSpec(1,2,width_ratios=[2,1],height_ratios=[1,1]) 
        ax = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax.imshow(im,vmin=vmin, vmax=vmax,interpolation='nearest',cmap=cmap)
        rectNorm = patches.Rectangle((xROI,yROI),widthROI,heightROI,linewidth=1,edgecolor='m',facecolor='none')
        ax.add_patch(rectNorm)
        ax.set_title(titleOne)
        rangeim = range(1,len(stack_im_ar)+1)
        ax2.plot(rangeim,stack_im_ar,color='g',label='data')
        ax2.scatter(rangeim,stack_im_ar,marker='*',color='g')
        rangeob = range(1,len(stack_ob_ar)+1)
        ax2.plot(rangeob,stack_ob_ar,color='b',label='ob')
        ax2.scatter(rangeob,stack_ob_ar,color='b')
        ax2.legend(loc=1, shadow=True)
        ax2.set_title(titleTwo)
        ax2.set_xlim((0,len(stack_ob_ar)+2))
        ax2.grid(True)
        plt.tight_layout()
        if show:
            plt.show()
        if folder:
            if not os.path.exists(folder):
                makedirs(folder) 
                print('files saved in folder: ',str(folder))
            fig.savefig(str(folder)+'/oscillationPlot_X'+str(xROI)+'Y'+str(yROI)+'.png', bbox_inches='tight')
        plt.close('all')
    else:
        print('!!!WARNING!!! \nROI out of range')
    

def matrix(stack_im,numberPeriods):
    """
    Take the stack of OBs and projections to create TI, DPCI, DFI and visiblity map.
    The algorithm used in this step is based on Marathe et al.
    (2014) http://dx.doi.org/10.1063/1.4861199.
    
    Parameters
    ----------
    stack_im : array_like
        Input stack of projections.
        
    numberPeriods : float_like
        Numbers or fraction of stepped period.
    
    Returns
    -------
    a0 : array_like
        Offset.
        
    a1 : array_like
        Amplitude.
    
    phi : array_like
        Phase.
    
    Notes
    -----
    """
    shapeStack = np.shape(stack_im)
    B = np.zeros((shapeStack[0],3))  
    
    stack_imReshaped = np.reshape(stack_im,[shapeStack[0],shapeStack[1]*shapeStack[2]])
    rangeStack = range(shapeStack[0])
    for j in rangeStack:
        B[j][0] = 1.0
        B[j][1] = np.cos(2*np.pi*rangeStack[j]*numberPeriods/(shapeStack[0]-1))
        B[j][2] = np.sin(2*np.pi*rangeStack[j]*numberPeriods/(shapeStack[0]-1))
    B = np.matrix(B)
    G = (B.T * B).I * B.T
    A = (G*stack_imReshaped)
    offSet,absoluteAmpl,absPhase = A[0,:],A[1,:],A[2,:]
    a0 = np.reshape(np.asarray(offSet),[shapeStack[1],shapeStack[2]])
    a1 = np.reshape(np.sqrt(np.asarray(absoluteAmpl)**2+np.asarray(absPhase)**2),[shapeStack[1],shapeStack[2]])
    phi = np.reshape(np.arctan((np.asarray(absPhase)/np.asarray(absoluteAmpl))),[shapeStack[1],shapeStack[2]])
    
    return a0,a1,phi
     
def reductionMatrix(stack_im,stack_ob,numberPeriods):
    """
    Apply matrix() to the projections and open beam stacks.
   
    Parameters
    ----------
    stack_im : array_like
        Input stack of projections.
    
    stack_ob : array_like
        Input stack of open beam.
        
    numberPeriods : float_like
        Numbers or fraction of stepped period.
    
    Returns
    -------
    Return an array_like containing the a0, a1, phi of the projections and open beam stack.
    
    Notes
    -----
    """
    return (matrix(stack_im,numberPeriods),matrix(stack_ob,numberPeriods))

def createIm_fft(stack_im,stack_ob):
    """
    Apply the fourier component analysis to retrieve dfi, ti, dpci and visibility map.

    Parameters
    ----------
    stack_im : array_like
        Input stack of projections.
    
    stack_ob : array_like
        Input stack of open beam.
    
    Returns
    -------
    ti : array_like
        Reconstructed fft trasmission array.
        
    dpci : array_like
        Reconstructed fft DPCI array.
        
    dfi : array_like
        Reconstructed fft DFI array.
        
    visi : array_like
        Reconstructed fft visibility array.
    Notes
    -----
    """
    ## Projection
    shapeStack_im = np.shape(stack_im)
    stack_imReshaped = np.reshape(stack_im,[shapeStack_im[0],shapeStack_im[1]*shapeStack_im[2]])
    steps = len(stack_imReshaped[:,:])
    outfft_a_im = []
    outfft_b_im = []
    outfft_c_im = []
    for i in range(len(stack_imReshaped[0,:])):
        fft_osc = np.fft.rfft(stack_imReshaped[:,i])/(steps-1)
        outfft_a_im.append(fft_osc[0])
        outfft_b_im.append(2*np.sqrt(np.real(fft_osc[1])**2+np.imag(fft_osc[1])**2))
        outfft_c_im.append(-np.angle(fft_osc[1]))
    outfft_a_im = np.reshape(outfft_a_im, [shapeStack_im[1],shapeStack_im[2]])
    outfft_b_im = np.reshape(outfft_b_im, [shapeStack_im[1],shapeStack_im[2]])
    outfft_c_im = np.reshape(outfft_c_im, [shapeStack_im[1],shapeStack_im[2]])

    ## open beam
    shapeStack_ob = np.shape(stack_ob)
    stack_obReshaped = np.reshape(stack_ob,[shapeStack_ob[0],shapeStack_ob[1]*shapeStack_ob[2]])
    steps = len(stack_obReshaped[:,:])
    outfft_a_ob = []
    outfft_b_ob = []
    outfft_c_ob = []
    for i in range(len(stack_obReshaped[0,:])):
        fft_osc = np.fft.rfft(stack_obReshaped[:,i])/(steps-1)
        outfft_a_ob.append(fft_osc[0])
        outfft_b_ob.append(2*np.sqrt(np.real(fft_osc[1])**2+np.imag(fft_osc[1])**2))
        outfft_c_ob.append(-np.angle(fft_osc[1]))
    outfft_a_ob = np.reshape(outfft_a_ob, [shapeStack_ob[1],shapeStack_ob[2]])
    outfft_b_ob = np.reshape(outfft_b_ob, [shapeStack_ob[1],shapeStack_ob[2]])
    outfft_c_ob = np.reshape(outfft_c_ob, [shapeStack_ob[1],shapeStack_ob[2]])
    ti = np.real(outfft_a_im)/np.real(outfft_a_ob)
    dpci = outfft_c_im - outfft_c_ob
    dfi = (np.real(outfft_b_im)*np.real(outfft_a_ob))/(np.real(outfft_b_ob)*np.real(outfft_a_im))
    visi = np.real(outfft_b_ob)/np.real(outfft_a_ob)
    
    return ti, dpci, dfi, visi


def createIm(stack_im,stack_ob,numberPeriods):
    """
    Process the projections and open beam stacks to retrieve dfi, ti, dpci and visibility map.
    
    Parameters
    ----------
    stack_im : array_like
        Input stack of projections.
    
    stack_ob : array_like
        Input stack of open beam.
        
    numberPeriods : float_like
        Numbers or fraction of stepped period.
        
    Returns
    -------
    TI : array_like
        Reconstructed trasmission array.
        
    DPCI : array_like
        Reconstructed DPCI array.
        
    DFI : array_like
        Reconstructed DFI array.
        
    VIS_map : array_like
        Reconstructed visibility array.
    
    Notes
    -----
    """
    imParam,obParam = reductionMatrix(stack_im,stack_ob,numberPeriods)
    TI = np.divide(imParam[0],obParam[0])
    DPCI = imParam[2]-obParam[2]
    DPCI = np.arctan(np.tan(DPCI))
    DFI = np.divide(np.divide(imParam[1],imParam[0]),np.divide(obParam[1],obParam[0]))
    VIS_map = np.divide(obParam[1],obParam[0])
    
    return TI, DPCI, DFI, VIS_map
    
def saveIm(ti,dpci,dfi,vis_map,name='name',folder='folder',overWrite=False):
    """
    Save the images to specific folder.
    
    Parameters
    ----------
    ti : array_like
        Input reconstructed trasmission array.
        
    dpci : array_like
        Input reconstructed DPCI array.
        
    dfi : array_like
        Input reconstructed DFI array.
        
    vis_map : array_like
        Input reconstructed visibility array.
    
    name : sring_like
        Specific name for the images.
        
    folder : string_like
        Path of the folder where to save the reconstructed images.
        
    overWrite : boolean
        If it's True it overwrite the images with the same name.
        
    Returns
    -------
    
    Notes
    -----
    """
    if not os.path.exists(folder):
        makedirs(folder) 
    print('files saved in folder: ',folder)
    fits.writeto(folder+'/ti_'+str(name)+'.fits',ti,clobber=overWrite)
    fits.writeto(folder+'/dpci_'+str(name)+'.fits',dpci,clobber=overWrite)
    fits.writeto(folder+'/dfi_'+str(name)+'.fits',dfi,clobber=overWrite)
    fits.writeto(folder+'/visi_'+str(name)+'.fits',vis_map,clobber=overWrite)
    
def binning(stack_im,stack_ob,bin_fac=None):
    """
    Bin the projections and open beam stacks. 
    
    Parameters
    ----------
    stack_im : array_like
        Input stack of projections.
    
    stack_ob : array_like
        Input stack of open beam.
        
    bin_fac : int_like
        Cluster of pixels into a single pixel.
    
    Returns
    -------
    stack_im_bin : array_like
            A stack containing all the binned projections.
    
    stack_ob_bin : array_like
            A stack containing all the binned references.  
    
    Notes
    -----
    """
    num_im,x_im,y_im = np.shape(stack_im)
    stack_im_tmp = list()
    if bin_fac:
        for i in range(num_im):
            t = stack_im[i]
            t_resh = t.reshape(int(x_im/bin_fac), bin_fac, int(y_im/bin_fac), bin_fac)
            stack_im_tmp.append(t_resh.mean(axis=3).mean(axis=1))
    
        stack_im_bin = np.asarray(stack_im_tmp) 
    else:
        stack_im_bin = stack_im
        
    num_ob,x_ob,y_ob = np.shape(stack_ob)
    stack_ob_tmp = list()
    if bin_fac:
        for i in range(num_ob):
            t = stack_ob[i]
            t_resh = t.reshape(int(x_ob/bin_fac), bin_fac, int(y_ob/bin_fac), bin_fac)
            stack_ob_tmp.append(t_resh.mean(axis=3).mean(axis=1))
    
        stack_ob_bin = np.asarray(stack_ob_tmp) 
    else:
        stack_ob_bin = stack_ob
        
    return stack_im_bin, stack_ob_bin
