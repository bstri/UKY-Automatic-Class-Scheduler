import sys, os
sys.path.append("E:\\GitHub\\UKY-Automatic-Class-Scheduler")

from CourseInput import CourseInput as ci
from CourseInput import Course

def equal(ci, course, sections=None, mandatory=False):
	assert ci.Course == course
	assert len(ci.SectionNumbers) == (sections and len(sections) or 0)
	assert ci.Mandatory == mandatory

def test_ParseSimple():
	assert equal(ci.Parse("MA 310"), Course("MA", 310)) is None
