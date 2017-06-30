from pathlib import Path
import numpy as np

from tapy.loader import load_hdf, load_tiff, load_fits

class GratingInterferometer(object):
    
    sample = []
    ob = []
    
    def __init__(self):
        self.sample = []
        self.ob = []
    
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
                data = load_fits(my_file)
            elif file_name.lower().endswith(('.tiff','.tif')) :
                data = load_tiff(my_file)
            elif file_name.lower().endswith(('.hdf','.h4','.hdf4','.he2','h5','.hdf5','.he5')): 
                data = load_hdf(my_file)
            else:
                raise OSError('file extension not yet implemented....Do it your own way!')     
            
            # save data in right array according to type
            if data_type == 'sample':
                self.sample = data
            else:
                self.ob = data

        else:
            raise OSError("The file name does not exist")

    def dark_field_correction(self):
        '''remove dark field from data set'''
        if self.ob != []:
            self.sample = np.asarray(self.sample) - self.ob