class CType(object):

	def __init__(self, r, g, b, a):
		self._r = min(r, 1.0)
		self._g = min(g, 1.0)
		self._b = min(b, 1.0)
		self._a = min(a, 1.0)
		
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
	
	def mul(self, other, output):
		output._r = self._r * other._r
		output._g = self._g * other._g
		output._b = self._b * other._b
		output._a = self._a * other._a

	def add(self, other, output):
		output._r = min(self._r + other._r, 1.0)
		output._g = min(self._g + other._g, 1.0)
		output._b = min(self._b + other._b, 1.0)
		output._a = min(self._a + other._a, 1.0)
		
	def __str__(self):
		return "(%.2f, %.2f, %.2f, %.2f)" % (self.r, self.g, self.b, self.a)
	def __eq__(self, o):
		return self._r == o._r and self._g == o._g and self._b == o._b and self._a == o._a
null_cadd = CType(0.0, 0.0, 0.0, 0.0)
null_cmul = CType(1.0, 1.0, 1.0, 1.0)
