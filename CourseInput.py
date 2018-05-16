class CourseInput:
	"""Represents what the user has input regarding a specific course."""
	
	def __init__(self, coursePrefix, courseNumber, sectionNumber=None, mandatory=False):
		self.coursePrefix = coursePrefix
		self.courseNumber = courseNumber
		self.sectionNumber = sectionNumber
		self.mandatory = mandatory