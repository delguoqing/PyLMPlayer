import pyglet
import lm_tag_base

from lm import lm_consts
from lm.type import lm_type_pos
from lm.type import lm_type_rect
from lm.drawable import lm_shape_clipped_image
from lm.drawable import lm_shape_tiled_image
from lm.drawable import lm_shape_solid_color

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = CTag.parse_tag(ctx, tag)
		
		x_min = min(d["x0"], d["x1"], d["x2"], d["x3"])
		x_max = max(d["x0"], d["x1"], d["x2"], d["x3"])
		y_min = min(d["y0"], d["y1"], d["y2"], d["y3"])
		y_max = max(d["y0"], d["y1"], d["y2"], d["y3"])
		
		self._rect = lm_type_rect.CType(x_min, y_min, x_max, y_max)
				
		self.fill_style = d["fill_style"]
		self.fill_idx = d["fill_idx"]
		
		self.color = None 
		self.texture = None
		self.tex_coords = None
		if self.fill_style == lm_consts.FILL_STYLE_SOLID_COLOR:
			self.color = self.ctx.color_list.get_val(self.fill_idx)
		else:
			self.texture = self.ctx.img_list.get_val(self.fill_idx)
			self.tex_coords = self.texture.tex_coords
		
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_SHAPE2
		
	def instantiate(self, inst_id, depth, parent=None):
		if self.fill_style == lm_consts.FILL_STYLE_SOLID_COLOR:
			shape = lm_shape_solid_color.CDrawable(self.color, self._rect, 
				inst_id, depth, parent=parent)
		elif self.fill_style == lm_consts.FILL_STYLE_CLIPPED_IMAGE:
			image = self.ctx.img_list.get_val(self.fill_idx)
			shape = lm_shape_clipped_image.CDrawable(self.texture, 
				self._rect, self.tex_coords, inst_id, depth, parent=parent)
		elif self.fill_style == lm_consts.FILL_STYLE_TILED_IMAGE:
			image = self.ctx.img_list.get_val(self.fill_idx)
			shape = lm_shape_tiled_image.CDrawable(self.texture, 
				self._rect, self.tex_coords, inst_id, depth, parent=parent)
		else:
			assert False, "not supported fill type! 0x%02x" % self.fill_style
		return shape