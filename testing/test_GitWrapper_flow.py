#!/usr/bin/python3



import os
import typing

import jk_json
import jk_logging
import jk_typing
import jk_git

from TestHelper import TestHelper





with jk_logging.wrapMain() as log:
	with TestHelper(log) as th:

		th.createRepository(log)

		th.createSingleFileAndCommitIt(log)

		with log.descend("Running git flow init ...") as log2:
			ret = th.git.flowInit(th.tempDirPath, log=log2)
			th._dumpOutput(ret, log2)

		with log.descend("Listing branches ...") as log2:
			ret = th.git.listBranches(th.tempDirPath, log=log2)
			th._dumpOutput(ret, log2)
			assert isinstance(ret, list)
			assert len(ret) == 2
			assert ret[0] == "* develop"
			assert ret[1] == "  master"

#





