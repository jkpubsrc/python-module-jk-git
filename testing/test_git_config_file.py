#!/usr/bin/python3



import os

import jk_json
import jk_logging

import jk_git
import jk_git.impl
import jk_git.workingcopy




REPOSITORY_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


with jk_logging.wrapMain() as log:

	cfg = jk_git.impl.GitConfigFile.loadFromFile(
		os.path.join(REPOSITORY_ROOT, ".git", "config")
	)
	cfg.dump()




