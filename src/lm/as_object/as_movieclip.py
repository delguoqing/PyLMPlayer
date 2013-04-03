import as_obj_base
from lm.drawable import lm_sprite
from pyglet.gl import *
from lm.type import lm_type_mat

class CObj(lm_sprite.CDrawable):
	
	def __init__(self, frame_tags, max_depth, inst_id, depth, parent=None):
		super(CObj, self).__init__(max_depth, inst_id, depth, parent=parent)
		
		self._play_head = 0	# 0-based frame id
		self._frame_tags = frame_tags # frame tags		
		self._total_frame = len(self._frame_tags)
		self._is_playing = True		
		
		# TODO:
		#   implement the following
		self._key_frame_tags = [] # key frame, used to rebuild a frame when 
								  # navigate along the timeline
		self._frame_label_tags = [] # frame label tags
		self._clip_actions = [] # the clip actions
		self._real_mat = lm_type_mat.CType((0,0))

		# Character instance cache
		# All the characters that will be used along the timeline at depth `d`
		# will be cached in self._pool[d]
		#
		# If a timeline advances in normal order, find a cached character will
		# be super efficient!
		self._pool =[[]] * self._max_depth
		
		self.onEnterFrame = None
		
	def alloc_drawable(self, depth, inst_id):
		idx = -1
		for i, inst in enumerate(self._pool[depth]):
			if inst.inst_id == inst_id:
				idx = i
				break
		if idx >= 0:
			inst = self._pool[depth].pop(idx)
			inst.clear()
		return None
		
	def add_drawable(self, drawable, depth, name=""):
		super(CObj, self).add_drawable(drawable, depth)
		if name:
			setattr(self, name, drawable)
	
	def remove_drawable(self, depth):
		# Cache the instance before remove!
		_d = self.get_drawable(depth)
		if _d is not None:
			self._pool[depth].append(_d)
		super(CObj, self).remove_drawable(depth)
	
	# TODO:
	#	1.implement auto loop play
	#	2.implement rebuild frame method(build frame 0, or when jump happens)
	def advance(self):
		
		# Force advance for the 1st frame
		if self._play_head == 0:
			self._frame_tags[self._play_head].execute(target=self)
			self._play_head += 1
			if self._total_frame == 1:
				self.stop()
										
		if self.onEnterFrame:
			self.onEnterFrame(self)
			
		# Movieclip can be stopped from actionscript
		if self._is_playing:
		
			if self._play_head >= self._total_frame:
				self.clear()
			self._frame_tags[self._play_head].execute(target=self)
			self._play_head += 1
				
		for drawable in self:
			if hasattr(drawable, "advance"):
				drawable.advance()
				
	def play(self):
		self._is_playing = True
	
	def stop(self):
		self._is_playing = False
		
	def clear(self):
		for _d in self:
			self._pool[_d.depth].append(_d)
			_d.clear()
		self._drawables = [None] * self._max_depth
		self._play_head = 0
		self._is_playing = True
	
	def draw(self, render_state):
		if self._real_mat:
			glPushMatrix()
			glMultMatrixf(self._real_mat.get_ctype())
		if self.color_mul:
			glColor4f(self.color_mul.r,  self.color_mul.g, self.color_mul.b, self.color_mul.a)
		for drawable in self:
			drawable.draw(render_state)
		if self._real_mat:
			glPopMatrix()
		if self.color_mul:
			glColor4f(1, 1, 1, 1)
	
	# Modified from actionscrip			
	def _set_x(self, x):
		self._real_mat.translate = (x, self._real_mat.translate[1])
	def _get_x(self):
		return self._real_mat.translate[0]
	_x = property(_get_x, _set_x)
		
	# Set matrix from timeline, overwrite action script!
	def set_matrix(self, matrix):
		super(CObj, self).set_matrix(matrix)
		self._real_mat.copy_from(self.matrix)