'''Adds async functionality to tkinter widgets.'''
import threading

def AddAsync(self):
	'''Add Async functionality to 'self', a tkinter object; adds NewTask and CancelCallbacks.

	Note: If you want to be able to kill the threads, you must pass some sort of state to each thread that enables you to tell the thread to cancel what it's doing.'''

	# Syntax note: "FunctionName.__get__(self)" binds 'FunctionName' to 'self'
	after = self.master.after
	inLoop = False
	asyncResults = [] # of AsyncResult (each with .Callback added)
	
	def NewTask(self, callback, func, *args, **kwargs):
		'''Add a new task. 'callback' is what to call with whatever 'func(*args, **kwargs)' returns.'''
		nonlocal inLoop, asyncResults
		new = AsyncResult(func, *args, **kwargs)
		new.Callback = callback
		asyncResults.append(new)
		start()
	self.NewTask = NewTask.__get__(self)
	
	def start():
		nonlocal inLoop
		if inLoop: # no need to restart loop
			return
		inLoop = True
		after(1, check)
	
	def check():
		nonlocal inLoop, asyncResults
		if not inLoop: #cancelled
			return
		newList = []
		for ar in asyncResults:
			if ar.ResultReady:
				ar.Callback(ar.Result)
			else:
				newList.append(ar)
		asyncResults = newList
		if len(asyncResults) == 0:
			inLoop = False
		if inLoop:
			after(1, check)

	def CancelCallbacks(self):
		nonlocal inLoop, asyncResults
		inLoop = False
		asyncResults = []
	self.CancelCallbacks = CancelCallbacks.__get__(self)

	return self

class AsyncResult:
	'''Runs a task asynchronously. Use .Result to get the returned value after .ResultReady becomes true.'''
	def __init__(self, func, *args, **kwargs):
		self.ResultReady = False
		self.Result = None
		self.Thread = threading.Thread(target=self.run, args=[func, *args], kwargs=kwargs)
		self.Thread.start()

	def run(self, func, *args, **kwargs):
		self.Result = func(*args, **kwargs)
		self.ResultReady = True