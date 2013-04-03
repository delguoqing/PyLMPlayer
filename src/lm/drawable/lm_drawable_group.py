import itertools
import pyglet
from pyglet.gl import *
	
class CGroup(pyglet.graphics.Group):
	
	def __init__(self, texture, blend_src, blend_dest, depth, parent=None):
		super(CGroup, self).__init__(parent)
		self.texture = texture
		self.blend_src = blend_src
		self.blend_dest = blend_dest
		self.depth = depth

	def set_state(self):
		glEnable(self.texture.target)
		glBindTexture(self.texture.target, self.texture.id)

		glPushAttrib(GL_COLOR_BUFFER_BIT)
		glEnable(GL_BLEND)
		glBlendFunc(self.blend_src, self.blend_dest)

	def unset_state(self):
		glPopAttrib()
		glDisable(self.texture.target)

	def __repr__(self):
		return '%s(%r)' % (self.__class__.__name__, self.texture)

	def __eq__(self, other):
		return (other.__class__ is self.__class__ and
				self.parent is other.parent and
				self.texture.target == other.texture.target and
				self.texture.id == other.texture.id and
				self.blend_src == other.blend_src and
				self.blend_dest == other.blend_dest and
				self.depth == other.depth)

	def __hash__(self):
		return hash((id(self.parent),
					 self.texture.id, self.texture.target,
					 self.blend_src, self.blend_dest, self.depth))
	
	def __lt__(self, other):
		return True
		for x, y in itertools.izip(self.depth, other.depth):
			if x != y:
				return x < y
		return True