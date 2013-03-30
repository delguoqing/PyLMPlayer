from lm import lm_consts
from lm.util import lm_tag_reader
from lm.type import lm_type_pos

import lm_tag_base

class CTag(lm_tag_base.CTag):

	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		
		self._data = []
		for info in d["pos_list"]:
			pos = lm_type_pos.CType(info["x"], info["y"])
			self._data.append(pos)
		self._data = tuple(self._data)
		
	def get_val(self, idx):
		return self._data[idx]
		
	@classmethod
	def get_id(self):
		return lm_consts.TAG_POS_LIST