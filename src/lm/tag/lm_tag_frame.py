import lm_tag_base
import lm_tag_place_obj

from lm import lm_consts


class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		
		self._frame_id = d["frame_id"]
		self._cmd_cnt = d["cmd_cnt"]
		self._ctrl_tags = []
		self._as_tags = []
		self._allowed_depth = set()
	# 0 based frame id
	def get_frame_id(self):
		return self._frame_id
		
	def add_sub_tag(self, tag):
		if tag.get_id() == lm_consts.TAG_DO_ACTION:
			self._as_tags.append(tag)
		else:
			self._ctrl_tags.append(tag)
		if len(self._ctrl_tags) + len(self._as_tags) == self.get_sub_tag_cnt():
			self._calc_allowed_depth()
			
	def get_sub_tag_cnt(self):
		return self._cmd_cnt
		
	def _calc_allowed_depth(self):
		for tag in self._ctrl_tags:
			if isinstance(tag, lm_tag_place_obj.CTag):
				self._allowed_depth.add(tag._depth)
				
	# Execute tags
	# First non-actionscripts
	# Second actionscripts
	def execute(self, target=None):
		# Must have a target!
		if not target: return
		
		for tag in self._ctrl_tags:
			tag.execute(target=target)
		for tag in self._as_tags:
			tag.execute(target=target)
	
	def get_id(cls):
		return lm_consts.TAG_FRAME
	
	def do_actions(self, target=None):
		if not target: return
		for tag in self._as_tags:
			tag.execute(target=target)
	