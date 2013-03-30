from pyglet.gl import *
from lm import lm_consts

class CType(object):
	
	BLEND_FUNC = {
		lm_consts.BLEND_NORMAL: (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA),
		lm_consts.BLEND_NORMAL1: (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA),
	}
	
	def __init__(self, blend_mode_idx):
		self._idx = blend_mode_idx
		
	def setup(self):
		src, dst = self.BLEND_FUNC[self._idx]
		glEnable(GL_BLEND)
		glBlendFunc(src, dst)

null_blend = CType(lm_consts.BLEND_NORMAL)