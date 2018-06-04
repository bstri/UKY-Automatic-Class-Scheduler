from copy import copy, deepcopy
from datetime import datetime
from itertools import chain, combinations, product
from Courses import CourseInfo

class Schedule:
	'''Info about a class schedule'''
	
	def __init__(self):
		self.NumCredits = 0
		self.Sections = []
		self.EarliestStartTimeToStr = None
		self.LatestEndTimeToStr = None
		self.EarliestStartTime = datetime.strptime("11:59 pm", "%I:%M %p")
		self.LatestEndTime = datetime.strptime("12:00 am", "%I:%M %p")
		
	def setStartTime(self, t):
		self.EarliestStartTime = t
		self.EarliestStartTimeToStr = t.strftime('%I:%M%p')
		
	def setEndTime(self, t):
		self.LatestEndTime = t
		self.LatestEndTimeToStr = t.strftime('%I:%M%p')
		
	def SectionFits(self, section):
		for s in self.Sections:
			if s.OverlapsWith(section):
				return False
		return True	
	
	def AddSection(self, section):
		self.Sections.append(section)
		self.NumCredits += section.NumCredits
		if self.EarliestStartTime > section.EarliestStartTime:
			self.setStartTime(section.EarliestStartTime)
		if self.LatestEndTime < section.LatestEndTime:
			self.setEndTime(section.LatestEndTime)
		
	def __str__(self):
		return '; '.join(['{}-{}'.format(str(s.Course), str(s.SectionNumber)) for s in self.Sections]) 
	
	def __deepcopy__(self, memo):
		cls = self.__class__
		result = cls.__new__(cls)
		# memo[id(self)] = result # Don't care about the memo because there is no recursive structure
		for k, v in self.__dict__.items():
			setattr(result, k, copy(v)) # self.Sections doesn't need a deep copy
		return result

def makeScheduleTree(rootSchedule, courseInfoList):
	if len(courseInfoList) == 0:
		return []
	schedules = []
	_scheduleTreeHelper(rootSchedule, courseInfoList, schedules)
	return schedules	
def _scheduleTreeHelper(rootSchedule, courseInfoList, schedules):
	if len(courseInfoList) == 0:
		schedules.append(rootSchedule)
		return
	for s in courseInfoList[0].Sections:
		if rootSchedule.SectionFits(s):
			cpy = deepcopy(rootSchedule)
			cpy.AddSection(s)
			_scheduleTreeHelper(cpy, courseInfoList[1:], schedules)

class ScheduleList(list):
	'''A list of generated schedules'''
	
	def __init__(self, minCredits, maxCredits, mandatoryBlocks=[], optionalBlocks=[]):
		# get all schedules that satisfy the mandatory blocks
		numCreditsToRootSchedules = {0:[Schedule()]}
		for block in mandatoryBlocks:
			if len(block) == 0:
				continue
			combos = combinations(block, block.Count)
			numCreditsToLeafSchedules = {}
			for c in combos:
				comboCreditSize = sum(course.NumCredits for course in c)
				for k,v in numCreditsToRootSchedules.items():
					newNumCredits = k + comboCreditSize
					if not numCreditsToLeafSchedules.get(newNumCredits):
						numCreditsToLeafSchedules[newNumCredits] = []
					for s in v:
						numCreditsToLeafSchedules[newNumCredits].extend(makeScheduleTree(s,c))
			if len(numCreditsToLeafSchedules) == 0:
				print("No schedules found containing the specified mandatory courses.")
				return
			numCreditsToRootSchedules = numCreditsToLeafSchedules
			
		iterables = []
		for block in optionalBlocks:
			iterables.append(list(block.Count and combinations(block, block.Count) or chain.from_iterable(combinations(block, r) for r in range(len(block) + 1))))
		# Tried limiting which all combinations were tested, but it produced only a small speed increase
		allCombinations = list(product(*iterables))
		
		for credits,rootSchedules in numCreditsToRootSchedules.items():
			# check if the mandatory schedules (if there are any) can be standalone schedules
			if credits >= minCredits:
				if credits > maxCredits:
					continue
				else:
					self.extend(rootSchedules)

			if not optionalBlocks:
				continue
		
			branchMinCredits = minCredits - credits
			branchMaxCredits = maxCredits - credits
			
			# for each combination, make sure num credits is valid, and only add schedules that use all the courses in the combination, to prevent overlap
			for i in range(len(rootSchedules)):
				for c in allCombinations:
					c = list(chain.from_iterable(c)) # flatten this tuple of tuples so you just have the courses
					if not (branchMinCredits <= sum(course.NumCredits for course in c) <= branchMaxCredits):
						continue
					self.extend(makeScheduleTree(rootSchedules[i], c))
			
	def __str__(self):
		return '\n'.join(map(str, self))
		
class CourseBlock(list):
	'''A list of CourseInfo with scheduling data'''
	
	def __init__(self, courses, mandatory, count=None):
		self.extend(courses)
		self.Mandatory = mandatory
		self.Count = count # None means 'any'; if mandatory is true this is not allowed
		if not count:
			self.MinCredits = 0
			self.MaxCredits = sum(c.NumCredits for c in courses)
		else:
			self.sort(key = lambda c: c.NumCredits, reverse=True)
			self.MaxCredits = sum(c.NumCredits for c in self[:count])
			self.MinCredits = sum(c.NumCredits for c in self[-count:])
			
class VariableCreditCourseBlock(CourseBlock):
	'''A course block except a list of sections related to one course'''
	
	def __init__(self, sections, mandatory, count):
		courses = [CourseInfo(s.Course, [s], s.NumCredits) for s in sections]
		super().__init__(courses, mandatory, count)