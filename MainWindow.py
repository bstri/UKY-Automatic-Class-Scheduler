#!/usr/bin/env python
import tkinter as tk
from tkinter import N, E, S, W
ALL = N+E+S+W
from Async import AddAsync
from Entry import EntryLetters, EntryNumbers

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
		configureRows(self, [1, 3, 1])
		configureColumns(self, [1, 3, 1])
		self.CourseInputFrame = grid(CourseInputFrame(self), row=1, column=1, sticky=ALL)

def FrameWrap(self, cls):
	frame = tk.Frame(self, highlightthickness=1, highlightbackground="orange", highlightcolor="blue")
	grid(cls(frame))
	return frame

class CourseInputFrame(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master, borderwidth=2, relief="groove")
		AddAsync(self)
		# configureRows(self, [1, 3, 1])
		# configureColumns(self, [1, 3, 1])
		grid(tk.Label(self, text="Course Input"), sticky=W)
		holder = grid(tk.Frame(self)) #, highlightthickness=1, highlightbackground="red", highlightcolor="red"), sticky=E+W)
		configureColumns(holder, [3, 1, 3, 1, 3])
		self.coursePrefix = grid(EntryLetters(holder), row=0, column=0)
		self.courseNumber = grid(EntryNumbers(holder), row=0, column=2)
		self.sectionNumber = grid(EntryNumbers(holder), row=0, column=4) # TODO allow commas and spaces?
		#self.courseDisplay = grid(CourseDisplay(self), sticky=ALL)
		# TODO when user presses enter in any of the above Entries, call EnterPressed
	
	def EnterPressed(self):
		# See if coursePrefix/etc are in courseDisplay
		# See if coursePrefix/etc are in cache
		# Attempt to fetch data from website
		# Update courseDisplay as needed
		pass

class CourseDisplay(tk.Frame):
	pass

app = MainWindow()
app.mainloop()