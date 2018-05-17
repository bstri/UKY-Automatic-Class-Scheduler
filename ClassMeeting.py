class ClassMeeting():
	'''Contains the information related to a single weekly class meeting'''
	
	def __init__(self, dayOfWeek, time, duration, location, professor):
		self.Day = dayOfWeek
		self.Time = time # datetime.datetime
		self.Duration = duration #datetime.timedelta
		self.Location = location
		self.Professor = professor
		
	def OverlapsWith(self, other):
		return other.Day == self.Day and (self.Time <= other.Time <= self.Time + duration or other.Time <= self.Time <= other.Time + other.Duration)
		