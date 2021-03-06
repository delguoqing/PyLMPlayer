import sys
import optparse

# avoid use python module as config file
import enso_skin_def
import enso_skin_idol
from tja.tja_consts import OPTION_AUTO
from game_state import GAME_STATE_ENSO, GAME_STATE_SONG_SELECT

DATA = {
	"fullscreen": False,
	"widescreen": True,
	"wnd_width": 640,
	"wnd_height": 480,
	"wnd_scale": 2,
	"widescreen_padding": 108,
	
	"onp_hit_x": 150,
	"onp_y": 154,
	"onp_in_x": 640,
	"onp_out_x": 110,
	"onp_dist": 30,
	
	"enso_skin": enso_skin_idol,
	"lm_root": "../wii_packages",
	
	"fumen_file": r"C:\Users\GQ\Documents\GitHub\PyLMPlayer\song\animation\endless_story\Endless Story.tja",
	"course_idx": 0,
	
	"enso_option": 0,#OPTION_AUTO,
	
	"def_song_name_label": "../font/sn_game.png",
	"use_texture_as_song_name": False,
	
	"don_cos": "don/cos/cos_000/cos_000_%s/cos_000_%s.lm",
	"start_state": GAME_STATE_SONG_SELECT,
}

if len(sys.argv) > 1:
	DATA["fumen_file"] = sys.argv[1]

def save():
	pass

def load():
	pass

def update():
	pass
