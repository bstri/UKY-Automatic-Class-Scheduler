import tkinter as tk
from tkinter import ttk

class Entry(ttk.Entry):
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
	'''Accepts only integers as input (no decimals or negatives).'''
	def __init__(self, *args, min=None, max=None, **kwargs):
		# Strategy is to allow any number in validation and then snap it to the min/max on FocusOut.
		self.min = min
		self.max = max
		self.minInput = None if min is None else 0
		self.maxInput = None if max is None else int("9" * len(str(max)))
		super().__init__(*args, **kwargs)
		self.bind("<FocusOut>", self.putInRange)

	def validate(self, newText):
		return newText == "" or (newText.isdigit() and self.inRange(int(newText)))

	def inRange(self, v):
		return (self.minInput is None or v >= self.minInput) and (self.maxInput is None or v <= self.maxInput)

	def putInRange(self, event):
		if self.text == "":
			if self.min:
				self.text = self.min
			elif self.max:
				self.text = self.max
			return
		v = int(self.text)
		if self.min and v < self.min:
			self.text = self.min
		elif self.max and v > self.max:
			self.text = self.max

import re
class EntryRange(EntryValidate):
	'''Allow entry of ranges, ex "0-10, 13, 15, 17-20"'''
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
