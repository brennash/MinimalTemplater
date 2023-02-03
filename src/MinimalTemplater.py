import re
import os
import sys
import enum
import yaml
import datetime
import configparser
from jinja2 import Template
from optparse import OptionParser

class MinimalTemplater:

	def __init__(self, config_filename):
		# Initialise the config parser
		config = configparser.RawConfigParser()
		config.read(config_filename)

		# Metadata dict
		self.metadata_dict = {}

		# Blog config settings
		self.blog_config = dict(config.items('BLOG'))

		# Links
		self.links = dict(config.items('LINKS'))
		self.twitter_url = self.links['twitter_url']
		self.home_url = self.links['home_url']

	def run(self, markdown_filename):
		"""
		The main execution loop which does the following,
		- Reads the metadata preamble in the markdown into a dict.
		"""
		meta_dict = self.get_markdown_metadata(markdown_filename)
		#html = self.create_html(meta_dict, markdown_filename)
		print(meta_dict)
		#self.load_templates(title, page_body)


	def get_markdown_metadata(self, markdown_filename):
		"""
		Returns the metadata header from the markdown file, basically
		anything that's between the dashed lines at the top of the file.
		"""
		start = -1
		end = -1
		delim = re.compile("^-+$")

		yaml_data = ""

		# Open the file for reading
		markdown_file = open(markdown_filename, "r")

		# Read the file into memory
		for index, input_line in enumerate(markdown_file):
			line = input_line.strip()
			if delim.match(line):
				if start == -1:
					start = index
				else:
					end = index
					break
			else:
				yaml_data += line + "\n"
		return yaml.safe_load(yaml_data)


	def create_html(self, metadata, markdown_filename):
		start = -1
		end = -1
		delim = re.compile("^-+$")

		markdown_data = []

		# Open the file for reading
		markdown_file = open(markdown_filename, "r")

		# Read the markdown portion of the file into an array of strings
		for index, input_line in enumerate(markdown_file):
			line = input_line.strip()
			if end == -1:
				if delim.match(line):
					if start == -1:
						start = index
					else:
						end = index
			else:
				markdown_data.append(line.strip())

		# Process the array of strings line by line
		html_body = ""
		state = "STATE::TEXT"
		paragraph = ""

		# The line regexes
		header_regex = re.compile("^#\s*\w+.*$")
		bullet_regex = re.compile("^\*{1,2}\s*\w+.*$")
		text_regex = re.compile("^[A-Za-z0-9]+.*$")
		empty_regex = re.compile("^\s*$")

		for line_num, line in enumerate(markdown_data):
			line_len = len(line)

			if state == "STATE::TEXT" and header_regex.match(line):
				html_body += self.get_header(line) + "\n\n"
				state = "STATE::TEXT"

			elif state == "STATE::TEXT" and text_regex.match(line):
				paragraph += line + " "
				state = "STATE::TEXT"

			elif state == "STATE::TEXT" and bullet_regex.match(line):
				if len(paragraph) > 0:
					html_body += "<p>" + paragraph.strip()  + "</p>\n"
					paragraph = ""
				html_body += "<ul>" + "\n"
				html_body += "  <li>" + self.get_bullet(line) + "</li>\n"
				state = "STATE::LIST"

			elif state == "STATE::LIST" and text_regex.match(line):
				paragraph += line + " "
				state = "STATE::TEXT"

			elif state == "STATE::TEXT" and empty_regex.match(line):
				if len(paragraph) > 0:
					html_body += "<p>" + paragraph.strip() +"</p>\n\n"
					paragraph = ""
				state = "STATE::TEXT"

			elif state == "STATE::LIST" and bullet_regex.match(line):
				html_body += "  <li>" + self.get_bullet(line) + "</li>\n"
				state = "STATE::LIST"

			elif state == "STATE::LIST" and empty_regex.match(line):
				html_body += "</ul>\n\n"

			elif state == "STATE::CODE" and line == "```":
				state = "STATE::TEXT"
				html_body += "</code></pre>\n\n"

			elif state == "STATE::CODE" and text_regex.match(line):
				state = "STATE::CODE"
				html_body += line+" "

			elif state == "STATE::TEXT" and line == "```":
				if len(paragraph) > 0:
					html_body += "<p>" + paragraph.strip() +"</p>\n\n"
					paragraph = ""
				html_body += "<pre><code>"
				state = "STATE::CODE"

		if len(paragraph) > 0:
			html_body += "<p>" + paragraph.strip() +"</p>\n\n"
		elif state == "STATE::LIST":
			html_body += "</ul>\n\n"
		elif state == "STATE::CODE":
			html_body += "</code></pre>\n\n"

		return html_body



	def load_templates(self, title, page_body):
		"""
		Load the templates
		"""
		blog_page_template_file = self.blog_config['blog_page_template_file']
		with open(blog_page_template_file) as blog_page_file:
			blog_page_template = Template(blog_page_file.read())
		print(blog_page_template.render(page_title=title, page_body=page_body))


	def load_markdown(self, markdown_filename):
		# The HTML returned
		html = ""

		# Open the file for reading
		markdown_file = open(markdown_filename, "r")

		# The list containing the line-by-line markdown
		markdown = []

		# Read the file into memory
		for input_line in markdown_file:
			line = input_line.strip()
			markdown.append(input_line)

		# Returns a dict of the page metadata
		metadata = self.get_page_metadata(markdown)

		return metadata, markdown

	def replace_links(self, paragraph):
		"""
		Replace the markdown style links with html tags.
		"""
		result = ""
		link_list = []
		start = 0
		end = 0
		prev_end = 0
		link_regex = re.compile("\[{1}\w+\s*.+\]{1}\({1}(http://|https://)[a-z-.:0-9]+\){1}")
		for match in re.finditer(link_regex, paragraph):
			start = match.start()
			end = match.end()
			print("START/END",start,",",end)
			markdown_link = paragraph[start:end]
			link = markdown_link.split('(')[-1][:-1]
			link_text = markdown_link.split(']')[0][1:]
			html = '<a href="{0}">{1}</a>'.format(link, link_text)
			result += paragraph[prev_end:start]
			result += html
			prev_end = end
		result += paragraph[prev_end:]
		return result


	def get_bullet(self, line):
		"""
		Given a bulleted markdown list, this function
		extracts and cleans the list item, returning it
		as a string
		:param line: A bulleted markdown string.
		:return: The string value of the bulleted item.
		"""
		text = line.split("*")[-1].strip()
		return text


	def get_header(self, line):
		"""
		The get_header function takes a markdown header symbol
		and converts it to a html header <h1> to <h4> depending 
		on the number of hash symbols designating the prominence of
		the header.
		:param line: A markdown header line, which should start with a hash symbol.
		:return: A html snippet with the header title. 
		"""
		level = line.count("#")
		title = line.split("#")[-1].strip()
		if level == 1:
			return "<h1>{0}</h1>".format(title)
		if level == 2:
			return "<h2>{0}</h2>".format(title)
		if level == 3:
			return "<h3>{0}</h3>".format(title)
		if level == 4:
			return "<h4>{0}</h4>".format(title)
		else:
			return "<b>{0}</b><br/>".format(title)



def main(argv):
	parser = OptionParser(usage="Usage: MinimalTemplater <markdown-file.md>")
	(options, filename) = parser.parse_args()

	if len(filename) == 1 and os.path.isfile(filename[0]):
		templater = MinimalTemplater('conf/config.ini')
		templater.run(filename[0])
	else:
		parser.print_help()
		sys.exit(1)

if __name__ == "__main__":
	sys.exit(main(sys.argv))


