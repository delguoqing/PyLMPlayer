import lm_tag_reader
import lm_consts
import lm_type_pos

class CTag(object):

	def __init__(self, ctx, tag):
		fmt = ctx.format[self.get_id()]
		d = lm_tag_reader.read_tag(fmt, tag)
		
		self.ctx = ctx
		self._data = []
		for info in d["pos_list"]:
			pos = lm_type_pos.CType(info["x"], info["y"])
			self._data.append(pos)
		self._data = tuple(self._data)
		
	def get_val(self, idx):
		return self._data[idx]
		
	def get_as_mat(self, idx):
		# TODO
		raise NotImplementedError
		
	def get_id(self):
		return lm_consts.TAG_POS_LIST