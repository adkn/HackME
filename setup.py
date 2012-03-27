from distutils.core import setup
import py2exe

setup(
	version = "0.1",
    description = "HackME",
    name = "HackME",
	windows=['main.py'],
	options={"py2exe": {"skip_archive": False, "bundle_files":3, "optimize":2, "compressed":2}},
	zipfile=None
	)
