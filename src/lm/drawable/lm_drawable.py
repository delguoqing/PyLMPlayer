from lm.type import lm_type_color
from lm.type import lm_type_blend_mode
from lm.type import lm_type_mat

import pyglet
import lm_render_state

class CDrawable(object):

	def __init__(self, parent=None):
		self.color_add = lm_type_color.null_cadd
		self.color_mul = lm_type_color.null_cmul
		self.matrix = lm_type_mat.null_mat
		self.blend_mode = lm_type_blend_mode.null_blend
		self.depth = None
		self.parent = parent

		self._is_cxform_dirty = True
		self._tot_cadd = None
		self._tot_cmul = None
		self._super_cadd = lm_type_color.null_cadd
		self._super_cmul = lm_type_color.null_cmul
		
		self._is_mat_dirty = True
		self._tot_mat = None
		self._super_mat = lm_type_mat.null_mat
		
		if parent is None:
			self._batch = pyglet.graphics.Batch()
			self._render_state = lm_render_state.CObj()
		else:
			self._batch = self.parent._batch
			
	def draw(self, render_state):
		raise NotImplementedError
	
	def set_cxform(self, cadd, cmul):
		if cadd:
			self.color_add = cadd
			self._is_cxform_dirty = True
		if cmul:
			self.color_mul = cmul
			self._is_cxform_dirty = True
	
	def get_color_add(self):
		return self.color_add
		
	def get_color_mul(self):
		return self.color_mul
				
	def apply_cxform(self, cadd, cmul):
		if cadd:
			self._super_cadd = cadd
			self._is_cxform_dirty = True
		if cmul:
			self._super_cmul = cmul
			self._is_cxform_dirty = True
		
	def _update_cxform(self):
		self._tot_cadd = self.color_add * self._super_cmul + self._super_cadd
		self._tot_cmul = self.color_mul * self._super_cmul		
			
	def apply_matrix(self, matrix):
		if matrix:
			self._super_mat = matrix
			self._is_mat_dirty = True
		
	def set_matrix(self, matrix):
		if matrix:
			self.matrix = matrix
			self._is_mat_dirty = True
			
	def _update_matrix(self):
		self._tot_mat = self._super_mat * self.matrix
		
#		print "matrix multiply:"
#		print self._super_mat
#		print "-" * 10
#		print self.matrix
#		print "-" * 10		
#		print self._tot_mat
#		print "================"
		
	def get_matrix(self):
		return self.matrix
		
	def refresh(self):
		if self._is_cxform_dirty:
			self._update_cxform()
		if self._is_mat_dirty:
			self._update_matrix()
		self._is_cxform_dirty = self._is_mat_dirty = False
			
	def set_blend_mode(self, blend_mode):
		self.blend_mode = blend_mode
		
	def set_depth(self, depth):
		self.depth = depth
		
	def destroy(self):
		self.color_add = None
		self.color_mul = None
		self.matrix = None
		self.blend_mode = None
		self.parent = None