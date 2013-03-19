import lm_tag_reader
import lm_consts

class CTag(object):

	def __init__(self, ctx, tag):
		fmt = ctx.format[self.get_id()]
		d = lm_tag_reader.read_tag(fmt, tag)
		
		self.ctx = ctx
		self._data = []
		for info in d["symbol_list"]:
			self._data.append(info["symbol"])
		self._data = tuple(self._data)
			
	def get_val(self, idx):
		return self._data[idx]
	
	def get_id(self):
		return lm_consts.TAG_STR_LIST
		
	def get_ctx(self):
		return self.ctx