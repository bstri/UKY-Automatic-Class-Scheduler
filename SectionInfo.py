class SectionInfo():
	'''Info about a section of a course'''
	
	def __init__(self, sectionNumber):
		self.SectionNumber = sectionNumber
		self.Warnings = []
		self.ClassMeetings = []
		
	def AddClassMeeting(self, meeting):
		self.ClassMeetings.append(meeting)