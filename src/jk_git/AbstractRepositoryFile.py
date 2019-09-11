


class AbstractRepositoryFile(object):

	ADDED = "A"
	MODIFIED = "M"
	DELETED = "D"
	IGNORED = "I"
	RENAMED = "R"
	UNVERSIONED = "?"
	NOT_MODIFIED = " "
	CONFLICTED = "C"

	STATE_MAP = {
		"A": "added",
		"M": "modified",
		"D": "deleted",
		"I": "ignored",
		"R": "renamed",
		"?": "unversioned",
		" ": "not modified",
		"C": "conflicted",
	}

	def __init__(self, status:str, filePath:str):
		self.status = status
		self.filePath = filePath
	#

	def __str__(self):
		return self.__class__.__name__ + "< " + self.STATE_MAP[self.status] + " " + repr(self.filePath) + " >"
	#

	def __repr__(self):
		return self.__class__.__name__ + "< " + self.STATE_MAP[self.status] + " " + repr(self.filePath) + " >"
	#

#

