

import os
import re
import collections
import typing

import jk_typing
import jk_prettyprintobj

from .GitConfigFileSection import GitConfigFileSection





class GitConfigFile(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, filePath:str):
		self.__filePath = filePath
		self.__sections:typing.List[GitConfigFileSection] = []
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def filePath(self) -> str:
		return self.__filePath
	#

	@property
	def sections(self) -> typing.List[GitConfigFileSection]:
		return self.__sections
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"filePath",
			"sections",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __iter__(self) -> typing.Iterable[GitConfigFileSection]:
		return self.__sections.__iter__()
	#

	def __getitem__(self, ii) -> typing.Union[GitConfigFileSection,None]:
		if isinstance(ii, int):
			return self.__sections[ii]
		elif isinstance(ii, str):
			return self.getSection(ii)
		else:
			raise TypeError(repr(ii) + " - " + str(type(ii)))
	#

	def __len__(self):
		return len(self.__sections)
	#

	def __bool__(self):
		return bool(self.__sections)
	#

	@jk_typing.checkFunctionSignature()
	def getSections(self, sectionName:str) -> typing.List[GitConfigFileSection]:
		ret = []
		for sect in self.__sections:
			if sect.name == sectionName:
				ret.append(sect)
		return ret
	#

	@jk_typing.checkFunctionSignature()
	def getValue(self, sectionName:str, propertyKey:str) -> typing.Union[str,None]:
		section = self.getSection(sectionName)
		if section:
			return section.getProperty(propertyKey)
		else:
			return None
	#

	#
	# This method replaces <c>getValue()</c>.
	#
	# @param	str sectionName			(required) The name of the section to retrieve
	# @param	str argument			(optional) Additional search condition: The name of the section argument.
	#									Using <c>null</c> by default to indicate 'no section argument'.
	# @param	str propertyKey			(required) The name of the section property to retrieve
	# @return							The requested value if a) the section and b) the value requested was found. <c>null</c> otherwise.
	#
	@jk_typing.checkFunctionSignature()
	def getValue2(self, sectionName:str, argument:typing.Union[str,None], propertyKey:str) -> typing.Union[str,None]:
		section = self.getSection(sectionName, argument)
		if section:
			return section.getProperty(propertyKey)
		else:
			return None
	#

	#
	# Get a specific setion.
	#
	# @param	str sectionName			(required) The name of the section to retrieve
	# @param	str argument			(optional) Additional search condition: The name of the section argument.
	#									Using <c>null</c> by default to indicate 'no section argument'.
	# @return							The git configuration section object if the section was found. <c>null</c> otherwise.
	#
	@jk_typing.checkFunctionSignature()
	def getSection(self, sectionName:str, argument:str = None) -> typing.Union[GitConfigFileSection,None]:
		if argument:
			for sect in self.__sections:
				if (sect.name == sectionName) and (sect.argument == argument):
					return sect
		else:
			for sect in self.__sections:
				if sect.name == sectionName:
					return sect
		return None
	#

	@staticmethod
	@jk_typing.checkFunctionSignature()
	def loadFromFile(filePath:str):
		with open(filePath, "r") as fin:
			rawText = fin.read()

		ret = GitConfigFile(filePath)

		currentSection = None
		for line in rawText.split("\n"):
			line = line.rstrip()	# just to be sure
			if not line:			# just to be sure
				continue

			# something like: [foo "bar"]
			m = re.match(r"\[([a-z]+)\s+\"([^\"]+)\"\]", line)
			if m:
				currentSection = GitConfigFileSection(m.group(1), m.group(2))
				ret.__sections.append(currentSection)
			else:
				# something like: [foo]
				m = re.match(r"\[([a-z]+)\]", line)
				if m:
					currentSection = GitConfigFileSection(m.group(1), None)
					ret.__sections.append(currentSection)
				else:
					# something like: key = value
					m = re.match(r"\s+([a-zA-Z0-9_]+)\s+=\s+(.+)", line)
					if m:
						currentSection.setProperty(m.group(1), m.group(2))

		return ret
	#

#





