from lm.util import lm_tag_reader
from lm import lm_consts
from lm.type import lm_type_mat
import lm_tag_base

class CTag(lm_tag_base.CTag):

	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)

		self._data = []
		for info in d["mat_list"]:
			mat = lm_type_mat.CType((info["trans_x"], info["trans_y"]), (info["scale_x"], info["scale_y"]), (info["rotateskew_x"], info["rotateskew_y"]))
			self._data.append(mat)
		self._data = tuple(self._data)
		
	def get_val(self, idx):
		return self._data[idx]
	
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_MAT_LIST