import copy

class Schedule:
	''''''
	
	def __init__(self):
		self.NumCredits = 0
		self.Sections = []
		self.AverageStartTime = None
		self.AverageEndTime = None
		
	def TryAddSection(self, section):
		for s in self.Sections:
			if s.OverlapsWith(section):
				return False
		self.Sections.append(section)
		self.NumCredits += section.NumCredits
		# todo: update average start and end times
		return True	
		
	def __str__(self):
		string = ''
		for s in self.Sections:
			string += '{}-{}; '.format(str(s.Course), str(s.SectionNumber)) 
		return string

def MakeScheduleTree(rootSchedule, courseInfoList):
	schedules = []
	# pdb.set_trace()
	scheduleTreeHelper(rootSchedule, courseInfoList, schedules)
	return schedules
	
def scheduleTreeHelper(rootSchedule, courseInfoList, schedules):
	if len(courseInfoList) == 0:
		schedules.append(rootSchedule)
		return
	for s in courseInfoList[0].Sections:
		cpy = copy.deepcopy(rootSchedule)
		if cpy.TryAddSection(s):
			scheduleTreeHelper(cpy, courseInfoList[1:], schedules)
			
def SubmitSchedules(schedules):
	for s in schedules:
		print(s)
	