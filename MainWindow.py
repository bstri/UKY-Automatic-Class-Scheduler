#!/usr/bin/env python
import tkinter as tk
from tkinter import N, E, S, W
ALL = N+E+S+W
from Async import AddAsync
from Entry import EntryLetters, EntryNumbers, EntryRange
# from WebsiteInterface import WebsiteInterface

_basePrint = print
def print(*args):
	import sys
	_basePrint(*args)
	sys.stdout.flush()

def center(toplevel):
	toplevel.update_idletasks()
	w = toplevel.winfo_screenwidth()
	h = toplevel.winfo_screenheight()
	size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
	x = w/2 - size[0]/2
	y = h/2 - size[1]/2
	toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

# todo see https://stackoverflow.com/questions/31918073/tkinter-how-to-set-font-for-text for idea of sharing font so resize can be done

def grid(obj, *args, **kwargs):
	obj.grid(*args, **kwargs)
	return obj

def configureWeights(func, weights):
	for i, weight in enumerate(weights):
		func(i, weight=weight)

def configureRows(obj, weights):
	configureWeights(obj.rowconfigure, weights)

def configureColumns(obj, weights):
	configureWeights(obj.columnconfigure, weights)

class MainWindow(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("UKY Class Scheduler")
		self.geometry("600x400")
		center(self)
		self.rowconfigure(0, weight=1, pad=2)
		self.columnconfigure(0, weight=1, pad=2)
		# configureRows(self, [1, 98, 1])
		# configureColumns(self, [1, 98, 1])
		self.CourseInputFrame = grid(CourseInputFrame(self), row=0, column=0, sticky=ALL)

class MultiMessageStringVar():
	'''Enable multiple independent messages to be contained within a single StringVar (named .Var).

	Throughout this class, 'line' is a number. Line numbers do not need to be consecutive (or even integers).'''
	def __init__(self, stringVar=None, delimiter="\n"):
		self.lines = {}
		self.Var = stringVar or tk.StringVar()
		self.delimiter = delimiter

	def Get(self, line):
		return self.lines.get(line)

	def GetAll(self):
		return self.Var.get()

	def update(self):
		self.Var.set("\n".join(map(lambda n: self.lines[n], sorted(self.lines))))
	
	def Set(self, line, text):
		if text:
			self.lines[line] = text
		else:
			self.lines.pop(line, None)
		self.update()

	def Remove(self, line):
		self.lines.pop(line, None)
		self.update()

	def Clear(self):
		self.lines = {}
		self.update()

def standardConfigure(obj, width, height):
	for w in range(width):
		obj.rowconfigure(w, weight=1)
	for h in range(height):
		obj.columnconfigure(w, weight=1)

class CourseInputFrame(tk.Frame):
	# The following are line numbers for the MultiMessageStringVar class
	INPUT_ERROR_PREFIX = 1
	INPUT_ERROR_NUMBER = 2
	INPUT_ERROR_SECTIONS = 3
	INPUT_ERROR_GENERAL = 4
	INPUT_ERRORS = [INPUT_ERROR_PREFIX, INPUT_ERROR_NUMBER, INPUT_ERROR_SECTIONS, INPUT_ERROR_GENERAL]
	WEB_ERROR = 5
	def __init__(self, master=None):
		super().__init__(master, borderwidth=2, relief="groove")
		AddAsync(self)
		holder = grid(tk.Frame(self, highlightthickness=1, highlightbackground="red", highlightcolor="red"), sticky=E+W)
		standardConfigure(holder, 2, 2)
		grid(tk.Label(holder, text="Select Term"), sticky=W+E)
		self.Term = tk.StringVar()
		self.Term.set("Fall") # TODO use: WebsiteInterface.GetDefaultSemester())
		grid(tk.OptionMenu(holder, self.Term, "Fall", "Winter", "Spring"), row=0, column=1)
		self.Year = grid(EntryNumbers(holder), row=0, column=2)
		self.Year.bind("<Return>", lambda obj: self.master.focus())
		grid(tk.Label(self, text="Course Input"), sticky=W)
		holder = grid(tk.Frame(self)) #, highlightthickness=1, highlightbackground="red", highlightcolor="red"), sticky=E+W)
		#configureColumns(holder, [3, 1, 3, 1, 3]) # Note: This line doesn't do anything; instead, dummy labels are added below to force spacing
		def bind(obj):
			obj.bind("<Return>", self.EnterPressed)
			return obj
		self.coursePrefix = bind(grid(EntryLetters(holder), row=0, column=0))
		grid(tk.Label(holder, text = "  "), row=0, column=1)
		self.courseNumber = bind(grid(EntryNumbers(holder), row=0, column=2))
		grid(tk.Label(holder, text = "  "), row=0, column=3)
		self.sectionNumbers = bind(grid(EntryRange(holder), row=0, column=4))
		self.errorMessages = MultiMessageStringVar()
		grid(tk.Label(self, textvariable=self.errorMessages.Var, fg="red"), sticky=W)
		#self.courseDisplay = grid(CourseDisplay(self), sticky=ALL)

	def clearInput(self):
		self.coursePrefix.text = ""
		self.courseNumber.text = ""
		self.sectionNumbers.text = ""

	def clearInputErrors(self):
		for error in self.INPUT_ERRORS:
			self.errorMessages.Remove(error)

	def EnterPressed(self, event):
		self.clearInputErrors()
		if not self.coursePrefix.text and not self.courseNumber.text and not self.sectionNumbers.text:
			# All textboxes clear, so:
			self.master.focus()
			return
		# Ensure input coursePrefix/number textboxes have values and sectionNumbers are OK
		errorSource = None
		if not self.coursePrefix.text:
			self.errorMessages.Set(self.INPUT_ERROR_PREFIX, "You must enter a course prefix")
			errorSource = self.coursePrefix
		if not self.courseNumber.text:
			self.errorMessages.Set(self.INPUT_ERROR_NUMBER, "Course Prefix must have a value")
			errorSource = errorSource or self.courseNumber
		try:
			sections = self.sectionNumbers.GetRange()
		except ValueError as e:
			num = e.args[1]
			if num < 0:
				self.errorMessages.Set(self.INPUT_ERROR_SECTIONS, "Section numbers cannot be negative (input: {})".format(num))
			else:
				self.errorMessages.Set(self.INPUT_ERROR_SECTIONS, "Section number '{}' is too large".format(num))
			errorSource = errorSource or self.sectionNumbers
		if errorSource:
			errorSource.focus()
			return
		# See if coursePrefix/etc are in courseDisplay
		# See if coursePrefix/etc are in cache
		# If anything went wrong, set INPUT_ERROR_GENERAL. Otherwise, clear all inputs and input errors
		# Attempt to fetch data from website and update either courseDisplay or errorMessage.

class CourseDisplay(tk.Frame):
	pass

app = MainWindow()
app.mainloop()