import Tkinter
import threading
import const
import tkFont
import os

class Terminal(Tkinter.Label):
	def __init__(self, mWindow, width, height, bgcolor, lang, opts, fgcolor, initTime=2.0):
		Tkinter.Label.__init__(self, master=mWindow, foreground=fgcolor, background=bgcolor, anchor=Tkinter.SW, justify=Tkinter.LEFT)

		self.lang = lang
		self.lang2 = None
		self.options = opts

		self.height, self.width = height, width
		self.initTime = initTime
		self.userName = ""
		self.passWord = ""
		
		if os.name == "posix":
			self.font = tkFont.Font(family="Monospace", size=10, weight="normal")
		elif os.name == "nt":
			self.font = tkFont.Font(family="courier", size=8, weight="normal")
			
		cw = self.font.measure('A')
		ch = self.font.metrics("linespace")
		self.th = height/ch
		self.lw = width/cw - 2

		self.config(font=self.font, width=self.lw, height=self.th, relief=Tkinter.SUNKEN)

		self.text = ""
		self.lineL = 0
		self.lineC = 0
		self.last = -1
		
		self.state = const.states.boot
		self.game = mWindow
		self.sendCommands = []
		self.aliases = {}

		self.loadCommands()

	def loadCommands(self):
		self.commands =	[
			["help", [self.lang["c_help"], self.c_help]],
			["shutdown", [self.lang["c_shutdown"], self.c_shutdown]],
			["restart", [self.lang["c_restart"], self.c_restart]],
			["clear", [self.lang["c_clear"], self.c_clear]],
			["alias", [self.lang["c_alias"], self.c_alias]],
			["version", [self.lang["c_version"], self.c_version]],
			["whoami", [self.lang["c_whoami"], self.c_whoami]],
			["color", [self.lang["c_color"], self.c_color]],
			["lang", [self.lang["c_lang"], self.c_lang]],
			["mkdir", [self.lang["c_mkdir"], self.c_mkdir]],
			["cd", [self.lang["c_cd"], self.c_cd]],
		]
	

	def keyPressed(self, event):
		if self.state == const.states.boot or self.state == const.states.init:
			return
		if event.keysym == "Return" or event.keysym == "KP_Enter":
			command = self.getLastLine()
			self.printOut('\n')
			self.doCommand(command)
			if self.state == const.states.hack:
				self.printOut(":>")
		elif event.keysym == "BackSpace":
			line = self.getLastLine(clean=False)
			if self.state == const.states.login:
				if line == self.lang["login"] or line == self.lang["password"]:
					return
				if line.startswith(self.lang["password"]):
					self.passWord = self.passWord[:-1]
			if line == ":>":
				return
			self.printOut('\b')
		elif event.keycode == "Escape":
			pass
		elif event.keysym == "Up": #up arrow
			self.getPrevCommand()
		elif event.keysym == "Down": #down arrow
			self.getNextCommand()
		else:
			if len(event.char) == 1:
				if self.state == const.states.login:
					line = self.getLastLine(clean=False)
					if line.startswith(self.lang["password"]):
						self.printOut('*')
						self.passWord += event.char
						return
				self.printOut(event.char)

		#for key in event.__dict__:
		#	print key, ':', event.__dict__[key]

	def updateText(self):
		if not self.winfo_exists():
			return
		self.config(text=self.text + '_')

	def doCommand(self, line, printout=True):
		command = line
		if self.state == const.states.login:
			if self.userName == "":
				self.userName = command[len(self.lang["login"]):]
				self.printOut(self.lang["password"])
			else:
				self.login(self.userName, self.passWord)
			return
		
		cSplit = line.split(' ', 1)
		command = cSplit[0]
		self.line = line
		if command in self.aliases:
			value = self.aliases[command]
			self.addCommand(line)
			for comEntry in self.commands:
				if value == comEntry[0]:
					comEntry[1][1]()
					command = ""
			if command != "" and printout:
				self.printOut(value + '\n')
			return value
		else:
			for comEntry in self.commands:
				if command == comEntry[0]:
					self.addCommand(line)
					return comEntry[1][1]()
		
		self.printOut(command + ": " + self.lang["notfound"] + '\n')
		self.addCommand(line)
		return -1
	
	def addCommand(self, command):
		if len(self.sendCommands)>0:
			if self.sendCommands[len(self.sendCommands)-1] == command:
				return
		self.sendCommands.append(command)
		self.last = len(self.sendCommands) - 1
	
	def c_version(self):
		self.printOut("KadOS v2.3\n")
	
	def c_mkdir(self):
		params = self.line.split(' ')
		if len(params) == 2:
			self.files.makeDir(params[1])
			self.event_generate("<<files>>")
		else:
			self.printOut(self.lang["mkdir_invsyn"])
	
	def c_cd(self):
		params = self.line.split(' ')
		if len(params) == 2:
			dir = params[1]
			if not self.files.changeDir(dir):
				self.printOut(self.lang["cd_nodir"] + '\n')
			else:
				self.event_generate("<<files>>")
		else:
			self.printOut(self.lang["cd_invsyn"] + '\n')
		print self.files.curLoc

	def c_color(self):
		params = self.line.split(' ')
		if len(params) == 1:
			self.printOut(self.options.getOpts()["tcol"] + '\n')
		elif len(params) == 2:
			try:
				self.textColor(params[1])
				self.options.setOpts(tcol = params[1])
			except:
				self.printOut(self.lang["color_notfnd"].format(params[1]) + '\n')
		else:
			self.printOut(self.lang["color_invsyn"] + '\n')
	
	def c_lang(self):
		params = self.line.split(' ')
		if len(params) == 1:
			self.printOut(self.lang["lang_code"] + '\n')
		elif len(params) == 2:
			self.options.setOpts(lang = params[1])
			self.lang2 = params[1]
			self.event_generate("<<lang>>")
		else:
			self.printOut(self.lang["lang_invsyn"] + '\n')
		
	def c_whoami(self):
		self.printOut(self.userName + '\n')
		
	def c_whoareyou(self):
		self.printOut('\n')
	
	def c_alias(self):
		params = self.line.split(' ', 2)
		if len(params) == 2:
			if params[1] in self.aliases:
				del self.aliases[params[1]]
				self.event_generate("<<alias>>")
				self.printOut(params[1] + " " + self.lang["deleted"] + '\n')
				return
		if len(params) != 3:
			self.printOut(self.lang["alias_invsyn"] + '\n')
			return
		variable = params[1]
		for comEntry in self.commands:
			if comEntry[0] == variable:
				self.printOut(self.lang["alias_cantass"] + '\n')
				return
		value = params[2]
		self.aliases[variable] = value
		self.options.setOpts(aliases = self.aliases)
		self.event_generate("<<alias>>")
		self.printOut(self.lang["alias_setto"].format(variable, value) + '\n')

	def c_shutdown(self):
		self.event_generate("<<shut>>")
		self.destroy()

	def c_restart(self):
		self.state = const.states.restart
		self.event_generate("<<shut>>")
		self.destroy()

	def c_help(self):
		for comEntry in self.commands:
			self.printOut(comEntry[0] + ': ' + comEntry[1][0] + '\n')
	
	def c_clear(self):
		self.text = ""
		self.lineC = 0
		self.lineL = 0

		self.updateText()
	
	def getLastLine(self, clean=True):
		line = self.text
		if self.text.find('\n') == -1:
			line = self.text
		else:
			line = self.text[self.text.rfind('\n')+1:]
		
		if clean:
			if line.startswith(":>"):
				line = line[2:]
		if line.endswith('\n'):
			line = line[:-1]
		return line

	def autoComp(self, event=None):
		line = self.getLastLine()
		lineSplit = line.split(' ')
		if len(lineSplit) == 1:
			if line.startswith('./'):
				#file implement
				pass
			else:
				possibilities = []
				for comEntry in self.commands:
					if comEntry[0].startswith(line):
						possibilities.append(comEntry[0])
						
				for key in self.aliases:
					if key.startswith(line):
						possibilities.append(key)
						
				if len(possibilities) == 0:
					return
				if len(possibilities) == 1:
					self.printOut(possibilities[0][len(line):])
				else:
					self.printOut('\n')
					for poss in possibilities:
						self.printOut(poss + '\n')
					self.printOut(":>" + line)

	def getPrevCommand(self):
		if self.last >= 0:
			lcommand = self.sendCommands[self.last]
			self.last -= 1

			self.printOut("\r:>" + lcommand)
	
	def getNextCommand(self):
		if len(self.sendCommands) - 1 > self.last:
			self.last += 1
			lcommand = self.sendCommands[self.last]

			self.printOut("\r:>" + lcommand)
	
	def printOut(self, text):
		for c in text:
			if c=='\n':
				self.lineC += 1
				self.lineL = 0
				self.text += c
			elif c=='\b':
				if self.lineL > 0:
					self.lineL -= 1
					self.text = self.text[:-1]
			elif c=='\r':
				self.lineL = 0
				self.text = self.text[:self.text.rfind('\n')+1]
			else:
				self.lineL += 1
				self.text += c
			
			if self.lineL >= self.lw - 1:
				command = self.getLastLine(clean=False)
				self.text += '\n'
				self.lineL = 0
				self.lineC += 1
				if command.startswith(":>"):
					self.printOut(": " + self.lang["notfound"] + "\n:>")
				elif self.state == const.states.login:
					self.doCommand(command)

			if self.lineC >= self.th:
				self.lineC -= 1
				self.text = self.text[self.text.find('\n')+1:]

		self.updateText()
		
	def initialize(self):
		f = open(self.lang["initialize"])
		initText = f.read()
		f.close()

		initTime = self.initTime
		timepl = initTime/len(initText.split('\n'))

		for c in initText.split('\n'):
			if len(c) > 1:
				if not c.endswith('.'):
					self.printOut(c + '\n')
				else:
					self.printOut(c)
			threading._sleep(timepl)
		self.printOut('\b' + self.userName + '\n')
		
		self.event_generate("<<files>>")
		self.state = const.states.hack
		self.event_generate("<<alias>>")

		self.printOut(":>")

	def textColor(self, color):
		self.config(foreground=color)
		
	def login(self, userName, passWord):
		if self.options.checkSession(userName, passWord):
			self.event_generate("<<alias>>")
			self.printOut(self.lang["login_suc"] + "\n")
			opts = self.options.getOpts()
			self.textColor(opts["tcol"])
			self.lang2 = opts["lang"]
			self.state = const.states.init
			self.aliases = self.options.getOpts()["aliases"]
			self.event_generate("<<lang>>")
			threading.Thread(target=self.initialize).start()
		else:
			self.printOut(self.lang["login_inv"] + "\n")
			self.userName = ""
			self.passWord = ""
			self.printOut(self.lang["login"])

	def getParams(self):
		params = self.line.split(' ')
