import Tkinter
import tkFont
import os

class Explorer(Tkinter.Canvas):
	def __init__(self, mWindow, name, width, height, bgcolor, lang):
		Tkinter.Canvas.__init__(self, master=mWindow, background=bgcolor, width=width, height=height)

		self.height, self.width = height, width
		self.name = name
		self.bgcolor = bgcolor
		self.lang = lang

		self.config(highlightcolor="white")
		
		if os.name == "posix":
			self.font = tkFont.Font(family="Monospace", size=10, weight="normal")
		elif os.name == "nt":
			self.font = tkFont.Font(family="courier", size=8, weight="normal")
		cw = self.font.measure('A')
		ch = self.font.metrics("linespace")

		self.nameLabel = Tkinter.Label(self, text=self.lang[name], fg="green", bg=bgcolor, anchor=Tkinter.NW, justify=Tkinter.LEFT)
		self.nameLabel.config(width=self.width/cw, height=1, font=self.font, highlightthickness=0, bd=0)
		self.nameLabel.pack(side=Tkinter.TOP, fill=Tkinter.X, padx=3, pady=3)

		self.statusLabel = Tkinter.Label(self, fg="green", bg=bgcolor, anchor=Tkinter.SW, justify=Tkinter.LEFT)
		self.statusLabel.config(width=self.width/cw, text=self.lang[self.name + "_statusbar"])
		self.statusLabel.config(height=1, font=self.font, highlightthickness=0, bd=0)
		self.statusLabel.pack(side=Tkinter.BOTTOM, fill=Tkinter.X, padx=3, pady=3)

		if name == "aliases":
			self.initAliases()

	def initAliases(self):
		self.width = self.width / 3
		self.config(width = self.width)
		cw = self.font.measure('A')
		ch = self.font.metrics("linespace")
		self.aliasBar = Tkinter.Scrollbar(self)
		self.aliasBar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y, pady=10, padx=2)

		self.aliasBox = Tkinter.Listbox(self, background=self.bgcolor, foreground="green", width=self.width/cw, height=self.height/ch - 9)
		self.aliasBox.config(bd=0, relief=Tkinter.FLAT, font=self.font, yscrollcommand=(self.aliasBar, 'set'))
		self.aliasBox.config(selectforeground="green", selectbackground=self.bgcolor, activestyle="none", highlightthickness=0)
		self.aliasBox.pack(pady=8, padx=2, side=Tkinter.RIGHT, fill=Tkinter.X, expand=True, anchor=Tkinter.NW)

		self.aliasBar.config(command=(self.aliasBox, 'yview'))

	def loadLang(self, lang):
		self.lang = lang
		self.nameLabel.config(text=self.lang[self.name])
		self.statusLabel.config(text=self.lang[self.name + "_statusbar"])

	def updAlias(self, aliases):
		self.aliasBox.delete(0, Tkinter.END)
		for var in aliases:
			self.aliasBox.insert(Tkinter.END, var + ": " + aliases[var])

