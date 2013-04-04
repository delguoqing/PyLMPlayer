import as_obj_base
from lm.drawable import lm_sprite
from pyglet.gl import *
from lm.type import lm_type_mat

class CObj(lm_sprite.CDrawable):
	
	def __init__(self, frame_tags, key_frame_tags, label_dict, max_depth, inst_id, depth, parent=None):
		super(CObj, self).__init__(max_depth, inst_id, depth, parent=parent)
		
		self._play_head = 0	# 0-based frame id
		self._frame_tags = frame_tags # frame tags		
		self._total_frame = len(self._frame_tags)
		self._is_playing = True		
		
		# TODO:
		#   implement the following
		self._key_frame_tags = key_frame_tags # key frame, used to rebuild a 
											  # frame when 
											  # navigate along the timeline
		self._clip_actions = [] # the clip actions
		self._real_mat = lm_type_mat.CType((0,0))

		self._label_2_frame = label_dict # look up frame id
		# Character instance cache
		# All the characters that will be used along the timeline at depth `d`
		# will be cached in self._pool[d]
		#
		# If a timeline advances in normal order, find a cached character will
		# be super efficient!
		self._pool =[[]] * self._max_depth
		
		self.onEnterFrame = None
		
		# Cache gotos
		self._target_frame = None
		self._after_jump = None
		
	def alloc_drawable(self, depth, inst_id):
		idx = -1
		for i, inst in enumerate(self._pool[depth]):
			if inst.inst_id == inst_id:
				idx = i
				break
		if idx >= 0:
			inst = self._pool[depth].pop(idx)
			return inst
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
	
	def goto_frame(self, frame_id):
		for _t in self._key_frame_tags:
			if _t.get_frame_id() == frame_id:
				_t.execute(target=self)
				self._play_head = frame_id + 1
				return 
		# Must have a key frame!!
		assert False, "Must be a key frame"
		
	def gotoAndPlay(self, frame_id):
		if isinstance(frame_id, str):
			frame_id = self._label_2_frame[frame_id]	
		self._target_frame = frame_id
		self._after_jump = self.play
		
	def gotoAndStop(self, frame_id):
		if isinstance(frame_id, str):
			frame_id = self._label_2_frame[frame_id]
		self._target_frame = frame_id
		self._after_jump = self.stop
		
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
			
			# Whether we jumped?		
			if self._target_frame is not None:
				self.goto_frame(self._target_frame)
				self._after_jump()
				self._play_head = self._target_frame + 1
				self._target_frame = self._after_jump = None
			else:
				self._play_head += 1			

		self._sub_advance()
		
	# For Debug
	# Remember remove it!
	def _sub_advance(self):
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
		has_cxform = self.color_mul or self.color_add			
		if has_cxform:
			render_state.push_cxform(self.color_add, self.color_mul)
		for drawable in self:
			drawable.draw(render_state)
		if self._real_mat:
			glPopMatrix()
		if has_cxform:
			render_state.pop_cxform()
	
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