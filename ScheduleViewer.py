from tkinter import *
from tkinter import ttk # themed widgets (more up-to-date looking)
from datetime import datetime, timedelta
from Event import Event

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

def discardZeroPrefix(string):
	if string[0] == '0':
		return string[1:]
	else:
		return string
			
class meetingBlock(Frame):
	''''''
	
	def __init__(self, parent, classMeeting, course, **kwargs):
		super().__init__(parent, **kwargs)
		Label(self, text=str(course), font=('Segoe', 8, 'bold'), bg=self['bg']).place(x=0, y=0)
		Label(self, text=discardZeroPrefix(classMeeting.StartTime.strftime('%I:%M%p')) + ' - ' + discardZeroPrefix(classMeeting.EndTime.strftime('%I:%M%p')), font=('Segoe', 7), bg=self['bg']).place(x=0, y=16)
		# todo: mousing over this frame should give additional info like location, professor, and type
		
class scheduleImage(Canvas):
	''''''
	
	xOffset = 1/15
	dayWidth = (1 - xOffset)/7
	originTime = datetime.strptime('8am', '%I%p')
	yOffset = 1/27
	hourHeight = (1 - yOffset)/13
	days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
	oneHour = timedelta(hours=1)
	blockPadding = .05*dayWidth
	blockColors = ['light slate gray', 'sky blue', 'peru', 'coral', 'medium sea green', 'dodger blue', 'medium orchid', 'light salmon', 'DarkOliveGreen3']
	
	def __init__(self, parent):
		super().__init__(parent, bd=1, relief='solid')
		self.dayToXPos = {d: i*self.dayWidth + self.xOffset for i,d in enumerate('UMTWRFS')} # made up abbr for Sat and Sun
		self.blocks = []
		
	def updateSize(self):
		self.delete('all')
		w = self.winfo_width()
		h = self.winfo_height()
		for i in range(13):
			y = h*(self.yOffset + i*self.hourHeight)
			self.create_line(0, y, w, y, fill='black')
			y += h*self.hourHeight/2
			self.create_line(self.xOffset*w, y, w, y, fill='grey')
			
			t = discardZeroPrefix(datetime.strftime(self.originTime + i*self.oneHour, '%I%p'))
			self.create_text(5, h*(self.yOffset + self.hourHeight*i), anchor='nw', text=t, font=('Segoe', 8))
			
		for i,d in enumerate(self.days):
			x = w*(self.xOffset + i*self.dayWidth)
			self.create_line(x, 0, x, h, fill='black')
			
			self.create_text(w*(self.xOffset + (i + .5)*self.dayWidth), 5, anchor='n', text=d, font=('Segoe', 8))		
		
	def datetimeToYPos(self, dt):
		delta = dt - self.originTime
		return delta.seconds/3600*self.hourHeight + self.yOffset
		
	def timedeltaToHeight(self, td):
		return td.seconds/3600*self.hourHeight
		
	def SetSchedule(self, schedule):
		for b in self.blocks:
			b.destroy()
		self.blocks = []
		for i,s in enumerate(schedule.Sections):
			for m in s.ClassMeetings:
				for d in m.Days:
					block = meetingBlock(self, m, s.Course, bg=self.blockColors[i])
					block.place(relwidth=self.dayWidth - 2*self.blockPadding, 
						relheight=self.timedeltaToHeight(m.Duration), 
						relx=self.dayToXPos[d] + self.blockPadding, 
						rely=self.datetimeToYPos(m.StartTime))
					self.blocks.append(block)

class scheduleInfoFrame(Frame):
	'''A frame containing basic schedule info'''
	
	def __init__(self, parent):
		super().__init__(parent, highlightthickness=1)
		self.parent = parent
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
		self.Selected = False
		self.mouseIn = False
	
	def onEnter(self):
		self.mouseIn = True
		# todo: change mouse cursor to button click cursor
		if self.Selected:
			return
		self.config(highlightbackground='black', highlightcolor='black')
	
	def onLeave(self):
		self.mouseIn = False
		if self.Selected:
			return
		bg = self.parent['bg']
		self.config(highlightbackground=bg, highlightcolor=bg)
		
	def Select(self):
		self.Selected = True
		self.config(highlightbackground='red', highlightcolor='red')
		
	def Deselect(self):
		self.Selected = False
		if not self.mouseIn:
			self.onLeave()
		else:
			self.onEnter()
		
	def SetSchedule(self, schedule):
		self.Schedule = schedule
		self.CreditLabel['text'] = str(schedule.NumCredits)
		self.StartTimeLabel['text'] = discardZeroPrefix(schedule.EarliestStartTimeToStr)
		self.EndTimeLabel['text'] = discardZeroPrefix(schedule.LatestEndTimeToStr)
		self.grid()
		
	def ClearSchedule(self):
		self.grid_remove()

class scheduleInfoListContainer:
	
	def __init__(self, infoLists, schImg):
		self.schImg = schImg
		for l in infoLists:
			l.Entered.append(self.onEnter)
			l.Clicked.append(self.onClick)
		self.currentSelection = None

	def onEnter(self, infoFrame):
		infoFrame.onEnter()
		if not self.currentSelection:
			self.schImg.SetSchedule(infoFrame.Schedule)
		
	def onClick(self, infoFrame):
		if self.currentSelection:
			self.currentSelection.Deselect()
		if self.currentSelection == infoFrame:
			self.currentSelection = None
			return
		infoFrame.Select()
		self.schImg.SetSchedule(infoFrame.Schedule)
		self.currentSelection = infoFrame
		
