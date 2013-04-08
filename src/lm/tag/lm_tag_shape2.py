import pyglet
import lm_tag_base

from lm import lm_consts
from lm.type import lm_type_pos
from lm.type import lm_type_rect

class CTag(lm_tag_base.CTag):
	
	def get_id(cls):
		return lm_consts.TAG_SHAPE2
