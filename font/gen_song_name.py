# -*- coding: utf8 -*-
import os
import gen_glyph

SN_ENSO_SIZE = 14
SN_ENSO_HEIGHT = 35
SN_ENSO_WIDTH = 560

SN_TITLE_SIZE = 29
SN_TITLE_HEIGHT = 296
SN_TITLE_WIDTH = 48

SN_SUBTITLE_SIZE = 26
SN_SUBTITLE_HEIGHT = 296
SN_SUBTITLE_WIDTH = 48

TXT_COLOR = 0x000000FF
FONT = "DFKTLB.ttc"

ROTATE_CHARACTER = set(u"「」～（）ー-~")

def convert(out_path, txt=u"Test", size=None, font=None, bgcolor=None, txt_color=None, hspacing=None, vspacing=None, align=None, font_size=None, rotate=0):
	cmd = "convert.exe"
	if size is not None and not (size[0] is None and size[1] is None):
		width_str = str(size[0]) if size[0] is not None else ""
		height_str = str(size[1]) if size[1] is not None else ""
		cmd += " -size %sx%s" % (width_str, height_str)
	if font is not None:
		cmd += " -font %s" % font
	if bgcolor is not None:
		cmd += " -background #%08x" % bgcolor
	if txt_color is not None:
		cmd += " -fill #%08x" % txt_color
	if hspacing is not None:
		cmd += " -kerning %d" % hspacing
	if vspacing is not None:
		cmd += " -interline-spacing %d" % vspacing
	if align is not None:
		cmd += " -gravity %s" % align
	if font_size is not None:
		cmd += " -pointsize %d" % font_size
	cmd += ' label:"%s"' % txt.encode("gbk")
	if rotate != 0:
		cmd += " -rotate %d" % rotate
	cmd += " %s" % out_path
	print cmd
	os.system(cmd)

def vconvert(out_path, txt=u"Test", size=None, font=None, bgcolor=None, txt_color=None, hspacing=None, vspacing=None, align=None, font_size=None, rotate=0):
	# make background texture
	os.system("convert.exe -size %dx%d xc:#%08x %s" % (size[0], size[1], bgcolor, out_path))
	
	# generate character pic
	for idx, ch in enumerate(txt):
		r = 0
		if ch in ROTATE_CHARACTER: r = 90
		convert("token%d.png" % idx, txt=ch, font=font, bgcolor=bgcolor,
			txt_color=txt_color, rotate=r)
		
	# join all tokens
	os.system("convert.exe -gravity North -append %s test.png" % (" ".join(["token%d.png" % i for i in xrange(len(txt))])))
	

def gen_song_name_non_select(title, subtitle, out_folder):
	vtitle = u"\\n".join(title)
	convert(os.path.join(out_folder, "sn_non_select.png"), txt=vtitle,
		size=(SN_TITLE_WIDTH, SN_TITLE_HEIGHT), font=FONT,
		bgcolor=0x00000000, txt_color=TXT_COLOR, vspacing=-5, align="North",
		font_size=SN_TITLE_SIZE)

def gen_song_name_select_short(title, subtitle, out_folder):
	vtitle = u"\\n".join(title)
	convert(os.path.join(out_folder, "sn_select_short.png"), txt=vtitle,
		size=(80, SN_TITLE_HEIGHT), font=FONT,
		bgcolor=0x00000000, txt_color=TXT_COLOR, vspacing=-5, align="North",
		font_size=SN_TITLE_SIZE)
	
def gen_song_name_select_full(title, subtitle, out_folder):
	if not subtitle:
		vtitle = u"\\n".join(title)
		convert(os.path.join(out_folder, "sn_select_full.png"), txt=vtitle,
			size=(80, SN_TITLE_HEIGHT), font=FONT,
			bgcolor=0x00000000, txt_color=TXT_COLOR, vspacing=-5, align="North",
			font_size=SN_TITLE_SIZE)
	else:
		vconvert2(os.path.join(out_folder, "sn_subtitle.png"), txt=subtitle,
			size=(48, SN_SUBTITLE_HEIGHT), font=FONT,
			bgcolor=0x00000000, txt_color=TXT_COLOR, vspacing=-4, align="South",
			font_size=SN_SUBTITLE_SIZE)
		os.system("convert.exe -size 80x296 xc:#00000000 %s" % os.path.join(out_folder, "sn_select_full.png"))
		os.system("composite.exe -gravity East %s %s %s" % (
			os.path.join(out_folder, "sn_non_select.png"),
			os.path.join(out_folder, "sn_select_full.png"),
			os.path.join(out_folder, "sn_select_full.png")
			))		
		os.system("composite.exe %s %s %s" % (
			os.path.join(out_folder, "sn_subtitle.png"),
			os.path.join(out_folder, "sn_select_full.png"),
			os.path.join(out_folder, "sn_select_full.png")
			))

		#os.system("del %s" % os.path.join(out_folder, "sn_subtitle.png"))
		
def gen_song_name_enso(title, subtitle, out_folder):
	convert(os.path.join(out_folder, "sn_game.png"), txt=title,
		size=(SN_ENSO_WIDTH, SN_ENSO_HEIGHT), font=FONT,
		bgcolor=0xFFFFFF00, txt_color=TXT_COLOR, hspacing=-3, align="East",
		font_size=SN_ENSO_SIZE)

def gen_song_name_texture(title, subtitle, out_folder):
	gen_song_name_enso(title, subtitle, out_folder)
	gen_song_name_non_select(title, subtitle, out_folder)
	gen_song_name_select_short(title, subtitle, out_folder)
	gen_song_name_select_full(title, subtitle, out_folder)
	
def gen_glyphs_from_text(text):
	for token_idx, ch in enumerate(text):
		if not ch.isspace():
			gen_glyph.gen0(FONT, SN_TITLE_SIZE, ch, "token%d.png" % token_idx)
	
# vconvert version2
# using freetype generated glyph(without extra space) to build a good vertical text
def vconvert2(out_path, txt=u"Test", size=None, font=None, bgcolor=None, txt_color=None, hspacing=None, vspacing=None, align=None, font_size=None, rotate=0):
	# make background texture
	os.system("convert.exe -size %dx%d xc:#%08x %s" % (size[0], size[1], bgcolor, out_path))
	
	# gen character pic
	gen_glyphs_from_text(txt)
	
	# handle special character
	for token_idx, ch in enumerate(txt):
		if ch.isspace():	# increase a small gap
			os.system("convert.exe -size %dx%d xc:#%08x token%d.png" % (size[0], 3, bgcolor, token_idx))
			continue
		if ch in ROTATE_CHARACTER:	# rotate if needed
			os.system("convert.exe -rotate 90 token%d.png token%d.png" % (token_idx, token_idx))
			continue
					
	# join all tokens
	os.system("convert.exe -gravity South -append %s %s" % (" ".join(["token%d.png" % i for i in xrange(len(txt))]), out_path))

if __name__ == '__main__':
	gen_song_name_texture(u"カロン", u"ＴＶＣＭ「ＬＩＳＭＯ！」より", ".")
	gen_song_name_texture(u"ガツガツ！！", u"「トリコ」より", ".")
	#vconvert2("test.png", txt=u"ＴＶＣＭ「ＬＩＳＭＯ！」より",
			#size=(80, SN_TITLE_HEIGHT), font=FONT,
			#bgcolor=0x00000000, txt_color=TXT_COLOR, vspacing=-5, align="North",
			#font_size=SN_TITLE_SIZE)
	#gen_glyphs_from_text(u"恋は混沌の隷也")#Seasons of Asia～～")