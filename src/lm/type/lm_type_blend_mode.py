from pyglet.gl import *
import lm import lm_consts

class CType(object):
	
	BLEND_ARG = {
		lm_consts.BLEND_ALPHA: (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA),
	}
	
	def __init__(self, blend_mode_idx):
		self.idx = blend_mode_idx
		
	def setup(self):
		if self._idx == lm_consts.BLEND_NONE or self._idx not in self.BLEND_FUNC:
			glDisable(GL_BLEND)
			return
		src, dst = self.BLEND_FUNC[self.idx]
		glEnable(GL_BLEND)
		glBlendFunc(src, dst)

null_blend = CType(lm_consts.BLEND_ALPHA)