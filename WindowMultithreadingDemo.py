#Backup of MainWindow when it was multithreading proof of concept

import tkinter as tk
from Async import AddAsync

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

class CourseInput(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master, highlightthickness=1, highlightbackground="orange", highlightcolor="green")
		label = grid(tk.Label(self, text="Course Input"))
		tk.Label(self, text="Test Input").grid()
		#label3 = grid(tk.Label(self, text="MoreTest"), row=0)
		prefixValue = tk.StringVar()
		self.prefixValue = prefixValue
		self.prefixInput = tk.Entry(self, textvariable=prefixValue)

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
		self.CourseInputFrame = grid(CourseInputFrame(self), row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

class CourseInputFrame(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master, highlightthickness=5, highlightbackground="red")
		AddAsync(self)
		self.createWidgets()

	def createWidgets(self):
		configureRows(self, [1, 3, 1])
		configureColumns(self, [1, 3, 1])
		self.courseInput = grid(CourseInput(self), row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
		grid(tk.Button(self, text='Quit', command=self.quit), row=2, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
		grid(tk.Button(self, text='Start Task', command=self.startTask), row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
		taskStatus = tk.StringVar()
		# TODO I cannot determine why the label increases in size when endTask is run
		obj = grid(tk.Label(self, textvariable=taskStatus, borderwidth=2, relief="groove"), row=2, column=1)
		taskStatus.set("Hi!")
		self.taskStatus = taskStatus
		self.i = 0

	def startTask(self):
		self.i += 1
		self.taskStatus.set("Start #" + str(self.i))
		self.NewTask(self.endTask, runTask, self.i)

	def endTask(self, result):
		self.taskStatus.set("End Msg: " + result)

import time
def runTask(i):
	time.sleep(2)
	return "Result (" + str(i) + "): " + str((i * i) % 1000)

app = MainWindow()
app.mainloop()