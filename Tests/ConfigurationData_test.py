from ConfigurationData import ConfigurationData as cd
def test_MinMax():
	assert not cd(minCredits=15, maxCredits=14).FindProblems() is None