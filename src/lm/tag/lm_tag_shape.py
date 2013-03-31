import pyglet
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
		
		x_min = min(d["x0"], d["x1"], d["x2"], d["x3"])
		x_max = max(d["x0"], d["x1"], d["x2"], d["x3"])
		y_min = min(d["y0"], d["y1"], d["y2"], d["y3"])
		y_max = max(d["y0"], d["y1"], d["y2"], d["y3"])
		
		for i in xrange(4):
			u = d["u%d" % i]
			v = d["v%d" % i]
			x = d["x%d" % i]
			y = d["y%d" % i]
			if x == x_min and y == y_min:
				self.coords[0*4+0] = x
				self.coords[0*4+1] = y
				self.coords[0*4+2] = 0
				self.coords[0*4+3] = 0
			elif x == x_max and y == y_min:
				self.coords[1*4+0] = x
				self.coords[1*4+1] = y
				self.coords[1*4+2] = 1
				self.coords[1*4+3] = 0
			elif x == x_max and y == y_max:
				self.coords[2*4+0] = x
				self.coords[2*4+1] = y
				self.coords[2*4+2] = 1
				self.coords[2*4+3] = 1
			elif x == x_min and y == y_max:
				self.coords[3*4+0] = x
				self.coords[3*4+1] = y
				self.coords[3*4+2] = 0
				self.coords[3*4+3] = 1
		
		self.fill_style = d["fill_style"]
		self.fill_idx = d["fill_idx"]
		coords = self.coords
		
		if self.fill_style == lm_consts.FILL_STYLE_SOLID_COLOR:
			color = self.ctx.color_list.get_val(self.fill_idx)
			self._vertex_list = pyglet.graphics.vertex_list(4,
				("v2f/static", (coords[0], coords[1], coords[4], 
					coords[5], coords[8], coords[9], coords[12], coords[13])),
				("c4B/static", (color.rB, color.gB, color.bB, color.aB) * 4),
			)
		else:
			self._vertex_list = pyglet.graphics.vertex_list(4,
				("v2f/static", (coords[0], coords[1], coords[4], coords[5],
					coords[8], coords[9], coords[12], coords[13])),
				("t2f/static", (coords[2], coords[15], coords[6], coords[11],
					coords[10], coords[7], coords[14], coords[3])),
			)
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_SHAPE
		
	def instantiate(self, parent=None):
		if self.fill_style == lm_consts.FILL_STYLE_SOLID_COLOR:
			shape = lm_shape_solid_color.CDrawable(self._vertex_list,
				parent=parent)
		elif self.fill_style == lm_consts.FILL_STYLE_CLIPPED_IMAGE:
			image = self.ctx.img_list.get_val(self.fill_idx)
			shape = lm_shape_clipped_image.CDrawable(image.get_texture(), 
				self._vertex_list, parent=parent)
		elif self.fill_style == lm_consts.FILL_STYLE_TILED_IMAGE:
			image = self.ctx.img_list.get_val(self.fill_idx)
			shape = lm_shape_tiled_image.CDrawable(image.get_texture(), 
				self._vertex_list, parent=parent)
		else:
			assert False, "not supported fill type! 0x%02x" % self.fill_style
		return shape