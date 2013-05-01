def func_0(this, _global):
	def onEnterFrame(_this, _global):
		bg = _this
		bg._x -= 0.5
		if bg._x <= -256:
			bg._x = 0
	this.onEnterFrame = onEnterFrame

def func_1(this, _global):
	pass
	
def func_2(this, _global):
	this.stop()
	
def func_3(this, _global):
	this.gotoAndPlay("fever")

def func_4(this, _global):
	this.gotoAndPlay("miss")
	
def func_5(this, _global):
	this.gotoAndPlay("normal")
			
DATA = (
	func_0,
	func_1,
	func_2,
	func_3,
	func_4,				
	func_5,	
)