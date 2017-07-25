import unittest
import numpy as np
import os
from PIL import Image

from tapy.grating_interferometer import GratingInterferometer
from tapy.roi import ROI

# USE REAL DATA SET HERE !

class TestInterferometry(unittest.TestCase):
    
    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data/'))
        
    def test_offset_correctly_calculated_for_sample(self):
        '''assert offset is correctly calculated'''
        o_grating = GratingInterferometer()
        sample_path = self.data_path + '/tif/sample/'
        o_grating.load(folder=sample_path)
        ob_path = self.data_path + '/tif/ob/'
        o_grating.load(folder=ob_path, data_type='ob')
        _dict = o_grating._create_reduction_matrix()
        _line = np.matrix(np.linspace(0,4,5)).T
        _col = np.matrix(np.ones((5)))
        _expected_offset = (_line * _col).T
        _expected_offset[:,0] = 1
        _expected_offset[0,0] = 5
        self.assertTrue((_expected_offset == _dict['offset']).all())
        
    def test_amplitute_correctly_calculated_for_sample(self):
        '''assert offset is correctly calculated'''
        o_grating = GratingInterferometer()
        sample_path = self.data_path + '/tif/sample/'
        o_grating.load(folder=sample_path)
        ob_path = self.data_path + '/tif/ob/'
        o_grating.load(folder=ob_path, data_type='ob')
        _dict = o_grating._create_reduction_matrix()
        _line = np.matrix(np.array([5.55e-17, 5.55e-17, 1.11e-16, 2.22e-16, 2.22e-16])).T
        _col = np.matrix(np.ones((5)))
        _expected_amplitude_0_0 = 0
        _expected_amplitude_0_1 = 5.55e-17
        self.assertAlmostEqual(_expected_amplitude_0_0, _dict['amplitude'][0,0], delta=0.01)
        self.assertAlmostEqual(_expected_amplitude_0_1, _dict['amplitude'][0,1], delta=0.01)
        
    def test_phase_correctly_calculated_for_sample(self):
        '''assert phase is correctly calculated'''
        o_grating = GratingInterferometer()
        sample_path = self.data_path + '/tif/sample/'
        o_grating.load(folder=sample_path)
        ob_path = self.data_path + '/tif/ob/'
        o_grating.load(folder=ob_path, data_type='ob')
        _dict = o_grating._create_reduction_matrix()
        _line = np.matrix(np.array([5.55e-17, 5.55e-17, 1.11e-16, 2.22e-16, 2.22e-16])).T
        _col = np.matrix(np.ones((5)))
        _expected_phase_0_0 = 0
        _expected_phase_0_1 = 5.55e-17
#        print(_dict['phase'])

    def test_interferometry_code_runs(self):
        '''assert interferometry code that creates final images works'''
        o_grating = GratingInterferometer()
        sample_path = self.data_path + '/tif/sample/'
        o_grating.load(folder=sample_path)
        ob_path = self.data_path + '/tif/ob/'
        o_grating.load(folder=ob_path, data_type='ob')
        o_grating.create_interferometry_images()
        

