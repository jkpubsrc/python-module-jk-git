################################################################################
################################################################################
###
###  This file is automatically generated. Do not change this file! Changes
###  will get overwritten! Change the source file for "setup.py" instead.
###  This is either 'packageinfo.json' or 'packageinfo.jsonc'
###
################################################################################
################################################################################


from setuptools import setup

def readme():
	with open("README.md", "r", encoding="UTF-8-sig") as f:
		return f.read()

setup(
	author = "Jürgen Knauth",
	author_email = "pubsrc@binary-overflow.de",
	classifiers = [
		"Development Status :: 4 - Beta",
		"License :: OSI Approved :: Apache Software License",
		"Programming Language :: Python :: 3",
	],
	description = "This python module is a wrapper around git (= the git binary file). It is ment as a simple interface to basic git functionality.",
	include_package_data = True,
	install_requires = [
		"python-dateutil",
		"jk_simpleexec",
		"jk_prettyprintobj",
		"jk_typing",
		"jk_utils",
		"jk_prettyprintobj",
		"jk_logging",
		"jk_version",
	],
	keywords = [
		"git",
	],
	license = "Apache2",
	name = "jk_git",
	package_data = {
		"": [
		],
	},
	packages = [
		"jk_git",
		"jk_git.impl",
		"jk_git.workingcopy",
	],
	scripts = [
	],
	version = '0.2022.7.24',
	zip_safe = False,
	long_description = readme(),
	long_description_content_type = "text/markdown",
)
