import os
import random
import pyglet
from pyglet.gl import *

from lm import lm_consts
from lm import lm_loader
from lm.extensions import lm_render_state

import config

inited = False
renderer = None
loader = None

def on_update(dt):
	pass

def on_enter(this):
	if not inited:
		renderer = lm_render_state.CRenderer()
		renderer.init()
		
		loader = lm_loader.CLoader("wii", config["lm_root"], renderer)

def on_exit():
	pass

def on_key_press(symbol, modifiers):
	pass