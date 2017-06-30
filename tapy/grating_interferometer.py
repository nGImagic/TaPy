from pathlib import Path
from astropy.io import fits
import numpy as np


class GratingInterferometer(object):
    
    data = []
    
    def __init__(self):
        pass
    
    def load(self, file_name=''):
        """
        Function to read data from the specified path, it can read FITS, TIFF and HDF.
    
        Parameters
        ----------
        path : string_like
            Path of the input file with his extention.
    
        Notes
        -----
        In case of corrupted header it skips the header and reads the raw data.
        For the HDF format you need to specify the hierarchy.
        """
    
        my_file = Path(file_name)
        if my_file.is_file():
            if file_name.lower().endswith('.fits'):
                try:
                    self.load_fits(my_file)
                except OSError:
                    import fitsio
                    im_a1.append(fitsio.read(path))
            elif file_name.lower().endswith(('.tiff','.tif')) :
                im_a1.append(np.asarray(Image.open(path)))
            elif file_name.lower().endswith(('.hdf','.h4','.hdf4','.he2','h5','.hdf5','.he5')): 
                # change here the hierarchy 
                hdf = h5py.File(path,'r')['entry']['data']['data'].value    
                for iScan in hdf:
                    im_a1.append(iScan)
            else:
                raise OSError('file extension not yet implemented....Do it your own way!')     
            #im_a1 = np.asarray(im_a1)-dc            
        else:
            raise OSError("The file name does not exist")
        
    def load_fits(self, file_name):
        '''load fits image
        
        Parameters
        ----------
           full file name of fits image
        '''
        temp = fits.open(file_name,ignore_missing_end=True)[0].data
        if len(temp.shape) == 3:
            temp = temp.reshape(temp.shape[1:])                
        self.data = temp