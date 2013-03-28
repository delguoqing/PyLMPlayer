import lm_type_color
import lm_drawable
import lm_drawable_container

class CDrawable(lm_drawable_container.CDrawable):

	def __init__(self, max_depth, parent=None):
		super(CDrawable, self).__init__(max_depth, parent)
		self._is_dirty = True
		self._tot_cadd = None
		self._tot_cmul = None
		self._super_cadd = lm_type_color.null_cadd
		self._super_cmul = lm_type_color.null_cmul
		self._update_cxform()
		
	def set_cxform(self, cadd, cmul):
		super(CDrawable, self).set_cxform(cadd, cmul)
		self._update_cxform()
		
	def apply_cxform(self, cadd, cmul):
		self._super_cadd = cadd
		self._super_cmul = cmul
		self._update_cxform()
		
	def _update_cxform(self):
		self._tot_cadd = self.color_add * self._super_cadd + self._super_cmul
		self._tot_cmul = self.color_mul * self._super_cmul
		self._is_dirty = True
				
	def draw(self):
		glPushMatrix()
		glMultMatrixf(self.matrix.get_ctype())
		
		for drawable in self:
			if self._is_dirty:
				drawable.apply_cxform(self._tot_cadd, self._tot_cmul)
			drawable.draw()
		self._is_dirty = False
		
		glPopMatrix()