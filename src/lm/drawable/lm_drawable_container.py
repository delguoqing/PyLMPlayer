import itertools
import lm_drawable

class CDrawable(lm_drawable.CDrawable):
	
	def __init__(self, max_depth, parent=None):
		super(CDrawable, self).__init__(parent)
		self._drawables = [None] * max_depth
		self._max_depth = max_depth
		
	def add_drawable(self, drawable, depth):
		self._drawables[depth] = drawable
		drawable.set_depth(depth)
		
	def get_drawable(self, depth):
		return self._drawables[depth]
		
	def remove_drawable(self, depth):
		self._drawables[depth] = None
		
	def __iter__(self):
		return itertools.ifilter(None, self._drawables)
		
	def destroy(self):
		for drawable in self:
			drawable.destroy()
		self._drawables = []
		super(CDrawable, self).destroy()