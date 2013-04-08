from lm import lm_consts
from lm.util import lm_tag_reader
from lm.type import lm_type_rect

import lm_tag_base

class CTag(lm_tag_base.CTag):

	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		
		self._data = []
		for info in d["box_list"]:
			rect = lm_type_rect.CType(info["xmin"], info["ymin"], info["xmax"], info["ymax"])
			self._data.append(rect)
			
	def get_val(self, idx):
		return self._data[idx]
	
	
	def get_id(self):
		return lm_consts.TAG_RECT_LIST
			
			