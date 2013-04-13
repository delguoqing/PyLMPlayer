	
def func_0(this, fscommand):
	this.stop()

def func_1(this, fscommand):
	fscommand("callback", "update_menu_matsu_normal")
	fscommand("callback", "update_menu_matsu_sbopen")
	fscommand("callback", "update_menu_matsu_sb4")
	this.stop()
		
def func_2(this, fscommand):
	fscommand("callback", "update_menu_matsu_normal")
	fscommand("callback", "update_menu_matsu_sb4")
	
def func_3(this, fscommand):
	fscommand("callback", "update_menu_matsu_normal")
	fscommand("callback", "update_menu_matsu_sbopen_l")
	fscommand("callback", "update_menu_matsu_sb4")
	
def func_4(this, fscommand):
	fscommand("callback", "update_menu_left")
	fscommand("callback", "update_menu_matsu_normal_b")
	fscommand("callback", "update_menu_matsu_sbopen_l_b")
	this.stop()

def func_5(this, fscommand):	
	fscommand("callback", "update_menu_left")
	fscommand("callback", "update_menu_matsu_normal_b")
	fscommand("callback", "update_menu_matsu_sbopen_l")
	fscommand("callback", "update_menu_matsu_sb3")
	this.stop()

def func_6(this, fscommand):
	fscommand("callback", "update_menu_matsu_normal_b")
	fscommand("callback", "update_menu_matsu_sbopen_r")
	fscommand("callback", "update_menu_matsu_sb3")
	
def func_7(this, fscommand):	
	fscommand("callback", "update_menu_right")
	fscommand("callback", "update_menu_matsu_normal")
	fscommand("callback", "update_menu_matsu_sbopen_r_b")
	this.stop()
	
def func_8(this, fscommand):
	fscommand("callback", "update_menu_right")
	fscommand("callback", "update_menu_matsu_normal")
	fscommand("callback", "update_menu_matsu_sbopen_r")
	fscommand("callback", "update_menu_matsu_sb4")
	this.stop()
	
def func_9(this, fscommand):
	fscommand("callback", "update_menu_matsu_normal")
	fscommand("callback", "update_menu_matsu_sb4")
	
def func_10(this, fscommand):
	fscommand("callback", "update_menu_matsu_normal")
	fscommand("callback", "update_menu_matsu_sbopen")
	fscommand("callback", "update_menu_matsu_sb4")
	
def func_11(this, fscommand):
	fscommand("callback", "update_menu_sort")
	fscommand("callback", "update_menu_matsu_normal")
	fscommand("callback", "update_menu_matsu_sbopen")
	fscommand("callback", "update_menu_matsu_sb4")
	
def func_12(this, fscommand):
	fscommand("callback", "update_menu_matsu_normal")
	fscommand("callback", "update_menu_matsu_sb4")
	
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
)