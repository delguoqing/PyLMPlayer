# sprite[17] names=lower,
# Note: `bg` contains a `lower` and an `upper`.
# when the `bg` wants to change genre, `lower` is set to old genre, `upper` is
# set to new genre. When the 'upper' plays a tween animation, it seems that a
# new genre bg is appearing on top of the old(the 'lower')
def func0(this, _global):
	this._parent.board_move.genreNo = 0
	this._root.currentBgGenre = 0
	this.stop()

def func1(this, _global):
	this._parent.board_move.genreNo = 1
	this._root.currentBgGenre = 1
	this.stop()

def func2(this, _global):
	this._parent.board_move.genreNo = 2
	this._root.currentBgGenre = 2
	this.stop()

def func3(this, _global):
	this._parent.board_move.genreNo = 3
	this._root.currentBgGenre = 3
	this.stop()

def func4(this, _global):
	this._parent.board_move.genreNo = 4
	this._root.currentBgGenre = 4
	this.stop()

def func5(this, _global):
	this._parent.board_move.genreNo = 5
	this._root.currentBgGenre = 5
	this.stop()

def func6(this, _global):
	this._parent.board_move.genreNo = 6
	this._root.currentBgGenre = 6
	this.stop()

def func7(this, _global):
	this._parent.board_move.genreNo = 6
	this._root.currentBgGenre = 7
	this.stop()

# sprite[19] names=upper,
# Note: `bg` contains a `lower` and an `upper`.
# when the `bg` wants to change genre, `lower` is set to old genre, `upper` is
# set to new genre. When the 'upper' plays a tween animation, it seems that a
# new genre bg is appearing on top of the old(the 'lower')
def func8(this, _global):
	this.stop()

def func9(this, _global):
	this._parent.lower.gotoAndPlay("genre0")
	this.stop()

def func10(this, _global):
	this._parent.lower.gotoAndPlay("genre1")
	this.stop()
	
def func11(this, _global):
	this._parent.lower.gotoAndPlay("genre2")
	this.stop()

def func12(this, _global):
	this._parent.lower.gotoAndPlay("genre3")
	this.stop()

def func13(this, _global):
	this._parent.lower.gotoAndPlay("genre4")
	this.stop()

def func14(this, _global):
	this._parent.lower.gotoAndPlay("genre5")
	this.stop()

def func15(this, _global):
	this._parent.lower.gotoAndPlay("genre6")
	this.stop()

def func16(this, _global):
	this._parent.lower.gotoAndPlay("genre7")
	this.stop()

# sprite[20] bg
# Note: `bg` contains a `lower` and an `upper`.
# when the `bg` wants to change genre, `lower` is set to old genre, `upper` is
# set to new genre. When the 'upper' plays a tween animation, it seems that a
# new genre bg is appearing on top of the old(the 'lower')
def bg_onEnterFrame(this, _global):
	if (this._root.currentGenre != this._root.currentBGGenre):
		this.gotoAndPlay("genre%d" % this._root.currentGenre)

def func17(this, _global):
	this._root._Bg_init(this);
	this.onEnterFrame = bg_onEnterFrame

def func18(this, _global):
	this.gotoAndPlay("loop")

# sprite[117] names=,crown
# WTF?
def func19(this, _global):
	#zzzzzzz;
	pass

def func20(this, _global):
	this.stop()
	#Z;
	pass

# sprite[123]
# Is this song name?
def func21(this, _global):
	this.gotoAndStop("song_title%d" % this._parent.board_num)

# sprite[130] names=song_board_0~song_board10,

# sprite[151] names=bunk1,
def func22(this, _global):
	if this._parent.hasBunki:
		this.gotoAndPlay("visible")

def func23(this, _global):
	this.gotoAndPlay("visible")

# sprite[172] names=star,
def func24(this, _global):
	this.stop()

# sprite[177]
# Muzukashii
def func25(this, _global):
	if _root.isExFumen():
		this.nextFrame()
	else:
		this._root._RankStar_init(star, 2)
		this.stop()

# sprite[180]
# Futsu
def func26(this, _global):
	if _root.isExFumen():
		this.nextFrame()
	else:
		this._root._RankStar_init(star, 1)
		this.stop()
		
# sprite[183]
# Kantan
def func27(this, _global):
	if _root.isExFumen():
		this.nextFrame()
	else:
		this._root._RankStar_init(star, 0)
		this.stop()

# sprite[186]
# Oni	
def func28(this, _global):
	this._root._RankStar_init(star, 3)
	this.stop()

