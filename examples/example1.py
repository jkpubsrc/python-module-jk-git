#!/usr/bin/python3



import jk_logging
import jk_git



with jk_logging.wrapMain() as log:

	git = jk_git.GitWorkingCopy(".", log=log)
	print("root directory:", git.rootDir)
	print("remote origin:", git.remoteOriginURL)
	print("status:")
	for f in git.status(bIncludeIgnored=False):
		print("\t", f)








