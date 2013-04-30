def func_0(this):
	def onEnterFrame(_this):
		bg = _this
		bg._x -= 0.5
		if bg._x <= -256:
			bg._x = 0
	this.onEnterFrame = onEnterFrame

def func_1(this):
	pass
	
def func_2(this):
	this.stop()
	
def func_3(this):
	this.gotoAndPlay("fever")

def func_4(this):
	this.gotoAndPlay("miss")
	
def func_5(this):
	this.gotoAndPlay("normal")
			
DATA = (
	func_0,
	func_1,
	func_2,
	func_3,
	func_4,				
	func_5,	
)