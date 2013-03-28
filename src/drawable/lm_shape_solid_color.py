import pyglet
import lm_drawable

from pyglet.gl import *

class CDrawable(lm_drawable.CDrawable):
	
	def __init__(self, color, rect, parent=None):
		super(CDrawable, self).__init__(parent, depth)
		self._vertex_list = pyglet.graphics.vertex_list(4,
			("v2f/static", (rect.left, rect.top, rect.right, rect.top, 
				rect.right, rect.bottom, rect.left, rect.bottom)),
			("c4B/static", (color.r, color.g, color.b, color.a) * 4),
			)
		self.shader = lm_shader.cxform_shader_no_texture
		
	def draw(self):
		self.shader.bind()
		c = self._tot_cadd
		shader.uniformf("color_add", c.r, c.g, c.b, c.a)
		c = self._tot_cmul		
		shader.uniformf("color_mul", c.r, c.g, c.b, c.a)
	
		self._vertex_list.draw(GL_QUADS)
		self.shader.unbind()