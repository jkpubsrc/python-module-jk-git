#!/usr/bin/python3



import os
import typing
import tempfile

import jk_json
import jk_logging
import jk_typing
import jk_git

from TestHelper import TestHelper





with jk_logging.wrapMain() as log:
	with TestHelper(log) as th:

		th.createRepository(log)

		th.createSingleFileAndCommitIt("foo1.txt", "mycommitmsg1", log)

		th.createSingleFileAndCommitIt("foo2.txt", "mycommitmsg2", log)

		"""
		with log.descend("Creating another file and committing it ...") as log2:
			filePath = os.path.join(tempDirPath, "foo2.txt")
			with open(filePath, "w") as fout:
				fout.write("")
			ret = git.add(tempDirPath, filePath, log=log2)
			_dumpOutput(ret, log2)
			ret = git.commit(tempDirPath, "mycommitmsg2", log=log2)
			_dumpOutput(ret, log2)
		"""

		with log.descend("Creating a branch ...") as log2:
			ret = th.git.createBranch(th.tempDirPath, "mybranch", log=log2)
			th._dumpOutput(ret, log2)

		with log.descend("Listing branches ...") as log2:
			ret = th.git.listBranches(th.tempDirPath, log=log2)
			th._dumpOutput(ret, log2)
			assert isinstance(ret, list)
			assert len(ret) == 2
			assert ret[0] == "  master"
			assert ret[1] == "* mybranch"

		"""
		with log.descend("Creating even another file and committing it ...") as log2:
			filePath = os.path.join(th.tempDirPath, "foo3.txt")
			with open(filePath, "w") as fout:
				fout.write("")
			ret = th.git.add(th.tempDirPath, filePath, log=log2)
			th._dumpOutput(ret, log2)
			ret = th.git.commit(th.tempDirPath, "mycommitmsg3", log=log2)
			th._dumpOutput(ret, log2)
		"""

		th.createSingleFileAndCommitIt("foo3.txt", "mycommitmsg3", log)

		with log.descend("Show log ...") as log2:
			ret = th.git.showLog(th.tempDirPath, log=log2)
			th._dumpOutput(ret, log2)

#





