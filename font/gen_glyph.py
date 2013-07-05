import freetype
import Image
import array

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
			expanded_buffer.extend([0, 0, 0, byte])
		bitmap_array.fromlist(expanded_buffer)
		bitmap_string = bitmap_array.tostring()
		image = Image.fromstring('RGBA', (bitmap.width, bitmap.rows), bitmap_string)
		image.save(out_path)
		
	return face.glyph.bitmap_left, face.glyph.bitmap_top, bitmap.width, bitmap.rows