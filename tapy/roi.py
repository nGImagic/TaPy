import numpy as np


class ROI(object):
    '''class that list the type of ROI available'''

    x0 = np.NaN
    y0 = np.NaN
    x1 = np.NaN
    y1 = np.NaN

    def __init__(self, x0=np.NaN, y0=np.NaN, x1=np.NaN, y1=np.NaN, width=np.NaN, height=np.NaN):
        
        if np.isnan(x0) or np.isnan(y0):
            raise ValueError("x0 and y0 must be provided!")
        
        self.x0 = x0
        self.y0 = y0
        
        if not np.isnan(y1):
            self.y1 = np.max([y0,y1])
            self.y0 = np.min([y0,y1])
        elif not np.isnan(height):
            self.y1 = y0 + height
        else:
            raise ValueError("You must defined either y1 or height!")
            
        if not np.isnan(x1):
            self.x1 = np.max([x0,x1])
            self.x0 = np.min([x0,x1])
        elif not np.isnan(width):
            self.x1 = x0 + width
        else:
            raise ValueError("you must defined either x1 or width!")
        
    
