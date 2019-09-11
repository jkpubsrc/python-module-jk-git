

import re
import os

import jk_simpleexec

from .GitFile import AbstractRepositoryFile, GitFile
from .git_config_file import GitConfigFile






class Git(object):

	def __init__(self, rootDir:str):
		if not os.path.isfile("/usr/bin/git"):
			raise Exception("Git seems not to be installed!")
		gitRootDir = self.__findRootDir(os.path.abspath(rootDir))
		if gitRootDir:
			self.__gitRootDir = gitRootDir
			self.__gitCfgFile = GitConfigFile(gitRootDir)
		else:
			raise Exception("Can't find git root directory: " + rootDir)
	#

	@property
	def rootDir(self) -> str:
		return self.__gitRootDir
	#

	@property
	def remoteOrigin(self) -> str:
		return self.__gitCfgFile.getValue("remote \"origin\"", "url")
	#

	def __findRootDir(self, rootDir:str):
		if len(rootDir) <= 1:
			return None
		testDir = rootDir + "/.git"
		if os.path.isdir(testDir):
			return rootDir
		pos = rootDir.rfind("/")
		if pos <= 0:
			return None
		return self.__findRootDir(rootDir[:pos])
	#

	def __parseAny(self, line:str):
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
				([0-9\\.]+)
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

	#
	# @return	GitFile[]	Files
	#
	def status(self, bIncludeIgnored:bool = False) -> list:
		r = jk_simpleexec.invokeCmd("/usr/bin/git", [ "-C", self.__gitRootDir, "status", "--porcelain=2", "-uall", "--ignored=traditional" ])
		if (r is None) or r.isError:
			raise Exception("Running git failed!")
		ret = []
		for line in r.stdOutLines:
			m = self.__parseAny(line)
			if m:
				g = m.groups()
				sType = g[0]
				m = g[1:]
				if sType == "?":
					# untracked
					ret.append(GitFile(GitFile.UNVERSIONED, m[0]))
				elif sType == "!":
					# ignored
					ret.append(GitFile(GitFile.IGNORED, m[0]))
				elif sType == "1":
					# modified
					ret.append(GitFile(GitFile.MODIFIED, m[-1]))
				elif sType == "2":
					# renamed
					ret.append(GitFile(GitFile.RENAMED, m[-1]))
				elif sType == "u":
					# conflicted
					ret.append(GitFile(GitFile.CONFLICTED, m[-1]))
				else:
					raise Exception("Failed to parse line: " + repr(line))
			else:
				raise Exception("Failed to parse line: " + repr(line))

		if bIncludeIgnored:
			return ret
		else:
			return [ x for x in ret if x.status != GitFile.IGNORED ]
	#

#











