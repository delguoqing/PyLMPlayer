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
		self.speed = 1
		self._frames = 0
		self._to_recycle = set()
		
	def on_movieclip_end(self, mc, data):
		obj_id = id(mc)
		assert obj_id not in self._to_recycle
		self._to_recycle.add(obj_id)
		
#		self.log("self._to_recycle id %d" % id(mc))
		
	def log(self, str):
		if True or len(self._pools) > 3:
			print str
			
	def register(self, mcs):
#		random.shuffle(mcs)
		pool_id = len(self._pools)
		for mc in mcs: 
			mc.__pool_id = pool_id
			mc.register_event("end", self.on_movieclip_end, None)
#			print "%d" % id(mc)
			
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
				
	def _update(self, render_state, operation=lm_consts.MASK_ALL):
		# recycle old mc
		while self._active_mc:
			mc = self._active_mc[0]
			if id(mc) not in self._to_recycle: 
#				self.log("id %d can't be recycled!" % id(mc))
				break
			_pool = self._pools[mc.__pool_id]
			if random.random() < 0.5:
				_pool.append(mc)
			else:
				_pool.appendleft(mc)
			self._active_mc.popleft()
			self._to_recycle.remove(id(mc))			
#			self.log("recycled %d" % id(mc))
			
		# update current active mc
		for mc in self._active_mc:
			mc.update(render_state, operation)
		
#		if len(self._active_mc): self.log("remaining! %d: %d" % (len(self._pools), len(self._active_mc)))