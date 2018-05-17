import requests
from lxml import html
import datetime
from CourseInfo import CourseInfo
from SectionInfo import SectionInfo
from ClassMeeting import ClassMeeting

class WebsiteInterface:
	''''''
	
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
		
	def RequestInfoAboutCourse(self, courseInput, semester, year):
		prefix = courseInput.CoursePrefix.upper()
		courseNum = str()
		'''r = session.post("https://myuk.uky.edu/zAPPS/CourseCatalog/Offering", data = {
			"CoursePrefix": courseInput.CoursePrefix.upper(),
			"CourseNumber": str(courseInput.CourseNumber),
			"CourseSection": str(courseInput.SectionNumber or ''),
			"Year": str(year + (semester == "Fall" and 1 or 0)),
			"Period": semester == "Fall" and "010" or "030",
			"SearchTerms": "",
			"UkCore": "",
			"Is300LevelPlus": "false",
			"IsVariableCredit": "false",
			"HasPartOfTermSections": "false",
			"HasDistanceSections": "false"})'''
		
		#tree = html.fromstring(r.text.replace('\\','')) 
		with open('EGR103Info.html', 'r') as f:
			tree = html.fromstring(f.read())
			goodTerm = tree.xpath("//div/@data-offered-in-specified-term")[0]
			if goodTerm != "True":
				return "Invalid term. Please choose a different year and/or semester."
			courseInfo = CourseInfo()
			sections = tree.xpath('//div[starts-with(@class,"table-thin-row small filterable")]')
			for element in sections:
				classVal = element.xpath("div[1]/@class")
				if "course-cancelled" in classVal:
					continue
				warnings = element.xpath('div[starts-with(@class,"clearfix course-row expanded-section table-thin-row-event")]/p/text()')
				meetings = element.xpath('div[starts-with(@class,"clearfix course-row expanded-section table-thin-row-event")]')
				sectionNumber = meetings[0].xpath("a")
				sectionInfo = SectionInfo(int(sectionNumber))
				sectionInfo.Warnings = warnings
				print(sectionNumber)
				for meeting in meetings:
					location = meeting.xpath('div[@class="pull-left"][@style="width: 170px;"]/div')
					strLocation = ''
					for l in location:
						strLocation += l.xpath('/text()')
					print(strLocation)
					professor = meeting.xpath('div[@class="pull-left"][@style="width: 130px;"]/div/text()')[0]
					daysAndTime = meeting.xpath('div[@class="pull-left"][@style="width: 140px;"]/div/text()')
					if daysAndTime[0] == "TBD":
						sectionInfo.Warnings.append("NOTE: This section has some TBD meeting times.")
						continue
					days = daysAndTime[0]
					print(days)
					timeframe = daysAndTime[1]
					print(timeframe)
					startTime = timeframe[:timeframe.find(' -')]
					endTime = timeframe[timeframe.find('-') + 2:]
					startDateTime = datetime.datetime.strptime(startTime, "%I:%M %p")
					endDateTime = datetime.datetime.strptime(startTime, "%I:%M %p")
					duration = endDateTime - startDateTime
					for day in days:
						classMeeting = ClassMeeting(day, startDateTime, duration, strLocation, professor)
						sectionInfo.AddClassMeeting(classMeeting)
						
					