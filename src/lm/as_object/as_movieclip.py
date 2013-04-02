import as_obj_base
from lm.drawable import lm_sprite

class CObj(lm_sprite.CDrawable):
	
	def __init__(self, frame_tags, max_depth, parent=None):
		super(CObj, self).__init__(max_depth, parent=parent)
		
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

	def add_drawable(self, drawable, depth):
		super(CObj, self).add_drawable(drawable, depth)
		if hasattr(drawable, "get_name"):
			setattr(self, drawable.get_name(), drawable)
	
	# TODO:
	#    1.implement auto loop play
	#    2.implement rebuild frame method(build frame 0, or when jump happens)
	def advance(self):
		
		# Movieclip can be stopped from actionscript
		if self._is_playing:
		
			if self._play_head >= self._total_frame:
				# TODO:
				#   Gabage collection?
#				self.destroy()
#				self._play_head = 0
				pass
			else:
				self._frame_tags[self._play_head].execute(target=self)
				self._play_head += 1
		
			if self._total_frame == 1:
				self.stop()
				
		for drawable in self:
			if hasattr(drawable, "advance"):
				drawable.advance()
				
	def play(self):
		self._is_playing = True
	
	def stop(self):
		self._is_playing = False