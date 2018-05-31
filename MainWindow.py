#!/usr/bin/env python
import tkinter as tk
from tkinter import ttk
from tkinter import N, E, S, W
ALL = N+E+S+W
from Async import AddAsync
from Entry import EntryLetters, EntryNumbers, EntryRange
# from ConfigurationData import ConfigurationData
# from WebsiteInterface import WebsiteInterface

_basePrint = print
def print(*args, **kwargs):
	kwargs["flush"] = True
	_basePrint(*args, **kwargs)

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
		self.rowconfigure(0, weight=1, pad=2)
		self.columnconfigure(0, weight=1, pad=2)
		# configureRows(self, [1, 98, 1])
		# configureColumns(self, [1, 98, 1])
		self.CourseInputFrame = grid(CourseInputFrame(self), row=0, column=0, sticky=ALL)
		center(self)

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

class MultiMessageStringVarHideEmpty(MultiMessageStringVar):
	'''Hides specified widget (assign using SetWidget *after* all other layout done) when text is empty.'''

	def __init__(self, *args, **kwargs):
		self.widget = None
		super().__init__(*args, **kwargs)

	def SetWidget(self, widget):
		# Allowing for widget to change not implemented
		self.widget = widget
		self.updateGrid()

	def update(self):
		super().update()
		if not self.widget:
			return
		self.updateGrid()

	def updateGrid(self):
		if len(self.Var.get()) == 0:
			self.widget.grid_remove()
		else:
			self.widget.grid()

class Row:
	'''Help put widgets in a single row'''
	def __init__(self):
		self.column = -1

	def Reset(self):
		self.column = -1

	def Add(self, obj, **kwargs):
		'''Add 'obj' to the row. Returns 'obj' for convenience. You can specify additional keyword arguments to be sent to columnconfigure.

		Note that if you send in padx/pady, those will be directed to the 'grid' command.'''
		self.column = self.column + 1
		grid = {}
		for x in {"padx", "pady"}:
			if x in kwargs:
				grid[x] = kwargs.pop(x)
		obj.grid(row=0, column=self.column, **grid)
		if kwargs:
			obj.columnconfigure(self.column, **kwargs)
		return obj

class CourseInputFrame(tk.Frame):
	'''Enables the user to input their desired courses (and related information).'''
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
		
		padx = 5
		_row = Row()
		def newRow():
			'''Signify a new row (must also use a new frame/holder for the new row)'''
			nonlocal _row
			_row.Reset()
		def add(obj, *args, **kwargs):
			'''Add to the current row'''
			nonlocal _row
			_row.Add(obj, *args, **kwargs)
			return obj
		def addp(obj, *args, **kwargs):
			'''Add to the current row, with default padding'''
			nonlocal _row, padx
			kwargs.setdefault("padx", padx)
			_row.Add(obj, *args, **kwargs)
			return obj
		
		newRow()
		holder = grid(tk.Frame(self), sticky=E+W)
		add(tk.Label(holder, text="Select Term:"))
		self.Term = tk.StringVar()
		self.Term.set("Fall") # TODO use: WebsiteInterface.GetDefaultSemester())
		addp(ttk.OptionMenu(holder, self.Term, None, "Fall", "Winter", "Spring"))
		self.Year = tk.StringVar()
		self.Year.set("2018") # TODO use: WebsiteInterface.GetDefaultYear())
		addp(ttk.OptionMenu(holder, self.Year, None, 2018, 2019, 2020)) # todo use next line (GetValidYears maybe just is curYear -> curYear+3)
		#addp(ttk.OptionMenu(holder, self.Year, None, *WebsiteInterface.GetValidYears()))
		
		newRow()
		holder = grid(tk.Frame(self))
		add(tk.Label(holder, text="Course Input:"))
		def bind(obj):
			obj.bind("<Return>", self.enterPressed)
			return obj
		self.coursePrefix = bind(addp(EntryLetters(holder, width=8)))
		self.courseNumber = bind(addp(EntryNumbers(holder, width=8)))
		self.sectionNumbers = bind(addp(EntryRange(holder, width=8)))
		self.mandatoryInt = tk.IntVar()
		self.mandatoryInt.set(0)
		self.mandatoryButton = addp(tk.Checkbutton(holder, text="Mandatory", var=self.mandatoryInt))
		add(tk.Button(holder, text="Enter", command=lambda:self.enterPressed(None)))

		self.errorMessages = MultiMessageStringVarHideEmpty()
		self.errorMessagesLabel = grid(tk.Label(self, textvariable=self.errorMessages.Var, fg="red", justify="left"), sticky=W)
		self.rowconfigure(2, minsize=5)

		self.courseDisplay = grid(CourseDisplay(self, height=20, highlightbackground="grey", highlightthickness=1, highlightcolor="grey"), sticky=E+W)

		self.rowconfigure(4, minsize=5)

		newRow()
		holder = grid(tk.Frame(self), row=5)
		add(ttk.Button(holder, text="Make", command=self.schedule))
		add(tk.Label(holder, text="schedules with"))
		#todo replace: text=WebsiteInterface.MinCreditDefault, min=ConfigurationData.HardCreditMinimum, max=ConfigurationData.HardCreditMaximum, default=WebsiteInterface.MinCreditDefault
		self.minCredits = add(EntryNumbers(holder, width=2, text=12, min=1, max=30, default=12))
		add(tk.Label(holder, text="-"))
		#todo replace: text=WebsiteInterface.MinCreditDefault, min=ConfigurationData.HardCreditMinimum, max=ConfigurationData.HardCreditMaximum, default=WebsiteInterface.MaxCreditDefault
		self.maxCredits = add(EntryNumbers(holder, width=2, text=18, min=1, max=30, default=18))
		add(tk.Label(holder, text="credits"))

		# The following must be done after all other layout finished
		self.errorMessages.SetWidget(self.errorMessagesLabel)

	def isMandatory(self):
		return self.mandatoryInt.get() == 1

	def schedule(self):
		# todo verify no problems with data
		# data = ConfigurationData(self.Term.get(), self.Year.get(), minCredits=None, maxCredits=None)
		# msg = data.FindProblems()
		# if msg:
		#	self.errorMessages.Set(self.)
		if self.inputErrorsExist():
			# todo maybe flash the error messages? (ex make it bold for a moment)
			return
		# todo wait for all HTML info to come in
		# todo send information to scheduler
		print(self.Term.get(), self.Year.get(), self.minCredits.get(), self.maxCredits.get())


	def clearInput(self):
		self.coursePrefix.text = ""
		self.courseNumber.text = ""
		self.sectionNumbers.text = ""
		self.mandatoryInt.set(0)

	def inputErrorsExist(self):
		for error in self.INPUT_ERRORS:
			if self.errorMessages.Get(error):
				return True
		return False

	def clearInputErrors(self):
		for error in self.INPUT_ERRORS:
			self.errorMessages.Remove(error)

	def allInputClear(self):
		return not self.coursePrefix.text and not self.courseNumber.text and not self.sectionNumbers.text and not self.isMandatory()

	def enterPressed(self, event):
		self.clearInputErrors()
		if self.allInputClear():
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