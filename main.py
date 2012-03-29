import Tkinter
from Panels import *
import os
import threading

class HackMEWindow(Tkinter.Tk):
	def __init__(self, width=800, height=600, bgcolor="black"):
		Tkinter.Tk.__init__(self)
		self.title("HackME")
		if os.name == "posix":
			self.iconbitmap(bitmap="@./hackme.xbm")
		elif os.name == "nt":
			self.iconbitmap("./hackme.ico")
		self.bind_all("<Key>", self.eventHandler)
		self.bind_all("<Button>", self.eventHandler)
		self.bind_all("<<boot>>", self.eventHandler)
		self.bind_all("<<shut>>", self.shutDownHandler)
		self.bind_all("<<alias>>", self.eventHandler)
		self.config(bg=bgcolor)

		lang = "TR"
		self.loadLang(lang)
		
		#self.width, self.height = width, height
		self.width, self.height = self.winfo_screenwidth(), self.winfo_screenheight()

		self.bgcolor = bgcolor
		self.initView()

	def loadLang(self, lang):
		langs = []
		for dirpath, dirnames, filenames in os.walk("./Content"):
			for dir in dirnames:
				langs.append(dir)
		langDir = "./Content"
		if lang in langs:
			langDir = "./Content/" + lang

		langFile = langDir + "/templates.txt"
		f = open(langFile)
		langParams = f.read()
		f.close()

		exec("self.lang = " + langParams)
		self.lang["boot"] = langDir + "/boot.txt"
		self.lang["shutdown"] = langDir + "/shutDown.txt"
		self.lang["initialize"] = langDir + "/initialize.txt"
	
	def initView(self):
		bgcolor = self.bgcolor
		width, height = self.width, self.height
		if os.name == "nt":
			self.wm_attributes("-fullscreen", 1)

		self.focus_set()

		bootTime = 3.0
		shutTime = 1.0

		self.boot = boot.Boot(self, width, height, bgcolor, self.lang, bootTime=bootTime)
		self.boot.pack(fill=Tkinter.BOTH, expand=True)

		self.shut = shutdown.Shutdown(self, width, height, bgcolor, self.lang, shutTime=shutTime)
		
		self.explorerFrame = Tkinter.Frame(self, width=width, height=height/3*2)
		self.explorerFrame.pack(fill=Tkinter.BOTH, side=Tkinter.TOP, expand=True)

		explorerNames = ["fileexplorer", "texteditor", "aliases"]
		self.explorers = []

		for i in range(3):
			self.explorers.append(explorer.Explorer(self.explorerFrame, explorerNames[i], width/3, height/3*2, bgcolor, self.lang))
			self.explorers[i].pack(fill=Tkinter.BOTH, side=Tkinter.LEFT, expand=True)
		
		self.terminalFrame = Tkinter.Frame(self)
		self.terminalFrame.pack(side=Tkinter.BOTTOM, fill=Tkinter.BOTH, expand=True)

		self.terminal1 = terminal.Terminal(self.terminalFrame, width/2, height/3, bgcolor, self.lang, shutTime=shutTime)
		self.terminal1.pack(fill=Tkinter.BOTH, side=Tkinter.LEFT, expand=True)
		self.bind_all("<Tab>", self.terminal1.autoComp)
		
		self.terminal2 = terminal.Terminal(self.terminalFrame, width/2, height/3, bgcolor, self.lang)
		self.terminal2.pack(fill=Tkinter.BOTH, side=Tkinter.LEFT, expand=True)

	def shutDownHandler(self, event=None):
		if self.shut.state == const.states.hack:
			for i in range(3):
				self.explorers[i].destroy()
			self.explorerFrame.destroy()
			self.terminal2.destroy()
			self.terminalFrame.destroy()

			self.shut.pack(fill=Tkinter.BOTH, expand=True)
			if self.terminal1.state == const.states.restart:
				threading.Thread(target=self.shut.shutDown, args=(True,)).start()
			else:
				threading.Thread(target=self.shut.shutDown).start()
		elif self.shut.state == const.states.shutdown:
			del self.terminal1
			del self.terminal2
			del self.terminalFrame
			for i in range(3):
				del self.explorers[0]
			del self.explorerFrame

			self.destroy()
			self.quit()
		elif self.shut.state == const.states.restart:
			self.shut.destroy()
			self.initView()		

	def eventHandler(self, event=None):
		if event.type == "2":
			self.terminal1.keyPressed(event)
			self.terminal2.keyPressed(event)
		elif event.type == "35":
			if self.terminal1.state == const.states.boot:
				self.boot.destroy()
				self.terminal1.printOut(self.lang["login"])
				self.terminal1.state = const.states.login
			elif self.terminal1.state == const.states.hack:
				self.explorers[2].updAlias(self.terminal1.aliases)
		
		#for key in event.__dict__:
		#	print key, ':', event.__dict__[key]

def main():
	width, height = 1024, 768
	mWindow = HackMEWindow()
	mWindow.mainloop()

if __name__ == "__main__":
	if os.name == "nt" or os.name == "posix":
		main()
