import lm_tag_reader
import lm_consts
import lm_type_color

class CTag(object):
	
	def __init__(self, ctx, tag):
		fmt = ctx.format[self.get_id()]
		d = lm_tag_reader.read_tag(fmt, tag)
		
		self.ctx = ctx
		self._data = []
		for c in d["color_list"]:
			c = lm_type_color.CType(c["R"], c["G"], c["B"], c["A"])
			self._data.append(c)
		self._data = tuple(self._data)
		
	def get_val(self, idx):
		return self._data[idx]
		
	def get_id():
		return lm_consts.TAG_COLOR_LIST