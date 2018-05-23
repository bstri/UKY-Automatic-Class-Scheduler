'''Classes to represent information about courses'''

class Course:
	'''The prefix and number for a course.

	Prefix is guaranteed to be upper-case.'''

	def __init__(self, prefix, number):
		self.Prefix = prefix.upper()
		self.Number = number

	def __eq__(self, other):
		return self.Prefix == other.Prefix and self.Number == other.Number

	def __repr__(self):
		return "Course({!r}, {!r})".format(self.Prefix, self.Number)

	def __str__(self):
		return "{}{}".format(self.Prefix, self.Number)

class CourseInput:
	'''Represents user input regarding a specific course.'''

	def __init__(self, course, sectionNumbers=None, mandatory=False):
		self.Course = course
		self.Mandatory = mandatory
		self.SectionNumbers = sectionNumbers and set(sectionNumbers) or set()
	
	@staticmethod
	def Parse(string):
		'''Turns a string of space delimited info into a CourseInput'''
		string = string.rstrip()
		argList = []
		index = string.find(' ')
		while index != -1:
			argList.append(string[:index])
			string = string[index + 1:]
			index = string.find(' ')
		argList.append(string)
		return CourseInput(Course(argList[0], int(argList[1])), *argList[2:])

	def __repr__(self):
		return "CourseInput({!r}, {!r}, mandatory={!r})".format(self.Course, self.SectionNumbers, self.Mandatory)

	def __str__(self):
		return "{}-{}{}".format(self.Course, ",".join(map(str, sorted(self.SectionNumbers))), self.Mandatory and " (Mandatory)" or "")

class CourseInfo:
	'''Info retrieved about a course'''
	
	def __init__(self, course, numCredits):
		self.Course = course
		self.NumCredits = numCredits
		self.Sections = []
		
	def AddSection(self, sectionNum):
		s = SectionInfo(sectionNum, self.Course, self.NumCredits)
		self.Sections.append(s)
		return s
		
	def __str__(self):
		return "{}-{}".format(self.Course, ",".join(map(str, sorted(s.SectionNumber for s in self.Sections))))
		
class SectionInfo:
	'''Info about a section of a course'''
	
	def __init__(self, sectionNum, course, numCredits):
		self.Course = course
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
		if not self.EarlyTime or self.EarlyTime > meeting.StartTime:
			self.EarlyTime = meeting.StartTime
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
		self.StartTime = startTime # startTime and endTime are datetime.datetime (is to always refer to January 1st, 1900, as is provided by default by datetime.strptime)
		self.EndTime = endTime
		self.Duration = endTime - startTime
		self.Location = location
		self.Professor = professor
		
	def OverlapsWith(self, other):
		return other.Day == self.Day and (self.StartTime <= other.StartTime < self.StartTime + self.Duration or other.StartTime <= self.StartTime < other.StartTime + other.Duration)
