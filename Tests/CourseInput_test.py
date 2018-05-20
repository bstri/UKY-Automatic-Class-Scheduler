import sys, os
sys.path.append("E:\\GitHub\\UKY-Automatic-Class-Scheduler")

from CourseInput import CourseInput as ci
#import CourseInput as ci
def equal(ci, prefix, number, sections=None, mandatory=False):
	assert ci.CoursePrefix == prefix
	assert ci.CourseNumber == number
	assert len(ci.SectionNumbers) == (sections and len(sections) or 0)
	assert ci.Mandatory == mandatory

def Test(input, *args, **kwargs):
	assert equal(ci.Parse(input), *args, **kwargs)

def test_ParseSimpleNoSpace():
	Test("MA322", "MA", 322)
def test_ParseSimpleSpace():
	Test("MA 310", "MA", 310)
def test_ParseSimpleDash():
	Test("MA-100", "MA", 100)

def test_ParseSimpleLower():
	Test("ma 322", "MA", 322)

# TODO Do we actually need Parse? (If so, test section #s and Mandatory argument)
