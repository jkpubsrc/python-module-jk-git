

import os
import re
import collections
import typing

import jk_typing
import jk_prettyprintobj






class GitConfigFileSection(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, name:str, argument:str = None):
		self.__name = name
		self.__argument = argument
		self.__properties = collections.OrderedDict()
		self.__propertiesCachedDict = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def name(self) -> str:
		return self.__name
	#

	@property
	def argument(self) -> str:
		return self.__argument
	#

	@property
	def properties(self) -> typing.Dict[str,str]:
		if self.__propertiesCachedDict is None:
			self.__propertiesCachedDict = dict(self.__properties)
		return self.__propertiesCachedDict
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"name",
			"argument",
			"properties",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def getProperty(self, key:str) -> typing.Union[str,None]:
		return self.__properties.get(key)
	#

	@jk_typing.checkFunctionSignature()
	def setProperty(self, key:str, value:str):
		self.__properties[key] = value
		self.__propertiesCachedDict = None
	#

#





