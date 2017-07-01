from pathlib import Path
import numpy as np

from tapy.loader import load_hdf, load_tiff, load_fits

class GratingInterferometer(object):
    
    def __init__(self):
        self.dict_image = { 'data': [],
                            'file_name': []}
        self.dict_ob = {'data': [],
                        'file_name': []}
        self.dict_df = {'data': [],
                        'file_name': []}

        self.data = {}
        self.data['sample'] = self.dict_image
        self.data['ob'] = self.dict_ob
        self.data['df'] = self.dict_df
        
    
    def load(self, file='', folder='', data_type='sample'):
        '''
        Function to read individual files or entire files from folder specify for the given
        data type
        
        Parameters:
           file: full path to file
           folder: full path to folder containing files to load
           data_type: ['sample', 'ob', 'df]
        '''
        if not file == '':
            self.load_file(file=file, data_type=data_type)
        
        if not foler == '':
            # load all files from folder
            pass
        
    
    def load_file(self, file='', data_type='sample'):
        """
        Function to read data from the specified path, it can read FITS, TIFF and HDF.
    
        Parameters
        ----------
        file : string_like
            Path of the input file with his extention.
        data_type: ['sample', 'df']
    
        Notes
        -----
        In case of corrupted header it skips the header and reads the raw data.
        For the HDF format you need to specify the hierarchy.
        """
    
        my_file = Path(file)
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

            self.data[data_type]['data'].append(data)
            self.data[data_type]['file_name'].append(my_file)

        else:
            raise OSError("The file name does not exist")

    def dark_field_correction(self):
        '''remove dark field from data set'''
        if self.ob != []:
            self.sample = np.asarray(self.sample) - self.ob