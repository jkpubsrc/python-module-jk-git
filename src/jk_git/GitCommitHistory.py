

import re
import typing
import os

import dateutil
import dateutil.parser

import jk_typing
import jk_prettyprintobj

from .GitWrapper import GitWrapper
from .GitCommitHistoryEntry import GitCommitHistoryEntry








class GitCommitHistory(jk_prettyprintobj.DumpMixin):

	@jk_typing.checkFunctionSignature()
	def __init__(self, entriesList:list):
		assert entriesList
		assert entriesList[0].isOldest
		assert entriesList[-1].isLatest

		self._entriesList = entriesList

		self._oldestEntry = entriesList[0]
		self._latestEntry = entriesList[-1]

		self._entriesMap = {}
		for entry in entriesList:
			assert isinstance(entry, GitCommitHistoryEntry)
			entry._owner = self
			self._entriesMap[entry.commitHash] = entry
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def oldestEntry(self) -> GitCommitHistoryEntry:
		return self._oldestEntry
	#

	@property
	def latestEntry(self) -> GitCommitHistoryEntry:
		return self._latestEntry
	#

	@property
	def entriesMap(self) -> typing.Dict[str,GitCommitHistoryEntry]:
		return dict(self._entriesMap)
	#

	#
	# Returns the commits in forward order: The first entry is the oldest commit, the last entry is the latest commit
	#
	@property
	def entriesList(self) -> typing.List[GitCommitHistoryEntry]:
		return list(self._entriesList)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Protected Methods
	################################################################################################################################

	def _dumpVarNames(self):
		return [
			"oldestEntry",
			"latestEntry",
			"entriesList"
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
	# This method tries to create a GitCommitHistory object.
	#
	# @return		Returns (null) if no commits have been made jet, an instance of GitCommitHistory otherwise.
	#
	@staticmethod
	def create(rootDir:str, wrapper:GitWrapper):
		stdLines = wrapper.showLogParsable(rootDir)
		if not stdLines:
			return None

		return GitCommitHistory.createFromGitLogOutput(stdLines)
	#

	@staticmethod
	def createFromGitLogOutput(stdLines:str):
		entriesList = []
		for line in stdLines:
			parts = [
				x if x else None
					for x in line.split("|")
			]
			parts[4] = dateutil.parser.parse(parts[4])
			assert len(parts) == 6

			entry = GitCommitHistoryEntry(*parts)
			entriesList.append(entry)

		# now
		#	-> the first record is: latest
		#	-> the last record is: inital

		# the ordering of all records is from newest to olders => reverse order
		entriesList.reverse()

		# now:
		#	-> the first record is: inital
		#	-> the last record is: latest

		entriesList[0]._bIsOldest = True
		entriesList[-1]._bIsLatest = True

		return GitCommitHistory(entriesList)
	#

#











