def func_0(this):
	this.stop()
	
def func_1(this):
	this.stop()

def func_2(this):
	this.fscommand("event", "end")
	this.stop()

def func_3(this):
	#_root._RankingScore_init(this, order);
	this.stop();

def func_4(this):
	#mii_name_3rd = _root.rankingMii[2].getName();
	#score.order = 2;
	pass
	
def func_5(this):
	this.gotoAndStop("blink")
	
def func_6(this):	
	#mii_name_3nd = _root.rankingMii[2].getName();
	#score.order = 2;	
	pass

def func_7(this):		
	#mii_name_2st = _root.rankingMii[1].getName();
	#score.order = 1;
	pass
	
def func_8(this):
	#_root._Ranking_startRankInEffect(this);	
	pass
	
def func_9(this):
	this.gotoAndPlay("show jump 1st")
	
def func_10(this):
	this.gotoAndPlay("show jump 2nd")
	
def func_11(this):
	this.gotoAndPlay("show jump 3rd")	

def func_12(this):	
	#_parent.resultBoard_1p.gotoAndPlay("effect_end");
	this.stop()
	
def func_13(this):
	this.gotoAndPlay("loop")
		
DATA = (
	func_0,
	func_1,
	func_2,
	func_3,
	func_4,
	func_5,
	func_6,
	func_7,
	func_8,		
	func_9,
	func_10,
	func_11,			
	func_12,			
	func_13,				
)