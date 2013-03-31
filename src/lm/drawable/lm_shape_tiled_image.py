import pyglet
import lm_drawable

from lm.util import lm_shader

from pyglet.gl import *

class CDrawable(lm_drawable.CDrawable):
	
	def __init__(self, texture, vertex_list, parent=None):
		super(CDrawable, self).__init__(parent)
		self._texture = texture
		self._vertex_list = vertex_list
		self.shader = lm_shader.cxform_shader		

	def draw(self):
		self.blend_mode.setup()
		
		glEnable(self._texture.target)
		glBindTexture(self._texture.target, self._texture.id)
		
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		
		self.shader.bind()
		c = self._tot_cadd
		self.shader.uniformf("color_add", c.r, c.g, c.b, c.a)
		c = self._tot_cmul		
		self.shader.uniformf("color_mul", c.r, c.g, c.b, c.a)
		self.shader.uniformi("sampler", 0)
		
		self._vertex_list.draw(GL_QUADS)
		
		self.shader.unbind()