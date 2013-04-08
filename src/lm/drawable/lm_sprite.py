from lm.type import lm_type_color
import lm_drawable

from pyglet.gl import *

class CDrawable(lm_drawable.CDrawable):
		
	def __init__(self, vertex_lists, rect, inst_id, depth, parent=None):
		super(CDrawable, self).__init__(inst_id, depth, parent)
		self._rect = rect
		self._vertex_lists = vertex_lists
		
	def draw(self, render_state):
		render_state.push_matrix(self.matrix)
		render_state.push_cxform(self.color_add, self.color_mul)
		render_state.push_blend_mode(self.blend_mode)

		for is_image, vertex_list in self._vertex_lists:
			if is_image:
				render_state.draw_image(vertex_list)
			else:
				render_state.draw_solid(vertex_list)
				
		render_state.pop_matrix()
		render_state.pop_cxform()
		render_state.pop_blend_mode()	
		