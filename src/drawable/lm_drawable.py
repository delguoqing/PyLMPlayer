import type.lm_type_color as lm_type_color

class CDrawable(object):

	def __init__(self, parent=None):
		self.color_add = lm_type_color.null_cadd
		self.color_mul = lm_type_color.null_cmul
		self.matrix = None
		self.blend_mode = None
		self.depth = None
		self.parent = parent

		self._is_dirty = True
		self._tot_cadd = None
		self._tot_cmul = None
		self._super_cadd = lm_type_color.null_cadd
		self._super_cmul = lm_type_color.null_cmul
		self._update_cxform()
				
	def draw(self):
		raise NotImplementedError
	
	def set_cxform(self, cadd, cmul):
		self.color_add = cadd or lm_type_color.null_cadd
		self.color_mul = cmul or lm_type_color.null_cmul
		self._update_cxform()
	
	def apply_cxform(self, cadd, cmul):
		self._super_cadd = cadd
		self._super_cmul = cmul
		self._update_cxform()
		
	def _update_cxform(self):
		self._tot_cadd = self.color_add * self._super_cmul + self._super_cadd
		self._tot_cmul = self.color_mul * self._super_cmul
		self._is_dirty = True
			
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