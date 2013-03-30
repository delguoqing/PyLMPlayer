import ctypes

class CType(object):
	
	def __init__(self, translate, scale=None, rotateskew=None):
		self.translate = translate or (0.0, 0.0)
		self.scale = scale or (1.0, 1.0)
		self.rotateskew = rotateskew or (0.0, 0.0)
		
	def get_ctype(self):
		return (ctypes.c_float * 16)(
			self.scale[0], self.rotateskew[0], 0, 0,
			self.rotateskew[1], self.scale[1], 0, 0,
			0, 0, 1, 0,
			self.translate[0], self.translate[1], 0, 1,
		)
		
null_mat = CType((0.0, 0.0))