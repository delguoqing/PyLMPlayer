from lm import lm_consts
from lm.type import lm_type_pos

import lm_tag_base

class CTag(lm_tag_base.CTag):

	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		
		# Python level data		
		self._data = []
		for info in d["pos_list"]:
			pos = lm_type_pos.CType(info["x"], info["y"])
			self._data.append(pos)
		self._data = tuple(self._data)
		# C level data
		self.beg_index = self.register_all()
		
	def register_all(self):
		renderer = self.ctx.renderer
		for pos in self._data:
			index = renderer.reg_mat(pos._x, pos._y, 1.0, 1.0, 0.0, 0.0)
		return index - len(self._data) + 1
	
	def get_val(self, idx):
		return self._data[idx]	
	
	def get_id(self):
		return lm_consts.TAG_POS_LIST