class CNoteSection(object):
	
	def __init__(self):
		self.note_batches = []
		
	def read(self, reader):
		while not reader.check_commands(("#END", "#BRANCHSTART", "#BRANCHEND", "#N", "#E", "#M")):
			notes = reader.read_notes()
			cmd_name, args = reader.read_command()
			if notes:
				print "[NOTES]", notes
			elif cmd_name:
				print "[ CMD ]", cmd_name, args
			else:
				print "[EMPTY]"
			reader.skip_line()