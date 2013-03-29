import lm_tag_base
from lm import lm_consts

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = CTag.parse_tag(ctx, tag)
		
		self._frame_id = d["frame_id"]
		self._ctrl_tags = []
		
	# 0 based frame id
	def get_frame_id(self):
		return self._frame_id
		
	def add_ctrl_tag(self, tag):
		self._ctrl_tags.append(tag)
		
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_FRAME