#!/usr/bin/python3



import os

import jk_json
import jk_logging

import jk_git






REPOSITORY_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))




with jk_logging.wrapMain() as log:

	git = jk_git.GitWrapper(log)
	gitHistory = jk_git.GitCommitHistory.create(REPOSITORY_ROOT, git)
	gitHistory.dump()





