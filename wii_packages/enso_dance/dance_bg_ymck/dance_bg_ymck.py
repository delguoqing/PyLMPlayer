def onEnterFrame(this, _global):
	this.kumo._x += 0.4
	if this.kumo._x >= 128:
		this.kumo._x = 0

def func0(this, _global):
	this.stop()

def func1(this, _global):
	this._x = this._x + 0.2333333
	if this._x > -430:
		this._x = -1270

def func2(this, _global):
	this.onEnterFrame = onEnterFrame

def func3(this, _global):
	this.gotoAndPlay("fever")
		
DATA = (func0, func1, func2, func3)