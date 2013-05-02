import collections
import random

from lm import lm_loader
from lm import lm_consts
from lm.drawable import lm_drawable


class CDrawable(lm_drawable.CDrawable):
	
	def __init__(self, inst_id, depth, parent=None):
		super(CDrawable, self).__init__(inst_id, depth, parent=parent)
		self._pools = []
		self._active_mc = collections.deque()
		
	def register(self, mcs):
#		random.shuffle(mcs)
		pool_id = len(self._pools)
		for mc in mcs: mc.__pool_id = pool_id
		_pool = collections.deque(mcs)
		self._pools.append(_pool)
		return pool_id
		
	def alloc(self, pool_id):
		_pool = self._pools[pool_id]
		if not _pool: return None
		ret = _pool.pop()
		self._active_mc.append(ret)
		return ret
		
	def update(self, render_state, operation=lm_consts.MASK_ALL):
		# recycle old mc
		while self._active_mc:
			mc = self._active_mc[0]
			if mc._is_playing: break
			_pool = self._pools[mc.__pool_id]
			if random.random() < 0.5:
				_pool.append(mc)
			else:
				_pool.appendleft(mc)
			self._active_mc.popleft()
			
		# update current active mc
		for mc in self._active_mc:
			mc.update(render_state, operation)