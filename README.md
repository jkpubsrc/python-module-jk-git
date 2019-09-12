jk_git
==========

Introduction
------------

This python module is a wrapper around git (= the git binary file). It is ment as a simple interface to basic git functionality.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/....)
* [pypi.python.org](https://pypi.python.org/pypi/jk_git)

Why this module?
----------------

`git` is an excellent version control system. It is widely used by developers to manage their source code in application development. Unfortunately using this functionality from within Python is a bit difficult as Python modules either don't provide some functionality required or aren't documented sufficiently. This module aims to fill this gap to some extent. Moreover it aims to do that in a way where the API is kept as universal as possible to allow similar support of other version control systems in the future.

Limitations of this module
--------------------------

This Python module does not aim to be a perfect wrapper around `git`, providing every single feature `git` provides. Nevertheless the functionality typically used will be covered in the future.

State of development
--------------------

This module currently provides the following functionality:

* check if a directory is a `git` working copy directory
* retrieve the status: which files need to be committed?

Future versions of this module will provide the following functionality:

* confirm changes to files in preparation of a commit
* perform a commit
* perform a push
* create tags

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
from jk_git import *
```

### Check if a directory is a working copy directory

Sometimes it is convenient to check if a specific directory is a working copy directory:

```python
print(GitWorkingCopy.hasWorkingCopy("/some/dir/....."))
```

### Instantiate a working copy object to work with the working copy

In order to perform operations on the working copy you first have to instantiate an object representing your working copy:

```python
wc = GitWorkingCopy("/some/dir/.....")
```

### Display information about the current working copy

Example:

```python
wc = GitWorkingCopy("/some/dir/.....")

print("Working copy root directory:", wc.rootDir)
print("Working copy is clean:", wc.isClean)
print("Working copy is not clean:", wc.isDirty)
print("Credentials are stored in git configuration:", wc.areCredentialsStored)
print("The upstream repository URL:", wc.remoteOrigin)
```

### Display changes made to the current working copy

```python
wc = GitWorkingCopy("/some/dir/.....")

for f in git.status(bIncludeIgnored=True):
	print("\t", f)
```

Contact Information
-------------------

This is Open Source code. That not only gives you the possibility of freely using this code it also
allows you to contribute. Feel free to contact the author(s) of this software listed below, either
for comments, collaboration requests, suggestions for improvement or reporting bugs:

* Jürgen Knauth: jknauth@uni-goettingen.de, pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



