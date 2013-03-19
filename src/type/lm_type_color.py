class CType(object):

	def __init__(self, r, g, b, a):
		self._val = (r << 24) | (g << 16) | (b << 8) | (a << 0)