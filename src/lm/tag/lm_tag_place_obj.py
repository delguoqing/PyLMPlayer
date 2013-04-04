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
		
		# Check if multiple clip action ever appears
		assert self._clip_action_cnt <= 1
		
		# Generated from clip action tags
		# The only known type: on_enter_frame
		self._on_enter_frame = None
		
	def add_sub_tag(self, tag):
		self._clip_action_tags.append(tag)
		
		# Check if other clip event type than 'onEnterFrame' ever exists
		
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
		_mat = self._mat
		_cadd = self._cadd
		_cmul = self._cmul
		if old_inst:
			_mat = _mat or old_inst.get_matrix()
			_cadd = _cadd or old_inst.get_color_add()
			_cmul = _cmul or old_inst.get_color_mul()
		
		# Place or Move?
		if self._has_char:
		
			if not old_inst or old_inst.inst_id != self._inst_id:
				# remove old if any
				target.remove_drawable(self._depth)
				
				# try allocate from cache
				inst = target.alloc_drawable(self._depth, self._inst_id)
				if not inst:		
					char_tag = self.ctx.get_character(self._char_id)
					inst = char_tag.instantiate(self._inst_id, self._depth, parent=target)

				target.add_drawable(inst, self._depth, self._name)
				
			else:	# reuse the old inst
				inst = old_inst
		else:
			inst = target.get_drawable(self._depth)
#			print "move old at depth%d" % self._depth
		
		# Set Matrix and Cxform	
		inst.set_matrix(_mat)
		inst.set_cxform(_cadd, _cmul)
		inst.set_blend_mode(self._blend_mode)
		
		if self._char_id >= 0:
			inst.char_id = self._char_id
			
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_PLACE_OBJ