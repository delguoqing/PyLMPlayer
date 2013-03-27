import pyglet
import lm_drawable

from pyglet.gl import *

class CDrawable(object):
	
	def __init__(self, texture, rect, parent=None):
		super(CDrawable, self).__init__(parent)
		self._texture = texture
		self._vertex_list = pyglet.graphics.vertex_list(4,
			("v2f/static", (rect.left, rect.top, rect.right, rect.top, 
				rect.right, rect.bottom, rect.left, rect.bottom)),
			("t2f/static", (0, 0, 0, texture.width/rect.width, 
				texture.height/rect.height, texture.width/rect.width, 0, 
				texture.height/rect.height)),
		)
					
	def draw(self):
		glEnable(self._texture.target)
		glBindTexture(self._texture.target, self._texture.id)
		
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
				
		self._vertex_list.draw(GL_QUADS)
		
		glDisable(GL_BLEND)