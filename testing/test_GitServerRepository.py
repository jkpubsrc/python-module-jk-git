#!/usr/bin/python3



import os

import jk_git
import jk_json



REPOSITORY_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata/HGSUgLiZnT192ub8LJvqwPxYvF66atgg"))


wc = jk_git.GitServerRepository(REPOSITORY_ROOT)
wc.dump()




