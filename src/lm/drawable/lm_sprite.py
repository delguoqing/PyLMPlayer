from lm.type import lm_type_color
import lm_drawable

from pyglet.gl import *
from lm import lm_consts

class CDrawable(lm_drawable.CDrawable):
		
	def __init__(self, vertex_lists, rect, inst_id, depth, parent=None):
		super(CDrawable, self).__init__(inst_id, depth, parent)
		self._rect = rect
		self._vertex_lists = vertex_lists
		
	def old_update(self, render_state, operation=lm_consts.MASK_ALL):
		if (operation & lm_consts.MASK_DRAW) == 0:
			return
			
		render_state.push_matrix(self.matrix)
		render_state.push_cxform(self.color_add, self.color_mul)
		render_state.push_blend_mode(self.blend_mode)

		for shape_tag in self._vertex_lists:
			render_state.draw_image(shape_tag.texture, shape_tag.vertices, shape_tag.tex_coords)
				
		render_state.pop_matrix()
		render_state.pop_cxform()
		render_state.pop_blend_mode()	
		
	def update(self, render_state, operation=lm_consts.MASK_ALL):
		if (operation & lm_consts.MASK_DRAW) == 0:
			return
			
		render_state.push_state(self.color_add_index, self.color_mul_index,
								 self.matrix_index, self.blend_mode_index)

		for shape_tag in self._vertex_lists:
			tex = shape_tag.texture
			for i in xrange(len(shape_tag.coords_index)):
				render_state.draw_image(tex.target, tex.id,
										shape_tag.coords_index[i], shape_tag.tex_coords_index[i])
			
		render_state.pop_state()