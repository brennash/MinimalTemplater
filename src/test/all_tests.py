import os
import sys
import glob
import unittest
import datetime

def create_test_suite():
	"""
	Runs through the list of unit tests available in the src/test folder, executing
	each in turn. 
	"""

	testFolder       = sys.path[0]
	testFolderTokens = testFolder.split('/')
	moduleStrings    = []

	if testFolderTokens[-1] == 'src':
		testFiles = glob.glob(testFolder+'/test/test_*.py')
		for testFile in testFiles:
			testFileName = testFile.split('/')[-1].replace('.py','')
			moduleStrings.append('test.'+testFileName)
	else:
		testFiles = glob.glob(testFolder+'/test/test_*.py')
		for testFile in testFiles:
			testFileName = testFile.split('/')[-1].replace('.py','')
			moduleStrings.append('test.'+testFileName)

	print('Running Suite of Tests...',datetime.datetime.now())
	suites = [unittest.defaultTestLoader.loadTestsFromName(name) for name in moduleStrings]
	testSuite = unittest.TestSuite(suites)
	return testSuite
