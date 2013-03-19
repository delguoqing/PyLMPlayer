import struct

def _read_normal(fdef, tag, off, g):
	name, size, fmt = fdef
	if type(size) == type("") and "g['" in size:
		size = eval(size)
	if type(fmt) == type("") and "g['" in fmt:
		fmt = eval(fmt)
	
	if size <= 0:
		v = None
	else:
		assert size == struct.calcsize(fmt), "Size not match Format! %r, %r" % (size, struct.calcsize(fmt))
		v = struct.unpack(fmt, tag[off: off + size])[0]
		
	g[name] = v
	g['off'] = off + size
	
	return v, tag, off + size
	
def _read_list(fdef, tag, off, g):
	name, size, fmt, arr = fdef
	assert fmt == "list", "Not A List"
	if type(size) == type("") and "g['" in size:
		size = eval(size)
	
	v = []
	for i in xrange(size):
		_v, tag, off = _read_tag(arr, tag, off, g)
		v.append(_v)
	g[name] = v
	return v, tag, off
	
def _read_tag(fdef, tag, off, g):
	myv = {}
	for _fdef in fdef:
		name, size, fmt = _fdef[:3]
		if fmt == "list":
			v, tag, off = _read_list(_fdef, tag, off, g)
		else:
			v, tag, off = _read_normal(_fdef, tag, off, g)
		myv[name] = v
	return myv, tag, off
	
def read_tag(fdef, tag):
	off = 0
	g = {"off": 0}
	v, tag, off = _read_tag(fdef, tag, off, g)
	
	# TODO: Remove This!
	# Used to detect tag with bad size
	if len(fdef) != 2:
		header_size = fdef[0][1] + fdef[1][1]
		assert off == v["tag_size"] * 4 + header_size, "off = 0x%x, tag_type = 0x%04x, tag_size = 0x%x, header_size = 0x%x" % (off, v["tag_type"], v["tag_size"], header_size)
	
	v["off"] = off
	return v