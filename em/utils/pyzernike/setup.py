import setuptools
setuptools.setup()

"""
#! /usr/bin/env python

from setuptools import setup, Extension
import numpy

# Obtain the numpy include directory
def get_numpy_include():
    try:
        return numpy.get_include()
    except AttributeError:
        return numpy.get_numpy_include()

# Define the extension module
_zernike = Extension(
    "_zernike",
    sources=["zernike.i", "zernike.cpp", "zernike_wrap.cpp"],
    include_dirs=[get_numpy_include(), ".", "../map2zernike/"],
)

# Setup function
setup(
    name="zernike",
    version="1.0.0",
    author="Manuel Zumbado",
    description="zernike provides a function: computeDescriptors()",
    long_description="A module for computing Zernike descriptors.",
    long_description_content_type="text/plain",
    ext_modules=[_zernike],
    install_requires=["numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
"""
