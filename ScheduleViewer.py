from tkinter import *
from tkinter import ttk # themed widgets (more up-to-date looking)
from PIL import ImageTk, Image
from datetime import datetime

class checkbar(Frame):
	'''Frame of checkboxes that fire cmd when toggled
	
	cmd should take 2 arguments: the index in picks and the checkbox state'''
	
	def __init__(self, parent, picks, cmd, checked=False):
		super().__init__(parent)
		self.vars = []
		for i,pick in enumerate(picks):
			var = BooleanVar()
			chk = ttk.Checkbutton(self, text=pick, variable=var, command=lambda index=i,v=var: cmd(index, v.get()), padding=(0,0,10,0))
			chk.grid(row=1, column=i+1)
			self.vars.append(var)
			var.set(checked)
			
class meetingBlock(Frame):
	''''''
	
	def __init__(self, parent, classMeeting):
		super().__init__(parent, bd=1, relief='solid')
		
		
class scheduleImage(Label):
	''''''
	
	dayWidth = 115/850
	originTime = datetime.strptime('8am', '%I%p')
	totalMinutes = 13*60 + 30
	
	def __init__(self, parent):
		super().__init__(parent)
		self.dayToXPos = {d: i*self.dayWidth + 45/850 for i,d in enumerate('UMTWRFS')} # made up abbr for Sat and Sun
		self.original = Image.open('scheduleImage.gif')
		self.blocks = []
		# TODO: remove days and times from the image, then put them in here as labels, positioning them in updateSize
		
	def updateSize(self):
		resized = self.original.resize((self.winfo_width(), self.winfo_height()), Image.ANTIALIAS)
		self.image = ImageTk.PhotoImage(resized)
		self['image'] = self.image
		
	def datetimeToYPos(self, dt):
		delta = dt - self.originTime
		minutes = delta.seconds/60
		return (minutes + 30)/self.totalMinutes
		
	def timedeltaToHeight(self, td):
		return td.seconds/60/self.totalMinutes
		
	def SetSchedule(self, schedule):
		for b in self.blocks:
			b.destroy()
		self.blocks = []
		for s in schedule.Sections:
			for m in s.ClassMeetings:
				for d in m.Days:
					# TODO: these blocks are slightly off position depending on where they are
					block = meetingBlock(self, m)
					block.place(relwidth=self.dayWidth, 
						relheight=self.timedeltaToHeight(m.Duration), 
						relx=self.dayToXPos[d], 
						rely=self.datetimeToYPos(m.StartTime))
					self.blocks.append(block)

def discardZeroPrefix(string):
	if string[0] == '0':
		return string[1:]
	else:
		return string

class scheduleInfoFrame(Frame):
	'''A frame containing basic schedule info'''
	
	def __init__(self, parent, schImg):
		super().__init__(parent, bd=1)
		self.schImg = schImg
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
		self.schImg.SetSchedule(self.Schedule)
	
	def onLeave(self, e):
		self['relief'] = 'flat'
		
	def SetSchedule(self, schedule):
		self.Schedule = schedule
		self.CreditLabel['text'] = str(schedule.NumCredits)
		self.StartTimeLabel['text'] = discardZeroPrefix(schedule.EarliestStartTimeToStr)
		self.EndTimeLabel['text'] = discardZeroPrefix(schedule.LatestEndTimeToStr)
		self.grid()
		
	def ClearSchedule(self):
		self.grid_remove()
		
class scheduleInfoList(Frame):
	'''A frame containing rows of scheduleInfoFrames'''
	
	def __init__(self, parent, maxListLen, schImg):
		super().__init__(parent)
		ttk.Label(self, text='# Credits').grid(column=1, row=1, padx=(0,6))
		ttk.Label(self, text='Start Time').grid(column=2, row=1, padx=6)
		ttk.Label(self, text='End Time').grid(column=3, row=1, padx=6)
		self.scheduleFrames = []
		self.maxRows = maxListLen
		for i in range(maxListLen):
			f = scheduleInfoFrame(self, schImg)
			f.grid(row=2+i, column=1, columnspan=3, pady=3, sticky='ew')
			self.scheduleFrames.append(f)
		
	def SetSchedules(self, schedules):
		for i,s in enumerate(schedules):
			self.scheduleFrames[i].SetSchedule(s)
		for i in range(len(schedules), self.maxRows):
			self.scheduleFrames[i].ClearSchedule()