class scheduleInfoList(Frame):
	'''A frame containing rows of scheduleInfoFrames'''
	
	def __init__(self, parent):
		super().__init__(parent)
		self.Entered = Event()
		self.Clicked = Event()
		ttk.Label(self, text='# Credits').grid(column=1, row=1, padx=(0,6))
		ttk.Label(self, text='Start Time').grid(column=2, row=1, padx=6)
		ttk.Label(self, text='End Time').grid(column=3, row=1, padx=6)
		self.scheduleFrames = []
		
	def SetSchedules(self, schedules):
		for i,s in enumerate(schedules[:len(self.scheduleFrames)]):
			self.scheduleFrames[i].SetSchedule(s)
		for i,s in enumerate(schedules[len(self.scheduleFrames):]):
			f = scheduleInfoFrame(self)
			f.bind('<Enter>', lambda e, f=f: self.Entered(f))
			f.bind('<Leave>', lambda e, f=f: f.onLeave())
			f.bind('<1>', lambda e, f=f: self.Clicked(f))
			f.grid(row=len(self.scheduleFrames) + 2 + i, column=1, columnspan=3, pady=3, sticky='ew')
			self.scheduleFrames.append(f)
			f.SetSchedule(s)
		
		for s in self.scheduleFrames[len(schedules):]:
			s.ClearSchedule()

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
		
		scheduleCountFrame = Frame(self)
		scheduleCountFrame.grid(row=2, column=1, sticky='w', pady=(20,10))
		self.scheduleCount = ttk.Label(scheduleCountFrame)
		self.scheduleCount.grid(row=1, column=1)
		self.prevPageButton = ttk.Button(scheduleCountFrame, text='Previous Page')
		self.prevPageButton.grid(row=1, column=2, padx=(30,10))
		self.prevPageButton.bind('<1>', lambda e: self.prevPage())
		self.nextPageButton = ttk.Button(scheduleCountFrame, text='Next Page')
		self.nextPageButton.grid(row=1, column=3)
		self.nextPageButton.bind('<1>', lambda e: self.nextPage())
		
		self.scheduleFrame = Frame(self)
		self.scheduleFrame.grid(row=3, column=1, sticky='nesw')
		self.rowconfigure(3, weight = 1)
		
		self.scheduleFrame.columnconfigure(self.scheduleColumns + 1, weight = 1)
		self.scheduleFrame.rowconfigure(1, weight = 1)
		self.image = scheduleImage(self.scheduleFrame)
		self.image.grid(row=1, column=self.scheduleColumns + 1, sticky='nesw')
		
		self.scheduleInfoLists = []
		self.scheduleIndex = 0
		for i in range(self.scheduleColumns):
			s = scheduleInfoList(self.scheduleFrame)
			s.grid(row=1, column=i+1, padx=15, sticky='ns')
			self.scheduleInfoLists.append(s)
		
		self.infoListContainer = scheduleInfoListContainer(self.scheduleInfoLists, self.image)
		
		self._after_id = None
		self.scheduleFrame.bind('<Configure>', self.onResize)
		self.mainloop()
		
	def onResize(self, e):
		if self._after_id:
			self.after_cancel(self._after_id)
		self._after_id = self.after(250, lambda event=e: self.updateScheduleFrame(event))
		
	def updateScheduleFrame(self, e):
		self.schedulesPerColumn = e.height//28
		self.schedulesPerPage = self.schedulesPerColumn*self.scheduleColumns
		self.image.updateSize()	
		self.updateScheduleView()
		
	def getScheduleAttributeList(self, attr):
		l = {getattr(s, attr) for s in self.ScheduleList}
		self.attributeFilters[attr] = l
		return sorted(list(l))
		
	def nextPage(self):
		self.scheduleIndex += self.schedulesPerPage
		self.scheduleIndex = min(len(self.ActiveSchedules) - 1, self.scheduleIndex) # don't actually know if this is needed
		self.updateScheduleView()
		
	def prevPage(self):
		self.scheduleIndex -= self.schedulesPerPage
		self.scheduleIndex = max(0, self.scheduleIndex) 
		self.updateScheduleView()
		
	def updateScheduleCount(self):
		self.scheduleCount['text'] = 'Showing %d-%d of %d schedules found' % (self.scheduleIndex + 1, min(self.scheduleIndex + self.schedulesPerPage, len(self.ActiveSchedules)), len(self.ActiveSchedules))
			
	def updateScheduleView(self):
		for i in range(self.scheduleColumns):
			start = i*self.schedulesPerColumn + self.scheduleIndex
			self.scheduleInfoLists[i].SetSchedules(self.ActiveSchedules[start:start + self.schedulesPerColumn])
		self.updateScheduleCount()
		# todo: sometimes there is a bug where schedulespercolumn has increased but no new schedules are shown
		
		if self.schedulesPerPage >= len(self.ActiveSchedules) - self.scheduleIndex:
			# disabled next page button
			pass
		else: 
			pass
			# enable it
		if self.scheduleIndex == 0:
			# disabled prev page button
			pass
		else:
			pass
			# enable it
	
	def updateActiveSchedules(self):
		self.ActiveSchedules[:] = [s for s in self.ScheduleList if all(getattr(s,a) in vals for a,vals in self.attributeFilters.items()) and not any(sect for sect in s.Sections if sect.Course in self.excludedCourses)] # I love comprehensions
		self.scheduleIndex = 0
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
		