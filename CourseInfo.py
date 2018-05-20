class CourseInfo:
	'''Info retrieved about a course'''
	
	def __init__(self, prefix, number, minCredits, maxCredits):
		self.CoursePrefix = prefix
		self.CourseNumber = number
		self.Credits = list(range(minCredits, maxCredits + 1)) # covers cases of variable credit classes
		self.Sections = []
		
	def AddSection(self, sectionNum):
		s = SectionInfo(sectionNum, self.CoursePrefix, self.CourseNumber)
		self.Sections.append(s)
		return s
		
class SectionInfo:
	'''Info about a section of a course'''
	
	def __init__(self, sectionNum, prefix, courseNum):
		self.CoursePrefix = prefix
		self.CourseNumber = courseNum
		self.SectionNumber = sectionNum
		self.Warnings = []
		self.ClassMeetings = []
		self.TimesTBD = False
		self.LocationTBD = False
		self.ProfessorTBD = False
		
	def AddClassMeeting(self, meeting):
		self.ClassMeetings.append(meeting)
		
	def WarnTBDTimes(self):
		self.TimesTBD = True
		self.Warnings.append("NOTE: This section has TBD meeting time(s).")
		
	def WarnTBDLocation(self):
		self.LocationTBD = True
		self.Warnings.append("NOTE: This section has TBD location(s).")
		
	def WarnTBDProfessor(self):
		self.ProfessorTBD = True
		self.Warnings.append("NOTE: This section has TBD professor(s).")
		
class ClassMeeting:
	'''Contains the information related to a single weekly class meeting'''
	
	def __init__(self, dayOfWeek, time, duration, location, professor):
		self.Day = dayOfWeek
		self.Time = time # datetime.datetime
		self.Duration = duration # datetime.timedelta
		self.Location = location
		self.Professor = professor
		
	def OverlapsWith(self, other):
		return other.Day == self.Day and (self.Time <= other.Time < self.Time + self.Duration or other.Time <= self.Time < other.Time + other.Duration)
		