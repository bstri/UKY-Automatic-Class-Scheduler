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

def MakeScheduleTree(rootSchedule, courseInfoList):
	schedules = []
	scheduleTreeHelper(rootSchedule, courseInfoList, schedules)
	return schedules
	
def scheduleTreeHelper(rootSchedule, courseInfoList, schedules)
	if len(courseInfoList) == 0:
		schedules.append(rootSchedule)
	for s in courseInfoList[0].Sections:
		cpy = copy.deepcopy(rootSchedule)
		if cpy.TryAddSection(s):
			scheduleTreeHelper(cpy, courseInfoList[1:], schedules)