

import re
import os

import jk_simpleexec

from .GitWrapper import GitWrapper
from .GitFileInfo import AbstractRepositoryFile, GitFileInfo
from .git_config_file import GitConfigFile








class GitWorkingCopy(object):

	def __init__(self, rootDir:str):
		self.__git = GitWrapper()
		gitRootDir = GitWorkingCopy.__findRootDir(os.path.abspath(rootDir))
		if gitRootDir:
			self.__gitRootDir = gitRootDir
			self.__gitCfgFile = GitConfigFile(gitRootDir)
		else:
			raise Exception("Can't find git root directory: " + rootDir)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

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
	def remoteOrigin(self) -> str:
		return self.__gitCfgFile.getValue("remote \"origin\"", "url")
	#

	@property
	def areCredentialsStored(self) -> bool:
		s = self.__gitCfgFile.getValue("credential", "helper")
		return s == "store"
	#

	@property
	def repositoryURL(self) -> str:
		s = self.remoteOrigin
		if s and s.endswith(".git"):
			s = s[:-4]
		return s
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __parseAny1(self, line:str):
		m = re.match("^\s*([A-Z\?!]+)\s+(.+)$", line)
		if m:
			return m

		return None
	#

	def __parseAny2(self, line:str):
		ret = re.match(r"^(\?)\s+(.+)$", line)
		if ret:
			return ret

		ret = re.match(r"^(!)\s+(.+)$", line)
		if ret:
			return ret

		ret = re.match("""
			^
				(1)
				\\s+
				([A-Z\\.]{2})
				\\s+
				([A-Z\\.]{4})
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				([a-zA-Z0-9]+)
				\\s+
				([a-zA-Z0-9]+)
				\\s+
				(.+)
			$
			""", line, re.VERBOSE)
		if ret:
			return ret

		ret = re.match("""
			^
				(2)
				\\s+
				([A-Z\\.]{2})
				\\s+
				([A-Z\\.]{4})
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				([a-zA-Z0-9]+)
				\\s+
				([A-Z][0-9]+)
				\\s+
				(.+)
			$
			""", line, re.VERBOSE)
		if ret:
			return ret

		ret = re.match("""
			^
				(u)
				\\s+
				([A-Z\\.]{2})
				\\s+
				([A-Z\\.]{4})
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				(.+)
				\\s+
				(.+)
				\\s+
				(.+)
				\\s+
				(.+)
			$
			""", line, re.VERBOSE)
		if ret:
			return ret

		return None
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def addFile(self, filePath:str):
		lines = self.__git.add(self.__gitRootDir, filePath)
		if lines:
			raise Exception("Unexpected output received: " + repr(lines))

	#

	#
	# Retrieve the status of this working copy
	#
	# @return	GitFileInfo[]	A list of file information objects.
	#
	def status(self, bIncludeIgnored:bool = False) -> list:
		lines = self.__git.status(self.__gitRootDir, bIncludeIgnored)
		porcellainVersion = self.__git.porcelainVersion()

		ret = []
		for line in lines:
			bSuccess = False

			if porcellainVersion == 1:
				m = self.__parseAny1(line)
			elif porcellainVersion == 2:
				m = self.__parseAny2(line)
			else:
				raise Exception()

			if m:
				g = m.groups()

				if porcellainVersion == 1:
					sType = g[0][-1]
					m = g[1:]
					if sType == "?":
						# untracked
						ret.append(GitFileInfo(self, GitFileInfo.UNVERSIONED, m[0]))
						bSuccess = True
					elif sType == "!":
						# ignored
						ret.append(GitFileInfo(self, GitFileInfo.IGNORED, m[0]))
						bSuccess = True
					elif sType == "A":
						# added
						ret.append(GitFileInfo(self, GitFileInfo.ADDED, m[-1]))
						bSuccess = True
					elif sType == "M":
						# modified
						ret.append(GitFileInfo(self, GitFileInfo.MODIFIED, m[-1]))
						bSuccess = True
					elif sType == "R":
						# renamed
						ret.append(GitFileInfo(self, GitFileInfo.RENAMED, m[-1]))
						bSuccess = True
					elif sType == "D":
						# renamed
						ret.append(GitFileInfo(self, GitFileInfo.DELETED, m[-1]))
						bSuccess = True
					elif sType == "U":
						# conflicted
						ret.append(GitFileInfo(self, GitFileInfo.CONFLICTED, m[-1]))
						bSuccess = True

				elif porcellainVersion == 2:
					sType = g[0]
					m = g[1:]
					if sType == "?":
						# untracked
						ret.append(GitFileInfo(self, GitFileInfo.UNVERSIONED, m[0]))
						bSuccess = True
					elif sType == "!":
						# ignored
						ret.append(GitFileInfo(self, GitFileInfo.IGNORED, m[0]))
						bSuccess = True
					elif sType == "1":
						# modified
						if "A" in m[0]:
							ret.append(GitFileInfo(self, GitFileInfo.ADDED, m[-1]))
						else:
							ret.append(GitFileInfo(self, GitFileInfo.MODIFIED, m[-1]))
						bSuccess = True
					elif sType == "2":
						# renamed
						ret.append(GitFileInfo(self, GitFileInfo.RENAMED, m[-1]))
						bSuccess = True
					elif sType == "u":
						# conflicted
						ret.append(GitFileInfo(self, GitFileInfo.CONFLICTED, m[-1]))
						bSuccess = True

			if not bSuccess:
				raise Exception("Failed to parse line: " + repr(line))

		if not bIncludeIgnored:
			ret = [ x for x in ret if x.status() != GitFileInfo.IGNORED ]
		return ret
	#

	#
	# Download a single file from the HEAD revision.
	#
	# @return		str			Either returns the file content if the file exists or `None` if the file does not exist.
	#
	def downloadFromHead(self, filePath:str) -> str:
		return self.__git.downloadFromHead(self.__gitRootDir, filePath)
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

#











