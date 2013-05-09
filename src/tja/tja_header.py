import sys

class CData(object):
	
	def __init__(self, init_data=None):
		self._dict = {}
		if init_data: 
			self._dict.update(init_data)
		
	def read(self, reader):
		while True:
			# Start of fumen is end of header
			if reader.check_command("#START"):
				break
			
			key, val = reader.read_header()
			reader.skip_line()
			if key:
				self._dict[key] = val
			
	def _key_defs(self):
		return {
			"TITLE": (unicode, self._conv_unicode, u"UNTITLED"),
			"SUBTITLE": (unicode, self._conv_unicode, u""),
			"WAVE": (unicode, self._conv_unicode, u"NULL.ogg"),
			"BPM": (float, float, 100.0),
			"OFFSET": (float, float, 0.0),
			"SONGVOL": (float, float, 100.0),
			"SEVOL": (float, float, 100.0),
			"DEMOSTART": (float, float, 0.0),
			
			"BALLOON": (list, self._parse_int_list, [5, 5, 5]),
			"SCOREINIT": (int, int, 1),
			"SCOREDIFF": (int, int, 1),
			"LEVEL": (int, int, 9),
			"COURSE": (int, self._conv_course, 3),
		}.iteritems()

	# Guessing encoding		
	def _conv_unicode(self, str):
		try:
			ret1 = str.decode("gbk").encode("utf-8")
		except:
			ret1 = None
	
		try:
			ret2 = str.decode("shift-jis").encode("utf-8")
		except:
			ret2 = None
	
		try:
			ret3 = str.decode("big5").encode("utf-8")
		except:
			ret3 = None
		
		ret = []
		if ret1: ret.append(ret1)
		if ret2: ret.append(ret2)
		if ret3: ret.append(ret3)
		if not ret:
			return str
		else:
			ans = None
			for ret0 in ret:
				if ans is None or len(ret0) < len(ans):
					ans = ret0
			return ans.decode("utf-8")
		
	def _parse_int_list(self, str):
		str_list = str.split(",")
		ret = []
		for str in str_list:
			ret.append(int(str))
		return ret
		
	def _conv_course(self, str):
		# Try using course name
		try:
			course = ("Easy", "Normal", "Hard", "Oni").index(str)
			return course
		except ValueError:
			pass
		# Try using course index
		return max(0, min(int(str), 3))
		
	def refresh(self):
		for name, (value_type, converter, default) in self._key_defs():
			if name not in self._dict:
				self._dict[name] = default
			value = self._dict[name]
			if not isinstance(value, value_type):
				try:
					self._dict[name] = converter(value)
				except:
					print "%s convert failed! raw value=%s" % (name, value)
					self._dict[name] = default
	
	def print_out(self):
		print "\n".join(["%s:%r" % (k, v) for k, v in self._dict.iteritems()])
#		print "%s,%s,%s" % (self._dict["TITLE"], self._dict["SUBTITLE"], self._dict["WAVE"])
		
if __name__ == "__main__":
	f = open(sys.argv[1], "r")
	d = CData()
	d.read(f)
	d.refresh()
	
	print "-" * 10
	d.print_out()
	
	d.read(f)
	d.refresh()

	print "-" * 10	
	d.print_out()
	
	d.read(f)
	d.refresh()

	print "-" * 10	
	d.print_out()
	
	d.read(f)
	d.refresh()

	print "-" * 10	
	d.print_out()
