#!/usr/bin/python3



import jk_git



git = jk_git.GitWorkingCopy(".")
print("root directory:", git.rootDir)
print("remote origin:", git.remoteOrigin)
print("status:")
for f in git.status(bIncludeIgnored=False):
	print("\t", f)








