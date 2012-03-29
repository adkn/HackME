import Tkinter
import threading
import tkFont
import os
import const

class Shutdown(Tkinter.Label):
	def __init__(self, mWindow, width, height, bgcolor, lang, shutTime=2):
		Tkinter.Label.__init__(self, foreground="white", background=bgcolor, anchor=Tkinter.SW, justify=Tkinter.LEFT)

		if os.name == "posix":
			self.font = tkFont.Font(family="Monospace", size=10, weight="normal")
		elif os.name == "nt":
			self.font = tkFont.Font(family="courier", size=8, weight="normal")
		cw = self.font.measure('A')
		ch = self.font.metrics("linespace")
		self.th = height/ch
		self.lw = width/cw - 2

		self.lang = lang

		self.height, self.width = height, width
		self.state = const.states.hack

		self.shutTime = shutTime

		self.config(font=self.font, width=self.lw, height=self.th)

		self.text = ""
		self.lineL = 0
		self.lineC = 0

	def updateText(self):
		self.config(text=self.text)

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
			
			if self.lineL >= self.lw:
				self.text += '\n'
				self.lineL = 0
				self.lineC += 1

			if self.lineC >= self.th:
				self.lineC -= 1
				self.text = self.text[self.text.find('\n')+1:]

		self.updateText()
	
	def shutDown(self, restart=False):
		f = open(self.lang["shutdown"])
		shutText = f.read()
		f.close()

		self.text = ""
		self.updateText()

		height = self.height*3
		width = self.width*2
		cw = self.font.measure('A')
		ch = self.font.metrics("linespace")
		self.th = height/ch
		self.lw = width/cw
		self.config(foreground="white", height=self.th, width=self.lw)

		shutTime = self.shutTime #secs
		timepl = shutTime/len(shutText.split('\n'))

		for c in shutText.split('\n'):
			if len(c) > 1:
				if not c.endswith('.'):
					self.printOut(c + '\n')
				else:
					self.printOut(c)
			threading._sleep(timepl)

		if restart:
			self.state = const.states.restart
		else:
			self.state = const.states.shutdown
		self.event_generate("<<shut>>")
