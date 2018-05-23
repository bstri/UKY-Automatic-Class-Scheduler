import requests
from lxml import html
import datetime
from Courses import CourseInfo, SectionInfo, ClassMeeting

class WebsiteInterface:
	'''Fetches course data from the online course catalog'''
	
	MinCreditDefault = 12
	MaxCreditDefault = 21
	
	@staticmethod
	def GetDefaultSemester():
		t = datetime.date.today()
		return (3 <= t.month <= 9) and "Fall" or "Spring" # guesses fall semester if the current month is 
	
	@staticmethod
	def GetDefaultYear():
		return datetime.date.today().year
		
	def __init__(self):
		self.session = requests.Session()
		# Make the webpage think we're using Chrome
		self.session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
		
	def RequestInfoAboutCourse(self, course, semester, year):
		r = self.session.post("https://myuk.uky.edu/zAPPS/CourseCatalog/Offering", data = {
			"CoursePrefix": course.Prefix,
			"CourseNumber": str(course.Number),
			"CourseSection": "",
			"Year": str(year + (semester == "Fall" and 1 or 0)),
			"Period": semester == "Fall" and "010" or "030",
			"SearchTerms": "",
			"UkCore": "",
			"Is300LevelPlus": "false",
			"IsVariableCredit": "false",
			"HasPartOfTermSections": "false",
			"HasDistanceSections": "false"})
		
		tree = html.fromstring(r.text.replace('\\','')) 
		container = tree.xpath('div[@class="course-container"]')[0]
		
		# make sure we can actually get the course catalog for this term
		goodTerm = container.xpath("@data-offered-in-specified-term")[0]
		if goodTerm != "True":
			return "Invalid term. Please choose a different year and/or semester."
		
		credits = container.xpath('div/div/div/div/h5/span[2]/span/text()')[0] # Two forms: '3.0 Credits' ; '1.0 - 2.0 (variable) Credits'
		numC = int(credits[0])
		if '-' in credits:
			return "Variable credit hour classes not supported."
		
		# prep courseInfo (which will be returned)
		courseInfo = CourseInfo(course, numC)
		
		sections = container.xpath('div/div[starts-with(@class,"table-thin-row small filterable")]')
		for section in sections:
			# skip this section if it has been cancelled
			classVal = section.xpath("div[1]/@class")[0]
			if "course-cancelled" in classVal: 
				continue
			
			# different meetings might be lecture, lab, recitation, etc.
			meetings = section.xpath('div[starts-with(@class,"clearfix course-row expanded-section table-thin-row-event")]')
			
			sectionNumber = int(meetings[0].xpath("(.//a)[1]/text()")[0])
			sectionInfo = courseInfo.AddSection(sectionNumber)
			
			# warnings might be location warnings or controlled enrollment warnings
			warnings = section.xpath('div[starts-with(@class,"clearfix course-row expanded-section table-thin-row-event")]/p/descendant::text()')
			sectionInfo.Warnings = warnings
			
			for meeting in meetings:
				location = meeting.xpath('div[@class="pull-left"][@style="width: 170px;"]/div/descendant::text()')
				strLocation = ' '.join(location) # often will have building followed by room number
				if location[0] == "TBD":
					sectionInfo.WarnTBDLocation()
				
				professor = meeting.xpath('div[@class="pull-left"][@style="width: 130px;"]/div/text()')[0]
				if professor == "TBD":
					sectionInfo.WarnTBDProfessor()
				
				daysAndTime = meeting.xpath('div[@class="pull-left"][@style="width: 140px;"]/div/text()')
				if daysAndTime[0] == "TBD":
					sectionInfo.WarnTBDTimes()
					continue
				days = daysAndTime[0]
				timeframe = daysAndTime[1] # of the form '9:00 am - 9:50 am' for example
				startTime = timeframe[:timeframe.find(' -')]
				endTime = timeframe[timeframe.find('-') + 2:]
				startDateTime = datetime.datetime.strptime(startTime, "%I:%M %p")
				endDateTime = datetime.datetime.strptime(endTime, "%I:%M %p")
				for day in days:
					classMeeting = ClassMeeting(day, startDateTime, endDateTime, strLocation, professor)
					sectionInfo.AddClassMeeting(classMeeting)
					
		return courseInfo