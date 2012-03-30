import re

#hdd = [ ["bin", [ ["folder1", ["exe1"]], ["exe2"]]], ["test", []], ["exe3"] ]
#hdd = [ [file, 0], [dir, 1] ] -> choosen one

class FileSystem:
	def __init__(self, hdd = []):
		self.hdd = hdd
		self.curLoc = '/'

	def getFiles(self):
		curDir = re.compile(self.curLoc + "(.*?)/?")
		files = []
		for fileEntry in self.hdd:
			if curDir.match(fileEntry[0]):
				file = fileEntry[0]
				if fileEntry[1] == 1:
					file = '/' + file
				files.append(file)
		return files

	def changeDir(self, dir):
		if dir == "..":
			if self.curLoc != '/':
				self.curLoc = self.curLoc[:self.curLoc.rfind('/')]
		elif dir == ".":
			self.curLoc = self.curLoc
		elif dir in self.getFiles():
			self.curLoc += dir[1:]
		else:
			return False
		return True

