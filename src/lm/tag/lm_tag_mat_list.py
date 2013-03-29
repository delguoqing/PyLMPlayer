from lm.util import lm_tag_reader
from lm import lm_consts
import lm_type_mat

class CTag(object):

	def __init__(self, ctx, tag):
		fmt = ctx.format[self.get_id()]
		d = lm_tag_reader.read_tag(fmt, tag)
		
		self.ctx = ctx
		self._data = []
		for info in d["mat_list"]:
			mat = lm_type_mat.CType((info["trans_x"], info["trans_y"]), (info["scale_x"], info["scale_y"]), (info["rotateskew_x"], info["rotateskew_y"]))
			self._data.append(mat)
		self._data = tuple(self._data)
		
	def get_val(self, idx):
		return self._data[idx]
		
	def get_id(self):
		return lm_consts.TAG_MAT_LIST