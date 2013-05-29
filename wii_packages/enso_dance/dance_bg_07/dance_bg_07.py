count = 0
def onEnterFrame(this, _global):
	global count
	if this.kame._x <= -456:
		count += 1
		if count >= 400:
			count = 0
			this.kame._x = 474
	else:
		this.kame._x = this.kame._x - 2

def onEnterFrame2(this, _global):
	this._x -= 0.5
	if this._x <= -640:
		this._x = 0

def func0(this, _global):
	this.onEnterFrame = onEnterFrame
	
def func1(this, _global):
	this.onEnterFrame = onEnterFrame2
	
def func2(this, _global):
	this.stop()
	
DATA = (func0, func1, func2)