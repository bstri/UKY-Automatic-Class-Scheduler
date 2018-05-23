import tkinter as tk
class Entry(tk.Entry):
	'''An Entry with a .text property.'''
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

import re
class EntryRange(EntryValidate):
	pattern = re.compile(r"(\d+)(?: *\- *(\d+))?[, -]*")
	def __init__(self, *args, maxNum=1000, **kwargs):
		super().__init__(*args, **kwargs)
		self.maxNum = maxNum

	def validate(self, newText):
		return not any(not (c.isdigit() or c == '-' or c == ',' or c == ' ') for c in newText)
	
	def GetRange(self):
		'''Get a list representing the range input to 'validate'. Can throw ValueError if the user has input too large of a number.'''
		r = set()
		t = self.text
		pattern = EntryRange.pattern
		def toInt(i):
			i = int(i)
			if i > self.maxNum:
				raise ValueError("integer too large: '{}' > {}".format(i, self.maxNum), i)
			elif i < 0:
				raise ValueError("integer smaller than zero: '{}'".format(i), i)
			return i
		while len(t) > 0:
			match = pattern.match(t)
			if not match:
				break
			if match.group(2): # range
				r.update(range(toInt(match.group(1)), toInt(match.group(2)) + 1))
			else:
				r.add(toInt(match.group(1)))
			t = t[match.span()[1]:]
		return sorted(r)
