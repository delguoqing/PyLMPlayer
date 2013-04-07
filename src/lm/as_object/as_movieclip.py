import math
import as_obj_base
from lm.drawable import lm_drawable_container
from pyglet.gl import *
from lm.type import lm_type_mat



class CObj(lm_drawable_container.CDrawable):
	
	def __init__(self, frame_tags, key_frame_tags, label_dict, max_depth, inst_id, depth, parent=None):
		super(CObj, self).__init__(max_depth, inst_id, depth, parent=parent)

		# Tags
		self._frame_tags = frame_tags
		self._key_frame_tags = key_frame_tags
		self._label_2_frame = label_dict
		
		# Playing control
		self._play_head = 0	# 0-based frame id	
		self._total_frame = len(self._frame_tags)		
		self._is_playing = True	

		# The `clip actions`
		# support onEnterFrame only
		self.onEnterFrame = None
		
		# Movieclip attributes that can be manipulated by as		
		# ---- non-direct access
		self.__rotation = None
		# ---- direct access
		self._name = ""
		
		# Character instance cache
		# All the characters that will be used along the timeline at depth `d`
		# will be cached in self._pool[d]
		#
		# If a timeline advances in normal order, find a cached character will
		# be super efficient!
		self._pool =[[]] * self._max_depth
		
	# Allocate a cached drawable from pool
	def alloc_drawable(self, depth, inst_id):
		_cache = self._pool[depth]
		idx = None
		for i, drawable in enumerate(_cache):
			if drawable.inst_id == inst_id:
				idx = i
				break
		if idx is None:
			return None
		return _cache.pop(idx)
		
	# Add an drawable.
	# if it is specified with a name, this object has an attr
	def add_drawable(self, drawable, depth, name=""):
		super(CObj, self).add_drawable(drawable, depth)
		if name:
			setattr(self, name, drawable)
			drawable._name = name
	
	# Remove object
	# if it is specified with a name, this object removes the attr
	# The object is not really deleted, it is cached for reuse
	def remove_drawable(self, depth):
		_d = self.get_drawable(depth)
		if _d is not None:
			self._pool[depth].append(_d)
			_d._as_tween_only = False
		super(CObj, self).remove_drawable(depth)

	def is_movieclip(self):
		return True
		
	# -------------------------
	# The Action script stuff
	# -------------------------	
	# Play mode: jump!
	# if the new
	def goto_frame(self, frame_id):
		if frame_id == 0:
			key_frame = self._frame_tags[0]
		else:
			for key_frame_tag in self._key_frame_tags:
				if key_frame_tag.get_frame_id() == frame_id:
					key_frame = key_frame_tag
					break
		key_frame.execute(target=self)
		
	# Play mode: Normal!
	def advance(self):
			
		# what ever, should do the onEnterFrame
		if self.onEnterFrame:
			self.onEnterFrame(self)
		
		# if a movieclip has only one frame, then it won't play
		if self._is_playing and self._total_frame > 1:
			self._play_head += 1
			if self._play_head >= self._total_frame:
				self.init()
			else:
				self._frame_tags[self._play_head].execute(target=self)
	
		# whatever, sub movieclip is not stopped!
		for drawable in self:
			if isinstance(drawable, CObj):
				drawable.advance()
				
	# initialization when first placed on stage
	def init(self, fully=False):
		
		# Remove all
		to_remove = []
		for drawable in self:
			if fully or not drawable.forbid_timeline:
				to_remove.append(drawable.depth)

		for depth in to_remove:
			self.remove_drawable(depth)	
		# Warning: The following set up may be changed by as
		self._play_head = 0
		self._is_playing = True
		self._as_tween_only = False

		# Execute the frame 0 tags
		self._frame_tags[0].execute(target=self)

	# Movieclip property and method!!		
	def gotoAndPlay(self, frame_id):
		if isinstance(frame_id, str):
			frame_id = self._label_2_frame[frame_id]
			
		self._is_playing = True
		if frame_id == self._play_head:
			return
		self._play_head = frame_id		
		
		self.goto_frame(frame_id)
		
	def gotoAndStop(self, frame_id):
		if isinstance(frame_id, str):
			frame_id = self._label_2_frame[frame_id]
			
		self._is_playing = False
		if frame_id == self._play_head:
			return
		self._play_head = frame_id
		
		self.goto_frame(frame_id)
	
	def play(self):
		self._is_playing = True
	
	def stop(self):
		self._is_playing = False
		
	def _get_x(self):
		if not self.matrix: return 0
		return self.matrix.translate[0]
	
	def _set_x(self, x):
		if not self.matrix:
			_m = self.matrix = lm_type_mat.CType()
		else:
			_m = self.matrix
		_t = _m.translate
		_m.translate = (x, _t[1])
		self._as_tween_only = True
	
	_x = property(_get_x, _set_x)
	
	# Don't bother to do extra math
	# I don't see a movieclip with different x, y scale rate,
	# and don't see a movieclip with rotation and scale at the
	# same time.
	def _get_rotation(self):
		if self.__rotation: return self.__rotation
		if self.matrix:
			return math.asin(self.matrix.rotateskew[0]) * 180.0 / math.pi
		return 0
		
	def _set_rotation(self, rotation):
		self.__rotation = rotation
		radian = rotation * math.pi / 180.0
		cos = math.cos(radian)
		sin = math.sin(radian)
		
		self.matrix.rotateskew = (sin, -sin)
		self.matrix.scale = (cos, cos)
		self._as_tween_only = True
		
	_rotation = property(_get_rotation, _set_rotation)