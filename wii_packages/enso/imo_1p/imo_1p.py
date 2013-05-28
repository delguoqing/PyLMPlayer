def func0(this, _global):
	this.gotoAndPlay("geki_01")
	
def func1(this, _global):
	this.gotoAndPlay("geki_02")
	
def func2(this, _global):
	this.gotoAndPlay("geki_03")
	
def func3(this, _global):
	this.gotoAndPlay("geki_04")
	
def func4(this, _global):
	this.gotoAndPlay("geki_05")
	
def func5(this, _global):
	this.gotoAndPlay("geki_06")
	
def func6(this, _global):
	this.gotoAndPlay("loop")
	
def func7(this, _global):
	this.stop()
	
def func8(this, _global):
	#digit1.gotoAndPlay("number_" + int(_root.current_count));
	pass

def func9(this, _global):	
	#digit1.gotoAndPlay("number_" + int(_root.current_count % 10));
	#digit2.gotoAndPlay("number_" + int(_root.current_count / 10 % 10));
	pass

def func10(this, _global):	
	#digit1.gotoAndPlay("number_" + int(_root.current_count % 10));
	#digit2.gotoAndPlay("number_" + int(_root.current_count / 10 % 10));
	#digit3.gotoAndPlay("number_" + int(_root.current_count / 100 % 10));	
	pass	
	
# Initialize
def func11(this, _global):	
	pass
	
def func12(this, _global):	
	#SetState(STATE_HIT);
	this._root.fscommand("callback", "on_imo_in_end")
	pass
	
def func13(this, _global):	
	#ResultMiss(this.kusudama);
	pass
	
def func14(this, _global):
	#ResultHigh(this.kusudama);
	pass
	
def func15(this, _global):
	#ResultLow(this.kusudama);	
	pass
	

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
)