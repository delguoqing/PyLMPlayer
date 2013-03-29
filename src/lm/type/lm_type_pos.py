import lm_type_mat

class CType(object):
	def __init__(self, x, y):
		self._x = x
		self._y = y
		
	def to_mat(self):
		return lm_type_mat.CType((self._x, self._y))