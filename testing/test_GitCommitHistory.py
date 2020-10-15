#!/usr/bin/python3



import os

import jk_git
import jk_json



REPOSITORY_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


git = jk_git.GitWrapper()
gitHistory = jk_git.GitCommitHistory.create(REPOSITORY_ROOT, git)
gitHistory.dump()





