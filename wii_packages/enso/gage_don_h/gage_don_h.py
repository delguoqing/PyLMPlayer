def func0(this, _global):
	this.stop()

def func1(this, _global):
	this.gotoAndPlay("fever")

def func2(this, _global):
	if 2 <= this.fever_gage._play_head <= 23:
		this.fever_gage.totoAndPlay("toNormal")
	this.stop()

def func3(this, _global):
	this.fever_gage.gotoAndPlay("toFever")
	this.stop()
	
DATA = (
	func0,
	func1,
	func2,
	func3,
)