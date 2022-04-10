


import re
import os
import typing

from ..GitFileInfo import GitFileInfo






class _GitStatusOutputParser(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@staticmethod
	def __parseAny1(line:str) -> typing.Union[re.Match,None]:
		m = re.match("^\s*([A-Z\?!]+)\s+(.+)$", line)
		if m:
			return m

		return None
	#

	@staticmethod
	def __parseAny2(line:str) -> typing.Union[re.Match,None]:
		ret = re.match(r"^(\?)\s+(.+)$", line)
		if ret:
			return ret

		ret = re.match(r"^(!)\s+(.+)$", line)
		if ret:
			return ret

		ret = re.match("""
			^
				(1)
				\\s+
				([A-Z\\.]{2})
				\\s+
				([A-Z\\.]{4})
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				([a-zA-Z0-9]+)
				\\s+
				([a-zA-Z0-9]+)
				\\s+
				(.+)
			$
			""", line, re.VERBOSE)
		if ret:
			return ret

		ret = re.match("""
			^
				(2)
				\\s+
				([A-Z\\.]{2})
				\\s+
				([A-Z\\.]{4})
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				([a-zA-Z0-9]+)
				\\s+
				([A-Z][0-9]+)
				\\s+
				(.+)
			$
			""", line, re.VERBOSE)
		if ret:
			return ret

		ret = re.match("""
			^
				(u)
				\\s+
				([A-Z\\.]{2})
				\\s+
				([A-Z\\.]{4})
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				([0-9\\.]+)
				\\s+
				(.+)
				\\s+
				(.+)
				\\s+
				(.+)
				\\s+
				(.+)
			$
			""", line, re.VERBOSE)
		if ret:
			return ret

		return None
	#

	@staticmethod
	def parse(lines:typing.List[str], porcelainVersion:int, bIncludeIgnored:bool, parent) -> typing.List[GitFileInfo]:
		ret = []
		for line in lines:
			bSuccess = False

			if porcelainVersion == 1:
				m = _GitStatusOutputParser.__parseAny1(line)
			elif porcelainVersion == 2:
				m = _GitStatusOutputParser.__parseAny2(line)
			else:
				raise Exception()

			if m:
				g = m.groups()

				if porcelainVersion == 1:
					sType = g[0][-1]
					m = g[1:]
					if sType == "?":
						# untracked
						ret.append(GitFileInfo(parent, GitFileInfo.UNVERSIONED, m[0]))
						bSuccess = True
					elif sType == "!":
						# ignored
						ret.append(GitFileInfo(parent, GitFileInfo.IGNORED, m[0]))
						bSuccess = True
					elif sType == "A":
						# added
						ret.append(GitFileInfo(parent, GitFileInfo.ADDED, m[-1]))
						bSuccess = True
					elif sType == "M":
						# modified
						ret.append(GitFileInfo(parent, GitFileInfo.MODIFIED, m[-1]))
						bSuccess = True
					elif sType == "R":
						# renamed
						ret.append(GitFileInfo(parent, GitFileInfo.RENAMED, m[-1]))
						bSuccess = True
					elif sType == "D":
						# renamed
						ret.append(GitFileInfo(parent, GitFileInfo.DELETED, m[-1]))
						bSuccess = True
					elif sType == "U":
						# conflicted
						ret.append(GitFileInfo(parent, GitFileInfo.CONFLICTED, m[-1]))
						bSuccess = True

				elif porcelainVersion == 2:
					sType = g[0]
					m = g[1:]
					if sType == "?":
						# untracked
						ret.append(GitFileInfo(parent, GitFileInfo.UNVERSIONED, m[0]))
						bSuccess = True
					elif sType == "!":
						# ignored
						ret.append(GitFileInfo(parent, GitFileInfo.IGNORED, m[0]))
						bSuccess = True
					elif sType == "1":
						# modified
						if "A" in m[0]:
							ret.append(GitFileInfo(parent, GitFileInfo.ADDED, m[-1]))
						else:
							ret.append(GitFileInfo(parent, GitFileInfo.MODIFIED, m[-1]))
						bSuccess = True
					elif sType == "2":
						# renamed
						ret.append(GitFileInfo(parent, GitFileInfo.RENAMED, m[-1]))
						bSuccess = True
					elif sType == "u":
						# conflicted
						ret.append(GitFileInfo(parent, GitFileInfo.CONFLICTED, m[-1]))
						bSuccess = True

			if not bSuccess:
				raise Exception("Failed to parse line: " + repr(line))

		if not bIncludeIgnored:
			ret = [ x for x in ret if x.status() != GitFileInfo.IGNORED ]

		return ret
	#

#






