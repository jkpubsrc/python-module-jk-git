#!/usr/bin/python3



import os

import jk_git
import jk_json



REPOSITORY_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


wc = jk_git.GitWorkingCopy(REPOSITORY_ROOT)
print(wc.remotes)




