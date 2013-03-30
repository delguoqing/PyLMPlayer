from lm import lm_consts
from lm.type import lm_type_img
from lm.util import lm_tag_reader

import lm_tag_base

class CTag(lm_tag_base.CTag):

	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		
		_data = []
		for info in d["img_list"]:
			fname = ctx.str_list.get_val(info["name_idx"])
			img = lm_type_img.CType(fname, info["img_idx"], info["width"], info["height"])
			_data.append(img)
		self.ctx = ctx
		self._data = tuple(_data)
			
	def get_val(self, idx):
		return self._data[idx]

	@classmethod	
	def get_id(self):
		return lm_consts.TAG_IMG_LIST