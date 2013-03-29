from lm import lm_consts
import lm_type_color
import lm_tag_base

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = CTag.parse_tag(ctx, tag)

		self._data = []
		for c in d["color_list"]:
			c = lm_type_color.CType(c["R"], c["G"], c["B"], c["A"])
			self._data.append(c)
		self._data = tuple(self._data)
		
	def get_val(self, idx):
		return self._data[idx]
	
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_COLOR_LIST