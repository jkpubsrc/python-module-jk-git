


import os



class GitConfigFile(object):

	def __init__(self, path:str):
		if os.path.isdir(path):
			p = path + "/.git/config"
			if not os.path.isfile(p):
				raise Exception("Not a git root directory: " + repr(path))
		else:
			if os.path.isfile(path):
				p = path
			else:
				raise Exception("Not a git configuration file: " + repr(path))

		self.__data = self.__loadFile(p)
	#

	def getValue(self, sectionName:str, key:str):
		section = self.__data.get(sectionName)
		if section:
			return section.get(key)
		else:
			return None
	#

	def getSection(self, sectionName:str):
		return self.__data.get(sectionName)
	#

	def sectionNames(self):
		return sorted(self.__data.keys())
	#

	def __loadFile(self, path:str):
		sections = {}
		with open(path, "r") as f:
			section = {}
			sectionName = None
			for line in f.readlines():
				line = line.strip()
				if line:
					if line[0] == "[":
						if sectionName:
							sections[sectionName] = section
							section = {}
						sectionName = line[1:-1]
					else:
						pos = line.find("=")
						if pos < 0:
							raise Exception()
						key = line[:pos].strip()
						value = line[pos+1:].strip()
						section[key] = value
		if sectionName:
			sections[sectionName] = section

		return sections
	#

#