from WebsiteInterface import WebsiteInterface
class ConfigurationData:
	"""Represents a user's input to the program."""
	
	HardCreditMinimum = 1
	HardCreditMaximum = 30
	HardCourseNumberMaximum = 15
	
	def __init__(self, year=None, semester=None, minCredits=None, maxCredits=None):
		self.Year = year or WebsiteInterface.GetDefaultYear()
		self.Semester = semester or WebsiteInterface.GetDefaultSemester()
		self.MinCredits = max(self.HardCreditMinimum, minCredits or WebsiteInterface.MinCreditDefault)
		self.MaxCredits = min(self.HardCreditMaximum, maxCredits or WebsiteInterface.MaxCreditDefault)
		self.CourseInput = []
	
	def FindProblems(self):
		"""Ensure that the input isn't contradictory, returning a string error message if there's a problem or None if it's fine"""
		if self.MinCredits > self.MaxCredits:
			return "Min Credits must not be greater than Max Credits"
	
	def AtCourseLimit(self):
		return len(self.CourseInput) == HardCourseNumberMaximum

	def updateCourseInput(self, index, newCourseInput):
		self.CourseInput[index] = newCourseInput

	def AddCourse(self, courseInput):
		if self.AtCourseLimit():
			return False
		for index, ci in enumerate(self.CourseInput):
			if ci.SameCourseAs(courseInput):
				self.updateCourseInput(index, courseInput)
				return True
		self.CourseInput.append(courseInput)
		return True