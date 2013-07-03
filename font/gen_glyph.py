import freetype
import Image
import array

def gen0(font_file, pointsize, ch, out_path):
	face = freetype.Face(font_file)
	face.set_char_size(pointsize * 64)
	face.load_char(ch)
	bitmap = face.glyph.bitmap
	bitmap_array = array.array('B')
	bitmap_array.fromlist(bitmap.buffer)
	bitmap_string = bitmap_array.tostring()
	image = Image.fromstring('L', (bitmap.width, bitmap.rows), bitmap_string)
	image.save(out_path)
