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
		
		drawable.apply_matrix(self._tot_mat)
		drawable.apply_cxform(self._tot_cadd, self._tot_cmul)
		
	def get_drawable(self, depth):
		return self._drawables[depth]
		
	def remove_drawable(self, depth):
		self._drawables[depth] = None
		
	def refresh(self):
		_matd = self._is_mat_dirty
		_cxfd = self._is_cxform_dirty
		super(CDrawable, self).refresh()
	
		for drawable in self:
			if _matd:
				drawable.apply_matrix(self._tot_mat)
			if _cxfd:
				drawable.apply_cxform(self._tot_cadd, self._tot_cmul)
			drawable.refresh()
		
#		print "container refreshed!"
			
	def __iter__(self):
		return itertools.ifilter(None, self._drawables)
		
	def destroy(self):
		for drawable in self:
			drawable.destroy()
		self._drawables = [None] * self._max_depth
#		super(CDrawable, self).destroy()