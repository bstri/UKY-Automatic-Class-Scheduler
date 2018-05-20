class CourseInput:
	"""Represents what the user has input regarding a specific course."""
	
	@staticmethod
	def Parse(string):
		"""Turns a string of space delimited info into a CourseInput"""
		argList = []
		index = string.find(' ')
		while index != -1:
			argList.append(string[:index])
			string = string[index + 1:]
			index = string.find(' ')
		argList.append(string)
		return CourseInput(*argList)
	
	def __init__(self, coursePrefix, courseNumber, sectionNumbers=None, mandatory=False):
		self.CoursePrefix = coursePrefix.upper()
		self.CourseNumber = courseNumber
		self.Mandatory = mandatory
		self.SectionNumbers = sectionNumbers and set(sectionNumbers) or set()
		
	def __repr__(self):
		"""Allows printing of courses"""
		return "{}{}-{}{}".format(self.CoursePrefix, str(self.CourseNumber), str(self.SectionNumbers), self.mandatory and " (Mandatory)" or "")
		
	def __eq__(self, otherCourse):
		"""Allows comparison of courses"""
		return (self.CoursePrefix == otherCourse.CoursePrefix and
			self.CourseNumber == otherCourse.CourseNumber and
			self.SectionNumbers == otherCourse.SectionNumbers and
			self.Mandatory == otherCourse.Mandatory)

	def SameCourseAs(self, otherCourse):
		return (self.CoursePrefix == otherCourse.CoursePrefix and
			self.CourseNumber == otherCourse.CourseNumber)
		
"""		
print(CourseInput('ma', 123))
print(CourseInput.Parse("ma 123"))
print(CourseInput.Parse("ma 123 001 True"))
"""