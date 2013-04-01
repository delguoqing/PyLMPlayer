from pyglet.gl import *

class CObj(object):
	
	def __init__(self):
		self.texture = None
		
	def set_active_texture(self, texture):
		if self.texture == texture:
			return
		glEnable(texture.target)
		glBindTexture(texture.target, texture.id)
		self.texture = texture