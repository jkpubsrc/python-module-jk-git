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

		th.createSingleFileAndCommitIt("foo.txt", "mycommitmsg1", log)

		with log.descend("Listing tags ...") as log2:
			ret = th.git.listTags(th.tempDirPath, log=log2)
			th._dumpOutput(ret, log2)
			assert isinstance(ret, list)
			assert len(ret) == 0

		with log.descend("Creating a tag ...") as log2:
			ret = th.git.createTag(th.tempDirPath, "mytag", "mytagmsg1", log=log2)
			th._dumpOutput(ret, log2)

		with log.descend("Listing tags ...") as log2:
			ret = th.git.listTags(th.tempDirPath, log=log2)
			th._dumpOutput(ret, log2)
			assert isinstance(ret, list)
			assert len(ret) == 1
			assert ret[0] == "mytag"

		with log.descend("Deleting the tag ...") as log2:
			ret = th.git.deleteTag(th.tempDirPath, "mytag", log=log2)
			th._dumpOutput(ret, log2)

		with log.descend("Listing tags ...") as log2:
			ret = th.git.listTags(th.tempDirPath, log=log2)
			th._dumpOutput(ret, log2)
			assert isinstance(ret, list)
			assert len(ret) == 0

#





