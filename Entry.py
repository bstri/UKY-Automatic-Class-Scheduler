import tkinter as tk
class Entry(tk.Entry):
	"""An Entry with a .text property."""
	def __init__(self, *args, **kwargs):
		self.textVar = tk.StringVar()
		self.textVar.set(kwargs.pop("text", ""))
		kwargs["textvariable"] = self.textVar
		kwargs.setdefault("exportselection", False)
		super().__init__(*args, **kwargs)

	@property
	def text(self):
		return self.textVar.get()

	@text.setter
	def text(self, value):
		self.textVar.set(value)

class EntryValidate(Entry): #abstract
	def __init__(self, master, *args, **kwargs):
		kwargs["validate"] = "key"
		kwargs["validatecommand"] = (master.register(self.validate), "%P")
		super().__init__(master, *args, **kwargs)

class EntryLetters(EntryValidate):
	def validate(self, newText):
		return newText == "" or newText.isalpha()

class EntryNumbers(EntryValidate):
	def validate(self, newText):
		return newText == "" or newText.isdigit()
