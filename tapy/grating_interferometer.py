from pathlib import Path
import numpy as np
import os

from tapy.loader import load_hdf, load_tiff, load_fits

class GratingInterferometer(object):
    
    im_ext = ['.fits','.tiff','.tif','.hdf','.h4','.hdf4','.he2','h5','.hdf5','.he5']
    
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
        
        if not folder == '':
            # load all files from folder
            list_images = self.get_sorted_list_images(folder=folder)
            for _image in list_images:
                full_path_image = os.path.join(folder, _image)
                self.load_file(file=full_path_image, data_type=data_type)
        
    def get_sorted_list_images(self, folder=''):
        '''return the list of images sorted that have the correct format
        
        Parameters:
           folder: string of the path containing the images
           
        Return:
           sorted list of only images that can be read by program
        '''
        filenames = [name for name in os.listdir(folder) if name.lower().endswith(tuple(self.im_ext))]
        filenames.sort()
        return filenames
    
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
            if file.lower().endswith('.fits'):
                data = load_fits(my_file)
            elif file.lower().endswith(('.tiff','.tif')) :
                data = load_tiff(my_file)
            elif file.lower().endswith(('.hdf','.h4','.hdf4','.he2','h5','.hdf5','.he5')): 
                data = load_hdf(my_file)
            else:
                raise OSError('file extension not yet implemented....Do it your own way!')     

            self.data[data_type]['data'].append(data)
            self.data[data_type]['file_name'].append(file)

        else:
            raise OSError("The file name does not exist")

    def normalization(self):
        '''normalization of the data 
        normalized_data = (sample - DF)/(OB - DF)
        '''
        if self.data['sample']['data'] == []:
            raise IOError("No normalization available as no data have been loaded")

        if self.data['ob']['data'] == []:
            raise IOError("No normalization available as no OB have been loaded")

        nbr_sample = len(self.data['sample']['file_name'])
        nbr_ob = len(self.data['ob']['file_name'])
        if nbr_sample != nbr_ob:
            raise IOError("Number of sample and ob do not match!")

        if not self.data['df']['data'] == []:
            self.df_correction(data_type='sample')
            self.df_correction(data_type='ob')
            
        return True
    
    def df_correction(self, data_type='sample'):
        '''dark field correction
        
        Parameters:
           data_type: string ['sample','ob]
        '''
        if not data_type in ['sample', 'ob']:
            raise KeyError("Wrong data type passed. Must be either 'sample' or 'ob'!")

        if self.data['df']['data'] == []:
            return

        if data_type == 'sample':
            if np.shape(self.data['sample']['data'][0]) != np.shape(self.data['df']['data'][0]):
                raise IOError("sample and df data must have the same shpae!")
        
            pass
            
        if data_type == 'ob':
            if np.shape(self.data['ob']['data'][0]) != np.shape(self.data['df']['data'][0]):
                raise IOError("ob and df data must have the same shpae!")
            
            pass