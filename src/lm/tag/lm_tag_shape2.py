from lm import lm_consts
import lm_tag_shape

class CTag(lm_tag_shape.CTag):
	
	def get_id(cls):
		return lm_consts.TAG_SHAPE2
