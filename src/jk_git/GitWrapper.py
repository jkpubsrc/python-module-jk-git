


import os
import typing
import re

import jk_typing
import jk_logging
import jk_prettyprintobj
import jk_simpleexec
import jk_version

from .impl.GitHelper import GitHelper











#
# This class wraps around the program 'git'.
#
class GitWrapper(jk_prettyprintobj.DumpMixin):

	__GIT_HELPER = None

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, log:jk_logging.AbstractLogger = None):
		if GitWrapper.__GIT_HELPER is None:
			GitWrapper.__GIT_HELPER = GitHelper(log)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def version(self) -> jk_version.Version:
		return GitWrapper.__GIT_HELPER.version
	#

	@property
	def porcelainVersion(self):
		return GitWrapper.__GIT_HELPER.porcelainVersion
	#

	@property
	def gitBinPath(self) -> str:
		return GitWrapper.__GIT_HELPER.gitBinPath
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self):
		return [
			"version",
			"gitBinPath",
			"porcelainVersion",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature(logDescend="Executing git ...", logLevel=jk_logging.EnumLogLevel.NOTICE)
	def runGit(self,
			*args,
			cmdArgs:typing.Union[typing.List[str],typing.Tuple[str]],
			workingDirectory:str = None,
			bRaiseExceptionOnError:bool = True,
			log:jk_logging.AbstractLogger = None,
			**kwargs,
		) -> jk_simpleexec.CommandResult:

		assert not args
		assert not kwargs

		# ---

		return GitWrapper.__GIT_HELPER.runGitWD(
			workingDirectory,
			cmdArgs,
			log,
			bRaiseExceptionOnError=bRaiseExceptionOnError,
		)
	#

	################################################################################################################################
	## Public High Level Methods
	################################################################################################################################

	#
	# Retrieve the status of a working copy
	#
	# @return	str[]		Text output of the 'status' command
	#
	@jk_typing.checkFunctionSignature()
	def status(self, gitRootDir:str, bIncludeIgnored:bool = False, log:jk_logging.AbstractLogger = None) -> typing.List[str]:
		if GitWrapper.__GIT_HELPER.porcelainVersion == 1:

			if bIncludeIgnored:
				_cmdArgs = [ "-C", ".", "status", "--porcelain", "-uall", "--ignored" ]
			else:
				_cmdArgs = [ "-C", ".", "status", "--porcelain", "-uall" ]

			r = GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, _cmdArgs, log)

		elif GitWrapper.__GIT_HELPER.porcelainVersion == 2:

			if bIncludeIgnored:
				#	_cmdArgs = [ "-C", gitRootDir, "status", "--porcelain=2", "-uall", "--ignored=traditional" ],
				_cmdArgs = [ "-C", ".", "status", "--porcelain=2", "-uall", "--ignored" ]
			else:
				_cmdArgs = [ "-C", ".", "status", "--porcelain=2", "-uall" ]

			r = GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, _cmdArgs, log)

		else:
			raise Exception()
		if (r is None) or r.isError:
			if log:
				r.dump(printFunc=log.warn)
			raise Exception("Running git failed!")
		if r.stdOutLines:
			return r.stdOutLines
		else:
			return []
	#

	@jk_typing.checkFunctionSignature()
	def lsRemote_url(self, url:str, log:jk_logging.AbstractLogger = None) -> list:
		r = GitWrapper.__GIT_HELPER.runGitNoWD(None, [ "ls-remote", url ], log)
		if (r is None) or r.isError:
			if log:
				r.dump(printFunc=log.warn)
			raise Exception("Running git failed!")
		ret = []
		for line in r.stdOutLines:
			m = re.match("^([a-zA-Z0-9]+)\s+(.*)$", line.strip())
			if m:
				ret.append([ m.group(1), m.group(2) ])
		return ret
	#

	@jk_typing.checkFunctionSignature()
	def lsRemote_dir(self, gitRootDir:str, log:jk_logging.AbstractLogger = None) -> list:
		r = GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "-C", ".", "ls-remote" ], log)
		if (r is None) or (r.returnCode != 0):
			if log:
				r.dump(printFunc=log.warn)
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
	@jk_typing.checkFunctionSignature()
	def add(self, gitRootDir:str, filePath:str, log:jk_logging.AbstractLogger = None) -> typing.List[str]:
		assert os.path.isabs(filePath)

		s = gitRootDir
		if not s.endswith("/"):
			s += "/"
		if not filePath.startswith(s):
			raise Exception("File does not seem to be part of the git tree: " + filePath)

		r = GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "-C", ".", "add", filePath ], log)
		if (r is None) or r.isError:
			if log:
				r.dump(printFunc=log.warn)
			raise Exception("Running git failed!")
		if r.stdOutLines:
			return r.stdOutLines
		else:
			return []
	#

	@jk_typing.checkFunctionSignature()
	def pull(self, gitRootDir:str, log:jk_logging.AbstractLogger = None) -> typing.List[str]:
		assert os.path.isdir(gitRootDir)

		r = GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "-C", ".", "pull" ], log)

		# STDOUT: 'Updating 293bc22..81ad022'
		# STDOUT: 'Fast-forward'
		# STDOUT: ' packageinfo.jsonc | 4 +++-'
		# STDOUT: ' 1 file changed, 3 insertions(+), 1 deletion(-)'
		# STDERR: 'From ssh://123.45.67.89:/foo/bar/some_repo_dir'
		# STDERR: '   293bc22..81ad022  master     -> origin/master'
		# RETURNCODE: 0

		if (r is None) or (r.returnCode != 0):
			if log:
				r.dump(printFunc=log.warn)
			raise Exception("Running git failed!")

		ret = []
		if r.stdOutLines:
			ret.extend(r.stdOutLines)
		if r.stdErrLines:
			ret.extend(r.stdErrLines)
		return ret
	#

	@jk_typing.checkFunctionSignature()
	def clone(self, gitRootDir:str, url:str, log:jk_logging.AbstractLogger = None) -> typing.List[str]:
		assert os.path.isdir(gitRootDir)
		assert isinstance(url, str)
		assert url

		os.makedirs(gitRootDir, exist_ok=True)
		for something in os.listdir(gitRootDir):
			raise Exception("Target directory is not empty: " + gitRootDir)

		r = GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "clone", url, "." ], log)
		if (r is None) or (r.returnCode != 0):
			if log:
				r.dump(printFunc=log.warn)
			raise Exception("Running git failed!")
		if r.stdErrLines:
			return r.stdErrLines
		else:
			return []
	#

	#
	# Download a single file from the HEAD revision.
	#
	# @return		str			Either returns the file content if the file exists or `None` if the file does not exist.
	#
	@jk_typing.checkFunctionSignature()
	def downloadFromHead(self, gitRootDir:str, filePath:str, log:jk_logging.AbstractLogger = None) -> str:
		r = GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "-C", ".", "show", "HEAD:" + filePath ], log, bRaiseExceptionOnError=False)
		if (r is None) or r.isError:
			if (r.returnCode == 128) and r.stdErrLines and r.stdErrLines[0].startswith("fatal:"):
				if ("does not exist" in r.stdErrLines[0]) or ("but not in 'HEAD'" in r.stdErrLines[0]):
					return None
			if log:
				r.dump(printFunc=log.warn)
			raise Exception("Running git failed!")
		if r.stdOutLines:
			return "\n".join(r.stdOutLines)
		else:
			return ""
	#

	@jk_typing.checkFunctionSignature()
	def init(self, gitRootDir:str, log:jk_logging.AbstractLogger = None) -> None:
		GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "init" ], log)
	#

	#
	# Run 'git flow init' with using all default settings.
	#
	@jk_typing.checkFunctionSignature()
	def flowInit(self, gitRootDir:str, log:jk_logging.AbstractLogger = None) -> None:
		r = GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "flow", "init", "-d" ], log, bRaiseExceptionOnError=False)
		if "'flow' is not a git command" in r.stdErrStr:
			raise Exception("git-flow is not installed!")
		if r.isErrorRC:
			if log:
				r.dump(printFunc=log.warn)
			raise Exception("Running git failed!")
	#

	@jk_typing.checkFunctionSignature()
	def commit(self, gitRootDir:str, commitMsg:str, log:jk_logging.AbstractLogger = None) -> None:
		assert commitMsg

		GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "commit", "-m", commitMsg ], log)
	#

	@jk_typing.checkFunctionSignature()
	def listTags(self, gitRootDir:str, log:jk_logging.AbstractLogger = None) -> typing.List[str]:
		r = GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "-C", ".", "tag", "--list" ], log)
		return r.stdOutLines
	#

	@jk_typing.checkFunctionSignature()
	def createTag(self, gitRootDir:str, tagName:str, commitMsg:str, log:jk_logging.AbstractLogger = None) -> None:
		assert tagName
		assert commitMsg

		GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "-C", ".", "tag", "-a", tagName, "-m", commitMsg ], log)
	#

	@jk_typing.checkFunctionSignature()
	def deleteTag(self, gitRootDir:str, tagName:str, log:jk_logging.AbstractLogger = None) -> None:
		assert tagName

		GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "-C", ".", "tag", "-d", tagName ], log)
	#

	@jk_typing.checkFunctionSignature()
	def listBranches(self, gitRootDir:str, log:jk_logging.AbstractLogger = None) -> typing.List[str]:
		r = GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "-C", ".", "branch", "--all" ], log)
		if r.isError:
			if log:
				r.dump(printFunc=log.warn)
			raise Exception("Running git failed!")
		return r.stdOutLines
	#

	@jk_typing.checkFunctionSignature()
	def createBranch(self, gitRootDir:str, branchName:str, log:jk_logging.AbstractLogger = None) -> None:
		assert branchName

		GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "-C", ".", "checkout", "-b", branchName ], log)
		# NOTE: STDERR is something like "Switched to a new branch '....'"
	#

	@jk_typing.checkFunctionSignature()
	def switchToBranch(self, gitRootDir:str, branchName:str, log:jk_logging.AbstractLogger = None) -> None:
		assert branchName

		GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "-C", ".", "checkout", branchName ], log)
		# NOTE: STDERR is something like "Switched to a branch '....'"
	#

	#@jk_typing.checkFunctionSignature()
	#def describeAll(self, gitRootDir:str, log:jk_logging.AbstractLogger = None) -> typing.List[str]:
	#	r = GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "-C", ".", "describe", "--tags", "--all" ], log)
	#	r.dump()
	#	return r.stdOutLines
	##

	@jk_typing.checkFunctionSignature()
	def showLog(self, gitRootDir:str, log:jk_logging.AbstractLogger = None) -> typing.List[str]:
		r = GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "-C", ".", "log" ], log)
		return r.stdOutLines
	#

	#
	# Show the log
	#
	# @return	str[]		Text output of the 'log' command
	#
	@jk_typing.checkFunctionSignature()
	def showLogParsable(self, gitRootDir:str, log:jk_logging.AbstractLogger = None) -> typing.List[str]:
		# %P	parent hashes
		# %H	commit hash
		# %cn	committer name
		# %ce	committer email
		# %cd	committer date
		# %s	subject (= commit message)
		r = GitWrapper.__GIT_HELPER.runGitWD(gitRootDir, [ "-C", ".", "log", "--pretty=format:\"%P|%H|%cn|%ce|%cd|%s\"" ], log)
		if (r is None) or r.isError:
			if r.stdErrLines \
				and (r.stdErrLines[0].find("fatal: your current branch") >= 0) \
				and (r.stdErrLines[0].find("does not have any commits yet") >= 0):
				return []
			else:
				if log:
					r.dump(printFunc=log.warn)
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










