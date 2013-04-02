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
		
		self.coords = [0] * 16
		
		x_min = min(d["x0"], d["x1"], d["x2"], d["x3"])
		x_max = max(d["x0"], d["x1"], d["x2"], d["x3"])
		y_min = min(d["y0"], d["y1"], d["y2"], d["y3"])
		y_max = max(d["y0"], d["y1"], d["y2"], d["y3"])
		
		self._rect = lm_type_rect.CType(x_min, y_min, x_max, y_max)
				
		self.fill_style = d["fill_style"]
		self.fill_idx = d["fill_idx"]
		
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_SHAPE
		
	def instantiate(self, parent=None):
		if self.fill_style == lm_consts.FILL_STYLE_SOLID_COLOR:
			color = self.ctx.color_list.get_val(self.fill_idx)
			shape = lm_shape_solid_color.CDrawable(color, self._rect, 
				parent=parent)
		elif self.fill_style == lm_consts.FILL_STYLE_CLIPPED_IMAGE:
			image = self.ctx.img_list.get_val(self.fill_idx)
			shape = lm_shape_clipped_image.CDrawable(image.get_texture(), 
				self._rect, parent=parent)
		elif self.fill_style == lm_consts.FILL_STYLE_TILED_IMAGE:
			image = self.ctx.img_list.get_val(self.fill_idx)
			shape = lm_shape_tiled_image.CDrawable(image.get_texture(), 
				self._rect, parent=parent)
		else:
			assert False, "not supported fill type! 0x%02x" % self.fill_style
		return shape