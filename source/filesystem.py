import re

#hdd = [ ["bin", [ ["folder1", ["exe1"]], ["exe2"]]], ["test", []], ["exe3"] ]
#hdd = [ [file, 0], [dir, 1] ] -> choosen one

class FileSystem:
	def __init__(self, hdd = []):
		self.hdd = hdd
		self.curLoc = '/'

	def getFiles(self):
		curDir = re.compile(self.curLoc + "([a-zA-Z0-9_])")
		files = []
		curD = len(self.curLoc.split('/'))
		for fileEntry in self.hdd:
			tarD = len(fileEntry[0].split('/'))
			if curD == tarD and fileEntry[0].startswith(self.curLoc):
				file = fileEntry[0]
				if fileEntry[1] == 1 and not fileEntry[0].startswith('/'):
					file = '/' + file
				files.append(file)
		return files

	def changeDir(self, dir):
		if dir == "..":
			if self.curLoc != '/':
				self.curLoc = self.curLoc[:self.curLoc[:-1].rfind('/') + 1]
			return True
		elif dir == ".":
			self.curLoc = self.curLoc
			return True

		if not dir.startswith('/'):
			dir = self.curLoc + dir

		if dir in self.getFiles():
			self.curLoc = dir
			if not self.curLoc.endswith('/'):
				self.curLoc += '/'
			return True
		
		return False
	
	def fileExists(self, file):
		return (self.curLoc + file) in self.getFiles()
	
	def makeDir(self, dir):
		if dir == ".." or dir == ".":
			return False
		if [(self.curLoc + dir), 1] in self.hdd:
			return False
		self.hdd.append([self.curLoc + dir, 1])
		return True
	
	def crFile(self, file):
		if file == ".." or file == ".":
			return False
		if (self.curLoc + file) in self.hdd:
			return False
		self.hdd.append([self.curLoc + file, 0])
		return True
