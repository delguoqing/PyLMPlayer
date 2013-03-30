from lm.util import lm_tag_reader
from lm.type import lm_type_mat, lm_type_blend_mode
from lm import lm_consts


import lm_tag_base

class CTag(lm_tag_base.CTag):
	
	# ALL Character Tag should have a method called `instantiate`!
	# And the we need a character dictionary 
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		
		self._char_id = d["character_id"]
		self._inst_id = d["inst_id"]
		self._has_char = (self._char_id > 0)
		self._depth = d["depth"]
		self._name = ctx.str_list.get_val(d["name_idx"])
		self._mat = self._get_matrix(d["trans_idx"])
		self._blend_mode = lm_type_blend_mode.CType(d["blend_mode"])
		self._clip_depth = d["clip_depth"]	# how to impl?
		
	def _get_matrix(self, trans_idx):
		ctx = self.ctx
		if trans_idx == -1:
			return lm_type_mat.null_mat
		elif trans_idx >= 0:
			return ctx.mat_list.get_val(trans_idx)
		else:
			size = 0
			for vname, size, fmt in ctx.format.DATA[self.get_id()]:
				if vname == "trans_idx":
					break
			mask = (1 << (size * 8 - 1))-1
			trans_idx &= mask
			return ctx.pos_list.get_val(trans_idx).to_mat()
			
	def execute(self, env):
		target = env.get_target()
		
		char_dict = self.ctx["char_dict"]
		char_tag = char_dict.get(self._char_id)
		
		char_tag.instantiate()
	
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_PLACE_OBJ