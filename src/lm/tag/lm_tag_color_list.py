from lm import lm_consts
from lm.type import lm_type_color
import lm_tag_base

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)

		# Python level data
		self._data = []
		for c in d["color_list"]:
			c = lm_type_color.CType(c["R"]/256.0, c["G"]/256.0, c["B"]/256.0, c["A"]/256.0)
			self._data.append(c)
		self._data = tuple(self._data)
		# C level data
		self.beg_index = self.register_all()
		
	def register_all(self):
		renderer = self.ctx.renderer
		for color in self._data:
			index = renderer.reg_color(color.r, color.g, color.b, color.a)
		return index + 1 - len(self._data)
		
	def get_val(self, idx):
		return self._data[idx]	
	
	def get_id(cls):
		return lm_consts.TAG_COLOR_LIST