import lm_drawable
from lm import lm_consts

class CDrawable(lm_drawable.CDrawable):
		
	def __init__(self, vertex_lists, rect_index, inst_id, depth, parent=None):
		super(CDrawable, self).__init__(inst_id, depth, parent)
		self._rect_index = rect_index
		self._vertex_lists = vertex_lists
		
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