# sprite[187], names=course
def func29(this, _global):
	if this._root.oniReleased:
		if this._root.isExFumen():
			this.gotoAndPlay("ex")
		else:
			this.gotoAndPlay("oni")

# sprite[202], names=use_lyric
def func30(this, _global):
	this._root._LyricBoard_init(this)

def func31(this, _global):
	this._parent.board_move.genreNo = 0
	this.stop()

def func32(this, _global):
	this._parent.board_move.genreNo = 1
	this.stop()

def func33(this, _global):
	this._parent.board_move.genreNo = 2
	this.stop()

def func34(this, _global):
	this._parent.board_move.genreNo = 3
	this.stop()

def func35(this, _global):
	this._parent.board_move.genreNo = 4
	this.stop()

def func36(this, _global):
	this._parent.board_move.genreNo = 5
	this.stop()

def func37(this, _global):
	this._parent.board_move.genreNo = 6
	this.stop()

# sprite[217], names=base_board,
# sprite[239], names=base_board,

# sprite[220], names=board_easy,
# sprite[223], names=board_normal,
# sprite[226], names=board_hard,
# sprite[242], names=board_option
# sprite[245], names=board_tone
# sprite[248], names=board_score
# sprite[251], names=board_back
# sprite[254], names=board_mania
def func38(this, _global):
	this.gotoAndPlay(this._parent.board_label)

# sprite[255], names=menu,
def func39(this, _global):
	if this._root.oniReleased:
		if this._root.isExFumen():
			this.gotoAndPlay("ex")
		else:
			this.gotoAndPlay("oni")
	else:
		this.gotoAndPlay("no_oni")

# sprite[257], names=selected_board_1p~selected_board_4p,
def func40(this, _global):
	this.gotoAndPlay("unselected")

def func41(this, _global):
	this.gotoAndPlay("select")

def func42(this, _global):
	this.swapDepths(this._parent.selected_dummy)

def func43(this, _global):
	this.swapDepths(this._parent.selected_dummy)
	this._root._CourseMenu_nextSequence(_parent)
	this.gotoAndPlay("unselect")

# sprite[258], names=selected_board_dummy
# sprite[289], names=cursor

# sprite[290], names=move_cursor
def func44(this, _global):
	this._root._Cursor_init(this)

# sprite[291], names=cursor1p~cursor4p
def func45(this, _global):
	this._root._CourseMenu_updateSelection(this._parent, this)
	this.stop()

def func46(this, _global):
	this.gotoAndStop("pos0")

def func47(this, _global):
	this.gotoAndStop("pos4oni")



# sprite[300], names=course_select
def func64(this, _global):
	this._root._CourseMenu_init(this)
	this.gotoAndPlay("animation")

def func65(this, _global):
	this._root._CourseMenu_start(this)

def func66(this, _global):
	this._root._CourseMenu_timerCountUp(this._parent)

def func67(this, _global):
	this._root.main_movie.gotoAndPlay("submenu")
	this.stop()

def func68(this, _global):
	this._parent.gotoAndPlay("to_song_select")

def func69(this, _global):
	this._parent.gotoAndPlay("to_rule_select")

def func70(this, _global):
	this._root.exitSongSelect()
	this.stop()

# sprite[304], names=board_back
def func71(this, _global):
	this._root._CourseMenuBoard_selectAnimeStart(this)

# sprite[317], names=board
# sprite[333], names=board

# sprite[318], names=board_random
# sprite[320], names=board_total
# sprite[322], names=board_great
# sprite[324], names=board_combo
# sprite[326], names=board_score
# sprite[341], names=board_nakayoku
def func72(this, _global):
	this.stop()
	this._parent.gotoAndPlay("to_select_end")

# sprite[334], names=board
def func73(this, _global):
	if this._root.ruleMenuUseItem:
		this.board.gotoAndPlay("item")
	else:
		this.board.gotoAndPlay("no_item")
	this.gotoAndPlay("wait")

def func74(this, _global):
	if this._root.ruleMenuUseItem:
		this.board.gotoAndPlay("item")
	else:
		this.board.gotoAndPlay("no_item")

# sprite[334], names=board_item
# sprite[353], names=panel

# sprite[354], names=help_panel
def func75(this, _global):
	this._root._RuleHelp_init(this)

def func76(this, _global):
	this._root._RuleHelp_change0(this)

def func77(this, _global):
	this._root._RuleHelp_change(this)



