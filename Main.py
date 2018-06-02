from ConfigurationData import ConfigurationData
from Courses import CourseInput, Course

def CInput(prefix, number, sections=None, mandatory=None):
	return CourseInput(Course(prefix, number), sections, mandatory)
	
courseInput = [
	CInput('ma', 322, [1,2,3,4], True),
	CInput('cs', 485), # variable credit
	CInput('arc', 101), # multiple instructors
	CInput('cs', 215, list(range(1,8))),
	CInput('phy', 231),
	CInput('ma', 213),
	CInput('bio', 209),
	CInput('che', 226),
	CInput('eco', 201)] # TBD class times

configData = ConfigurationData("Fall", 2018, 14, 17)
for c in courseInput:
	failure = configData.AddCourse(c)
	if failure:
		print(failure)
		continue
		
from WebsiteInterface import WebsiteInterface
from copy import deepcopy
iWebsite = WebsiteInterface()
courseInfoList = []
for c in configData.CourseInput:
	info = iWebsite.RequestInfoAboutCourse(c.Course, configData.Semester, configData.Year)
	courseInfoList.append(info)
	
# distinguish between mandatory and optional courses
mandatoryCourses = []
optionalCourses = []
# remove sections found in the catalog that aren't in the input
for cInfo in courseInfoList:
	cInfo = deepcopy(cInfo)
	cInput = next((c for c in configData.CourseInput if c.Course == cInfo.Course), None)
	if not cInput:
		continue 
	if len(cInput.SectionNumbers) > 0: # todo: remove when done testing because normally this would mean 'I don't want any sections' but for now it means all sections are good
		cInfo.Sections[:] = [s for s in cInfo.Sections if s.SectionNumber in cInput.SectionNumbers]
	if cInput.Mandatory:
		mandatoryCourses.append(cInfo)
	else:
		optionalCourses.append(cInfo)

from Scheduler import ScheduleList, CourseBlock
from time import perf_counter as tick
now = tick()
scheduleList = ScheduleList(configData.MinCredits, configData.MaxCredits, [CourseBlock(mandatoryCourses, True, len(mandatoryCourses))], [CourseBlock(optionalCourses, False)])
elapsed = tick() - now
print(str(len(scheduleList)) + ' schedules found')
print("completed in " + str(elapsed) + ' seconds')

from ScheduleViewer import ScheduleViewer
viewer = ScheduleViewer(scheduleList, [c.Course for c in optionalCourses])
