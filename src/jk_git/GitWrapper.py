

import re
import os

import jk_simpleexec
import jk_utils
import jk_version

from .GitFile import AbstractRepositoryFile, GitFile
from .git_config_file import GitConfigFile






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
	# @return	GitFile[]	Files
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
		return r.stdOutLines
	#

#

_GIT_WRAPPER_INST = None






class GitWrapper(object):

	def status(self, gitRootDir:str, bIncludeIgnored:bool = False) -> list:
		pass
	#

	def porcelainVersion(self):
		pass
	#

	def __init__(self):
		global _GIT_WRAPPER_INST
		if _GIT_WRAPPER_INST is None:
			_GIT_WRAPPER_INST = _GitWrapper()
			self.porcelainVersion = _GIT_WRAPPER_INST.porcelainVersion
			self.status = _GIT_WRAPPER_INST.status
	#

#








