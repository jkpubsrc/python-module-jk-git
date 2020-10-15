

import re
import os

import jk_simpleexec

from .GitWrapper import GitWrapper
from .GitFileInfo import AbstractRepositoryFile, GitFileInfo
from .git_config_file import GitConfigFile
from .GitCommitHistory import GitCommitHistory







class GitServerRepository(object):

	def __init__(self, rootDir:str):
		self.__gitWrapper = GitWrapper()
		bIsGitRoot = GitServerRepository.__isRootDir(os.path.abspath(rootDir))
		if bIsGitRoot:
			self.__gitRootDir = rootDir
		else:
			raise Exception("Can't find git root directory: " + rootDir)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def rootDir(self) -> str:
		return self.__gitRootDir
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Retrieve the commit history.
	#
	def getCommitHistory(self) -> GitCommitHistory:
		return GitCommitHistory.create(self.__gitRootDir, self.__gitWrapper)
	#

	################################################################################################################################
	## Static Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Static Methods
	################################################################################################################################

	@staticmethod
	def hasRepository(dirPath:str) -> bool:
		assert isinstance(dirPath, str)
		assert os.path.isdir(dirPath)
		dirPath = os.path.abspath(dirPath)
		return GitServerRepository.__isRootDir(dirPath)
	#

	@staticmethod
	def __isRootDir(rootDir:str) -> bool:
		if os.path.isfile(os.path.join(rootDir, "config")) \
			and os.path.isfile(os.path.join(rootDir, "description")) \
			and os.path.isfile(os.path.join(rootDir, "HEAD")) \
			and os.path.isdir(os.path.join(rootDir, "branches")) \
			and os.path.isdir(os.path.join(rootDir, "hooks")) \
			and os.path.isdir(os.path.join(rootDir, "objects")) \
			and os.path.isdir(os.path.join(rootDir, "refs")) \
			:
			return True
		else:
			return False
	#

#











