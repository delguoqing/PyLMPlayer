from lm import lm_consts
from lm.type import lm_type_pos

import lm_tag_base
import lm_tag_shape

# it is basically the same with TAG_SHAPE a.t.m
class CTag(lm_tag_shape.CTag):
		
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_SHAPE2