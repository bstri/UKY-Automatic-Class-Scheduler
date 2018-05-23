from ConfigurationData import ConfigurationData
from Courses import CourseInput, Course
from WebsiteInterface import WebsiteInterface
from Scheduler import *
from itertools import chain, combinations
from sys import exit

# TESTING STUFF
def CInput(prefix, number, sections=None, mandatory=None):
	return CourseInput(Course(prefix, number), sections, mandatory)
courseInput = [
	CInput('ma', 322, [1,2,3,4], True),
	CInput('cs', 315),
	CInput('ma', 415, [1], True),
	CInput('cs', 215, list(range(1,8))),
	CInput('phy', 231)]
config = ConfigurationData("Fall", 2018, 14, 17)
for c in courseInput:
	failure = config.AddCourse(c)
	if failure:
		print(failure)
		continue
# END TESTING STUFF

iWebsite = WebsiteInterface()
courseInfoList = []
for c in config.CourseInput:
	info = iWebsite.RequestInfoAboutCourse(c.Course, config.Semester, config.Year)
	if type(info) is str:
		print("Error occurred when getting info for ", c, ": \n", info)
		continue
	courseInfoList.append(info)

# delete all sections in the course catalog that are excluded in the input
# move all mandatory courses to a separate list
mandatedCourses = []
for course in courseInfoList[:]:
	for cInput in config.CourseInput:
		if cInput.Course == course.Course: 
			if len(cInput.SectionNumbers) > 0: # todo: remove when done testing because normally this would mean 'I don't want any sections' but for now it means all sections are good
				course.Sections[:] = [s for s in course.Sections if s.SectionNumber in cInput.SectionNumbers]
			if cInput.Mandatory:
				mandatedCourses.append(course)
				courseInfoList.remove(course)

schedules = []
if len(mandatedCourses) > 0:
	# get all schedules that (only) contain each mandatory course
	rootSchedules = MakeScheduleTree(Schedule(), mandatedCourses)
	if len(rootSchedules) > 0: 
		numMandatedCredits = rootSchedules[0].NumCredits
	else:
		print("No schedules found containing the specified mandatory courses.")
		SubmitSchedules(schedules)
		exit()
else: # no courses are mandatory
	numMandatedCredits = 0

# check if the mandatory schedules (if there are any) can be standalone schedules
if numMandatedCredits >= config.MinCredits:
	if numMandatedCredits > config.MaxCredits:
		print("Specified mandatory courses exceed given credit maximum")
		SubmitSchedules(schedules)
		exit()
	else:
		schedules = rootSchedules

if len(courseInfoList) == 0:
	SubmitSchedules(schedules)
	exit()

# sort remaining (non-mandatory) courses by descending num credits
courseInfoList.sort(key=lambda c: c.NumCredits, reverse=True)
# the credit sum of the first m of these sorted courses gets a lower bound on the number of courses we need to add to each schedule in schedules
creditSum = 0
minCredits = config.MinCredits - numMandatedCredits
maxCredits = config.MaxCredits - numMandatedCredits
for i,c in enumerate(courseInfoList):
	creditSum += c.NumCredits
	if creditSum >= minCredits:
		lowerCombinationBound = i + 1
		break
if not lowerCombinationBound:
	SubmitSchedules(schedules)
	exit()
# the last n of these sorted courses gets an upper bound
creditSum = 0
upperCombinationBound = len(courseInfoList)
for i in reversed(range(len(courseInfoList))):
	creditSum += courseInfoList[i].NumCredits
	if creditSum > maxCredits:
		upperCombinationBound -= i
		break
if upperCombinationBound < lowerCombinationBound:
	# e.g. 5-6 credits; [4,4,3]. Lower is 2 and upper is 1.
	SubmitSchedules(schedules)
	exit()
		
# form an iterable that contains all m- through n-combinations of the courses in courseInfoList
combos = chain.from_iterable(combinations(courseInfoList, r) for r in range(lowerCombinationBound, upperCombinationBound + 1)) # already checked for 0-combinations above

# for each combination, make sure num credits is valid, and only add schedules that use all the courses in the combination, to prevent overlap
for i in range(len(rootSchedules)):
	for c in combos:
		creditSum = 0
		for course in c:
			creditSum += course.NumCredits
		if not (minCredits <= creditSum <= maxCredits):
			continue
		schedules += MakeScheduleTree(rootSchedules[i], list(c))
	
SubmitSchedules(schedules)
