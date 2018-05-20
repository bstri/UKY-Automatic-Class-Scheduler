class CourseInput:
	"""Represents what the user has input regarding a specific course."""
	
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
		return CourseInput(*argList)
	
	def __init__(self, coursePrefix, courseNumber, sectionNumber=None, mandatory=False):
		self.CoursePrefix = coursePrefix
		self.CourseNumber = courseNumber
		self.Mandatory = mandatory
		self.SectionNumbers = [sectionNumber]
		
	def __repr__(self):
		'''Allows printing of courses'''
		return self.CoursePrefix + str(self.CourseNumber) + '-' + ','.join(self.SectionNumbers) + ' ' + str(self.mandatory)
		
	def __eq__(self, otherCourse):
		'''Allows comparison of courses'''
		return self.CoursePrefix == otherCourse.CoursePrefix and self.CourseNumber == otherCourse.CourseNumber
		
'''		
print(CourseInput('ma', 123))
print(CourseInput.Parse("ma 123"))
print(CourseInput.Parse("ma 123 001 True"))
'''