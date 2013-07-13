# -*- coding: utf8 -*-
import os
import gen_glyph

SN_ENSO_SIZE = 28
SN_ENSO_HEIGHT = 35
SN_ENSO_WIDTH = 560

SN_TITLE_SIZE = 29
SN_TITLE_HEIGHT = 280
SN_TITLE_WIDTH = 48

SN_SUBTITLE_SIZE = 22
SN_SUBTITLE_HEIGHT = 280
SN_SUBTITLE_WIDTH = 48

BG_COLOR = 0x00000000
TXT_COLOR = 0xFFFFFFFF

# For test
BG_COLOR = 0xEEEEEE00
TXT_COLOR = 0x000000FF

FONT = "DFKTLB.TTC"
EXE_CONVERT = "convert.exe"
EXE_COMPOSITE = "composite.exe"

ROTATE_CHARACTER = set(u"「」～（）ー-~－∞—()《》{}<>『』[]…")

def gen_song_name_non_select(title, subtitle, out_folder):
	vconvert2(os.path.join(out_folder, "sn_non_select.png"), txt=title,
		size=(SN_TITLE_WIDTH, SN_TITLE_HEIGHT), font=FONT,
		bgcolor=BG_COLOR, txt_color=TXT_COLOR, vspacing=-5, align="North",
		font_size=SN_TITLE_SIZE)

def gen_song_name_select_short(title, subtitle, out_folder):
	vconvert2(os.path.join(out_folder, "sn_select_short.png"), txt=title,
		size=(80, SN_TITLE_HEIGHT), font=FONT,
		bgcolor=BG_COLOR, txt_color=TXT_COLOR, vspacing=-5, align="North",
		font_size=SN_TITLE_SIZE)
	
def gen_song_name_select_full(title, subtitle, out_folder):
	if not subtitle:
		vconvert2(os.path.join(out_folder, "sn_select_full.png"), txt=title,
			size=(80, SN_TITLE_HEIGHT), font=FONT,
			bgcolor=BG_COLOR, txt_color=TXT_COLOR, vspacing=-5, align="North",
			font_size=SN_TITLE_SIZE)
	else:
		vconvert2(os.path.join(out_folder, "sn_subtitle.png"), txt=subtitle,
			size=(48, SN_SUBTITLE_HEIGHT), font=FONT,
			bgcolor=BG_COLOR, txt_color=TXT_COLOR, vspacing=-4, align="South",
			font_size=SN_SUBTITLE_SIZE)
		os.system("%s -size 80x280 xc:#%08x \"%s\"" % (EXE_CONVERT, BG_COLOR, os.path.join(out_folder, "sn_select_full.png")))
		os.system("%s -gravity Southwest \"%s\" \"%s\" \"%s\"" % (
			EXE_COMPOSITE,
			os.path.join(out_folder, "sn_subtitle.png"),
			os.path.join(out_folder, "sn_select_full.png"),
			os.path.join(out_folder, "sn_select_full.png")
			))		
		os.system("%s -gravity Northeast \"%s\" \"%s\" \"%s\"" % (
			EXE_COMPOSITE,
			os.path.join(out_folder, "sn_non_select.png"),
			os.path.join(out_folder, "sn_select_full.png"),
			os.path.join(out_folder, "sn_select_full.png")
			))
		os.system("del \"%s\"" % os.path.join(out_folder, "sn_subtitle.png"))


		#os.system("del %s" % os.path.join(out_folder, "sn_subtitle.png"))
		
def gen_song_name_enso(title, subtitle, out_folder):
	hconvert2(os.path.join(out_folder, "sn_game.png"), txt=title,
		size=(SN_ENSO_WIDTH, SN_ENSO_HEIGHT), font=FONT,
		bgcolor=BG_COLOR, txt_color=TXT_COLOR, hspacing=-3, align="East",
		font_size=SN_ENSO_SIZE)

def gen_song_name_texture(title, subtitle, out_folder, font="DFKTLB.TTC"):
	global FONT
	FONT = font
	gen_song_name_enso(title, subtitle, out_folder)
	gen_song_name_non_select(title, subtitle, out_folder)
	gen_song_name_select_short(title, subtitle, out_folder)
	gen_song_name_select_full(title, subtitle, out_folder)
	
