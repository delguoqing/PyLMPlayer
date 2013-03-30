import pyglet
import lm_drawable
from lm.util import lm_shader
from lm.type import lm_type_rect

from pyglet.gl import *

class CDrawable(lm_drawable.CDrawable):
	
	def __init__(self, texture, coords, parent=None):
		super(CDrawable, self).__init__(parent)
		self._texture = texture
		self._vertex_list = pyglet.graphics.vertex_list(4,
			("v2f/static", (coords[0], coords[1], coords[4], coords[5],
				coords[8], coords[9], coords[12], coords[13])),
			("t2f/static", (coords[2], coords[15], coords[6], coords[11],
				coords[10], coords[7], coords[14], coords[3])),
		)
		self.shader = lm_shader.cxform_shader
		self._rect = lm_type_rect.CType(coords[0], coords[1], coords[8], coords[9])
		
	def draw(self):
#		center = self._rect.get_center()
#		glTranslatef(-center[0], -center[1], 0)
		
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