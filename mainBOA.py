#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 16:01:26 2017

@author: valsecchi
"""
import os
import re

path = '/Users/valsecchi/Documents/PSI/BOA_FOLDER/BOA_DICEMBRE/reload/2016December_BOA_beamtime_wsNIAGversion/04_DCM/08_5p7lambda770exposure'



    
    



def splitNewRoutine_BOA(path,firstSpinFlipperON=True):
    """
    when you acquire nGI data at BOA with the new routing (spinON spinOFF and step) this function splits the data into two folders
    """
    imExt = ['.fits','.tiff','.tif','.hdf','.h4','.hdf4','.he2','h5','.hdf5','.he5']
    filenames = [name for name in os.listdir(path) if name.lower().endswith(tuple(imExt)) or re.search(r'\.bad\d+$', name)]
    if all(re.search(r'\.bad\d+$', name) for name in filenames):
        reshapedFilenamesBad =[]
        print('All files ends .bad####')
        for name in filenames:
            nameSplit = re.split('_00001|\.bad',name)
            nameSplit = nameSplit[0]+nameSplit[2].zfill(5)+nameSplit[1]
            reshapedFilenamesBad.append(nameSplit)

    for bad,badResh in zip(filenames,reshapedFilenamesBad):
        print('old:', bad, '\nnew',badResh,2*'\n')
        os.rename(path+'/'+bad,path+'/'+badResh)
    filenames = reshapedFilenamesBad
    
    spin_ON,spin_OFF = '/spin_ON','/spin_OFF'
    if not os.path.exists(path+spin_ON):
        os.makedirs(path+spin_ON) 
    if not os.path.exists(path+spin_OFF):
        os.makedirs(path+spin_OFF)        
    if firstSpinFlipperON:
        for odd in filenames[::2]:
            os.rename(path+'/'+odd,path+'/'+spin_ON+'/'+odd)
        for even in filenames[1::2]:
            os.rename(path+'/'+even,path+'/'+spin_OFF+'/'+even)

