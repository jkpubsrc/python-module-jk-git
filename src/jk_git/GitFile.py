


from .AbstractRepositoryFile import AbstractRepositoryFile



class GitFile(AbstractRepositoryFile):

	def __init__(self, status:str, filePath:str):
		super().__init__(status, filePath)
	#

#

