class ConfigurationData:
	"""Represents a user's input to the program."""
	
	HardCreditMinimum = 1
	HardCreditMaximum = 30
	HardCourseNumberMaximum = 15
	
	def __init__(self, semester=None, year=None, minCredits=None, maxCredits=None):
		self.MinCredits = max(HardCreditMinimum, minCredits)
		self.MaxCredits = min(HardCreditMaximum, maxCredits)
		self.CourseInput = []
		self.Year = year
		self.Semester = semester
		self.courseCount = 0
	
	def FindProblems(self):
		"""Ensure that the input isn't contradictory, returning a string error message if there's a problem or None if it's fine"""
		if self.minCredits > self.maxCredits:
			return "Min Credits must not be greater than Max Credits"
	
	def AddCourse(self, courseInput):
		if self.courseCount == HardCourseNumberMaximum:
			return -1
		courseCount += 1
		self.CourseInput.append(courseInput)
		