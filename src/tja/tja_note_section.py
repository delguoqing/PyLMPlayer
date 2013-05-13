import tja_note_batch

class CNoteSection(object):
	
	def __init__(self):
		self.note_batches = []
		self.offset = 0
		self.scroll = 0
		self.bpm = 0
		
		self.end_cmd = set(("#END", "#BRANCHSTART", "#BRANCHEND", "#N", "#E", "#M"))
		
	def read(self, reader, state):
		self.offset = state.offset
		self.scroll = state.scroll
		self.bpm = state.bpm
		
		while not reader.check_commands(self.end_cmd):

			print "\t||||||BATCH BEG|||||| "
			batch = tja_note_batch.CNoteBatch()
			self.note_batches.append(batch)
			batch.read(reader, state)
			print "\t||||||BATCH END||||||\n"