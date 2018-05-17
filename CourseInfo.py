class CourseInfo:
	"""Info retrieved about a course"""
	
	def __init__(self, prefix, number):
		self.CoursePrefix = prefix
		self.CourseNumber = number
		self.Sections = []
		
	def AddSection(self, section):
		self.Sections.append(section)