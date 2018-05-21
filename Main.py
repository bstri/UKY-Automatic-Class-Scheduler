from ConfigurationData import ConfigurationData
from CourseInput import CourseInput
from WebsiteInterface import WebsiteInterface
from Scheduler import Schedule, MakeScheduleTree
from itertools import chain, combinations
import copy

iWebsite = WebsiteInterface()
courseInfoList = []
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
			info = iWebsite.RequestInfoAboutCourse(c.CoursePrefix, c.CourseNumber, config.Semester, config.Year)
			if type(info) is str:
				print("Error occurred when getting info for ", c, ": \n", info)
				continue
			courseInfoList.append(info)

mandatedCourses = []
for course in courseInfoList:
	for cInput in config.CourseInput:
		if cInput.Course == course.Course: 
			for i,s in enumerate(course.Sections):
				if not s.SectionNumber in cInput.SectionNumbers:
					del course.Sections[i]
			if cInput.Mandatory:
				mandatedCourses.append(course)
				courseInfoList.remove(course)

schedules = Scheduler.MakeScheduleTree(Schedule(), mandatedCourses)
if len(schedules) > 0:
	numMandatedCredits = schedules[0].NumCredits
else:
	numMandatedCredits = 0

courseInfoList.sort(key=lambda c: c.NumCredits, reverse=True)
creditSum = 0
for i,c in enumerate(courseInfoList):
	creditSum += c.NumCredits
	if creditSum >= config.MinCredits - numMandatedCredits:
		lowerCombinationBound = i
		break
creditSum = 0
for i in reversed(xrange(len(courseInfoList))):
	creditSum += courseInfoList[i].NumCredits
	if creditSum > config.MaxCredits - numMandatedCredits:
		break
	upperCombinationBound = i
	
combos = chain.from_iterable(combinations(courseInfoList, r) for r in range(lowerCombinationBound, upperCombinationBound + 1))
for i in range(len(schedules)):
	for c in combinations:
		creditSum = 0
		for course in c:
			creditSum += c.NumCredits
		if not (config.MinCredits <= creditSum <= config.MaxCredits):
			continue
		schedules += MakeScheduleTree(schedules[i], c)
	