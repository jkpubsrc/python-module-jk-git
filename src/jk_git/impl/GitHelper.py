


import os
import typing

import jk_typing
import jk_version
import jk_logging
import jk_simpleexec





class GitHelper(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, log:jk_logging.AbstractLogger):
		self.__gitBinPath = GitHelper._detectGitBinaryE()
		self.__gitVersion = GitHelper._getVersion(self.__gitBinPath, log)
		self.__gitPorcelainVersion = 1 if self.__gitVersion < jk_version.Version("2.8") else 2
	#
	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def version(self) -> jk_version.Version:
		return self.__gitVersion
	#

	@property
	def porcelainVersion(self) -> int:
		return self.__gitPorcelainVersion
	#

	@property
	def gitBinPath(self) -> str:
		return self.__gitBinPath
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	@staticmethod
	def _detectGitBinaryE() -> str:
		_pathcandidates = None
		if os.name == "nt":
			_pathcandidates = [ "C:\\Program Files\\Git\\cmd\\git.exe" ]
		else:
			_pathcandidates = [ "/usr/bin/git" ]

		# ----

		for pc in _pathcandidates:
			if os.path.isfile(pc):
				return pc

		# ----

		raise Exception("Git seems not to be installed!")
	#

	@staticmethod
	def _getVersion(gitBinPath:str, log:jk_logging.AbstractLogger) -> jk_version.Version:
		r = jk_simpleexec.invokeCmd2(
			cmdPath = gitBinPath,
			cmdArgs = [ "--version" ],
			log = log,
		)
		if (r is None) or r.isError:
			if log:
				r.dump(printFunc=log.warn)
			raise Exception("Running git failed!")

		lines = r.stdOutLines
		if lines[0].startswith("git version "):
			return jk_version.Version(lines[0][12:].strip())
		else:
			raise Exception("Failed to parse version! ({})".format(repr(lines[0])))
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def runGitWD(self,
			workingDirectory:typing.Union[str,None],
			arguments:typing.Union[typing.List[str],typing.Tuple[str]],
			log:jk_logging.AbstractLogger = None,
			*,
			bRaiseExceptionOnError:bool = True,
		) -> jk_simpleexec.CommandResult:

		ret = jk_simpleexec.invokeCmd2(
			cmdPath = self.__gitBinPath,
			cmdArgs = arguments,
			workingDirectory = workingDirectory,
			log = log,
		)

		if bRaiseExceptionOnError and ret.isErrorRC:
			if log:
				ret.dump(printFunc = log.notice)
			raise Exception("Failed to run git!")

		return ret
	#

	@jk_typing.checkFunctionSignature()
	def runGitNoWD(self,
			arguments:typing.Union[typing.List[str],typing.Tuple[str]],
			log:jk_logging.AbstractLogger = None,
			*,
			bRaiseExceptionOnError:bool = True,
		) -> jk_simpleexec.CommandResult:

		ret = jk_simpleexec.invokeCmd2(
			cmdPath = self.__gitBinPath,
			cmdArgs = arguments,
			log = log,
		)

		if bRaiseExceptionOnError and ret.isErrorRC:
			if log:
				ret.dump(printFunc = log.notice)
			raise Exception("Failed to run git!")

		return ret
	#

#





