

import typing
import re
import os

import jk_typing
import jk_prettyprintobj
import jk_utils
import jk_logging

from .GitWrapper import GitWrapper
from .GitFileInfo import AbstractRepositoryFile, GitFileInfo
from .impl.GitConfigFileSection import GitConfigFileSection
from .impl.GitConfigFile import GitConfigFile
from .GitCommitHistory import GitCommitHistory
from .workingcopy._GitStatusOutputParser import _GitStatusOutputParser









class GitWorkingCopy(jk_prettyprintobj.DumpMixin):

	def __init__(self,
			rootDir:str,
			gitWrapper:GitWrapper = None,
			log:jk_logging.AbstractLogger = None,
		):

		if gitWrapper:
			self.__gitWrapper = gitWrapper
		else:
			if log is None:
				raise Exception("Logger must not be None!")
			self.__gitWrapper = GitWrapper(log)

		gitRootDir = GitWorkingCopy.__findRootDir(os.path.abspath(rootDir))
		if gitRootDir:
			self.__gitRootDir = gitRootDir
			self.__gitCfgFile = GitConfigFile.loadFromFile(os.path.join(gitRootDir, ".git", "config"))
		else:
			raise Exception("Can't find git root directory: " + rootDir)

		# TODO: improve this - maybe just storing a value for a certain amount of time is not the best idea
		self.__volatileValue_lsRemote = jk_utils.VolatileValue(self.__lsRemote, 15)					# 15 seconds caching time
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def config(self) -> GitConfigFile:
		return self.__gitCfgFile
	#

	@property
	def isClean(self) -> bool:
		return len(self.status(bIncludeIgnored = False)) == 0
	#

	@property
	def isDirty(self) -> bool:
		return len(self.status(bIncludeIgnored = False)) > 0
	#

	@property
	def rootDir(self) -> str:
		return self.__gitRootDir
	#

	@property
	def remoteOriginURL(self) -> typing.Union[str,None]:
		#return self.__gitCfgFile.getValue("remote \"origin\"", "url")
		for section in self.__gitCfgFile.getSections("remote"):
			if section.argument == "origin":
				return section.getProperty("url")
		return None
	#

	@property
	def areCredentialsStored(self) -> bool:
		s = self.__gitCfgFile.getValue("credential", "helper")
		return s == "store"
	#

	"""
	@property
	def repositoryURL(self) -> str:
		s = self.remoteOriginURL
		if s and s.endswith(".git"):
			s = s[:-4]
		return s
	#
	"""

	#
	#
	# Get a list of all remotes
	@property
	def remotes(self) -> typing.List[str]:
		ret = []
		for section in self.__gitCfgFile.getSections("remote"):
			ret.append(section.argument)
		return ret
	#

	@property
	def headRevisionID(self) -> typing.Union[str,None]:
		for revID, revName in self.__volatileValue_lsRemote.value:
			if revName == "HEAD":
				return revID
		return None
	#

	################################################################################################################################
	## Protected Methods
	################################################################################################################################

	def _dumpVarNames(self):
		return [
			"rootDir",
			"isClean",
			"isDirty",
			"remoteOriginURL",
			"remotes",
			"areCredentialsStored",
			#"repositoryURL",
			"headRevisionID",
			"config",
		]
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	#
	# Returns something like:
	# [
	# 	[	"293bc22fa252a86039060986460275df3f5f0331",	"HEAD"	],
	# 	[	"293bc22fa252a86039060986460275df3f5f0331",	"refs/heads/master"	]
	# ]
	#
	def __lsRemote(self) -> list:
		if not self.remoteOriginURL:
			return []
		return self.__gitWrapper.lsRemote_dir(self.__gitRootDir)
	#

	@staticmethod
	def __findRootDir(rootDir:str, bRecursive:bool = True):
		if len(rootDir) <= 1:
			return None
		testDir = rootDir + "/.git"
		if os.path.isdir(testDir):
			return rootDir
		pos = rootDir.rfind("/")
		if pos <= 0:
			return None
		if bRecursive:
			return GitWorkingCopy.__findRootDir(rootDir[:pos])
		else:
			return None
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Run a <c>git pull</c> request.
	#
	@jk_typing.checkFunctionSignature()
	def pull(self, log:jk_logging.AbstractLogger = None) -> typing.List[str]:
		return self.__gitWrapper.pull(self.__gitRootDir, log)
	#

	@jk_typing.checkFunctionSignature()
	def addFile(self, filePath:str, log:jk_logging.AbstractLogger = None):
		lines = self.__gitWrapper.add(self.__gitRootDir, filePath, log)
		if lines:
			raise Exception("Unexpected output received: " + repr(lines))
	#

	@jk_typing.checkFunctionSignature()
	def flowInit(self, log:jk_logging.AbstractLogger = None) -> None:
		self.__gitWrapper.flowInit(self.__gitRootDir, log)
	#

	#
	# Retrieve the status of this working copy
	#
	# @return	GitFileInfo[]	A list of file information objects.
	#
	@jk_typing.checkFunctionSignature()
	def status(self, bIncludeIgnored:bool = False, log:jk_logging.AbstractLogger = None) -> typing.List[GitFileInfo]:
		lines = self.__gitWrapper.status(self.__gitRootDir, bIncludeIgnored, log)
		return _GitStatusOutputParser.parse(lines, self.__gitWrapper.porcelainVersion, bIncludeIgnored, self)
	#

	#
	# Download a single file from the HEAD revision.
	#
	# @return		str			Either returns the file content if the file exists or `None` if the file does not exist.
	#
	@jk_typing.checkFunctionSignature()
	def downloadFromHead(self, filePath:str, log:jk_logging.AbstractLogger = None) -> str:
		return self.__gitWrapper.downloadFromHead(self.__gitRootDir, filePath, log)
	#

	#
	# Retrieve the commit history.
	#
	def getCommitHistory(self) -> GitCommitHistory:
		return GitCommitHistory.create(self.__gitRootDir, self.__gitWrapper)
	#

	@jk_typing.checkFunctionSignature()
	def commit(self, commitMsg:str, log:jk_logging.AbstractLogger = None) -> None:
		self.__gitWrapper.commit(self.__gitRootDir, commitMsg, log)
	#

	@jk_typing.checkFunctionSignature()
	def listTags(self, log:jk_logging.AbstractLogger = None) -> typing.List[str]:
		return self.__gitWrapper.listTags(self.__gitRootDir, log)
	#

	@jk_typing.checkFunctionSignature()
	def createTag(self, tagName:str, commitMsg:str, log:jk_logging.AbstractLogger = None) -> None:
		self.__gitWrapper.createTag(self.__gitRootDir, tagName, commitMsg, log)
	#

	@jk_typing.checkFunctionSignature()
	def deleteTag(self, tagName:str, log:jk_logging.AbstractLogger = None) -> None:
		self.__gitWrapper.deleteTag(self.__gitRootDir, tagName, log)
	#

	@jk_typing.checkFunctionSignature()
	def listBranches(self, log:jk_logging.AbstractLogger = None) -> typing.List[str]:
		return self.__gitWrapper.listBranches(self.__gitRootDir, log)
	#

	@jk_typing.checkFunctionSignature()
	def createBranch(self, branchName:str, log:jk_logging.AbstractLogger = None):
		self.__gitWrapper.createBranch(self.__gitRootDir, branchName, log)
	#

	@jk_typing.checkFunctionSignature()
	def switchToBranch(self, branchName:str, log:jk_logging.AbstractLogger = None):
		self.__gitWrapper.switchToBranch(self.__gitRootDir, branchName, log)
	#

	################################################################################################################################
	## Static Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Static Methods
	################################################################################################################################

	@staticmethod
	def hasWorkingCopy(dirPath:str) -> bool:
		assert isinstance(dirPath, str)
		assert os.path.isdir(dirPath)
		dirPath = os.path.abspath(dirPath)
		gitRootDir = GitWorkingCopy.__findRootDir(dirPath, False)
		return gitRootDir is not None
	#

#











