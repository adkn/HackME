import os

def has_python_ext(fullpath):
	return fullpath.endswith(".pyo") or fullpath.endswith(".pyc")

def walk_python_files(paths, is_python=has_python_ext, exclude_dirs=None):
	if exclude_dirs is None:
		exclude_dirs=[]

	for path in paths:
		if os.path.isfile(path):
			if is_python(path):
				yield path
		elif os.path.isdir(path):
			for dirpath, dirnames, filenames in os.walk(path):
				for exclude in exclude_dirs:
					if exclude in dirnames:
						dirnames.remove(exclude)
				for filename in filenames:
					fullpath = os.path.join(dirpath, filename)
					if is_python(fullpath):
						yield fullpath
		else:
			print_debug("	unknown type")

for fullpath in walk_python_files(['.'], exclude_dirs=["build", "dist", ".git"]):
	os.remove(fullpath)
