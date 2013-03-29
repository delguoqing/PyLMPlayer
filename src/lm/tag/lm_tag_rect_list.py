import lm_tag_reader
import lm_consts
import lm_type_rect

class CTag(object):

	def __init__(self, ctx, tag):
		fmt = ctx.format[self.get_id()]
		d = lm_tag_reader.read_tag(fmt, tag)
		
		self.ctx = ctx
		self._data = []
		for info in d["box_list"]:
			rect = lm_type_rect.CType(info["xmin"], info["ymin"], info["xmax"], info["ymax"])
			self._data.append(rect)
			
	def get_value(self, idx):
		return self._data[idx]
	
	def get_id(self):
		return lm_consts.TAG_RECT_LIST
			
			