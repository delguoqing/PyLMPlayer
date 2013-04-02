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
		
		self._cadd = None
		if d["color_add_idx"] >= 0:
			self._cadd = self.ctx.color_list.get_val(d["color_add_idx"])
		
		self._cmul = None
		if d["color_mul_idx"] >= 0:
			self._cmul = self.ctx.color_list.get_val(d["color_mul_idx"])
		
		self._clip_action_cnt = d["clip_action_cnt"]
		self._clip_action_tags = []
		
	def add_sub_tag(self, tag):
		self._clip_action_tags.append(tag)
		
	def get_sub_tag_cnt(self):
		return self._clip_action_cnt
		
	def _get_matrix(self, trans_idx):
		ctx = self.ctx
		if trans_idx == -1:
			return None
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
		
	# Execute Place Object(3) Tag
	#    1. it may change the status of an exsiting character
	#    2. or it may add a new character to the timeline
	#
	# Notice:
	#	a new character replacing an old character which has no matrix(cxform) 
	# will have to use the old character's matrix(cxform)
	def execute(self, target=None):
		# Must have a target
		if not target: return
		
		old_inst = target.get_drawable(self._depth)
		if self._has_char:
			char_tag = self.ctx.get_character(self._char_id)
			inst = char_tag.instantiate(parent=target)
			target.add_drawable(inst, self._depth)
		else:
			inst = target.get_drawable(self._depth)
			
		if self._mat:
			inst.set_matrix(self._mat)
		elif old_inst:
			inst.set_matrix(old_inst.get_matrix())
			
		if self._cadd or self._cmul:
			inst.set_cxform(self._cadd, self._cmul)
		elif old_inst:
			inst.set_cxform(old_inst.get_color_add(), old_inst.get_color_mul())
			
		if self._has_char and old_inst:
			old_inst.destroy()
			
		inst.set_blend_mode(self._blend_mode)
	
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_PLACE_OBJ