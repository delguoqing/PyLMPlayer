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
		
	def is_active(self, state):
		return self.offset - state.offset <= state.measure * 60000.0 / state.bpm
	
	def _insert_active_batch(self, batch):
		pass
	
	def update(self, state, onps):
		# check if new batch will be activated
		activated_idx = 0
		for batch in self.note_batches:
			if not batch.is_active():
				break
			activated_idx += 1
			self._insert_active_batch(batch)
		if activated_idx > 0:
			self.note_batches = self.note_batches[activated_idx:]
			
		# execute command and rendering onps
		for batch in self._active_batch:
		    batch.update(state, onps)
			