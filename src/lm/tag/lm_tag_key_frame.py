import lm_tag_base
import lm_tag_frame
from lm import lm_consts

class CTag(lm_tag_frame.CTag):
		
	
	def get_id(cls):
		return lm_consts.TAG_KEY_FRAME