import tkinter as tk
from tkinter import ttk

_basePrint = print
def print(*args, **kwargs):
	kwargs["flush"] = True
	_basePrint(*args, **kwargs)

class Entry(tk.Entry):
	'''An Entry with a .text property. Also supports "placeholderText".'''

	# Note: For the sake of EntryValidate, never use self.textVar.set -- use self.text = "" instead; otherwise, validation may permanently break for this object.
	def __init__(self, *args, placeholderText=None, placeholderColor="grey", **kwargs):
		self.textVar = tk.StringVar()
		self.textVar.set(kwargs.pop("text", ""))
		self.placeholderText = placeholderText
		self.placeholderColor = placeholderColor

		kwargs["textvariable"] = self.textVar
		kwargs.setdefault("exportselection", False)
		super().__init__(*args, **kwargs)
		self.activeColor = self.cget("fg")

		self.bind("<FocusIn>", self.focusIn)
		self.bind("<FocusOut>", self.focusOut)

		if self.textVar.get() == "":
			self.text = ""

	def isPlaceholderActive(self):
		return self.placeholderText and self.cget("fg") == self.placeholderColor

	def activatePlaceholder(self):
		if self.placeholderText:
			self.config(fg=self.placeholderColor)
			self.textVar.set(self.placeholderText)

	def deactivatePlaceholder(self):
		if self.placeholderText:
			self.config(fg=self.activeColor)

	def get(self):
		return "" if self.isPlaceholderActive() else super().get()

	@property
	def text(self):
		return "" if self.isPlaceholderActive() else self.textVar.get()

	@text.setter
	def text(self, value):
		if self.placeholderText:
			if value == "":
				self.activatePlaceholder()
			else:
				self.deactivatePlaceholder()
				self.textVar.set(value)
		else:
			self.textVar.set(value)

	def focusIn(self, event):
		if self.isPlaceholderActive():
			self.textVar.set("")
			self.deactivatePlaceholder()

	def focusOut(self, event):
		if self.placeholderText and self.cget("fg") == self.activeColor and self.textVar.get() == "":
			self.activatePlaceholder()

class EntryValidate(Entry): #abstract
	def __init__(self, master, *args, **kwargs):
		kwargs["validate"] = "key"
		kwargs["validatecommand"] = (master.register(self._validate), "%P")
		self.alwaysReturnTrue = False
		super().__init__(master, *args, **kwargs)

	@Entry.text.setter
	def text(self, value):
		self.alwaysReturnTrue = True
		Entry.text.fset(self, value)
		self.alwaysReturnTrue = False

	def _validate(self, newText):
		if self.alwaysReturnTrue:
			return True
		return self.validate(newText)

class EntryLetters(EntryValidate):
	def validate(self, newText):
		print("letters validate:", repr(newText))
		return newText == "" or newText.isalpha()

class EntryNumbers(EntryValidate):
	'''Accepts only integers as input (no decimals or negatives).'''
	def __init__(self, *args, min=None, max=None, default=None, **kwargs):
		# Strategy is to allow any number in validation and then snap it to the min/max on FocusOut.
		self.min = min
		self.max = max
		self.minInput = None if min is None else 0
		self.maxInput = None if max is None else int("9" * len(str(max)))
		self.default = default
		super().__init__(*args, **kwargs)

	def validate(self, newText):
		print("n validate:", repr(newText))
		return newText == "" or (newText.isdigit() and self.inRange(int(newText)))

	def inRange(self, v):
		return (self.minInput is None or v >= self.minInput) and (self.maxInput is None or v <= self.maxInput)

	def focusOut(self, event):
		super().focusOut(event)
		self.putInRange()

	def putInRange(self):
		if self.text == "":
			if self.default:
				self.text = self.default
			elif self.min:
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
