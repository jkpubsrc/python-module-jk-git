#!/usr/bin/python3



import jk_git
import jk_json



git = jk_git.GitWrapper()
print(git.porcelainVersion())
s = git.downloadFromHead("..", "packageinfo.json")
print("=" * 200)
print(s)
print("=" * 200)