class ScheduleViewer(Tk):
	''''''
	
	scheduleColumns = 2 # todo: a nice feature would be to allow this to change with self's size
	
	def __init__(self, scheduleList=[], courseList=[]):
		super().__init__()
		self.title("Schedule Viewer")
		self.geometry("1200x750")
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
		self.startTimes = list(map(lambda t: t.strftime('%I:%M%p'), sorted(list(map(lambda t: datetime.strptime(t, '%I:%M%p'), self.startTimes)))))
		# Reasoning: Want the datetimes sorted like normal (using < so 8AM comes first), but self.startTimes is a list of string times like '8:00AM' (couldn't figure out how to get only the unique datetimes from the schedulelist) and so the normal sorting doesn't quite work because '11:00AM' comes before '8:00AM.' So I create datetimes out of these strings, sort that list, then convert the times back into a list of strings.
		checkbar(filterFrame, self.startTimes, self.changeStartTime, True).grid(row=2, column=2, sticky='w')
		
		ttk.Label(filterFrame, text="End Times: ").grid(row=3, column=1, sticky='e', pady=3)
		self.endTimes = self.getScheduleAttributeList("LatestEndTimeToStr")
		checkbar(filterFrame, self.endTimes, self.changeEndTime, True).grid(row=3, column=2, sticky='w')
		
		ttk.Label(filterFrame, text="Credits: ").grid(row=4, column=1, sticky='e', pady=3)
		self.creditNums = self.getScheduleAttributeList("NumCredits")
		checkbar(filterFrame, map(str, self.creditNums), self.changeNumCredits, True).grid(row=4, column=2, sticky='w')
		
		self.scheduleCount = ttk.Label(self)
		self.scheduleCount.grid(row=2, column=1, sticky='w', pady=(20,10))
		
		self.scheduleFrame = Frame(self)
		self.scheduleFrame.grid(row=3, column=1, sticky='nesw')
		self.rowconfigure(3, weight = 1)
		
		self.scheduleFrame.columnconfigure(self.scheduleColumns + 1, weight = 1)
		self.scheduleFrame.rowconfigure(1, weight = 1)
		self.image = scheduleImage(self.scheduleFrame)
		self.image.grid(row=1, column=self.scheduleColumns + 1, sticky='nesw')
		
		self.scheduleInfoLists = []
		
		self._after_id = None
		self.scheduleFrame.bind('<Configure>', self.onResize)
		self.mainloop()
		
	def onResize(self, e):
		if self._after_id:
			self.after_cancel(self._after_id)
		self._after_id = self.after(250, lambda event=e: self.updateScheduleFrame(event))
		
	def updateScheduleFrame(self, e):
		self.schedulesPerColumn = e.height//28
		# TODO: change scheduleinfolist so that it can be updated, rather than needing to make new ones
		for c in self.scheduleInfoLists:
			c.destroy()
		self.scheduleInfoLists = []
		for i in range(self.scheduleColumns):
			s = scheduleInfoList(self.scheduleFrame, self.schedulesPerColumn, self.image)
			s.grid(row=1, column=i+1, padx=15, sticky='ns')
			self.scheduleInfoLists.append(s)
		
		self.image.updateSize()	
		
		self.updateScheduleView()
		
	def getScheduleAttributeList(self, attr):
		l = {getattr(s, attr) for s in self.ScheduleList}
		self.attributeFilters[attr] = l
		return sorted(list(l))
		
	def updateScheduleCount(self):
		self.scheduleCount['text'] = 'Showing %d of %d schedules found' % (min(self.schedulesPerColumn*self.scheduleColumns, len(self.ActiveSchedules)), len(self.ActiveSchedules))
	
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
		