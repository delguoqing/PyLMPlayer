import collections
import random

from lm import lm_loader
from lm import lm_consts
from lm.drawable import lm_drawable


class CDrawable(lm_drawable.CDrawable):
	
	def __init__(self, inst_id, depth, parent=None):
		super(CDrawable, self).__init__(inst_id, depth, parent=parent)
		self._pool = collections.deque()
		self._active_mc = collections.deque()
		
	def register(self, mcs):
		for mc in mcs:
			if random.random() < 0.5:
				self._pool.append(mc)
			else:
				self._pool.appendleft(mc)
		
	# policy: Drop oldest
	def alloc(self):
		if not self._pool:
			ret = self._active_mc.popleft()
		else:
			ret = self._pool.pop()
		self._active_mc.append(ret)
		return ret
		
	def update(self, render_state, operation=lm_consts.MASK_ALL):
		# recycle old mc
		while self._active_mc:
			mc = self._active_mc[0]
			if mc._is_playing: break
			if random.random() < 0.5:
				self._pool.append(mc)
			else:
				self._pool.appendleft(mc)
			self._active_mc.popleft()
			
		# update current active mc
		for mc in self._active_mc:
			mc.update(render_state, operation)