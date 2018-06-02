from tkinter import *
from tkinter import ttk # themed widgets (more up-to-date looking)

class checkbar(Frame):
	def __init__(self, parent, picks, cmd, checked=False):
		super().__init__(parent)
		self.vars = []
		for i,pick in enumerate(picks):
			var = BooleanVar()
			chk = ttk.Checkbutton(self, text=pick, variable=var, command=lambda index=i,v=var: cmd(index, v.get()), padding=(0,0,10,0))
			chk.grid(row=1, column=i+1)
			self.vars.append(var)
			var.set(checked)
	def state(self):
		return map((lambda var: var.get()), self.vars)
		
class scheduleInfoFrame(Frame):
	'''A frame containing basic schedule info'''
	
	def __init__(self, parent):
		super().__init__(parent, bd=1)
		self.CreditLabel = ttk.Label(self)
		self.CreditLabel.grid(row=1, column=1, sticky='n')
		self.columnconfigure(1, weight=1, pad=25)
		self.StartTimeLabel = ttk.Label(self)
		self.StartTimeLabel.grid(row=1, column=2, sticky='n')
		self.columnconfigure(2, weight=1)
		self.EndTimeLabel = ttk.Label(self)
		self.EndTimeLabel.grid(row=1, column=3, sticky='n')
		self.columnconfigure(3, weight=1)
		self.Schedule = None
		self.bind('<Enter>', self.onEnter)
		self.bind('<Leave>', self.onLeave)
	
	def onEnter(self, e):
		self['relief'] = 'solid'
		print(self.Schedule)
	
	def onLeave(self, e):
		self['relief'] = 'flat'
		
	def SetSchedule(self, schedule):
		self.Schedule = schedule
		self.CreditLabel['text'] = str(schedule.NumCredits)
		self.StartTimeLabel['text'] = schedule.EarliestStartTimeToStr
		self.EndTimeLabel['text'] = schedule.LatestEndTimeToStr
		self.grid()
		
	def ClearSchedule(self):
		self.grid_remove()
		
class scheduleInfoList(Frame):
	'''A frame containing rows of scheduleInfoFrames'''
	
	def __init__(self, parent, maxListLen):
		super().__init__(parent)
		ttk.Label(self, text='# Credits').grid(column=1, row=1, padx=(0,6))
		ttk.Label(self, text='Start Time').grid(column=2, row=1, padx=6)
		ttk.Label(self, text='End Time').grid(column=3, row=1, padx=6)
		self.scheduleFrames = []
		self.maxRows = maxListLen
		for i in range(maxListLen):
			f = scheduleInfoFrame(self)
			f.grid(row=2+i, column=1, columnspan=3, pady=3, sticky='ew')
			self.scheduleFrames.append(f)
		
	def SetSchedules(self, schedules):
		for i,s in enumerate(schedules):
			self.scheduleFrames[i].SetSchedule(s)
		for i in range(len(schedules), self.maxRows):
			self.scheduleFrames[i].ClearSchedule()

class ScheduleViewer(Tk):
	''''''
	
	scheduleColumns = 2
	schedulesPerColumn = 20
	schedulesPerPage = scheduleColumns*schedulesPerColumn
	
	def __init__(self, scheduleList=[], courseList=[]):
		super().__init__()
		self.title("Schedule Viewer")
		self.geometry("1200x700")
		self.ScheduleList = scheduleList
		self.ActiveSchedules = scheduleList[:]
		self.courseList = courseList
		self.excludedCourses = []
		self.attributeFilters = {}
		
		filterFrame = Frame(self)
		filterFrame.grid(column=1, row=1, sticky='new')
		self.columnconfigure(1, weight=1)
		
		ttk.Label(filterFrame, text="Courses: ").grid(row=1, column=1, sticky='e', pady=3)
		checkbar(filterFrame, map(str, self.courseList), self.changeCourse, True).grid(row=1, column=2, sticky='w')
		
		ttk.Label(filterFrame, text="Start Times: ").grid(row=2, column=1, sticky='e', pady=3)
		self.startTimes = self.getScheduleAttributeList("EarliestStartTimeToStr")
		checkbar(filterFrame, self.startTimes, self.changeStartTime, True).grid(row=2, column=2, sticky='w')
		
		ttk.Label(filterFrame, text="End Times: ").grid(row=3, column=1, sticky='e', pady=3)
		self.endTimes = self.getScheduleAttributeList("LatestEndTimeToStr")
		checkbar(filterFrame, self.endTimes, self.changeEndTime, True).grid(row=3, column=2, sticky='w')
		
		ttk.Label(filterFrame, text="Credits: ").grid(row=4, column=1, sticky='e', pady=3)
		self.creditNums = self.getScheduleAttributeList("NumCredits")
		checkbar(filterFrame, map(str, self.creditNums), self.changeNumCredits, True).grid(row=4, column=2, sticky='w')
		
		self.scheduleCount = ttk.Label(self)
		self.scheduleCount.grid(row=2, column=1, sticky='w', pady=(20,10))
		
		scheduleFrame = Frame(self)
		scheduleFrame.grid(row=3, column=1, sticky='nesw')
		self.scheduleInfoLists = []
		for i in range(self.scheduleColumns):
			s = scheduleInfoList(scheduleFrame, self.schedulesPerColumn)
			s.grid(row=1, column=i+1, padx=15, sticky='n')
			self.scheduleInfoLists.append(s)
		
		self.updateScheduleView()
		self.mainloop()
		
	def updateScheduleCount(self):
		self.scheduleCount['text'] = 'Showing %d of %d schedules found' % (min(self.schedulesPerPage, len(self.ActiveSchedules)), len(self.ActiveSchedules))
		
	def getScheduleAttributeList(self, attr):
		l = {getattr(s, attr) for s in self.ScheduleList}
		self.attributeFilters[attr] = l
		return sorted(list(l))
	
	def updateScheduleView(self):
		for i in range(self.scheduleColumns):
			start = i*self.schedulesPerColumn
			self.scheduleInfoLists[i].SetSchedules(self.ActiveSchedules[start:start + self.schedulesPerColumn])
		self.updateScheduleCount()
	
	def updateActiveSchedules(self):
		self.ActiveSchedules[:] = [s for s in self.ScheduleList if all(getattr(s,a) in vals for a,vals in self.attributeFilters.items()) and not any(sect for sect in s.Sections if sect.Course in self.excludedCourses)] # I love comprehensions
		self.updateScheduleView()
	
	def changeAttribute(self, adding, attr, value):
		if adding:
			self.attributeFilters[attr].add(value)
		else:
			self.attributeFilters[attr].remove(value)
		self.updateActiveSchedules()
	
	def changeStartTime(self, index, value):
		self.changeAttribute(value, 'EarliestStartTimeToStr', self.startTimes[index])
	
	def changeEndTime(self, index, value):
		self.changeAttribute(value, "LatestEndTimeToStr", self.endTimes[index])
		
	def changeNumCredits(self, index, value):
		self.changeAttribute(value, "NumCredits", self.creditNums[index])
		
	def changeCourse(self, index, value):
		if value:
			self.excludedCourses.remove(self.courseList[index])
		else:
			self.excludedCourses.append(self.courseList[index])
		self.updateActiveSchedules()
		