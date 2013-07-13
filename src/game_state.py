import gc
import scn_song_select
import scn_enso
import scn_dummy

GAME_STATE_NULL = 0
GAME_STATE_SONG_SELECT = 1
GAME_STATE_ENSO = 2
GAME_STATE_RESULT = 3

STATE_MODULES = {
	GAME_STATE_NULL: scn_dummy,
	GAME_STATE_SONG_SELECT: scn_song_select,
	GAME_STATE_ENSO: scn_enso,
	GAME_STATE_RESULT: scn_dummy,
}

cur_state = None
active_m = None
def set_game_state(state):
	global cur_state
	global active_m
	
	if state == cur_state: return

	m_old = None
	if cur_state != None:	
		m_old = STATE_MODULES[cur_state]
	gc.collect()
	m_new = STATE_MODULES[state]
	
	if m_old is not None:
		m_old.on_exit()	
	m_new.on_enter(m_new)

	cur_state = state
	active_m = m_new