import pyglet
import lm_drawable

from pyglet.gl import *

class CDrawable(object):
	
	def __init__(self, texture, coords, parent=None):
		super(CDrawable, self).__init__(parent)
		self._texture = texture
		self._vertex_list = pyglet.graphics.vertex_list(4,
			("v2f/static", (coords[0], coords[1], coords[4], coords[5],
				coords[8], coords[9], coords[12], coords[13])),
			("t2f/static", (coords[2], coords[3], coords[6], coords[7],
				coords[10], coords[11], coords[14], coords[15])),
		)
		self.shader = lm_shader.cxform_shader
					
	def draw(self):
		glEnable(self._texture.target)
		glBindTexture(self._texture.target, self._texture.id)
		
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
			
		self.shader.bind()
		c = self._tot_cadd
		shader.uniformf("color_add", c.r, c.g, c.b, c.a)
		c = self._tot_cmul		
		shader.uniformf("color_mul", c.r, c.g, c.b, c.a)
		shader.uniformf("sampler", texture.id)
						
		self._vertex_list.draw(GL_QUADS)
		
		self.shader.unbind()
		glDisable(GL_BLEND)