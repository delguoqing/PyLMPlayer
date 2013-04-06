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
	
	def __mul__(self, o):
		s = self._s
		r = self._r
		t = self._t
		
		s1 = o._s
		r1 = o._r
		t1 = o._t
		
		return CType(
			(s[0]*t1[0]+r[1]*t1[1]+t[0], r[0]*t1[0]+s[1]*t1[1]+t[1]),
			(s[0]*s1[0]+r[1]+r1[0], r[0]*r1[0]+s[1]*s1[1]),
			(r[0]*s1[0]+s[1]*r1[0], s[0]*r1[1]+r[1]*s1[1])
			)
	
	def get_transformed_point(self, x, y):
		return \
			(int(x*self._s[0] + y*self._r[1] + self._t[0]),
			int(y*self._s[1] + x*self._r[0] + self._t[1]))
		
	def copy_from(self, other):
		self._t = other._t
		self._s = other._s
		self._r = other._r
		
	def __str__(self):
		return "%f %f \n%f %f \n%f %f" % (self._t + self._s + self._r)
		
	def __nonzero__(self):
		return self._t != (0.0, 0.0) \
			or self._s != (1.0, 1.0) \
			or self._r != (0.0, 0.0)
		
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