# sprite[356], names=rule_select
def func94(this, _global):
	this._root._RuleMenu_init(this)
	this.gotoAndPlay("animation")

def func95(this, _global):
	this._root._RuleMenu_randomAnimationStart(this)

def func96(this, _global):
	this._root._RuleMenu_randomSelectWait(this)

def func97(this, _global):
	this._root.main_movie.gotoAndPlay("caution")
	this.stop()

def func98(this, _global):
	this._parent.selected_course_1p.gotoAndPlay("none")
	this._parent.selected_course_2p.gotoAndPlay("none")
	this._parent.gotoAndPlay("to_course_select")

# sprite[364], names=open_board
def func99(this, _global):
	this._root.songStart()

def func100(this, _global):
	this.gotoAndPlay("to_course_select")

def func101(this, _global):
	this._parent.gotoAndPlay("restart")

def func102(this, _global):
	this._parent.gotoAndPlay("select_end")

def func103(this, _global):
	if not this._root.isRandomBoardSelected():
		this._visible = false

# sprite[364], names=out_board

# sprite[372], names=skip_genre
def func104(this, _global):
	this.continue_flag = False
	this.right_skip_flag = False
	this.left_skip_flag = False

def func105(this, _global):
	this.right_skip_flag = True
	this.left_skip_flag = False

def func106(this, _global):
	if not continue_flag:
		this.gotoAndPlay("right_skip_end")

def func107(this, _global):
	this.continue_flag = False;
	this.gotoAndPlay("right_skip")

def func108(this, _global):
	this.gotoAndPlay("init")
	this.stop()

def func109(this, _global):
	this.right_skip_flag = False
	this.left_skip_flag = True

def func110(this, _global):
	if not continue_flag:
		this.gotoAndPlay("left_skip_end")

def func111(this, _global):
	this.continue_flag = False
	this.gotoAndPlay("left_skip")

# sprite[388], names=board
# sprite[410], names=digit0~digit6

# sprite[411], names=score_mc
def func124(this, _global):
	this._root.setNumberDisplay(this, value, 7, false)
	this.stop()

# sprite[418], names=mania,hard,normal,easy,
def func125(this, _global):
	this.board.gotoAndPlay(this._name)
	this.hiscore_mii.gotoAndStop(this._name)
	this.score_mc.value = this.value
	this.stop()

# sprite[419], names=hiscore
def func126(this, _global):
	if this._root.oniReleased:
		if this._root.isExFumen():
			this.gotoAndPlay("ex")
		else:
			this.gotoAndPlay("oni")
	this._root._HiscoreData_init(this)

# sprite[420], names=hiscore
def func127(this, _global):
	this._root._Hiscore_init(this)

def func128(this, _global):
	this._root._Hiscore_countUp(this)

def func129(this, _global):
	this.gotoAndPlay(this._play_head - 1)

def func130(this, _global):
	this._root._Hiscore_fadeinEnd(this)

def func131(this, _global):
	this._root._Hiscore_fadeoutEnd(this)

# sprite[422], names=board_move
def func132(this, _global):
	this._root._SongMenu_init(this)
	this.stop()

def func133(this, _global):
	this._root._SongMenu_start(this)

def func134(this, _global):
	this._root._SongMenu_initialAnimationEnd(this)

def func135(this, _global):
	this.gotoAndPlay("select_start")

def func136(this, _global):
	this._root._SongMenu_SelectStart(this)
	this._root.dispCursor(this)

def func137(this, _global):
	this._root._SongMenu_randomSelectStart(this)

def func138(this, _global):
	this._root._SongMenu_randomSelectWait(this)

def func139(this, _global):
	this.gotoAndPlay("open")

def func140(this, _global):
	this._root._SongMenu_KisekaeWait(this)

def func141(this, _global):
	this.open_board.gotoAndPlay("open")

def func142(this, _global):
	this._root._SongMenu_openCountUp()

def func143(this, _global):
	this.open_board.gotoAndPlay("select")
	this._root.dispCursor(this)

def func144(this, _global):
	this._root._SongMenu_closeEnd(this)

def func145(this, _global):
	this.open_board.gotoAndPlay("wide_open")

def func146(this, _global):
	this.open_board.gotoAndPlay("select")
	this.gotoAndPlay("start")

# sprite[441] names=enso_option_1p~enso_option_4p
# sprite[458] names=selected_course_1p~selected_course_4p

# sprite[459]
# ?
def func148(this, _global):
	this._root.prepareCrown(0)
	this._root.prepareCrown(1)

