import unittest
import numpy as np
import os
from PIL import Image
import shutil

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
        

class TestExportPhase1(unittest.TestCase):
    
    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data/'))

    def test_export_raises_error_if_wrong_folder(self):
        '''assert error raised if folder do not exist'''
        o_grating = GratingInterferometer()
        sample_path = self.data_path + '/tif/sample/'
        o_grating.load(folder=sample_path)
        ob_path = self.data_path + '/tif/ob/'
        o_grating.load(folder=ob_path, data_type='ob')
        o_grating.create_interferometry_images()   
        self.assertRaises(IOError, o_grating.export, folder='/unknown/')

    def test_error_raised_if_data_type_is_not_valie(self):
        '''assert error is raised if data_type is wrong'''
        o_grating = GratingInterferometer()
        sample_path = self.data_path + '/tif/sample/'
        o_grating.load(folder=sample_path)
        ob_path = self.data_path + '/tif/ob/'
        o_grating.load(folder=ob_path, data_type='ob')
        o_grating.create_interferometry_images()   
        self.assertRaises(KeyError, o_grating.export, data_type='not_real_type')
        
    def test_do_nothing_if_nothing_to_export(self):
        '''assert do nothing if nothing to export'''
        o_grating = GratingInterferometer()
        sample_path = self.data_path + '/tif/sample/'
        o_grating.load(folder=sample_path)
        ob_path = self.data_path + '/tif/ob/'
        o_grating.load(folder=ob_path, data_type='ob')
        self.assertFalse(o_grating.export())
        
class TestExportPhase2(unittest.TestCase):

    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data/'))
        self.export_folder = self.data_path + '/temporary_folder/'
        os.mkdir(self.export_folder)
        
    def tearDown(self):
        shutil.rmtree(self.export_folder)

    def test_export_create_the_right_file_name(self):
        '''assert output file name are correctly created'''
        sample_path = self.data_path + '/tif/sample'
        ob_path = self.data_path + '/tif/ob'
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path)
        o_grating.load(folder=ob_path, data_type='ob')
        o_grating.create_interferometry_images()
        o_grating.export(folder=self.export_folder)

        output_file_name_list = o_grating._export_file_name
        _returned_file_0 = output_file_name_list[0]
        
        _expected = os.path.basename(o_grating.data['sample']['file_name'][0])
        _new_file_name = os.path.splitext(_expected)[0] + '.tif'
        _expected_file_0 = os.path.join(self.export_folder, _new_file_name)
        
        self.assertTrue(_expected_file_0, _returned_file_0)

    def test_export_works_for_tif(self):
        '''assert the file crated is correct for tif images'''
        sample_path = self.data_path + '/tif/sample'
        ob_path = self.data_path + '/tif/ob'
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path)
        o_grating.load(folder=ob_path, data_type='ob')
        o_grating.create_interferometry_images()
        o_grating.export(folder=self.export_folder)
        _sample_0 = o_grating.interferometry['transmission'][0]

        o_grating_2 = GratingInterferometer()
        o_grating_2.load(folder=self.export_folder)
        _sample_1 = o_grating_2.data['sample']['data'][0]
        
        self.assertTrue((_sample_0 == _sample_1).all())
        
