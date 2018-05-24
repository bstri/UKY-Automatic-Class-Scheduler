import sys, os
sys.path.append("E:\\GitHub\\UKY-Automatic-Class-Scheduler")

from Courses import *
from datetime import datetime

def equal(ci, course, sections=None, mandatory=False):
	assert ci.Course == course
	assert len(ci.SectionNumbers) == (sections and len(sections) or 0)
	assert ci.Mandatory == mandatory

def test_ParseSimple():
	assert equal(CourseInput.Parse("MA 310"), Course("MA", 310)) is None


def time(s): # ex, s="15:30"
	return datetime.strptime(s, "%H:%M")

def test_ClassMeetingOverlapsSame():
	args = ['M', time("9:30"), time("11:30"), "loc", "prof"]
	assert ClassMeeting(*args).OverlapsWith(ClassMeeting(*args)) is True

def test_ClassMeetingOverlaps():
	args = []
	assert (ClassMeeting('M', time("9:30"), time("11:30"), "loc", "prof").OverlapsWith(
		ClassMeeting('M', time("10:30"), time("11:00"), "loc2", "prof2"))) is True

def test_ClassMeetingOverlapDifDays():
	args = []
	assert (ClassMeeting('M', time("9:30"), time("11:30"), "loc", "prof").OverlapsWith(
		ClassMeeting('T', time("11:30"), time("12:00"), "loc2", "prof2"))) is False