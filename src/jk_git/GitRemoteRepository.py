 

import typing
import re
import os

import jk_utils
import jk_prettyprintobj

from .GitWrapper import GitWrapper
from .GitCommitHistory import GitCommitHistory









class GitRemoteRepository(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self, url:str):
		assert isinstance(url, str)

		self.__url = url
		self.__gitWrapper = GitWrapper()

		self.__volatileValue_lsRemote = jk_utils.VolatileValue(self.__lsRemote, 15)					# 15 seconds caching time
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def url(self) -> str:
		return self.__url
	#

	@property
	def headRevisionID(self) -> str:
		for revID, revName in self.__volatileValue_lsRemote.value:
			if revName == "HEAD":
				return revID
		raise Exception("Head revision not found!")
	#

	################################################################################################################################
	## Protected Methods
	################################################################################################################################

	def _dumpVarNames(self):
		return [
			"url",
			"headRevisionID",
		]
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	#
	# Returns something like:
	# [
	# 	[	"293bc22fa252a86039060986460275df3f5f0331",	"HEAD"	],
	# 	[	"293bc22fa252a86039060986460275df3f5f0331",	"refs/heads/master"	]
	# ]
	#
	def __lsRemote(self):
		return self.__gitWrapper.lsRemote_url(self.__url)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Run a <c>git clone</c> request.
	# The target directory must be empty. If it does not exist it will be created.
	#
	def checkout(self, toDirPath:str):
		assert isinstance(toDirPath, str)
		os.makedirs(toDirPath, exist_ok=True)

		self.__gitWrapper.clone(toDirPath, self.__url)
	#

	################################################################################################################################
	## Static Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#

