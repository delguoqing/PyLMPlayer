class CReader(object):
	
	def __init__(self):
		self._fobj = None
		self._fpos = 0
		
	def is_eof(self):
		self._fobj.seek(self._fpos)
		return self._fobj.readline() == ""
	
	def set_file(self, filename):
		if self._fobj:
			self._fobj.close()
		self._fobj = open(filename, "r")
		self._fpos = self._fobj.tell()
		
	def rem_comment(self, line):
		try:
			comment_pos = line.index("//")
			return line[:comment_pos]
		except ValueError:
			return line
		
	def peek_line(self):
		self._fobj.seek(self._fpos)
		raw_line = self._fobj.readline()
		if raw_line == "":
			return "#END"
		else:
			return self.rem_comment(raw_line)
		
	def skip_line(self):
		self._fobj.seek(self._fpos)
		line = self._fobj.readline()
		self._fpos = self._fobj.tell()
		
	def read_header(self):
		line = self.peek_line()
		# contains no header
		try:
			colon_pos = line.index(":")
		except ValueError:
			return None, None
		# split into {Key: Value}
		key = line[: colon_pos].strip()
		val = line[colon_pos + 1:].strip()
		return key, val

	def read_notes(self):
		notes = ""
		tot_notes = 0
		fpos = self._fpos
		
		while True:
			notes_line = self._read_notes_line()
			
			# first read fail
			if notes == "" and notes_line == "":
				return "", 0
			
			self.skip_line()
			# Only return the first notes line
			if notes == "":
				notes = notes_line
			tot_notes += len(notes_line)
			
			# check if reaches end
			if notes_line.endswith(","):
				break
		
		self._fpos = fpos
		self._fobj.seek(fpos)
		
		return notes, tot_notes - 1
			
	def _read_notes_line(self):
		line = self.peek_line()
		ripped = ""
		for c in line:
			# Digit, means a note
			if c.isdigit(): ripped += c
			# `,` means end of a bar
			elif c == ",": return ripped + c
			# Space is ignored
			elif c.isspace(): continue
			# Else is invalid
			else: return ""
		return ripped
	
	def read_command(self):
		line = self.peek_line()
		cmd_name = ""
		args = ()
		if line.startswith("#"):
			parts = line.split(" ", 1)
			if len(parts) in (1, 2):
				cmd_name = parts[0].strip()
				if len(parts) == 1:
					args = ()
				else:
					args2 = []
					for str in parts[1].split(","):
						args2.append(str.strip())
					args = tuple(args2)
		
		return cmd_name, args
		
	def check_command(self, cmd):
		return self.peek_line().split(" ")[0].strip() == cmd
		
	def check_commands(self, cmd):
		return self.peek_line().split(" ")[0].strip() in cmd		
		
	def close(self):
		if self._fobj:
			self._fobj.close()
			self._fobj = None
	
if __name__ == "__main__":
	import tja_header
	import sys
	
	reader = CReader()
	reader.set_file(sys.argv[1])

	header = tja_header.CData()
	header.read(reader)
	header.refresh()
	header.print_out()
	
	while True:
		if reader.check_command("#END"):
			break
		notes = reader.read_notes()
		cmd_name, args = reader.read_command()
		if notes:
			print "[NOTES]", notes
		elif cmd_name:
			print "[ CMD ]", cmd_name, args
		else:
			print "[EMPTY]"
		reader.skip_line()
		