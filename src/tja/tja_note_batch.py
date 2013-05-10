# A batch of note scrolling at the same speed
class CNoteBatch(object):
	
	def __init__(self, offset, bpm, scroll):
		self.offset = offset
		self.bpm = bpm
		self.scroll = scroll
		
		self.commands = []
		self.notes = []
		
	def read(self, reader):
		while not reader.check_commands(("#END", "#BRANCHSTART", "#BRANCHEND", "#N", "#E", "#M",)) and (not reader.check_commands(("#BPMCHANGE", "#SCROLL")) or len(self.notes) == 0):
		
			notes = reader.read_notes()
			cmd_name, args = reader.read_command()
			if notes:
				print "[NOTES]", notes
				self.notes.append(notes)
			elif cmd_name:
				print "[ CMD ]", cmd_name, args
				self.commands.append((cmd_name, args))
			else:
				print "[EMPTY]"
			reader.skip_line()		