import lm_tag_base
from lm import lm_consts

class CTag(lm_tag_base.CTag):

	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		
		self.depth = d["depth"]
		
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_REMOVE_OBJ
		
	def execute(self, target=None):
		if not target: return
				
		target.remove_drawable(self.depth)
		
#		print "Remove drawable at depth %d" % self.depth