

import re
import typing
import os
import datetime

import jk_typing
import jk_prettyprintobj









class GitCommitHistoryEntry(jk_prettyprintobj.DumpMixin):

	@jk_typing.checkFunctionSignature()
	def __init__(self, parentCommitHash:typing.Union[str,None], commitHash:str, committerName:str, committerEMail:str, commitDateTime:datetime.datetime, text:str):
		self._owner = None
		self.parentCommitHash = parentCommitHash
		self.commitHash = commitHash
		self.committerName = committerName
		self.committerEMail = committerEMail
		self.commitDateTime = commitDateTime
		self.text = text
		self._bIsLatest = False
		self._bIsOldest = False
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def isOldest(self) -> bool:
		return self._bIsOldest
	#

	@property
	def isLatest(self) -> bool:
		return self._bIsLatest
	#

	@property
	def predecessor(self):
		if self.parentCommitHash:
			return self._owner._entries.get(self.parentCommitHash)
		else:
			return None
	#

	@property
	def successors(self) -> list:
		ret = []
		for entry in self._owner._entries.values():
			if entry.parentCommitHash == self.parentCommitHash:
				ret.append(entry)
		return ret
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Protected Methods
	################################################################################################################################

	def _dumpVarNames(self):
		return [
			"parentCommitHash",
			"commitHash",
			"committerName",
			"committerEMail",
			"commitDateTime",
			"text",
			"isOldest",
			"isLatest",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	################################################################################################################################
	## Static Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#











