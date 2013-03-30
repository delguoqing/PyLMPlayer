import lm_tag_base

from lm import lm_consts
from lm.type import lm_type_pos
from lm.drawable import lm_shape_clipped_image
from lm.drawable import lm_shape_tiled_image
from lm.drawable import lm_shape_solid_color

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = CTag.parse_tag(ctx, tag)
		
		self.coords = [0] * 16
		
		u_min = min(d["u0"], d["u1"], d["u2"], d["u3"])
		u_max = max(d["u0"], d["u1"], d["u2"], d["u3"])
		v_min = min(d["v0"], d["v1"], d["v2"], d["v3"])
		v_max = max(d["v0"], d["v1"], d["v2"], d["v3"])
		
		for i in xrange(4):
			u = d["u%d" % i]
			v = d["v%d" % i]
			x = d["x%d" % i]
			y = d["y%d" % i]
			if u == u_min and v == v_min:
				self.coords[0*4+0] = x
				self.coords[0*4+1] = y
				self.coords[0*4+2] = u
				self.coords[0*4+3] = v
			elif u == u_max and v == v_min:
				self.coords[1*4+0] = x
				self.coords[1*4+1] = y
				self.coords[1*4+2] = u
				self.coords[1*4+3] = v
			elif u == u_max and v == v_max:
				self.coords[2*4+0] = x
				self.coords[2*4+1] = y
				self.coords[2*4+2] = u
				self.coords[2*4+3] = v
			elif u == u_min and v == v_max:
				self.coords[3*4+0] = x
				self.coords[3*4+1] = y
				self.coords[3*4+2] = u
				self.coords[3*4+3] = v
		
		self.fill_style = d["fill_style"]
		self.fill_idx = d["fill_idx"]
		
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_SHAPE
		
	def instantiate(self, parent=None):
		if self.fill_style == lm_consts.FILL_STYLE_SOLID_COLOR:
			color = self.ctx.color_list.get_val(self.fill_idx)
			shape = lm_shape_solid_color.CDrawable(color, self.coords, 
				parent=parent)
		elif self.fill_style == lm_consts.FILL_STYLE_CLIPPED_IMAGE:
			image = self.ctx.img_list.get_val(self.fill_idx)
			shape = lm_shape_clipped_image.CDrawable(image.get_texture(), 
				self.coords, parent=parent)
		elif self.fill_style == lm_consts.FILL_STYLE_TILED_IMAGE:
			image = self.ctx.img_list.get_val(self.fill_idx)
			shape = lm_shape_tiled_image.CDrawable(image.get_texture(), 
				self.coords, parent=parent)
		else:
			assert False, "not supported fill type! 0x%02x" % self.fill_style
		return shape