#!/usr/bin/python3



import jk_git



git = jk_git.GitWrapper()
print(git.porcelainVersion())
print(git.status(".."))







