

import re
import os
import typing

import jk_simpleexec
import jk_utils
import jk_version

from .GitFileInfo import AbstractRepositoryFile, GitFileInfo





def _detectGitBinary() -> typing.Union[str,None]:
	_pathcandidates = None
	if os.name == "nt":
		_pathcandidates = [ "C:\\Program Files\\Git\cmd\\git.exe" ]
	else:
		_pathcandidates = [ "/usr/bin/git" ]

	# ----

	for pc in _pathcandidates:
		if os.path.isfile(pc):
			return pc

	# ----

	return None
#




#
# This class wraps around the program 'git'. It's methods provide raw unprocessed output as returned by the git tool.
# This is a global instance for mimicking a singleton pattern.
#
class _GitWrapper(object):

	def __init__(self):
		self.__gitBinPath = _detectGitBinary()
		if not self.__gitBinPath:
			raise Exception("Git seems not to be installed!")

		r = jk_simpleexec.invokeCmd(self.__gitBinPath, [ "--version" ])
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
				r = jk_simpleexec.invokeCmd(self.__gitBinPath, [ "-C", gitRootDir, "status", "--porcelain", "-uall", "--ignored" ])
			else:
				r = jk_simpleexec.invokeCmd(self.__gitBinPath, [ "-C", gitRootDir, "status", "--porcelain", "-uall" ])
		elif self.__gitPorcelainVersion == 2:
			if bIncludeIgnored:
				#r = jk_simpleexec.invokeCmd(self.__gitBinPath, [ "-C", gitRootDir, "status", "--porcelain=2", "-uall", "--ignored=traditional" ])
				r = jk_simpleexec.invokeCmd(self.__gitBinPath, [ "-C", gitRootDir, "status", "--porcelain=2", "-uall", "--ignored" ])
			else:
				r = jk_simpleexec.invokeCmd(self.__gitBinPath, [ "-C", gitRootDir, "status", "--porcelain=2", "-uall" ])
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

	def lsRemote_url(self, url:str) -> list:
		r = jk_simpleexec.invokeCmd(self.__gitBinPath, [ "ls-remote", url ])
		if (r is None) or r.isError:
			r.dump()
			raise Exception("Running git failed!")
		ret = []
		for line in r.stdOutLines:
			m = re.match("^([a-zA-Z0-9]+)\s+(.*)$", line.strip())
			if m:
				ret.append([ m.group(1), m.group(2) ])
		return ret
	#

	def lsRemote_dir(self, gitRootDir:str) -> list:
		r = jk_simpleexec.invokeCmd(self.__gitBinPath, [ "-C", gitRootDir, "ls-remote" ])
		if (r is None) or (r.returnCode != 0):
			r.dump()
			raise Exception("Running git failed!")
		ret = []
		for line in r.stdOutLines:
			m = re.match("^([a-zA-Z0-9]+)\s+(.*)$", line.strip())
			if m:
				ret.append([ m.group(1), m.group(2) ])
		return ret
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

		r = jk_simpleexec.invokeCmd(self.__gitBinPath, [ "-C", gitRootDir, "add", filePath ])
		if (r is None) or r.isError:
			r.dump()
			raise Exception("Running git failed!")
		if r.stdOutLines:
			return r.stdOutLines
		else:
			return []
	#

	def pull(self, gitRootDir:str) -> list:
		assert os.path.isdir(gitRootDir)

		r = jk_simpleexec.invokeCmd(self.__gitBinPath, [ "-C", gitRootDir, "pull" ])

		# STDOUT: 'Updating 293bc22..81ad022'
		# STDOUT: 'Fast-forward'
		# STDOUT: ' packageinfo.jsonc | 4 +++-'
		# STDOUT: ' 1 file changed, 3 insertions(+), 1 deletion(-)'
		# STDERR: 'From ssh://123.45.67.89:/foo/bar/some_repo_dir'
		# STDERR: '   293bc22..81ad022  master     -> origin/master'
		# RETURNCODE: 0

		if (r is None) or (r.returnCode != 0):
			r.dump()
			raise Exception("Running git failed!")

		ret = []
		if r.stdOutLines:
			ret.extend(r.stdOutLines)
		if r.stdErrLines:
			ret.extend(r.stdErrLines)
		return ret
	#

	def clone(self, gitRootDir:str, url:str) -> list:
		assert os.path.isdir(gitRootDir)
		assert isinstance(url, str)
		assert url

		os.makedirs(gitRootDir, exist_ok=True)
		for something in os.listdir(gitRootDir):
			raise Exception("Target directory is not empty: " + gitRootDir)

		r = jk_simpleexec.invokeCmd(self.__gitBinPath, [ "clone", url, "." ], workingDirectory=gitRootDir)
		if (r is None) or (r.returnCode != 0):
			r.dump()
			raise Exception("Running git failed!")
		if r.stdErrLines:
			return r.stdErrLines
		else:
			return []
	#

	#
	# Show the log
	#
	# @return	str[]		Text output of the 'log' command
	#
	def logPretty(self, gitRootDir:str) -> list:
		r = jk_simpleexec.invokeCmd(self.__gitBinPath, [ "-C", gitRootDir, "log", "--pretty=format:\"%P|%H|%cn|%ce|%cd|%s\"" ])
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
		r = jk_simpleexec.invokeCmd(self.__gitBinPath, [ "-C", gitRootDir, "show", "HEAD:" + filePath ])
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







#
# This class wraps around _GitWrapper.
# This is a lightweight class.
#
# TODO: Implement a better solution.
#
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
		self.lsRemote_url = _GIT_WRAPPER_INST.lsRemote_url
		self.lsRemote_dir = _GIT_WRAPPER_INST.lsRemote_dir
		self.clone = _GIT_WRAPPER_INST.clone
		self.pull = _GIT_WRAPPER_INST.pull
	#

	def pull(self, gitRootDir:str) -> list:
		raise Exception()
	#

	def clone(self, gitRootDir:str, url:str) -> list:
		raise Exception()
	#

	def lsRemote_url(self, url:str) -> list:
		raise Exception()
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








