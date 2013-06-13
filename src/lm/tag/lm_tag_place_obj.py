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
		self._clip_depth = d["clip_depth"]	# how to impl?
		
		self._clip_action_cnt = d["clip_action_cnt"]
		self._clip_action_tags = []
		
		# Check if multiple clip action ever appears
		assert self._clip_action_cnt <= 1
		
		# Generated from clip action tags
		# The only known type: on_enter_frame
		self._on_enter_frame = None
		
		# C level data
		self._mat_index = self._get_matrix_index(d["trans_idx"])
		self._blend_mode_index = d["blend_mode"]
		if d["color_add_idx"] >= 0:
			self._cadd_index = self.ctx.color_list.beg_index + d["color_add_idx"]
		else:
			self._cadd_index = -1
		if d["color_mul_idx"] >= 0:
			self._cmul_index = self.ctx.color_list.beg_index + d["color_mul_idx"]
		else:
			self._cmul_index = -1
		
	def add_sub_tag(self, tag):
		self._clip_action_tags.append(tag)
		
		# Check if other clip event type than 'onEnterFrame' ever exists
		assert tag.clip_event_flag == 2
		self._on_enter_frame = self.ctx.as_list.get_val(tag.as_idx)
		
	def get_sub_tag_cnt(self):
		return self._clip_action_cnt

	def _conv_special_trans_idx(self, trans_idx):
		ctx = self.ctx
		size = 0
		for vname, size, fmt in ctx.format.DATA[self.get_id()]:
			if vname == "trans_idx":
				break
		mask = (1 << (size * 8 - 1))-1
		return trans_idx & mask
		
	def _get_matrix_index(self, trans_idx):
		ctx = self.ctx
		if trans_idx == -1:
			return -1
		elif trans_idx >= 0:
			return ctx.mat_list.beg_index + trans_idx
		else:
			pos_idx = self._conv_special_trans_idx(trans_idx)
			return ctx.pos_list.beg_index + pos_idx
			
	# Execute Place Object(3) Tag
	#	1. it may change the status of an exsiting character
	#	2. or it may add a new character to the timeline
	#
	# Notice:
	#	a new character replacing an old character which has no matrix(cxform) 
	# will have to use the old character's matrix(cxform)
	def execute(self, target=None):
		# Must have a target
		if not target: return
		
		# Old Character at `depth`
		old_inst = target.get_drawable(self._depth)
			
		# Matrix and Cxform
		_mat = self._mat_index
		_cadd = self._cadd_index
		_cmul = self._cmul_index
		_blend_mode = self._blend_mode_index
		if old_inst:
			if _mat == -1: _mat = old_inst.matrix_index
			if _cadd == -1: _cadd = old_inst.color_add_index
			if _cmul == -1: _cmul = old_inst.color_mul_index
			if _blend_mode <= 1: _blend_mode = old_inst.blend_mode_index
		
		# Place or Move?
		if self._has_char:
		
			if not old_inst or old_inst.inst_id != self._inst_id:
				# remove old if any
				target.remove_drawable(self._depth)
				
				# try allocate from cache
				inst = target.alloc_drawable(self._depth, self._inst_id)
				if not inst:		
					char_tag = self.ctx.get_character(self._char_id)
					if not char_tag: return
					inst = char_tag.instantiate(self._inst_id, self._depth, parent=target)
					inst.char_id = self._char_id
				inst.init()
				target.add_drawable(inst, self._depth, self._name)
				
				if self._on_enter_frame:
					inst.onEnterFrame = self._on_enter_frame
				
			else:	# reuse the old inst
				inst = old_inst

		else:
			if old_inst and old_inst.forbid_timeline:
				return
			inst = target.get_drawable(self._depth)
			if inst is None:
				return
		
		# Set Matrix and Cxform	
		inst.set_matrix_index(_mat)
		inst.set_cxform_index(_cadd, _cmul)
		inst.set_blend_mode_index(_blend_mode)
		inst.clip_depth = self._clip_depth
	
		# Set instance ID			
		if self._char_id >= 0:
			inst.char_id = self._char_id
			
	def get_id(cls):
		return lm_consts.TAG_PLACE_OBJ