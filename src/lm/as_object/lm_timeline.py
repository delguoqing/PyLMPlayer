class CObj(object):
	
	def __init__(self):
		self._play_head = 0	# 0-based frame id
		self._on_enter_frame = None	# The 'onEnterFrame' callback
		
	