from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='Cython preview_import_and_count',
    ext_modules=cythonize("mask.pyx", annotate=True, language_level=3),
    zip_safe=False,
    include_dirs=[numpy.get_include()],

)