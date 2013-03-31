import pyglet
import lm_drawable
from lm.util import lm_shader
from lm.type import lm_type_rect

from pyglet.gl import *

class CDrawable(lm_drawable.CDrawable):
	
	def __init__(self, texture, vertex_list, parent=None):
		super(CDrawable, self).__init__(parent)
		self._texture = texture
		self._vertex_list = vertex_list
		self.shader = lm_shader.cxform_shader
		
	def draw(self):
		
		self.blend_mode.setup()
		
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
			
		self.shader.bind()
		
		glEnable(self._texture.target)
		glBindTexture(self._texture.target, self._texture.id)
		self.shader.uniformi("sampler", 0)
		
		c = self._tot_cadd
		self.shader.uniformf("color_add", c.r, c.g, c.b, c.a)
		c = self._tot_cmul		
		self.shader.uniformf("color_mul", c.r, c.g, c.b, c.a)
		
		self._vertex_list.draw(GL_QUADS)
		
		self.shader.unbind()