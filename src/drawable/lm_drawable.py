
class CDrawable(object):

	def __init__(self, parent=None):
		self.color_add = None
		self.color_mul = None
		self.matrix = None
		self.blend_mode = None
		self.depth = depth
		self.parent = parent
		
	def draw(self):
		raise NotImplementedError
	
	def set_cxform(self, cadd, cmul):
		self.color_add = cadd
		self.color_mul = cmul
		
	def set_matrix(self, matrix):
		self.matrix = matrix
			
	def set_blend_mode(self, mode):
		self.blend_mode = blend_mode
		
	def set_depth(self, depth):
		self.depth = depth
		
	def destroy(self):
		self.color_add = None
		self.color_mul = None
		self.matrix = None
		self.blend_mode = None
		self.parent = None