from PIL import Image
from astropy.io import fits


def make_tif(data=[], file_name=''):
    '''create tif file'''
    new_image = Image.fromarray(data)
    new_image.save(file_name)    

def make_fits(data=[], file_name=''):
    '''create fits file'''
    fits.writeto(file_name, data, clobber=True)
