from pathlib import Path
from astropy.io import fits
import numpy as np
from PIL import Image


class GratingInterferometer(object):
    
    sample = []
    ob = []
    
    def __init__(self):
        pass
    
    def load(self, file_name='', data_type='sample'):
        """
        Function to read data from the specified path, it can read FITS, TIFF and HDF.
    
        Parameters
        ----------
        path : string_like
            Path of the input file with his extention.
        data_type: ['sample', 'df']
    
        Notes
        -----
        In case of corrupted header it skips the header and reads the raw data.
        For the HDF format you need to specify the hierarchy.
        """
    
        my_file = Path(file_name)
        if my_file.is_file():
            data = []
            if file_name.lower().endswith('.fits'):
                data = self.load_fits(my_file)
            elif file_name.lower().endswith(('.tiff','.tif')) :
                data = self.load_tiff(my_file)
            elif file_name.lower().endswith(('.hdf','.h4','.hdf4','.he2','h5','.hdf5','.he5')): 
                # change here the hierarchy 
                hdf = h5py.File(path,'r')['entry']['data']['data'].value    
                for iScan in hdf:
                    im_a1.append(iScan)
            else:
                raise OSError('file extension not yet implemented....Do it your own way!')     
            
            if data_type == 'sample':
                self.sample = data
            else:
                self.ob = data

        else:
            raise OSError("The file name does not exist")
        
    def load_fits(self, file_name):
        '''load fits image
        
        Parameters
        ----------
           full file name of fits image
        '''
        try:
            temp = fits.open(file_name,ignore_missing_end=True)[0].data
            if len(temp.shape) == 3:
                temp = temp.reshape(temp.shape[1:])                
            return temp
        except OSError:
            raise OSError("Unable to read the FITS file provided!")
        
    def load_tiff(self, file_name):
        '''load tiff image
        
        Parameters:
        -----------
           full file name of tiff image
        '''
        try:
            return np.asarray(Image.open(file_name))
        except:
            raise OSError("Unable to read the TIFF file provided!")
            
    
#    def dark_field_correction