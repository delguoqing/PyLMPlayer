from lm import lm_consts

import lm_tag_base

class CTag(lm_tag_base.CTag):
	
	def patch_py_actionscript(self, data):
		self._data = data
		
	def get_val(self, idx):
		return self._data[idx]
		
	
	def get_id(cls):
		return lm_consts.TAG_AS_LIST