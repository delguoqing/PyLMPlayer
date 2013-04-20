from pyglet.gl import *
from lm import lm_consts

class CType(object):
	
	BLEND_FUNC = {
		lm_consts.BLEND_NORMAL: (
			GL_FUNC_ADD,
			GL_SRC_ALPHA, 
			GL_ONE_MINUS_SRC_ALPHA
		),
			
		lm_consts.BLEND_NORMAL1: (
			GL_FUNC_ADD, 
			GL_SRC_ALPHA, 
			GL_ONE_MINUS_SRC_ALPHA
		),
		
		lm_consts.BLEND_ADD: (
			GL_FUNC_ADD,
			GL_SRC_ALPHA, 
			GL_ONE
		),
		
		lm_consts.BLEND_SUBTRACT: (
			GL_FUNC_REVERSE_SUBTRACT,
			GL_ONE, 
			GL_ONE
		),
	}
	
	def __init__(self, blend_mode_idx):
		self._idx = blend_mode_idx
		
	def set(self):
		equation, src, dst = self.BLEND_FUNC[self._idx]
		glBlendEquation(equation)
		glBlendFunc(src, dst)
				
	def __nonzero__(self):
		return self._idx != lm_consts.BLEND_NORMAL \
			and self._idx != lm_consts.BLEND_NORMAL1
		
	def __eq__(self, o):
		return self._idx == o._idx
null_blend = CType(lm_consts.BLEND_NORMAL)