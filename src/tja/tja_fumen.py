import copy
import tja_note_section
import tja_header
import tja_enso_state

SECTION_NORMAL = 2
SECTION_EXPERT = 3
SECTION_MASTER = 4

class CFumen(object):
	
	def __init__(self):
		self.header = tja_header.CData()
		self.sections = []

	def read_header(self, reader):
		self.header.read(reader)
		self.header.refresh()
		
	def read_fumen(self, reader):
		curr_state = tja_enso_state.CEnsoState(self.header)
		next_state = None
		
		while not reader.check_command("#END"):
			cmd_name, args = reader.read_command()
			
			if cmd_name == "#BRANCHSTART":
				reader.skip_line()
				if next_state:
					curr_state, next_state = next_state, None
				self.sections.append([True, args, None, None, None])
				print "======> BRANCHSTART"
			elif cmd_name in ("#N", "#E", "#M"):
				print "<======> %s BEG" % cmd_name
				reader.skip_line()
				sec = tja_note_section.CNoteSection()
				next_state = copy.copy(curr_state)
				sec.read(reader, next_state)
				if cmd_name == "#N":
					self.sections[-1][SECTION_NORMAL] = sec
				elif cmd_name == "#E":
					self.sections[-1][SECTION_EXPERT] = sec
				elif cmd_name == "#M":
					self.sections[-1][SECTION_MASTER] = sec
				print "<======> %s END" % cmd_name					
			elif cmd_name == "#BRANCHEND":
				print "=====> BRANCHEND"
				reader.skip_line()
				if next_state:
					curr_state, next_state = next_state, None
			else:
				print "=====> NO BUNKI BEG"
				section = tja_note_section.CNoteSection()
				self.sections.append([False, None, section, None, None])
				section.read(reader, curr_state)
				print "=====> NO BUNKI END"				
			
if __name__ == "__main__":
	import tja_reader
	import sys
	
	reader = tja_reader.CReader()
	reader.set_file(sys.argv[1])
	
	fumen = CFumen()
	fumen.read_header(reader)
	fumen.read_fumen(reader)