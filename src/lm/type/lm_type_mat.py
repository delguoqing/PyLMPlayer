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
	
	def __mul__(self, o):
		s = self.scale
		r = self.rotateskew
		t = self.translate
		
		s1 = o.scale
		r1 = o.rotateskew
		t1 = o.translate
		
		return CType(
			(s[0]*t1[0]+r[1]*t1[1]+t[0], r[0]*t1[0]+s[1]*t1[1]+t[1]),
			(s[0]*s1[0]+r[1]+r1[0], r[0]*r1[0]+s[1]*s1[1]),
			(r[0]*s1[0]+s[1]*r1[0], s[0]*r1[1]+r[1]*s1[1])
			)
	
	def get_transformed_point(self, x, y):
		return x * self.scale[0] + y * self.rotateskew[1] + self.translate[0],\
			y * self.scale[1] + x * self.rotateskew[0] + self.translate[1]
		
	def __str__(self):
		return "%f %f \n%f %f \n%f %f" % (self.translate + self.scale + self.rotateskew)
		
null_mat = CType((0.0, 0.0))