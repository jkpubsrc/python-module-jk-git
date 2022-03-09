#!/usr/bin/python3



import os

import jk_logging

import jk_git





REPOSITORY_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata/HGSUgLiZnT192ub8LJvqwPxYvF66atgg"))





with jk_logging.wrapMain() as log:

	wc = jk_git.GitServerRepository(REPOSITORY_ROOT, log)
	wc.dump()




