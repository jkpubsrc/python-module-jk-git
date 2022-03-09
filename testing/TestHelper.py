#!/usr/bin/python3



import os
import typing
import tempfile

import jk_json
import jk_logging
import jk_typing
import jk_git



class TestHelper(object):

	def __init__(self, log:jk_logging.AbstractLogger) -> None:
		self.git = jk_git.GitWrapper(log)

		self.__tempDir = None
		self.__tempDirPath = None
	#

	@property
	def tempDirPath(self) -> str:
		return self.__tempDirPath
	#

	def __enter__(self):
		self.__tempDir = tempfile.TemporaryDirectory()
		self.__tempDirPath = self.__tempDir.name
		return self
	#

	def __exit__(self, ex_class, ex_obj, ex_traceback):
		del self.__tempDir
		self.__tempDir = None
		self.__tempDirPath = None
	#

	@jk_typing.checkFunctionSignature(logDescend="RETURNED DATA:", logLevel=jk_logging.EnumLogLevel.NOTICE)
	def _dumpOutput(self, something:typing.Union[str,list,None], log:jk_logging.AbstractLogger):
		if something is None:
			log.notice("\t(null)")
		else:
			for line in jk_json.prettyPrintToStr(something).split("\n"):
				log.notice("\t" + line)
	#

	@jk_typing.checkFunctionSignature(logDescend="Creating repository ...")
	def createRepository(self, log:jk_logging.AbstractLogger):
		ret = self.git.init(self.__tempDirPath, log=log)
		self._dumpOutput(ret, log)
	#

	@jk_typing.checkFunctionSignature(logDescend="Creating a file and committing it ...")
	def createSingleFileAndCommitIt(self, fileName:str, commitMsg:str, log:jk_logging.AbstractLogger):
		filePath = os.path.join(self.__tempDirPath, fileName)
		with open(filePath, "w") as fout:
			fout.write("")
		ret = self.git.add(self.__tempDirPath, filePath, log=log)
		self._dumpOutput(ret, log)
		ret = self.git.commit(self.__tempDirPath, commitMsg, log=log)
		self._dumpOutput(ret, log)
	#

#

