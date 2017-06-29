#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "TaPy",
    version = "1.0.0",
    author = "Ralph P. Harti, Jacopo Valsecchi, Jean Bilheux",
    author_email = "Ralph.Harti@psi.ch, Jacopo.Valsecchi@psi.ch, bilheuxjm@ornl.gov", 
    packages = find_packages(exclude=['tests', 'notebooks']),
    include_package_data = True,
    test_suite = 'tests',
    install_requires = [
        'numpy',
        'pyfits',
        'pillow',
        'astropy',
        'h5p7',
        'scipy',
    ],
    dependency_links = [
    ],
    description = "grating interferometry of x-rays and neutrons data",
    license = 'BSD',
    keywords = "x-ray neutron interferometry dark-field",
    url = "https://github.com/nGImagic/TaPye",
    classifiers = ['Development Status :: 3 - Alpha',
                   'Topic :: Scientific/Engineering :: Physics',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5'],
)


# End of file
