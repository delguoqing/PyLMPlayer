import tja_note_batch

class CNoteSection(object):
	
	def __init__(self):
		self.note_batches = []
		self.offset = 0
		self.scroll = 0
		self.bpm = 0
		
		self.end_cmd = set(("#END", "#BRANCHSTART", "#BRANCHEND", "#N", "#E", "#M"))
		
	def read(self, reader):
		while not reader.check_commands(self.end_cmd):
		
			cmd_name, args = reader.read_command()
			if cmd_name == "#BPMCHANGE" or cmd_name == "#SCROLL":
				reader.skip_line()
				
			print "\t||||||BATCH BEG||||||"
			batch = tja_note_batch.CNoteBatch(self.offset, self.bpm, self.scroll)
			self.note_batches.append(batch)
			batch.read(reader)
			print "\t||||||BATCH END||||||"