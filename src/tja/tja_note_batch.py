class CNoteBatch(object):
	
	def __init__(self, offset, bpm, scroll):
		self.offset = offset
		self.bpm = bpm
		self.scroll = scroll
		
	def read(self, fobj):
		for line in fobj:
			if line.startswith("#BPMCHANGE")