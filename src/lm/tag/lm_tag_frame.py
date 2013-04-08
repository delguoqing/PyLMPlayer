import lm_tag_base
from lm import lm_consts

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		
		self._frame_id = d["frame_id"]
		self._cmd_cnt = d["cmd_cnt"]
		self._ctrl_tags = []
		
		self._action_tags = []
		
	# 0 based frame id
	def get_frame_id(self):
		return self._frame_id
		
	def add_sub_tag(self, tag):
		if tag.get_id() == lm_consts.TAG_DO_ACTION:
			self._action_tags.append(tag)
		else:
			self._ctrl_tags.append(tag)
		
	def get_sub_tag_cnt(self):
		return self._cmd_cnt
		
	# Execute tags
	# First non-actionscripts
	# Second actionscripts
	def execute(self, target=None):
		# Must have a target!
		if not target: return
		
		for tag in self._ctrl_tags:
			tag.execute(target=target)
			
		for tag in self._action_tags:
			tag.execute(target=target)
		
	
	def get_id(cls):
		return lm_consts.TAG_FRAME