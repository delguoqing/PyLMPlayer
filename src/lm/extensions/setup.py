from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("lm_render_state",
						 ["lm_render_state.pyx"],
						 language="c++",
						 #include_dirs=[r"C:\MinGW\include\GL"],
						 libraries = ['opengl32', 'glew32'])]

setup(
	name = 'LM Render State',
	cmdclass = {'build_ext': build_ext},
	ext_modules = ext_modules,	
)