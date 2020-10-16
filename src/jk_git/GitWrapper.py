

import re
import os

import jk_simpleexec
import jk_utils
import jk_version

from .GitFileInfo import AbstractRepositoryFile, GitFileInfo




GIT_PATH = "/usr/bin/git"




#
# This class wraps around the program 'git'. It's methods provide raw unprocessed output as returned by the git tool.
#
class _GitWrapper(object):

	def __init__(self):
		if not os.path.isfile(GIT_PATH):
			raise Exception("Git seems not to be installed!")
		r = jk_simpleexec.invokeCmd(GIT_PATH, [ "--version" ])
		if (r is None) or r.isError:
			r.dump()
			raise Exception("Running git failed!")
		lines = r.stdOutLines
		if lines[0].startswith("git version "):
			v = jk_version.Version(lines[0][12:].strip())
			self.__gitPorcelainVersion = 1 if v < jk_version.Version("2.8") else 2
		else:
			print(lines[0])
			raise Exception("Failed to parse version!")
	#

	def porcelainVersion(self):
		return self.__gitPorcelainVersion
	#

	#
	# Retrieve the status of this working copy
	#
	# @return	str[]		Text output of the 'status' command
	#
	def status(self, gitRootDir:str, bIncludeIgnored:bool = False) -> list:
		if self.__gitPorcelainVersion == 1:
			if bIncludeIgnored:
				r = jk_simpleexec.invokeCmd(GIT_PATH, [ "-C", gitRootDir, "status", "--porcelain", "-uall", "--ignored" ])
			else:
				r = jk_simpleexec.invokeCmd(GIT_PATH, [ "-C", gitRootDir, "status", "--porcelain", "-uall" ])
		elif self.__gitPorcelainVersion == 2:
			if bIncludeIgnored:
				#r = jk_simpleexec.invokeCmd(GIT_PATH, [ "-C", gitRootDir, "status", "--porcelain=2", "-uall", "--ignored=traditional" ])
				r = jk_simpleexec.invokeCmd(GIT_PATH, [ "-C", gitRootDir, "status", "--porcelain=2", "-uall", "--ignored" ])
			else:
				r = jk_simpleexec.invokeCmd(GIT_PATH, [ "-C", gitRootDir, "status", "--porcelain=2", "-uall" ])
		else:
			raise Exception()
		if (r is None) or r.isError:
			r.dump()
			raise Exception("Running git failed!")
		if r.stdOutLines:
			return r.stdOutLines
		else:
			return []
	#

	#
	# Add a file to the git repository.
	#
	# @return	str[]		Text output of the 'add' command
	#
	def add(self, gitRootDir:str, filePath:str) -> list:
		assert os.path.isabs(filePath)

		s = gitRootDir
		if not s.endswith("/"):
			s += "/"
		if not filePath.startswith(s):
			raise Exception("File does not seem to be part of the git tree: " + filePath)

		r = jk_simpleexec.invokeCmd(GIT_PATH, [ "-C", gitRootDir, "add", filePath ])
		if (r is None) or r.isError:
			r.dump()
			raise Exception("Running git failed!")
		if r.stdOutLines:
			return r.stdOutLines
		else:
			return []
	#

	#
	# Show the log
	#
	# @return	str[]		Text output of the 'log' command
	#
	def logPretty(self, gitRootDir:str) -> list:
		r = jk_simpleexec.invokeCmd(GIT_PATH, [ "-C", gitRootDir, "log", "--pretty=format:\"%P|%H|%cn|%ce|%cd|%s\"" ])
		if (r is None) or r.isError:
			if r.stdErrLines \
				and (r.stdErrLines[0].find("fatal: your current branch") >= 0) \
				and (r.stdErrLines[0].find("does not have any commits yet") >= 0):
				return []
			else:
				r.dump()
				raise Exception("Running git failed!")
		if r.stdOutLines:
			ret = []
			for line in r.stdOutLines:
				assert line[0] == "\""
				assert line[-1] == "\""
				ret.append(line[1:-1])
			return ret
		else:
			return []
	#

	#
	# Download a single file from the HEAD revision.
	#
	# @return		str			Either returns the file content if the file exists or `None` if the file does not exist.
	#
	def downloadFromHead(self, gitRootDir:str, filePath:str) -> str:
		r = jk_simpleexec.invokeCmd(GIT_PATH, [ "-C", gitRootDir, "show", "HEAD:" + filePath ])
		if (r is None) or r.isError:
			if (r.returnCode == 128) and r.stdErrLines and r.stdErrLines[0].startswith("fatal:"):
				if ("does not exist" in r.stdErrLines[0]) or ("but not in 'HEAD'" in r.stdErrLines[0]):
					return None
			r.dump()
			raise Exception("Running git failed!")
		if r.stdOutLines:
			return "\n".join(r.stdOutLines)
		else:
			return ""
	#

#

_GIT_WRAPPER_INST = None







class GitWrapper(object):

	def __init__(self):
		global _GIT_WRAPPER_INST

		if _GIT_WRAPPER_INST is None:
			_GIT_WRAPPER_INST = _GitWrapper()

		self.porcelainVersion = _GIT_WRAPPER_INST.porcelainVersion
		self.status = _GIT_WRAPPER_INST.status
		self.downloadFromHead = _GIT_WRAPPER_INST.downloadFromHead
		self.add = _GIT_WRAPPER_INST.add
		self.logPretty = _GIT_WRAPPER_INST.logPretty
	#

	def porcelainVersion(self):
		raise Exception()
	#

	#
	# Retrieve the status of this working copy
	#
	# @return	str[]		Text output of the 'status' command
	#
	def status(self, gitRootDir:str, bIncludeIgnored:bool = False) -> list:
		raise Exception()
	#

	def logPretty(self, gitRootDir:str) -> list:
		raise Exception()
	#

	#
	# Download a single file from the HEAD revision.
	#
	# @return		str			Either returns the file content if the file exists or `None` if the file does not exist.
	#
	def downloadFromHead(self, gitRootDir:str, filePath:str) -> list:
		raise Exception()
	#

	#
	# Add a file to the git repository.
	#
	# @return	str[]		Text output of the 'add' command
	#
	def add(self, gitRootDir:str, filePath:str) -> list:
		raise Exception()
	#

#








