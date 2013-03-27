import lm_drawable
import lm_drawable_container

class CDrawable(lm_drawable_container.CDrawable):

	def draw(self):
		# set up opengl state here
		glPushMatrix()
		glMultMatrixf()
		
		for drawable in self:
			drawable.draw()
			
		glPopMatrix()