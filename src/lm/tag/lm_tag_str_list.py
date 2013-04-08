from lm.util import lm_tag_reader
from lm import lm_consts
import lm_tag_base

class CTag(lm_tag_base.CTag):

	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		
		self._data = []
		for info in d["symbol_list"]:
			self._data.append(info["symbol"] or "")
		self._data = tuple(self._data)
			
	def get_val(self, idx):
		return self._data[idx]
	
	
	def get_id(cls):
		return lm_consts.TAG_STR_LIST
		
	def get_ctx(self):
		return self.ctx