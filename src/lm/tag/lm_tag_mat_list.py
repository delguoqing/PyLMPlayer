from lm.util import lm_tag_reader
from lm import lm_consts
from lm.type import lm_type_mat
import lm_tag_base

class CTag(lm_tag_base.CTag):

	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)

		# Python level data
		self._data = []
		for info in d["mat_list"]:
			mat = lm_type_mat.CType((info["trans_x"], info["trans_y"]), (info["scale_x"], info["scale_y"]), (info["rotateskew_x"], info["rotateskew_y"]))
			self._data.append(mat)
		self._data = tuple(self._data)
		# C level data
		self.beg_index = self.register_all()
		
	def register_all(self):
		renderer = self.ctx.renderer
		index = 0
		for mat in self._data:
			t0, t1 = mat.translate
			s0, s1 = mat.scale
			r0, r1 = mat.rotateskew
			index = renderer.reg_mat(t0, t1, s0, s1, r0, r1)
		return index - len(self._data) + 1
		
	def get_val(self, idx):
		return self._data[idx]
	
	def get_id(cls):
		return lm_consts.TAG_MAT_LIST