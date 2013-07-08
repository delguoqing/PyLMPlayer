# -*- coding: utf8 -*-
import freetype
import Image
import array
import numpy

FORCE_RGBA = True

def gen0(font_file, pointsize, ch, out_path):
	face = freetype.Face(font_file)
	face.set_char_size(pointsize * 64)
	face.load_char(ch)
	bitmap = face.glyph.bitmap
	bitmap_array = array.array('B')
	
	if not FORCE_RGBA and len(bitmap.buffer) > 0:
		if bitmap.pitch == bitmap.width:
			bitmap_array.fromlist(bitmap.buffer)
			bitmap_string = bitmap_array.tostring()			
			image = Image.fromstring('L', (bitmap.width, bitmap.rows), bitmap_string)
		elif bitmap.pitch == bitmap.width * 3:
			bitmap_array.fromlist(bitmap.buffer)
			bitmap_string = bitmap_array.tostring()						
			image = Image.fromstring('RGB', (bitmap.width, bitmap.rows), bitmap_string)
		elif bitmap.pitch == bitmap.width * 4:
			bitmap_array.fromlist(bitmap.buffer)
			bitmap_string = bitmap_array.tostring()						
			image = Image.fromstring('RGBA', (bitmap.width, bitmap.rows), bitmap_string)
		else:
			unpacked_buffer = []
			for j in xrange(bitmap.rows):
				for i in xrange(bitmap.width):
					byte = bitmap.buffer[j * bitmap.pitch + i / 8]
					unpacked_buffer.append((byte & (1 << (7 - i % 8))) != 0 and 255 or 0)
			bitmap_array.fromlist(unpacked_buffer)
			bitmap_string = bitmap_array.tostring()
			#print len(unpacked_buffer), bitmap.width, bitmap.rows
			image = Image.fromstring('L', (bitmap.width, bitmap.rows), bitmap_string)
		image.save(out_path)
		
	if FORCE_RGBA and len(bitmap.buffer) > 0:
		assert bitmap.pitch == bitmap.width, "Only support normal pixel mode"
		expanded_buffer = []
		for byte in bitmap.buffer:
			expanded_buffer.extend([255, 255, 255, byte])
		bitmap_array.fromlist(expanded_buffer)
		bitmap_string = bitmap_array.tostring()
		image = Image.fromstring('RGBA', (bitmap.width, bitmap.rows), bitmap_string)
		image.save(out_path)
		
	return face.glyph.bitmap_left, face.glyph.bitmap_top, bitmap.width, bitmap.rows

# gen a glyph with border
def gen1(font_file, pointsize, ch, out_path):
	face = freetype.Face(font_file)
	face.set_char_size(pointsize * 64)
	RGBA = [('R',numpy.ubyte), ('G',numpy.ubyte), ('B',numpy.ubyte), ('A',numpy.ubyte)]

	# Outline
	flags = freetype.FT_LOAD_DEFAULT | freetype.FT_LOAD_NO_BITMAP
	face.load_char(ch, flags)
	slot = face.glyph
	glyph = slot.get_glyph()
	stroker = freetype.Stroker( )
	stroker.set(32, freetype.FT_STROKER_LINECAP_ROUND, freetype.FT_STROKER_LINEJOIN_ROUND, 0)
	glyph.stroke(stroker)
	blyph = glyph.to_bitmap(freetype.FT_RENDER_MODE_NORMAL, freetype.Vector(0,0)) 
	bitmap = blyph.bitmap
	width, rows, pitch = bitmap.width, bitmap.rows, bitmap.pitch
	top, left = blyph.top, blyph.left
	data = []
	for i in range(rows):
		data.extend(bitmap.buffer[i*pitch:i*pitch+width])
	Z = numpy.array(data).reshape(rows, width)
	O = numpy.zeros((rows,width), dtype=RGBA)
	O['A'] = Z
	O['R'] = 0
	O['G'] = 0
	O['B'] = 0

	if width == 0 or rows == 0:
			return 0, 0, 0, 0
	# Plain
	flags = freetype.FT_LOAD_RENDER
	face.load_char(ch, flags)
	F = numpy.zeros((rows,width), dtype=RGBA)
	Z = numpy.zeros((rows, width))
	bitmap = face.glyph.bitmap
	width, rows, pitch = bitmap.width, bitmap.rows, bitmap.pitch
	top, left = face.glyph.bitmap_top, face.glyph.bitmap_left
	
	dy = max(0, blyph.top - face.glyph.bitmap_top)
	dx = max(0, face.glyph.bitmap_left - blyph.left)
	if dx + rows >= blyph.bitmap.rows:
		rows = blyph.bitmap.rows - dx
	if dy + width >= blyph.bitmap.width:
		width = blyph.bitmap.width - dy
	data = []
	for i in range(rows):
		data.extend(bitmap.buffer[i*pitch:i*pitch+width])
	#print dx, dy
	#print width, rows
	#print Z.shape
	#print blyph.bitmap.width, blyph.bitmap.rows
	Z[dx:dx+rows,dy:dy+width] = numpy.array(data).reshape(rows, width)
	F['R'] = 255
	F['G'] = 255
	F['B'] = 255
	F['A'] = Z

	# Combine outline and plain
	R1,G1,B1,A1 = O['R'],O['G'],O['B'],O['A']
	R2,G2,B2,A2 = F['R'],F['G'],F['B'],F['A']
	Z = numpy.zeros(O.shape, dtype=RGBA)
	Z['R'] = (A1 / 255.0 * R1 + A2 / 255.0 * (1 - A1 / 255.0) * R2)
	Z['G'] = (A1 / 255.0 * G1 + A2 / 255.0 * (1 - A1 / 255.0) * G2)
	Z['B'] = (A1 / 255.0 * B1 + A2 / 255.0 * (1 - A1 / 255.0) * B2)
	Z['A'] = (A1 / 255.0 	  + A2 / 255.0 * (1 - A1 / 255.0)) * 255.0
	
	image = Image.fromarray(Z, mode="RGBA")
	image.save(out_path)
	return blyph.left, blyph.top, blyph.bitmap.width, blyph.bitmap.rows