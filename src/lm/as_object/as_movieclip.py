import math
from lm.drawable import lm_drawable_container
from pyglet.gl import *
from lm.type import lm_type_mat
from lm import lm_glb
from lm import lm_consts

class CObj(lm_drawable_container.CDrawable):
	
	def __init__(self, frame_tags, key_frame_tags, label_dict, max_depth, inst_id, depth, parent=None):
		super(CObj, self).__init__(max_depth, inst_id, depth, parent=parent)

		# Tags
		self._frame_tags = frame_tags
		self._key_frame_tags = key_frame_tags
		self._label_2_frame = label_dict
		
		# Playing control
		self._play_head = 0	# 0-based frame id	
#		self.log("play head inited!")
		self._total_frame = len(self._frame_tags)		
		self._is_playing = True	
		self._init_frame = False
		
		# The `clip actions`
		# support onEnterFrame only
		self.onEnterFrame = None
		
		# Movieclip attributes that can be manipulated by as		
		# ---- non-direct access
		self.__rotation = None
		# ---- direct access
		self._name = ""
		# property root
		self._root = (self._parent and self._parent._root) or self

		self.speed = 1
		self._frames = 0
		# Character instance cache
		# All the characters that will be used along the timeline at depth `d`
		# will be cached in self._pool[d]
		#
		# If a timeline advances in normal order, find a cached character will
		# be super efficient!
		self._pool =[[]] * self._max_depth
			
		self._handlers = {}
		self._callbacks = {}
			
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
	def goto_frame(self, frame_id):
		key_frame = None
		nearest = None
		for key_frame_tag in self._key_frame_tags:
			key_frame_id = key_frame_tag.get_frame_id()
			if key_frame_id < frame_id:
				nearest = key_frame_tag
			elif key_frame_id == frame_id:
				key_frame = key_frame_tag
				break
			else:
				break
		if key_frame is None:
			key_frame = self._frame_tags[frame_id]
			if key_frame.empty() and nearest is not None:
				key_frame = nearest
		assert key_frame is not None, "[Movieclip %d][inst%d]Target frame is not a key frame!" % (self.char_id, self.inst_id)
		key_frame.execute(target=self)
		
#		self.log("Goto frame %d" % frame_id)
		# Remove those not existed frame
		to_remove = []
		for drawable in self:
			if drawable.depth not in key_frame._allowed_depth and not drawable.forbid_timeline:
				to_remove.append(drawable.depth)
		for depth in to_remove:
			self.remove_drawable(depth)	
#			self.log("remove out of key frame %d" % depth)
		
		# Key Frame is always missing action?
		self._frame_tags[frame_id].do_actions(target=self)
		
	def update(self, render_state, operation=lm_consts.MASK_ALL):
		if not self.active:
			return
		
		if self.speed != 1:
			self._frames += self.speed
			if self._frames < 1: return
			if self._frames > 1:
				n = int(self._frames)
				for i in xrange(n - 1):
					self._update(render_state, operation & lm_consts.MASK_NO_DRAW)
				self._frames -= n
				
		# Normal Update
		self._update(render_state, operation)
			
	# Play mode: Normal!
	def _update(self, render_state, operation=lm_consts.MASK_ALL):
		
		if self._init_frame:
			operation &= lm_consts.MASK_NO_UPDATE
			self._init_frame = False
		
		if not self._visible:
			operation &= lm_consts.MASK_NO_DRAW
			
		if operation & lm_consts.MASK_UPDATE:
			# what ever, should do the onEnterFrame
			if self.onEnterFrame:
				self.onEnterFrame(self, None)
	
			#if a movieclip has only one frame, then it won't play
			if self._is_playing and self._total_frame > 1:
				self._play_head += 1
				#self.log("playing %d" % self._play_head)
				if self._play_head >= self._total_frame:
					self.gotoAndPlay(0)
					self._init_frame = True
				else:
					self._frame_tags[self._play_head].execute(target=self)
			
		# Update & Render
		if operation & lm_consts.MASK_DRAW:
			render_state.push_matrix(self.matrix)
			render_state.push_cxform(self.color_add, self.color_mul)
			render_state.push_blend_mode(self.blend_mode)
		
		#self.log("rendering frame %d" % self._play_head)
		clip_depth = 0
		for drawable in self:
			if drawable.clip_depth > 0:
				render_state.set_mask(drawable)
				clip_depth = drawable.clip_depth
				continue
				
			drawable.update(render_state, operation)
			
			if clip_depth > 0 and drawable.depth == clip_depth:
				render_state.set_mask(None)
				clip_depth = 0
			
		if operation & lm_consts.MASK_DRAW:
			render_state.pop_matrix()
			render_state.pop_cxform()
			render_state.pop_blend_mode()
		
	# initialization when first placed on stage
	def init(self, fully=False):
		if self._init_frame: return
		
#		self.log("init!!!!======>")
		# Remove all
		to_remove = []
		for drawable in self:
			if fully or not drawable.forbid_timeline:
				to_remove.append(drawable.depth)

		for depth in to_remove:
			self.remove_drawable(depth)	
			
		# Warning: The following set up may be changed by as
		# Update: exactly what the official flash player does
		self._play_head = 0
#		self.log("play head inited ??")

		self._is_playing = True
		self._as_tween_only = False
		self._init_frame = True

		# Execute the frame 0 tags
		self._frame_tags[0].execute(target=self)

		for drawable in self:
			if not drawable.forbid_timeline:
				drawable.init()
	
	# Movieclip property and method!!		
	def gotoAndPlay(self, frame_id):
		if isinstance(frame_id, str):
			frame_id = self._label_2_frame[frame_id]
			
		self._is_playing = True
		if frame_id == self._play_head:
#			self.log("already at that frame!")
			return
		self._play_head = frame_id		
		
		self.goto_frame(frame_id)
		
		#self.log("After gotoAndPlay, play_head = %d" % self._play_head)
#		self.log("After gotoAndPlay, movie is playing = %r" % self._is_playing)
		
	def gotoAndStop(self, frame_id):
		if isinstance(frame_id, str):
			frame_id = self._label_2_frame[frame_id]
			
		self._is_playing = False
		if frame_id == self._play_head:
			return
		self._play_head = frame_id
		
		self.goto_frame(frame_id)

		#self.log("After gotoAndStop, play_head = %d" % self._play_head)
			
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
	#
	# Update: use rotateskew0 as the `_rotation` property. This is exactly 
	# what official flash player does. 
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
	
	def fscommand(self, type, event):
		if type == "callback" and event in self._callbacks:

			func, cbdata = self._callbacks[event]
			func(self, cbdata)
			
		elif type == "event" and event in self._handlers:

			func, cbdata = self._handlers[event]
			func(self, cbdata)
		
	def register_callback(self, event, func, cbdata):
		self._callbacks[event] = (func, cbdata)
		
	def register_event(self, event, func, cbdata):
		self._handlers[event] = (func, cbdata)
		