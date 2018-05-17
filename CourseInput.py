class CourseInput:
	"""Represents what the user has input regarding a specific course."""
	
	@staticmethod
	def Parse(string):
		'''Turns a string of space delimited info into a CourseInput'''
		argList = []
		index = string.find(' ')
		while index != -1:
			argList.append(string[:index])
			string = string[index + 1:]
			index = string.find(' ')
		argList.append(string)
		return CourseInput(*argList)
	
	def __init__(self, coursePrefix, courseNumber, mandatory=False):
		self.CoursePrefix = coursePrefix
		self.CourseNumber = courseNumber
		self.Mandatory = mandatory
		self.SectionNumbers = []
		
	def __repr__(self):
		'''Allows printing of courses'''
		return self.CoursePrefix + str(self.CourseNumber) + '-' + str(self.SectionNumber) + ' ' + str(self.mandatory)
		
	def __eq__(self, otherCourse):
		'''Allows comparison of courses
		
		courses must have the same prefix and number to be equal, and as long as one's section is a subset of the other's, it will also return true
		'''
		return self.CoursePrefix == otherCourse.coursePrefix and self.CourseNumber == otherCourse.courseNumber and (not self.SectionNumber or not otherCourse.sectionNumber or self.SectionNumber == otherCourse.sectionNumber)
		
	def AddSectionNumber(self, n):
		self.SectionNumbers
		
'''		
print(CourseInput('ma', 123))
print(CourseInput.Parse("ma 123"))
print(CourseInput.Parse("ma 123 001 True"))
'''