import ctypes
from pyglet.gl import *
# TODO:
#    1. May optimize this class by Cython?

class CType(object):
	
	def __init__(self, translate=None, scale=None, rotateskew=None):
		self._t = translate or (0.0, 0.0)
		self._s = scale or (1.0, 1.0)
		self._r = rotateskew or (0.0, 0.0)

	def _get_translate(self):
		return self._t
	
	def _set_translate(self, translate):
		self._t = translate

	translate = property(_get_translate, _set_translate)

	def _get_scale(self):
		return self._s
	
	def _set_scale(self, scale):
		self._s = scale

	scale = property(_get_scale, _set_scale)
	
	def _get_rotateskew(self):
		return self._r
	
	def _set_rotateskew(self, rotateskew):
		self._r = rotateskew

	rotateskew = property(_get_rotateskew, _set_rotateskew)
			
	def get_ctype(self):
		return (ctypes.c_float * 16)(
			self._s[0], self._r[0], 0, 0,
			self._r[1], self._s[1], 0, 0,
			0, 0, 1, 0,
			self._t[0], self._t[1], 0, 1,
		)
		
	def __repr__(self):
		return "%f %f \n%f %f \n%f %f" % (self._t + self._s + self._r)
		
	def __nonzero__(self):
		return self._t != (0.0, 0.0) \
			or self._s != (1.0, 1.0) \
			or self._r != (0.0, 0.0)

	# Multiply a by b and store result in self
	def mul(self, a, b):
		self._s = (a._s[0] * b._s[0] + a._r[1] * b._r[0],
			a._r[0] * b._r[1] + a._s[1] * b._s[1])
		self._t = (a._s[0] * b._t[0] + a._r[1] * b._t[1] + a._t[0],
			a._r[0] * b._t[0] + a._s[1] * b._t[1] + a._t[1])
		self._r = (a._s[0] * b._r[1] + a._r[1] * b._s[1],
			a._r[0] * b._s[0] + a._s[1] * b._r[0])
		
	# Transform a point
	def transform_point(self, p):
		x1 = p[0] * self._s[0] + p[1] * self._r[1] + self._t[0]
		y1 = p[0] * self._r[0] + p[1] * self._s[1] + self._t[1]
		return x1, y1
		
	# copy referrence of tuple, no problem
	def copy_from(self, o):
		self._r = o._r
		self._s = o._s
		self._t = o._t
		
	# Set up matrix transform in OpenGL
	def set(self):
		glPushMatrix()
		
		if self._r != (0.0, 0.0):
			glMultMatrixf(self.get_ctype())
		else:
			_t = self._t
			if _t != (0.0, 0.0):
				glTranslatef(_t[0], _t[1], 0.0)
			_s = self._s
			if _s != (1.0, 1.0):
				glScalef(_s[0], _s[1], 1.0)
	
	# Unset OpenGL state
	def unset(self):
		glPopMatrix()
		
null_mat = CType()