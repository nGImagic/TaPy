import os


im_ext = ['.fits','.tiff','.tif','.hdf','.h4','.hdf4','.he2','h5','.hdf5','.he5']

def get_sorted_list_images(folder=''):
    '''return the list of images sorted that have the correct format
    
    Parameters:
       folder: string of the path containing the images
       
    Return:
       sorted list of only images that can be read by program
    '''
    filenames = [name for name in os.listdir(folder) if name.lower().endswith(tuple(im_ext))]
    filenames.sort()
    return filenames