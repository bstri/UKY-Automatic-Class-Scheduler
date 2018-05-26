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

	def __repr__(self):
		return "CourseInput({!r}, {!r}, mandatory={!r})".format(self.Course, self.SectionNumbers, self.Mandatory)

	def __str__(self):
		return "{}-{}{}".format(self.Course, ",".join(map(str, sorted(self.SectionNumbers))), self.Mandatory and " (Mandatory)" or "")

class CourseInfo:
	'''Info about a course'''
	
	def __init__(self, course, numCredits, sections, variableCredit=False):
		self.Course = course
		self.NumCredits = numCredits
		self.IsVariableCredit = variableCredit # numCredits represents the minimum when this is True
		self.Sections = sections
		
	def __str__(self):
		return "{}-{}".format(self.Course, ",".join(map(str, sorted(s.SectionNumber for s in self.Sections))))
		
class SectionInfo:
	'''Info about a section of a course'''
	
	def __init__(self, sectionNum, course, numCredits):
		self.Course = course
		self.SectionNumber = sectionNum
		self.NumCredits = numCredits
		self.Warnings = []
		self.ClassMeetings = []
		# self.DayToStartTime = {} # each key is a day of the week M-F
		# self.DayToEndTime = {}
		self.TimesTBD = False
		self.LocationTBD = False
		self.ProfessorTBD = False
		self.sectionOverlapCache = {}
		
	def __str__(self):
		return '{}-{}'.format(str(self.Course), str(self.SectionNumber))
		
	def setSectionOverlap(self, otherSection, overlaps):
		self.sectionOverlapCache[str(otherSection)] = overlaps
		
	def AddClassMeeting(self, meeting):
		self.ClassMeetings.append(meeting)
		# if not self.DayToStartTime.get(day):
		# 	self.DayToStartTime[day] = meeting.StartTime
		# 	self.DayToEndTime[day] = meeting.EndTime
		# else: 
		# 	if self.DayToStartTime[day] > meeting.StartTime:
		# 		self.DayToStartTime[day] = meeting.StartTime
		# 	if self.DayToEndTime[day] < meeting.EndTime:
		# 		self.DayToEndTime[day] = meeting.EndTime
		
	def WarnTBDTimes(self):
		if self.TimesTBD:
			return
		self.TimesTBD = True
		self.Warnings.append("NOTE: This section has TBD meeting time(s).")
		
	def WarnTBDLocation(self):
		if self.LocationTBD:
			return
		self.LocationTBD = True
		self.Warnings.append("NOTE: This section has TBD location(s).")
		
	def WarnTBDProfessor(self):
		if self.ProfessorTBD:
			return
		self.ProfessorTBD = True
		self.Warnings.append("NOTE: This section has TBD professor(s).")
		
	def OverlapsWith(self, other):
		overlaps = self.sectionOverlapCache.get(str(other))
		if overlaps == None:
			for m in self.ClassMeetings: 
				for m2 in other.ClassMeetings:
					if m.OverlapsWith(m2):
						self.setSectionOverlap(other, True)
						other.setSectionOverlap(self, True)
						return True
			self.setSectionOverlap(other, False)
			other.setSectionOverlap(self, False)
		else:
			return overlaps

class ClassMeeting:
	'''Contains the information related to a single weekly class meeting'''
	
	def __init__(self, meetingType, days, startTime, endTime, location, professor):
		self.Type = meetingType # e.g. lab, lecture, recitation
		self.Days = days # e.g. 'MWF'
		self.StartTime = startTime # startTime and endTime are datetime.datetime (is to always refer to January 1st, 1900, as is provided by default by datetime.strptime)
		self.EndTime = endTime
		self.Duration = endTime - startTime
		self.Location = location
		self.Professor = professor
		
	def OverlapsWith(self, other):
		return any(day for day in self.Days if day in other.Days) and (self.StartTime <= other.StartTime < self.StartTime + self.Duration or other.StartTime <= self.StartTime < other.StartTime + other.Duration)
