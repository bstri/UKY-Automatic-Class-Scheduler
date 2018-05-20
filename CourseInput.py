'''Contains classes to represent a user's input with regards to courses.'''

class Course:
	def __init__(self, prefix, number):
		self.Prefix = prefix.upper()
		self.Number = number

	def __eq__(self, other):
		return self.Prefix == other.Prefix and self.Number == other.Number

	def __repr__(self):
		return "Course({}, {})".format(repr(self.Prefix), repr(self.Number))

	def __str__(self):
		return "{}{}".format(self.Prefix, self.Number)

class CourseInput:
	'''Represents what the user has input regarding a specific course.'''
	
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
		return CourseInput(Course(*argList[0:1], int(*argList[1:2])), *argList[2:])
	
	def __init__(self, course, sectionNumbers=None, mandatory=False):
		self.Course = course
		self.Mandatory = mandatory
		self.SectionNumbers = sectionNumbers and set(sectionNumbers) or set()

	def __str__(self):
		return "{}-{}{}".format(self.Course, ",".join(map(str, sorted(self.SectionNumbers))), self.Mandatory and " (Mandatory)" or "")
