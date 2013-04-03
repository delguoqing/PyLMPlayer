import os
from pyglet.resource import texture
from pyglet.image import CheckerImagePattern
import pyglet

class CType(object):
	def __init__(self, filename, idx, width, height):
		filenames = []
		if filename:
			filenames.append(filename)
		filenames.append("noname_%d" % idx)
		
		# find a valid file
		for filename in filenames:
			try:
				self._texture = texture(filename)
			except pyglet.resource.ResourceNotFoundException:
				self._texture = None
			else:
				break
		
		if self._texture is None:
#			print "No Image Found!"
			# fall back to a empty file
			self._texture = CheckerImagePattern().create_image(int(width), int(height))

	def get_texture(self):
		return self._texture.get_texture()