from ConfigurationData import ConfigurationData
from CourseInput import CourseInput
from WebsiteInterface import WebsiteInterface

iWebsite = WebsiteInterface()
infoList = []
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
			c = CourseInput.Parse(line)
			failure = config.AddCourse(c)
			if failure:
				print(failure)
				continue
			info = iWebsite.RequestInfoAboutCourse(c.Course, config.Semester, config.Year)
			if type(info) is str:
				print("Error occurred when getting info for ", c, ": \n", info)
				continue
			infoList.append(info)

