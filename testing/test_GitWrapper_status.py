#!/usr/bin/python3



import jk_git
import jk_json



git = jk_git.GitWrapper()
print(git.porcelainVersion())
jk_json.prettyPrint(git.status(".."))