def func149(this, _global):
	this._root.prepareCrown(2)
	this._root.prepareCrown(3)

def func150(this, _global):
	this._root.prepareCrown(4)
	this._root.prepareCrown(5)

def func151(this, _global):
	this._root.prepareCrown(6)
	this._root.prepareCrown(7)

def func152(this, _global):
	this._root.prepareCrown(8)
	this._root.prepareCrown(9)

def func153(this, _global):
	this._root.prepareCrown(10)

def func154(this, _global):
	this._root.initPlayerIcon(0)

def func155(this, _global):
	this._root.initPlayerIcon(1)

def func156(this, _global):
	this._root.initPlayerIcon(2)

def func157(this, _global):
	this._root.initPlayerIcon(3)

# sprite[470] names=caption,

# sprite[486] names=ranking,
def func158(this, _global):
	this.rank1.ranking_name = ""
	this.rank2.ranking_name = ""
	this.rank3.ranking_name = ""

def func159(this, _global):
	if not _root._Ranking_init(this):
		this.gotoAndPlay(this._play_head - 1)

def func160(this, _global):
	this.waitCount = 0

def func161(this, _global):
	if this.waitCount < this._root.RANKING_CHANGE_FRAME:
		this.waitCount += 1
		this.gotoAndPlay(this._play_head - 1)

def func162(this, _global):
	this._root._Ranking_change(this)

# sprite[487] names=ranking,
def func163(this, _global):
	this._root._Ranking_open(this.ranking)
	this.stop()

def func164(this, _global):
	this._root._Ranking_close(this.ranking)

def func165(this, _global):
	this.ranking.gotoAndPlay("init")
	this.gotoAndPlay("wait")

# sprite[495] names=caution,
def func167(this, _global):
	this._root.main_movie.board_move.open_board.rule_select.gotoAndPlay("rule_select")
	this._root.main_movie.gotoAndPlay("main")

# sprite[496] names=main_movie,
def func168(this, _global):
	this._root._Main_init(this)

def func169(this, _global):
	this._root._LoadCheck(this)

def func170(this, _global):
	this._root._Main_start1(this)

def func171(this, _global):
	this._root._Main_start2(this)
	
def func172(this, _global):
	this._root._Main_start3(this)

def func173(this, _global):
	this._root.waitSubMenuClose(this)
	
def func174(this, _global):
	this.board_move.open_board.course_select.gotoAndPlay("course_select")
	this.gotoAndPlay("main")

# sprite[498] names=_root,
# defining a song select sound class, ignore this.
def func175(this, _global):
	pass
	
def func176(this, _global):
	pass
	
def placeholder(this, _global):
	this.stop()

DATA = (
	func0,
	func1,
	func2,
	func3,	
	func4,
	func5,
	func6,
	func7,
	func8,
	func9,
	func10,
	func11,
	func12,
	func13,
	func14,
	func15,
	func16,
	func17,
	func18,
	func19,
	func20,
	func21,
	func22,
	func23,					
	func24,	
	func25,		
	func26,
	func27,
	func28,
	func29,
	func30,
	func31,
	func32,
	func33,					
	func34,	
	func35,		
	func36,
	func37,
	func38,
	func39,	
	func40,
	func41,
	func42,
	func43,					
	func44,	
	func45,		
	func46,
	func47,
	func48,
	func49,	
	func50,
	func51,
	func52,
	func53,					
	func54,	
	func55,		
	func56,
	func57,
	func58,
	func59,	
	func60,
	func61,
	func62,
	func63,					
	func64,	
	func65,		
	func66,
	func67,
	func68,
	func69,	
	func70,
	func71,
	func72,
	func73,					
	func74,	
	func75,		
	func76,
	func77,
	func78,
	func79,	
	func80,
	func81,
	func82,
	func83,
	func84,	
	func85,		
	func86,
	func87,
	func88,
	func89,
	func90,
	func91,
	func92,
	func93,
	func94,	
	func95,		
	func96,
	func97,
	func98,
	func99,
	func100,
	func101,
	func102,
	func103,
	func104,	
	func105,		
	func106,
	func107,
	func108,
	func109,
	func110,
	func111,
	func112,
	func113,
	func114,	
	func115,		
	func116,
	func117,
	func118,
	func119,
	func120,
	func121,
	func122,
	func123,
	func124,	
	func125,		
	func126,
	func127,
	func128,
	func129,
	func130,
	func131,
	func132,
)
#47 ~ 64
#77 ~ 94
#111~124
#147?
#166?
DATA = [place_holder] * 177