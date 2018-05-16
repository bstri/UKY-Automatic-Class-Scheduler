class ConfigurationData:
	"""Represents a user's input to the program."""
	def __init__(self):
		self.minCredits = 12
		self.maxCredits = 21
		self.courseInput = []
	
	def FindProblems(self):
		"""Ensure that the input isn't contradictory, returning a string error message if there's a problem or None if it's fine"""
		if self.minCredits > self.maxCredits:
			return "Min Credits must be less than Max Credits"