#! /usr/bin/env python

# System imports
from distutils.core import *
from distutils      import sysconfig

# Third-party modules - we depend on numpy for everything
import numpy

# Obtain the numpy include directory.  This logic works across numpy versions.
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()

# view extension module
_zernike = Extension("_zernike",
                   sources = ["zernike.cpp", "zernike_wrap.cpp"],
                   include_dirs = [numpy_include, ".", "../map2zernike/"]
                   )

# NumyTypemapTests setup
setup(  name        = "zernike module",
        description = "zernike provides a function: computeDescriptors()",
        author      = "Manuel Zumbado",
        version     = "1.0",
        ext_modules = [_zernike],
        )
