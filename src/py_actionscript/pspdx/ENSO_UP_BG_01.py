def func_0(this, fscommand):
	def onEnterFrame(_this):
		bg = _this
		bg._x -= 0.5
		if bg._x <= -256:
			bg._x = 0
	this.onEnterFrame = onEnterFrame

def func_1(this, fscommand):
	pass
	
def func_2(this, fscommand):
	this.stop()
	
def func_3(this, fscommand):
	this.gotoAndPlay("fever")

def func_4(this, fscommand):
	this.gotoAndPlay("miss")
	
def func_5(this, fscommand):
	this.gotoAndPlay("normal")
			
DATA = (
	func_0,
	func_1,
	func_2,
	func_3,
	func_4,				
	func_5,	
)