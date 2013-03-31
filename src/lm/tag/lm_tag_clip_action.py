import lm_tag_base
from lm import lm_consts

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		
		# In fact, the field `clip_event_flags` responses to only one event
		# because we can have several clip action tags in a row.
		self.clip_event_flag = d["clip_event_flags"]
		self.as_idx = d["as_idx"]
		self.key_code = d["key_code"]
		
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_CLIP_ACTION
		