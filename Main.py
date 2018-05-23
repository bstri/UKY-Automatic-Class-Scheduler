from WebsiteInterface import WebsiteInterface
from Scheduler import ScheduleList
import pickle
from datetime import datetime, timedelta

# ------------- TESTING STUFF --------------
from ConfigurationData import ConfigurationData
from Courses import CourseInput, Course

def CInput(prefix, number, sections=None, mandatory=None):
	return CourseInput(Course(prefix, number), sections, mandatory)
	
courseInput = [
	CInput('ma', 322, [1,2,3,4], True),
	CInput('cs', 315),
	CInput('ma', 415, [1], True),
	CInput('cs', 215, list(range(1,8))),
	CInput('phy', 231)]

configData = ConfigurationData("Fall", 2018, 14, 17)
for c in courseInput:
	failure = configData.AddCourse(c)
	if failure:
		print(failure)
		continue
		
# get info from cache, if available
try:
	f = open('catalogcache', 'rb')
except IOError: # couldn't open file
	cachedDict = {}
	lastRetrievalDict = {}
else:
	try:
		cachedDict = pickle.load(f)
	except EOFError: # didn't read anything
		cachedDict = {}
		lastRetrievalDict = {}
	else:
		lastRetrievalDict = pickle.load(f)
	f.close()
iWebsite = WebsiteInterface()
courseInfoList = []
now = datetime.utcnow()
EXPIRY = timedelta(hours=1)
needsRecaching = False
for c in configData.CourseInput:
	courseName = str(c.Course)
	info = cachedDict.get(courseName)
	recency = lastRetrievalDict.get(courseName)
	if not info or now > recency + EXPIRY: # get info from internet if cache is out of date
		needsRecaching = True
		info = iWebsite.RequestInfoAboutCourse(c.Course, configData.Semester, configData.Year)
		if type(info) is str:
			print("Error occurred when getting info for ", c, ": \n", info)
			continue
		cachedDict[courseName] = info
		lastRetrievalDict[courseName] = now
	courseInfoList.append(info)
# cache new info
if needsRecaching:
	with open('catalogcache', 'wb') as f:
		pickle.dump(cachedDict, f, pickle.HIGHEST_PROTOCOL)
		pickle.dump(lastRetrievalDict, f, pickle.HIGHEST_PROTOCOL)
	
# distinguish between mandatory and optional courses
mandatoryCourses = []
optionalCourses = []
# remove sections found in the catalog that aren't in the input
for cInfo in courseInfoList:
	cInput = next((c for c in configData.CourseInput if c.Course == cInfo.Course), None)
	if not cInput:
		continue 
	if len(cInput.SectionNumbers) > 0: # todo: remove when done testing because normally this would mean 'I don't want any sections' but for now it means all sections are good
		cInfo.Sections[:] = [s for s in cInfo.Sections if s.SectionNumber in cInput.SectionNumbers]
	if cInput.Mandatory:
		mandatoryCourses.append(cInfo)
	else:
		optionalCourses.append(cInfo)
# ------------- END TESTING STUFF ---------------

scheduleList = ScheduleList(optionalCourses, mandatoryCourses, configData.MinCredits, configData.MaxCredits)
print(scheduleList)
