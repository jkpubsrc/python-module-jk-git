


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

	def __init__(self, workingCopy, status:str, filePath:str):
		self.__workingCopy = workingCopy
		self.__status = status
		self.__filePath = filePath
	#

	def filePath(self) -> str:
		return self.__filePath
	#

	def status(self) -> str:
		return self.__status
	#

	def statusText(self) -> str:
		return self.STATE_MAP[self.__status]
	#

	def workingCopy(self):
		return self.__workingCopy
	#

	def __str__(self):
		return self.__class__.__name__ + "<" + self.STATE_MAP[self.__status] + ": " + repr(self.__filePath) + ">"
	#

	def __repr__(self):
		return self.__class__.__name__ + "<" + self.STATE_MAP[self.__status] + ": " + repr(self.__filePath) + ">"
	#

#

