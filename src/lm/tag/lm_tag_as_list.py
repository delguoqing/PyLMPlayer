from lm import lm_consts

import lm_tag_base

class CTag(lm_tag_base.CTag):
	
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_AS_LIST