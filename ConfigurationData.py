from WebsiteInterface import WebsiteInterface

class ConfigurationData:
	'''Represents a user's input to the program.'''
	
	HardCreditMinimum = 1
	HardCreditMaximum = 30
	HardCourseNumberMaximum = 15
	
	def __init__(self, semester=None, year=None, minCredits=None, maxCredits=None):
		self.Semester = semester or WebsiteInterface.GetDefaultSemester()
		self.Year = year or WebsiteInterface.GetDefaultYear()
		self.MinCredits = max(self.HardCreditMinimum, minCredits or WebsiteInterface.MinCreditDefault)
		self.MaxCredits = min(self.HardCreditMaximum, maxCredits or WebsiteInterface.MaxCreditDefault)
		self.CourseInput = []
	
	def FindProblems(self):
		'''Ensure that the input isn't contradictory, returning a string error message if there's a problem or None if it's fine'''
		if self.MinCredits > self.MaxCredits:
			return "Min Credits must not be greater than Max Credits"
	
	def AddCourse(self, courseInput):
		'''Attempt to add the course, returning a message if there's a problem or None otherwise.'''
		if any(c.Course == courseInput.Course for c in self.CourseInput):
			return 'Course already added'
		if len(self.CourseInput) == self.HardCourseNumberMaximum:
			return 'Course maximum reached'
		self.CourseInput.append(courseInput)
		