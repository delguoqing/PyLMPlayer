from pyglet.gl import *
from lm import lm_consts

class CType(object):
	
	BLEND_FUNC = {
		lm_consts.BLEND_NORMAL: (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA),
		lm_consts.BLEND_NORMAL1: (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA),
		lm_consts.BLEND_ADD: (GL_SRC_ALPHA, GL_ONE),
		lm_consts.BLEND_SUBTRACT: (GL_ONE, GL_ONE),
	}
	
	def __init__(self, blend_mode_idx):
		self._idx = blend_mode_idx
		
	def set(self):
		src, dst = self.BLEND_FUNC[self._idx]
		glBlendFunc(src, dst)
		if self._idx == lm_consts.BLEND_SUBTRACT:
			glBlendEquation(GL_FUNC_SUBTRACT)

	def unset(self):
		src, dst = self.BLEND_FUNC[lm_consts.BLEND_NORMAL]
		glBlendFunc(src, dst)	
				
	def __nonzero__(self):
		return self._idx != lm_consts.BLEND_NORMAL \
			and self._idx != lm_consts.BLEND_NORMAL1
		
	def __eq__(self, o):
		return self._idx == o._idx
null_blend = CType(lm_consts.BLEND_NORMAL)