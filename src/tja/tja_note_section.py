import tja_note_batch

class CNoteSection(object):
	
	def __init__(self):
		self.note_batches = []
		self.offset = 0
		self.scroll = 0
		self.bpm = 0
		
		self.end_cmd = set(("#END", "#BRANCHSTART", "#BRANCHEND", "#N", "#E", "#M"))
		
		self._active_batch = []
		
	def read(self, reader, state):
		
		while not reader.check_commands(self.end_cmd):

			print "\t||||||BATCH BEG|||||| "
			batch = tja_note_batch.CNoteBatch()
			self.note_batches.append(batch)
			batch.read(reader, state)
			print "\t||||||BATCH END||||||\n"
		
		# Update section state	
		if self.note_batches:
			batch = self.note_batches[0]
			self.offset = batch.offset
			self.scroll = batch.scroll
			self.bpm = batch.bpm
		else:
			self.offset = state.offset
			self.scroll = state.scroll
			self.bpm = state.bpm			
		
		# TODO:
		# add cmp function for note batches
		self.note_batches.sort()
		
	def active(self, state):
		return self.offset - state.offset <= state.measure * 60000.0 / state.bpm
	
	def empty(self):
		return len(self.note_batches) == 0 and len(self._active_batch) == 0
	
	def _insert_active_batch(self, src_batch):
		ins_pos = 0
		for ins_pos, dst_batch in enumerate(self._active_batch):
			if src_batch > dst_batch:
				break
		self._active_batch.insert(ins_pos, src_batch)
		
	def update(self, state, onps):
		# check if new batch will be activated
		activated_idx = 0
		for batch in self.note_batches:
			if not batch.active(state):
				break
			activated_idx += 1
			self._insert_active_batch(batch)
		if activated_idx > 0:
			self.note_batches = self.note_batches[activated_idx:]
			
		# execute command and rendering onps
		out_idx = 0
		for batch in self._active_batch:
			if batch.empty():
				out_idx += 1
			else:
				batch.update(state, onps)
		if out_idx > 0:
			self._active_batch = self._active_batch[out_idx:]
			