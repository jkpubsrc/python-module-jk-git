

import re
import os

import jk_logging
import jk_utils
import jk_prettyprintobj

from .GitWrapper import GitWrapper
from .GitCommitHistory import GitCommitHistory
#from .GitConfigFile import GitConfigFile			# not needed







class GitServerRepository(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self, rootDir:str, log:jk_logging.AbstractLogger):
		self.__gitWrapper = GitWrapper(log)
		bIsGitRoot = GitServerRepository.__isRootDir(os.path.abspath(rootDir))
		if bIsGitRoot:
			self.__gitRootDir = rootDir
		else:
			raise Exception("Can't find git root directory: " + rootDir)

		self.__gitHeadsDirPath = os.path.join(rootDir, "refs", "heads")
		self.__gitTagsDirPath = os.path.join(rootDir, "refs", "tags")
		#self.__gitCfgFile = GitConfigFile(os.path.join(rootDir, "config"))		# not needed

		self.__volatileValue_getSize = jk_utils.VolatileValue(self.__getSizeInBytes, 15)			# 15 seconds caching time
		self.__volatileValue_getHeadName = jk_utils.VolatileValue(self.__getHeadName, 15)			# 15 seconds caching time
		self.__volatileValue_getHeads = jk_utils.VolatileValue(self.__getHeads, 15)					# 15 seconds caching time
		self.__volatileValue_getTags = jk_utils.VolatileValue(self.__getTags, 15)					# 15 seconds caching time
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def rootDir(self) -> str:
		return self.__gitRootDir
	#

	#
	# The name of the head revision
	#
	@property
	def headName(self) -> str:
		return self.__volatileValue_getHeadName.value
	#

	#
	# The size of the repository folder in bytes
	#
	@property
	def sizeInBytes(self) -> int:
		return self.__volatileValue_getSize.value
	#

	@property
	def isEmpty(self) -> bool:
		return not self.__volatileValue_getHeads.value					# return True if we have no heads
	#

	@property
	def heads(self) -> list:
		return self.__volatileValue_getHeads.value
	#

	@property
	def tags(self) -> list:
		return self.__volatileValue_getTags.value
	#

	################################################################################################################################
	## Protected Methods
	################################################################################################################################

	def _dumpVarNames(self):
		return [
			"rootDir",
			"headName",
			"sizeInBytes",
			"isEmpty",
			"heads",
			"tags",
		]
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __getTags(self) -> list:
		ret = []
		for fe in os.scandir(self.__gitTagsDirPath):
			if fe.is_file:
				ret.append(fe.name)
		return sorted(ret)
	#

	def __getHeads(self) -> list:
		ret = []
		for fe in os.scandir(self.__gitHeadsDirPath):
			if fe.is_file:
				ret.append(fe.name)
		return sorted(ret)
	#

	#
	# Load the name of the head revision
	#
	def __getHeadName(self) -> str:
		p = os.path.join(self.__gitRootDir, "HEAD")
		if not os.path.isfile(p):
			raise Exception(repr(p))

		with open(p, "r") as f:
			lines = f.read().split("\n")
			line = lines[0]

		m = re.match("^ref:\s+refs/heads/(\w+)$", line)
		if not m:
			raise Exception(repr(line))

		return m.group(1)
	#

	#
	# Get the size of the repository folder in bytes
	#
	def __getSizeInBytes(self) -> int:
		return jk_utils.fsutils.getFolderSize(self.__gitRootDir)
	#

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











