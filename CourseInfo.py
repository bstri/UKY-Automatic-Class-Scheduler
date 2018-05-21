class CourseInfo:
	'''Info retrieved about a course'''
	
	def __init__(self, prefix, number, numCredits):
		self.CoursePrefix = prefix
		self.CourseNumber = number
		self.NumCredits = numCredits
		self.Sections = []
		
	def AddSection(self, sectionNum):
		s = SectionInfo(sectionNum, self.CoursePrefix, self.CourseNumber, self.NumCredits)
		self.Sections.append(s)
		return s
		
class SectionInfo:
	'''Info about a section of a course'''
	
	def __init__(self, sectionNum, prefix, courseNum, numCredits):
		self.CoursePrefix = prefix
		self.CourseNumber = courseNum
		self.SectionNumber = sectionNum
		self.NumCredits = numCredits
		self.EarlyTime = None # time of earliest class meeting
		self.LateTime = None # time of latest class let-out
		self.Warnings = []
		self.ClassMeetings = []
		self.TimesTBD = False
		self.LocationTBD = False
		self.ProfessorTBD = False
		
	def AddClassMeeting(self, meeting):
		self.ClassMeetings.append(meeting)
		if not self.EarlyTime or self.EarlyTime > meeting.Time:
			self.EarlyTime = meeting.Time
		if not self.LateTime or self.LateTime < meeting.EndTime:
			self.LateTime = meeting.EndTime
		
	def WarnTBDTimes(self):
		self.TimesTBD = True
		self.Warnings.append("NOTE: This section has TBD meeting time(s).")
		
	def WarnTBDLocation(self):
		self.LocationTBD = True
		self.Warnings.append("NOTE: This section has TBD location(s).")
		
	def WarnTBDProfessor(self):
		self.ProfessorTBD = True
		self.Warnings.append("NOTE: This section has TBD professor(s).")
		
	def OverlapsWith(self, other):
		for m1 in self.ClassMeetings:
			for m2 in other.ClassMeetings:
				if m1.OverlapsWith(m2):
					return True
		
class ClassMeeting:
	'''Contains the information related to a single weekly class meeting'''
	
	def __init__(self, dayOfWeek, startTime, endTime, location, professor):
		self.Day = dayOfWeek
		self.StartTime = startTime # datetime.datetime
		self.EndTime = endTime 
		self.Duration = endTime - startTime # datetime.timedelta
		self.Location = location
		self.Professor = professor
		
	def OverlapsWith(self, other):
		return other.Day == self.Day and (self.StartTime <= other.StartTime < self.StartTime + self.Duration or other.StartTime <= self.StartTime < other.StartTime + other.Duration)
		