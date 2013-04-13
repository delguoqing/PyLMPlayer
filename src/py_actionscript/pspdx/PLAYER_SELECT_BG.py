def func_0(this, fscommand):
	def onEnterFrame(_this):
		this._rotation += 0.2
	this.onEnterFrame = onEnterFrame	

def func_1(this, fscommand):
	def onEnterFrame(_this):
		this._rotation -= 0.3
	this.onEnterFrame = onEnterFrame
		
def func_2(this, fscommand):
	def onEnterFrame(_this):
		bg = _this.mc_bg
		bg._x -= 0.4
		if bg._x <= -480:
			bg._x = 0
	this.onEnterFrame = onEnterFrame
			
DATA = (
	func_0,
	func_1,
	func_2,
)