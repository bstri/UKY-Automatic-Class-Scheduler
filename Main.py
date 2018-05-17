from ConfigurationData import ConfigurationData
from CourseInput import CourseInput
from CourseInfo import CourseInfo
from WebsiteInterface import WebsiteInterface

'''config;
with open("courses.txt", "r") as f:
	for i,line in enumerate(f):
		if i == 0:
			lower = WebsiteInterface.MinCreditDefault
			upper = WebsiteInterface.MaxCreditDefault
			index = line.find('-')
			if index > 0:
				lower = int(line[:index])
			if len(line) > index + 1:
				upper = int(line[index + 1:])
			config = ConfigurationData("Fall", 2018, lower, upper)
		else:
			config.AddCourse(CourseInput.Parse(line))
'''
iWebsite = WebsiteInterface()
iWebsite.RequestInfoAboutCourse(CourseInput("ma", 322), "Fall", 2018)
'''
for course in config.CourseInput:
	info = iWebsite.RequestInfoAboutCourse(course, config.Semester, config.Year)
	if type(info) is str:
		print("Error occurred when getting info for ", course, ": \n", info)
		return
	'''