import Tkinter

class Explorer(Tkinter.Canvas):
	def __init__(self, mWindow, name, width, height, bgcolor):
		Tkinter.Canvas.__init__(self, master=mWindow, background=bgcolor, width=width, height=height)

		self.height, self.width = height, width
		self.name = name
		self.bgcolor = bgcolor

		self.config(highlightcolor="white")

		self.nameLabel = Tkinter.Label(self, text=name, fg="green", bg=bgcolor, anchor=Tkinter.NW, justify=Tkinter.LEFT)
		self.nameLabel.config(width=self.width/7, height=1, font=("courier",  8, "normal"), highlightthickness=0, bd=0)
		self.nameLabel.pack(side=Tkinter.TOP, fill=Tkinter.X, padx=3, pady=3)

		self.statusLabel = Tkinter.Label(self, text=name + " statusbar", fg="green", bg=bgcolor, anchor=Tkinter.SW, justify=Tkinter.LEFT)
		self.statusLabel.config(width=self.width/7, height=1, font=("courier",  8, "normal"), highlightthickness=0, bd=0)
		self.statusLabel.pack(side=Tkinter.BOTTOM, fill=Tkinter.X, padx=3, pady=3)

		if name.lower() == "aliases":
			self.initAliases()

	def initAliases(self):
		self.aliasBar = Tkinter.Scrollbar(self)
		self.aliasBar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y, pady=10, padx=2)

		self.aliasBox = Tkinter.Listbox(self, background=self.bgcolor, foreground="green", width=self.width, height=self.height/13 - 9)
		self.aliasBox.config(bd=0, relief=Tkinter.FLAT, font=("courier",  8, "normal"), yscrollcommand=(self.aliasBar, 'set'))
		self.aliasBox.config(selectforeground="green", selectbackground=self.bgcolor, activestyle="none", highlightthickness=0)
		self.aliasBox.pack(pady=8, padx=2, side=Tkinter.RIGHT, fill=Tkinter.X)

		self.aliasBar.config(command=(self.aliasBox, 'yview'))

	def updAlias(self, aliases):
		self.aliasBox.delete(0, Tkinter.END)
		for var in aliases:
			self.aliasBox.insert(Tkinter.END, var + ": " + aliases[var])
