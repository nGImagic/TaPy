from pathlib import Path
from astropy.io import fits
import numpy as np
from PIL import Image

def load_hdf(file_name):
    '''load HDF image
    
    Parameters
    ----------
       full file name of HDF5 file
    '''
    
    hdf = h5py.File(path,'r')['entry']['data']['data'].value    
    tmp = []
    for iScan in hdf:
        tmp.append(iScan)
    return tmp
    
    
def load_fits(file_name):
    '''load fits image
    
    Parameters
    ----------
       full file name of fits image
    '''
    tmp = []
    try:
        tmp = fits.open(file_name,ignore_missing_end=True)[0].data
        if len(tmp.shape) == 3:
            tmp = temp.reshape(tmp.shape[1:])                
        return tmp
    except OSError:
        raise OSError("Unable to read the FITS file provided!")
    
def load_tiff(file_name):
    '''load tiff image
    
    Parameters:
    -----------
       full file name of tiff image
    '''
    try:
        return np.asarray(Image.open(file_name))
    except:
        raise OSError("Unable to read the TIFF file provided!")