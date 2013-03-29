import pyglet
import lm_drawable
from lm.util import lm_shader
from lm.type import lm_type_color

from pyglet.gl import *

class CDrawable(lm_drawable.CDrawable):
	
	def __init__(self, color, coords, parent=None):
		super(CDrawable, self).__init__(parent)
		self._vertex_list = pyglet.graphics.vertex_list(4,
			("v2f/static", (coords[0], coords[1], coords[4], 
				coords[5], coords[8], coords[9], coords[12], coords[13])),
			("c4B/static", (color.rB, color.gB, color.bB, color.aB) * 4),
			)
		self.shader = util.lm_shader.cxform_shader_no_texture
		
	def draw(self):
		self.shader.bind()
		c = self._tot_cadd
		self.shader.uniformf("color_add", c.r, c.g, c.b, c.a)
		c = self._tot_cmul		
		self.shader.uniformf("color_mul", c.r, c.g, c.b, c.a)
	
		self._vertex_list.draw(GL_QUADS)
		self.shader.unbind()