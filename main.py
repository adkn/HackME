import Tkinter
from Panels import *
import os
import threading

class HackMEWindow(Tkinter.Tk):
	def __init__(self, width=800, height=600, bgcolor="black"):
		Tkinter.Tk.__init__(self)
		self.title("HackME")
		try:
			self.iconbitmap("./hackme.ico")
		except:
			self.iconbitmap(bitmap="@./hackme.xbm")
		self.bind_all("<Key>", self.eventHandler)
		self.bind_all("<Button>", self.eventHandler)
		self.bind_all("<<boot>>", self.eventHandler)
		self.bind_all("<<shut>>", self.eventHandler)
		self.bind_all("<<alias>>", self.eventHandler)
		self.config(bg=bgcolor)
		
		#self.width, self.height = width, height
		self.width, self.height = self.winfo_screenwidth(), self.winfo_screenheight()

		self.bgcolor = bgcolor
		self.initView()
	
	def initView(self):
		bgcolor = self.bgcolor
		width, height = self.width, self.height
		if os.name == "nt":
			self.overrideredirect(True)
		self.geometry(str(self.width)+"x"+str(self.height)+"+0+0")
		self.focus_set()

		bootTime = 4.0
		shutTime = 2.0

		self.boot = boot.Boot(self, width, height, bgcolor, bootTime=bootTime)
		self.boot.pack(fill=Tkinter.BOTH, expand=True)
		
		self.explorerFrame = Tkinter.Frame(self, width=width, height=height/3*2)
		self.explorerFrame.pack(fill=Tkinter.BOTH, side=Tkinter.TOP, expand=True)

		explorerNames = ["File Explorer", "Text Editor", "Aliases"]
		self.explorers = []

		for i in range(3):
			self.explorers.append(explorer.Explorer(self.explorerFrame, explorerNames[i], width/3, height/3*2, bgcolor))
			self.explorers[i].pack(fill=Tkinter.BOTH, side=Tkinter.LEFT, expand=True)
		
		self.terminalFrame = Tkinter.Frame(self)
		self.terminalFrame.pack(side=Tkinter.BOTTOM, fill=Tkinter.BOTH, expand=True)

		self.terminal1 = terminal.Terminal(self.terminalFrame, width/2, height/3, bgcolor, shutTime=shutTime)
		self.terminal1.pack(fill=Tkinter.BOTH, side=Tkinter.LEFT, expand=True)
		self.bind_all("<Tab>", self.terminal1.autoComp)
		
		self.terminal2 = terminal.Terminal(self.terminalFrame, width/2, height/3, bgcolor)
		self.terminal2.pack(fill=Tkinter.BOTH, side=Tkinter.LEFT, expand=True)

	def eventHandler(self, event=None):
		if event.type == "2":
			self.terminal1.keyPressed(event)
			self.terminal2.keyPressed(event)
		elif event.type == "35":
			if self.terminal1.state == const.states.boot:
				self.boot.destroy()
				self.terminal1.printOut("Login: ")
				self.terminal1.state = const.states.login
			elif self.terminal1.state == const.states.shutdown1:
				for i in range(3):
					self.explorers[i].destroy()
				self.explorerFrame.destroy()
			elif self.terminal1.state == const.states.shutdown2:
				self.terminal2.destroy()
				self.terminal1.destroy()
				self.terminalFrame.destroy()
				self.destroy()

				self.quit()
			elif self.terminal1.state == const.states.restart1:
				for i in range(3):
					self.explorers[i].destroy()
				self.explorerFrame.destroy()
				
				self.terminal1.config(highlightthickness=0, bd=0)
				self.terminal2.config(highlightthickness=0, bd=0)
				self.terminalFrame.config(highlightthickness=0, bd=0)
			elif self.terminal1.state == const.states.restart2:
				self.terminal2.destroy()
				self.terminal1.destroy()
				self.terminalFrame.destroy()

				self.initView()
			elif self.terminal1.state == const.states.hack:
				self.explorers[2].updAlias(self.terminal1.aliases)
		
		#for key in event.__dict__:
		#	print key, ':', event.__dict__[key]

def main():
	width, height = 1024, 768
	mWindow = HackMEWindow()
	mWindow.mainloop()

if __name__ == "__main__":
	main()
