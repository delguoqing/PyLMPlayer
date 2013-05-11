# A batch of note scrolling at the same speed
class CNoteBatch(object):
	
	def __init__(self, sub_1stbar):
		self.offset = None
		self.bpm = None
		self.scroll = None
		
		self.sub_1stbar = sub_1stbar
		self.next_sub_1stbar = sub_1stbar
		self.incomplete = False
		
		self.commands = []
		self.notes = []
		self.balloons = []
		
	def read(self, reader, state):
		self.offset = state.offset
		self.bpm = state.bpm
		self.scroll = state.scroll
		
		while not reader.check_commands(("#END", "#BRANCHSTART", "#BRANCHEND", "#N", "#E", "#M",)) \
			and (not reader.check_commands(("#BPMCHANGE", "#SCROLL")) or len(self.notes) == 0):
		
			notes, tot_notes = reader.read_notes()
			cmd_name, args = reader.read_command()

			# handle commands
			if cmd_name == "#DELAY":
				state.offset += float(args[0])
				if len(self.notes) == 0:
					self.offset = state.offset
			elif cmd_name == "#BPMCHANGE":
				if len(self.notes) == 0:
					self.bpm = state.bpm = float(args[0])
				elif state.bpm != float(args[0]):
					break
			elif cmd_name == "#SCROLL":
				if len(self.notes) == 0:
					self.scroll = state.scroll = float(args[0])
				elif state.scroll != float(args[0]):
					break
			elif cmd_name == "#MEASURE":
				a, b = args[0].split("/", 1)
				a = float(a.strip())
				b = float(b.strip())
				state.measure = 4 * a / b
					
			if len(self.notes) == 0 and notes:
				print "#####"
				print "#####bpm:%f, beats:%f" % (self.bpm, state.measure)
				print "#####scroll:%f, off:%f" % (self.scroll, self.offset)
				print "#####"
				
			# handle notes
			if notes:
				if notes == ",": notes = "0,"
				print "NOTES off=%d:\t%s" % (state.offset, notes)
				num_notes = len(notes) - int(notes.endswith(","))
				if len(self.notes) == 0 and self.sub_1stbar > 0:
					tot_notes += self.sub_1stbar
				if len(self.notes) > 0 and not self.notes[-1].endswith(","):
					tot_notes += len(self.notes[-1])
					self.notes[-1] += notes
				else:
					self.notes.append(notes)
				delta = (60000.0/state.bpm) * state.measure * (num_notes / tot_notes)
				print "delta %d %d" % (num_notes, tot_notes)
				state.offset += (60000.0/state.bpm) * state.measure * num_notes / tot_notes
				if not self.notes[-1].endswith(","):
					self.next_sub_1stbar += len(self.notes[-1])
				else:
					self.next_sub_1stbar = 0
			elif cmd_name:	# Runtime commands
				print "[ CMD ]", cmd_name, args
				self.commands.append((cmd_name, args))
			else:
				print
			reader.skip_line()
		
		# Join all 