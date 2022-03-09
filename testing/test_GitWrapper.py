#!/usr/bin/python3



import os

import jk_json
import jk_logging
import jk_git

from TestHelper import TestHelper





with jk_logging.wrapMain() as log:
	with TestHelper(log) as th:

		th.git.dump()

#
