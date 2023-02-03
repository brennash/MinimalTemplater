import re
import sys
import yaml
import json
import logging
import unittest
import datetime
from MinimalTemplater import MinimalTemplater

class Test(unittest.TestCase):

	def setUp(self):
		self.templater = MinimalTemplater('conf/config.ini')

	def test_MarkdownLink_1(self):
		paragraph = "This is a [test](https://www.test.com) for links"
		expected = 'This is a <a href="https://www.test.com">test</a> for links'
		actual = self.templater.replace_links(paragraph)
		self.assertEquals(expected, actual)

	def test_MarkdownLink_2(self):
		paragraph =  "This is a [test](https://www.test.com) for links "
		paragraph += "and another [test2](https://www.test2.com) for other [links](http://www.link.com)."
		expected =  'This is a <a href="https://www.test.com">test</a> for links'
		expected += 'and another <a href="https://www.test2.com">test</a> for other <a href="http://www.link.com">links</a>.'
		actual = self.templater.replace_links(paragraph)

		print("==================")
		print(actual)
		print("==================")

		self.assertEquals(expected, actual)


