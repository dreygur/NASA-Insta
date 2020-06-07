from distutils.core import setup
from Cython.Build import cythonize

setup(name="Json to CSV App",
	ext_modules=cythonize("app.pyx"))