# A batch of note scrolling at the same speed
class CNoteBatch(object):
	
	def __init__(self, offset, bpm, scroll):
		self.offset = offset
		self.bpm = bpm
		self.scroll = scroll
		
		self.commands = []
		self.notes = []
		
	def read(self, reader):
		