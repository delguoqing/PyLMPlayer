from lm.util from lm.util import lm_tag_reader
from lm from lm import lm_consts

import lm_tag_base

class CTag(lm_tag_base.CTag):
	
	# ALL Character Tag should have a method called `instantiate`!
	# And the we need a character dictionary 
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		
		self._char_id = d["character_id"]
		
	def exec(self):
		char_dict = self.ctx["char_dict"]
		char_tag = char_dict.get(self._char_id)
		
		char_tag.instantiate()
	
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_PLACE_OBJ