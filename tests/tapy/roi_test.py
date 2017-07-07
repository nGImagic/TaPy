import unittest
import numpy as np
import os

from tapy.roi import ROI


class TestRoi(unittest.TestCase):

    def test_setting_roi_x0_y0_x1_y1(self):
        '''assert roi are correctly defined using x0, y0, x1 and y1'''
        x0 = 1
        y0 = 1
        x1 = 5
        y1 = 10
        _roi = ROI(x0=x0, y0=y0, x1=x1, y1=y1)
        _expected = [x0, y0, x1, y1]
        _returned = [_roi.x0, _roi.y0, _roi.x1, _roi.y1]
        self.assertTrue(_expected == _returned)
        
    def test_setting_roi_x0_y0_width_height(self):
        '''assert roi are correctly defined using x0, y0, width and height'''
        x0 = 1
        y0 = 1
        width = 4
        height = 9
        _roi = ROI(x0=x0, y0=y0, width=width, height=height)
        _expected = [x0, y0, x0 + width, y0+height]
        _returned = [_roi.x0, _roi.y0, _roi.x1, _roi.y1]
        self.assertTrue(_expected == _returned)        
        
    def test_error_raised_when_x0_or_y0_not_provided(self):
        '''assert error is raised when either x0 or y0 are not provided'''
        y0 = 1
        x1 = 2
        y1 = 3
        self.assertRaises(ValueError, ROI, np.NaN, y0, x1, y1)

        x0 = 1
        x1 = 2
        y1 = 3
        self.assertRaises(ValueError, ROI, x0, x1, y1)

    def test_error_raised_when_x1_and_width_or_y1_and_height_not_provided(self):
        '''assert error is raised when either x1 and width or y1 and height are not provided'''
        x0 = 1
        y0 = 1
        y1 = 2
        self.assertRaises(ValueError, ROI, x0, y0, np.NaN, y1)

        x0 = 1
        y0 = 2
        x1 = 3
        self.assertRaises(ValueError, ROI, x0, y0, x1, np.NaN)

    def test_x_and_y_correctly_sorted(self):
        '''assert x0 and y0 are always the smallest of the x and y values'''
        x0 = 1
        y0 = 1
        x1 = 5
        y1 = 10
        _roi = ROI(x0=x0, y0=y0, x1=x1, y1=y1)
        _x0_expected = 1
        _x0_returned = _roi.x0
        self.assertTrue(_x0_expected == _x0_returned)
        
        x0 = 1
        y0 = 1
        width = 5
        height = 10
        _roi = ROI(x0=x0, y0=y0, width=width, height=height)
        _x0_expected = 1
        _x0_returned = _roi.x0
        self.assertTrue(_x0_expected == _x0_returned)
        
        x0 = 5
        y0 = 1
        x1 = 1
        y1 = 10
        _roi = ROI(x0=x0, y0=y0, x1=x1, y1=y1)
        _x0_expected = 1
        _x0_returned = _roi.x0
        self.assertTrue(_x0_expected == _x0_returned)        
        
        x0 = 5
        y0 = 1
        x1 = 1
        y1 = 10
        _roi = ROI(x0=x0, y0=y0, x1=x1, y1=y1)
        _y0_expected = 1
        _y0_returned = _roi.y0
        self.assertTrue(_y0_expected == _y0_returned)             
        
        x0 = 5
        y0 = 10
        x1 = 1
        y1 = 1
        _roi = ROI(x0=x0, y0=y0, x1=x1, y1=y1)
        _y0_expected = 1
        _y0_returned = _roi.y0
        self.assertTrue(_y0_expected == _y0_returned)            
        
        x0 = 1
        y0 = 1
        width = 5
        height = 10
        _roi = ROI(x0=x0, y0=y0, width=width, height=height)
        _y0_expected = 1
        _y0_returned = _roi.y0
        self.assertTrue(_y0_expected == _y0_returned)
        