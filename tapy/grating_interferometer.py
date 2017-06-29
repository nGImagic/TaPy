from pathlib import Path


class GratingInterferometer(object):
    
    def __init__(self):
        pass
    
    def load(self, file_name=''):
        """
        Function to read data from the specified path, it can read FITS, TIFF and HDF.
    
        Parameters
        ----------
        path : string_like
            Path of the input file with his extention.
        dc : array_like
            An array containing the dark current data.
    
        Notes
        -----
        In case of corrupted header it skips the header and reads the raw data.
        For the HDF format you need to specify the hierarchy.
        """
    
        my_file = Path(file_name)
        if my_file.is_file():
            pass
        else:
            raise OSError("The file name does not exist")