# -*- coding: utf8 -*-
import os

SN_ENSO_SIZE = 20
SN_ENSO_HEIGHT = 30
SN_ENSO_WIDTH = 200

SN_TITLE_SIZE = 20
SN_TITLE_HEIGHT = 296
SN_TITLE_WIDTH = 48

SN_SUBTITLE_SIZE = SN_TITLE_SIZE * 2 / 3
SN_SUBTITLE_HEIGHT = 296
SN_SUBTITLE_WIDTH = 32

def convert(out_path, txt=u"Test", size=None, font=None, bgcolor=None, txt_color=None, hspacing=None, vspacing=None, align=None, font_size=None):
	cmd = "convert"
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
	cmd += ' label:"%s" %s' % (txt.encode("gbk"), out_path)
	print cmd
	os.system(cmd)

def gen_song_name_non_select(title, subtitle, out_folder):
	vtitle = u"\\n".join(title)
	convert(os.path.join(out_folder, "sn02.png"), txt=vtitle,
		size=(SN_TITLE_WIDTH, SN_TITLE_HEIGHT), font="D:/ds/imageMagic/DFKTLB.ttc",
		bgcolor=0x00000000, txt_color=0x000000FF, vspacing=-4, align="North",
		font_size=SN_TITLE_SIZE)

def gen_song_name_select_full(title, subtitle, out_folder):
	vtitle = u"\\n".join(subtitle)
	convert(os.path.join(out_folder, "sn03.png"), txt=vtitle,
		size=(SN_SUBTITLE_WIDTH, SN_SUBTITLE_HEIGHT), font="D:/ds/imageMagic/DFKTLB.ttc",
		bgcolor=0x00000000, txt_color=0x000000FF, vspacing=-4, align="South",
		font_size=SN_SUBTITLE_SIZE)

def gen_song_name_enso(title, subtitle, out_folder):
	convert(os.path.join(out_folder, "sn01.png"), txt=title,
		size=(SN_ENSO_WIDTH, SN_ENSO_HEIGHT), font="D:/ds/imageMagic/DFKTLB.ttc",
		bgcolor=0x00000000, txt_color=0x000000FF, hspacing=-3, align="East",
		font_size=SN_ENSO_SIZE)

def gen_song_name_texture(title, subtitle, out_folder):
	gen_song_name_enso(title, subtitle, out_folder)
	gen_song_name_non_select(title, subtitle, out_folder)
	gen_song_name_select_full(title, subtitle, out_folder)
	
if __name__ == '__main__':
	gen_song_name_enso(u"きたさいたま２０００", " ", ".")
	gen_song_name_non_select(u"きたさいたま２０００", " ", ".")
	gen_song_name_select_full(u"きたさいたま２０００", " ", ".")