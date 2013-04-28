class CType(object):

	def __init__(self, r, g, b, a):
		self._r = r
		self._g = g
		self._b = b
		self._a = a
		
	def _get_r(self):
		return self._r
	r = property(_get_r)
	def _get_g(self):
		return self._g
	g = property(_get_g)
	def _get_b(self):
		return self._b
	b = property(_get_b)
	def _get_a(self):
		return self._a
	a = property(_get_a)
	def _get_rB(self):
		return int(self._r * 255)
	rB = property(_get_rB)
	def _get_gB(self):
		return int(self._g * 255)
	gB = property(_get_gB)
	def _get_bB(self):
		return int(self._b * 255)
	bB = property(_get_bB)
	def _get_aB(self):
		return int(self._a * 255)
	aB = property(_get_aB)
	
	def mul(self, a, b):
		self._r = a._r * b._r
		self._g = a._g * b._g
		self._b = a._b * b._b
		self._a = a._a * b._a

	def add(self, a, b):
		self._r = a._r + b._r
		self._g = a._g + b._g
		self._b = a._b + b._b
		self._a = a._a + b._a
		
	def __repr__(self):
		return "(%.2f, %.2f, %.2f, %.2f)" % (self.r, self.g, self.b, self.a)
	def __eq__(self, o):
		return (self._r == o._r and self._g == o._g and self._b == o._b and self._a == o._a)
		
	def __ne__(self, o):
		return self._r != o._r or self._g != o._g or self._b != o._b or self._a != o._a
		
	def copy_from(self, o):
		self._r = o._r
		self._g = o._g
		self._b = o._b
		self._a = o._a
	
	def zero(self):
		self._r = self._g = self._b = self._a = 0