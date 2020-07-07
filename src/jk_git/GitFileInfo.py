


from .AbstractRepositoryFile import AbstractRepositoryFile



class GitFileInfo(AbstractRepositoryFile):

	def __init__(self, workingCopy, status:str, filePath:str):
		super().__init__(workingCopy, status, filePath)
	#

#

