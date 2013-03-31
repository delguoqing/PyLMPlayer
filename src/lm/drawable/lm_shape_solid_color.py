import pyglet
import lm_drawable
from lm.util import lm_shader
from lm.type import lm_type_color

from pyglet.gl import *

class CDrawable(lm_drawable.CDrawable):
	
	def __init__(self, vertex_list, parent=None):
		super(CDrawable, self).__init__(parent)
		self._vertex_list = vertex_list
		self.shader = lm_shader.cxform_shader_no_texture
		
	def draw(self):
		self.blend_mode.setup()
		
		self.shader.bind()
		c = self._tot_cadd
		self.shader.uniformf("color_add", c.r, c.g, c.b, c.a)
		c = self._tot_cmul		
		self.shader.uniformf("color_mul", c.r, c.g, c.b, c.a)
	
		self._vertex_list.draw(GL_QUADS)
		self.shader.unbind()