def onEnterFrame(this, _global):
	this._x = this._x - 2;
	if this._x <= -856:
		this._x = 0
		
def func0(this, _global):
	this.gotoAndPlay(0)

def func1(this, _global):
	this.onEnterFrame = onEnterFrame

def func2(this, _global):
	this.stop()
		
DATA = (func0, func1, func2)