import pyglet
import lm_tag_base

from lm import lm_consts
from lm.type import lm_type_pos
from lm.type import lm_type_rect
from lm.drawable import lm_shape_clipped_image
from lm.drawable import lm_shape_tiled_image
from lm.drawable import lm_shape_solid_color

class CTag(lm_tag_base.CTag):
	
	def get_id(cls):
		return lm_consts.TAG_SHAPE2