def gen_glyphs_from_text(text, size):
	ret = []
	for token_idx, ch in enumerate(text):
		if not ch.isspace():
			left, top, w, h = gen_glyph.gen1(FONT, size, ch, "token%d.png" % token_idx)
			ret.append((w, h))
		else:
			ret.append((0, 0))
	return ret
	
def gen_glyphs_from_text_detailed(text, size):
	ret = []
	for token_idx, ch in enumerate(text):
		if not ch.isspace():
			left, top, w, h = gen_glyph.gen1(FONT, size, ch, "token%d.png" % token_idx)
			ret.append((left, top, w, h))
		else:
			ret.append((0, 0, 0, 0))
	return ret

# vconvert version2
# using freetype generated glyph(without extra space) to build a good vertical text
def vconvert2(out_path, txt=u"Test", size=None, font=None, bgcolor=None, txt_color=None, hspacing=None, vspacing=None, align=None, font_size=None, rotate=0):
	# gen character pic
	glyph_sizes = gen_glyphs_from_text(txt, font_size)
	
	# handle special character
	for token_idx, ch in enumerate(txt):
		if glyph_sizes[token_idx] == (0, 0):	# increase a small gap
			os.system("%s -size %dx%d xc:#%08x token%d.png" % (EXE_CONVERT, size[0], 6, bgcolor, token_idx))
			glyph_sizes[token_idx] = (size[0], 6)
			continue
		if ch in ROTATE_CHARACTER:	# rotate if needed
			os.system("%s -rotate 90 token%d.png token%d.png" % (EXE_CONVERT, token_idx, token_idx))
			glyph_sizes[token_idx] = (glyph_sizes[token_idx][1], glyph_sizes[token_idx][0])
			continue
					
	# join all tokens
	gravity = align or "North"
	os.system("%s -gravity %s -background #%08x -append %s \"%s\"" % (EXE_CONVERT, gravity, bgcolor, " ".join(["token%d.png" % i for i in xrange(len(txt))]), out_path))
	#os.system("convert.exe -gravity %s -background #%08x -append %s %s" % (gravity, bgcolor, " ".join(["token%d.png" % i for i in xrange(len(txt))]), "test.png"))
	os.system("del token*.png")
	
	# width and height
	height = 0
	width = 0
	for w, h in glyph_sizes:
		height += h
		width = max(width, w)

	#print "size = (%d, %d)" % (width, height)
	
	# scaling carefully
	scale = 1.0
	scale = min(scale, 1.0 * size[0] / width)
	scale = min(scale, 1.0 * size[1] / height)
	if scale < 1.0:
		os.system("%s \"%s\" -resize %f%% \"%s\"" % (EXE_CONVERT, out_path, scale * 100, out_path))
		width = int(width * scale)
		height = int(height * scale)
	#print "scale = %f" % scale
	#print "scaled_size = (%d, %d)" % (width, height)
	
	# Adding border
	border_x = abs((size[0] - width) // 2)
	border_y = abs((size[1] - height) // 2)
	if border_x != 0 or border_y != 0:
		os.system("%s \"%s\" -bordercolor #FFFFFF00 -border %dx0 \"%s\"" % (EXE_CONVERT, out_path, border_x, out_path))
		os.system("%s \"%s\" -gravity %s -background #FFFFFF00 -extent %dx%d \"%s\"" % (EXE_CONVERT, out_path, align, size[0], size[1], out_path))

def hconvert2(out_path, txt=u"Test", size=None, font=None, bgcolor=None, txt_color=None, hspacing=None, vspacing=None, align=None, font_size=None, rotate=0):
	# gen character pic
	glyph_metrics = gen_glyphs_from_text_detailed(txt, font_size)
	
	max_top = -1
	for token_idx, ch in enumerate(txt):
		_left, _top, _w, _h = glyph_metrics[token_idx]
		max_top = max(max_top, _top)
		
	# handle special character
	for token_idx, ch in enumerate(txt):
		_left, _top, _w, _h = glyph_metrics[token_idx]
		if (_w, _h) == (0, 0):	# increase a small gap
			os.system("%s -size %dx%d xc:#%08x token%d.png" % (EXE_CONVERT, 6, size[1], bgcolor, token_idx))
			glyph_metrics[token_idx] = (_left, _top, 6, size[1])
			continue
		else:
			padding = max_top - _top
			#print "padding %d" % padding
			if padding > 0:
				os.system("%s token%d.png -background #%08x -gravity South -extent %dx%d token%d.png" % (EXE_CONVERT, token_idx, bgcolor, _w, _h + padding, token_idx))
				glyph_metrics[token_idx] = (_left, _top, _w, _h + padding)
					
	# join all tokens
	gravity = align or "East"
	os.system("%s -gravity %s -background #%08x +append %s \"%s\"" % (EXE_CONVERT, gravity, bgcolor, " ".join(["token%d.png" % i for i in xrange(len(txt))]), out_path))
	#os.system("convert.exe -gravity %s -background #%08x -append %s %s" % (gravity, bgcolor, " ".join(["token%d.png" % i for i in xrange(len(txt))]), "test.png"))
	os.system("del token*.png")
	
	# width and height
	height = 0
	width = 0
	for left, top, w, h in glyph_metrics:
		width += h
		height = max(height, w)

	#print "size = (%d, %d)" % (width, height)
	
	# scaling carefully
	scale = 1.0
	scale = min(scale, 1.0 * size[0] / width)
	scale = min(scale, 1.0 * size[1] / height)
	if scale < 1.0:
		os.system("%s \"%s\" -resize %f%% \"%s\"" % (EXE_CONVERT, out_path, scale * 100, out_path))
		width = int(width * scale)
		height = int(height * scale)
	#print "scale = %f" % scale
	#print "scaled_size = (%d, %d)" % (width, height)
	
	# Adding border
	border_x = abs((size[0] - width) // 2)
	border_y = abs((size[1] - height) // 2)
	if border_x != 0 or border_y != 0:
		os.system("%s \"%s\" -bordercolor #FFFFFF00 -border 0x%d \"%s\"" % (EXE_CONVERT, out_path, border_y, out_path))
		os.system("%s \"%s\" -gravity %s -background #FFFFFF00 -extent %dx%d \"%s\"" % (EXE_CONVERT, out_path, align, size[0], size[1], out_path))
		
if __name__ == '__main__':
	#gen_song_name_texture(u"カロン", u"ＴＶＣＭ「ＬＩＳＭＯ！」より", ".")
	#gen_song_name_texture(u"ガツガツ！！", u"「トリコ」より", ".")
	#gen_song_name_texture(u"季曲", u"～Ｓｅａｓｏｎｓ　Ｏｆ　Ａｓｉａ～", ".")
	#gen_song_name_texture(u"蓄勢", u"～Ｇｅａｒ Ｕｐ～", ".")
	#gen_song_name_texture(u"蓄勢（裏）", u"～Ｇｅａｒ Ｕｐ～", ".")
	#gen_song_name_texture(u"蛻變", u"～Ｔｒａｎｓｆｏｒｍａｔｉｏｎ～", ".")
	gen_song_name_texture(u"Ｒｏｔｔｅｒ　Ｔａｒｍｉｎａｔｉｏｎ", u"　", ".")
	#gen_song_name_texture(u"きがつけば　あなた", u"ＫＩＲＩＮ「午後の紅茶」ＣＭソング", ".")
	#gen_song_name_texture(u"練習曲ＯＰ．１０－４", u"　", ".")    
	#vconvert2("test.png", txt=u"ＴＶＣＭ「ＬＩＳＭＯ！」より",
			#size=(80, SN_TITLE_HEIGHT), font=FONT,
			#bgcolor=0x00000000, txt_color=TXT_COLOR, vspacing=-5, align="North",
			#font_size=SN_TITLE_SIZE)
	#gen_glyphs_from_text(u"恋は混沌の隷也")#Seasons of Asia～～")
