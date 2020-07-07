

import re
import os

import jk_simpleexec
import jk_utils
import jk_version

from .GitFileInfo import AbstractRepositoryFile, GitFileInfo
from .git_config_file import GitConfigFile






#
# This class wraps around the program 'git'. It's methods provide raw unprocessed output as returned by the git tool.
#
class _GitWrapper(object):

	def __init__(self):
		if not os.path.isfile("/usr/bin/git"):
			raise Exception("Git seems not to be installed!")
		r = jk_simpleexec.invokeCmd("/usr/bin/git", [ "--version" ])
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
			r = jk_simpleexec.invokeCmd("/usr/bin/git", [ "-C", gitRootDir, "status", "--porcelain", "-uall", "--ignored" ])
		elif self.__gitPorcelainVersion == 2:
			r = jk_simpleexec.invokeCmd("/usr/bin/git", [ "-C", gitRootDir, "status", "--porcelain=2", "-uall", "--ignored=traditional" ])
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
	# Download a single file from the HEAD revision.
	#
	# @return		str			Either returns the file content if the file exists or `None` if the file does not exist.
	#
	def downloadFromHead(self, gitRootDir:str, filePath:str) -> str:
		r = jk_simpleexec.invokeCmd("/usr/bin/git", [ "-C", gitRootDir, "show", "HEAD:" + filePath ])
		if (r is None) or r.isError:
			if (r.returnCode == 128) and r.stdErrLines and r.stdErrLines[0].startswith("fatal:"):
				if ("does not exist" in r.stdErrLines[0]) or ("but not in head" in r.stdErrLines[0]):
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

	#
	# Download a single file from the HEAD revision.
	#
	# @return		str			Either returns the file content if the file exists or `None` if the file does not exist.
	#
	def downloadFromHead(self, gitRootDir:str, filePath:str) -> list:
		raise Exception()
	#

#








