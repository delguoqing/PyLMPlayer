from lm.type import lm_type_color
import lm_drawable

from pyglet.gl import *

class CDrawable(lm_drawable.CDrawable):
		
	def __init__(self, vertex_lists, rect, inst_id, depth, parent=None):
		super(CDrawable, self).__init__(inst_id, depth, parent)
		self._rect = rect
		self._vertex_lists = vertex_lists
		
	def update(self, render_state, operation=0x3):
		if (operation & 0x2) == 0:
			return
			
		render_state.push_matrix(self.matrix)
		render_state.push_cxform(self.color_add, self.color_mul)
		render_state.push_blend_mode(self.blend_mode)

		for vertices, tex_coords, texture in self._vertex_lists:
			render_state.draw_image(texture, vertices, tex_coords)
				
		render_state.pop_matrix()
		render_state.pop_cxform()
		render_state.pop_blend_mode()	
		