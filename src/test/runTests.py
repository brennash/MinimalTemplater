#!/usr/bin/env python3
import os
import sys
import unittest
import all_tests

testPath   = sys.path[0]
pathTokens = testPath.split('/')
srcPath    = '/'.join(pathTokens[0:-1])
sys.path.insert(0,srcPath)
sys.path.insert(1,testPath)
testSuite = all_tests.create_test_suite()
text_runner = unittest.TextTestRunner().run(testSuite)
