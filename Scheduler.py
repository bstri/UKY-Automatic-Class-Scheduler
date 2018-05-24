from copy import copy, deepcopy
from itertools import chain, combinations

class Schedule:
	'''Info about a class schedule'''
	
	def __init__(self):
		self.NumCredits = 0
		self.Sections = []
		self.AverageStartTime = None
		self.AverageEndTime = None
		
	def SectionFits(self, section):
		for s in self.Sections:
			if s.OverlapsWith(section):
				return False
		return True	
	
	def AddSection(self, section):
		self.Sections.append(section)
		self.NumCredits += section.NumCredits
		# todo: update average start and end times
		
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

class ScheduleList:
	'''Contains and generates a list of schedules'''
	
	def __init__(self, optionalCourses, mandatoryCourses, minCredits, maxCredits):
		self.Schedules = []

		numMandatoryCredits = 0
		# get all schedules that (only) contain each mandatory course
		rootSchedules = makeScheduleTree(Schedule(), mandatoryCourses)
		if len(rootSchedules) > 0: 
			numMandatoryCredits = rootSchedules[0].NumCredits
		elif len(mandatoryCourses) > 0:
			return "No schedules found containing the specified mandatory courses."

		# check if the mandatory schedules (if there are any) can be standalone schedules
		if numMandatoryCredits >= minCredits:
			if numMandatoryCredits > maxCredits:
				return "Specified mandatory courses exceed given credit maximum"
			else:
				self.Schedules = rootSchedules

		if len(optionalCourses) == 0:
			return
		
		minCredits -= numMandatoryCredits
		maxCredits -= numMandatoryCredits
			
		# NOTE: This next part is an optimization and is not necessary. It leads to fewer calls of combinations() below
		# sort remaining (non-mandatory) courses by descending num credits
		optionalCourses.sort(key=lambda c: c.NumCredits, reverse=True)
		# the credit sum of the first m of these sorted courses gets a lower bound on the number of courses we need to add to each schedule in schedules
		# m will be at least 1, which prevents any schedule overlap with mandatory-only schedules
		creditSum = 0
		for i,c in enumerate(optionalCourses):
			creditSum += c.NumCredits
			if creditSum >= minCredits:
				lowerCombinationBound = i + 1
				break
		if not lowerCombinationBound:
			return
		# the last n of these sorted courses gets an upper bound
		creditSum = 0
		upperCombinationBound = len(optionalCourses)
		for i,c in enumerate(reversed(optionalCourses)):
			creditSum += c.NumCredits
			if creditSum > maxCredits:
				upperCombinationBound -= (i + 1)
				break
		if upperCombinationBound < lowerCombinationBound:
			# e.g. 5-6 credits; [4,4,3]. Lower is 2 and upper is 1. No schedules are possible
			return
				
		# form an iterable that contains all m- through n-combinations of the courses in optionalCourses
		combos = chain.from_iterable(combinations(optionalCourses, r) for r in range(lowerCombinationBound, upperCombinationBound + 1)) 

		# for each combination, make sure num credits is valid, and only add schedules that use all the courses in the combination, to prevent overlap
		for i in range(len(rootSchedules)):
			for c in combos:
				creditSum = 0
				for course in c:
					creditSum += course.NumCredits
				if not (minCredits <= creditSum <= maxCredits):
					continue
				self.Schedules += makeScheduleTree(rootSchedules[i], list(c))
			
	def __str__(self):
		return '\n'.join(map(str, self.Schedules))
		
	def SortByNumCredits(self, descending=False):
		self.Schedules.sort(key=lambda s: s.NumCredits, reverse=descending)