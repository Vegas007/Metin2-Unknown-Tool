#! /usr/bin/env python
'''
	MIT License
	Copyright (c) 2018 VegaS
	
	LINK PREVIEW : 
		http://i.epvpimg.com/2gvyeab.png
		http://i.epvpimg.com/i0XIdab.png
		http://i.epvpimg.com/hKK8cab.png

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all
	copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.
'''
__author__      = "VegaS"
__date__        = "2018-11-30"
__consignee__   = '#Mithras'
__version__     = "0.1.6"

import os
import sys
import re
import time
import shutil
import operator
import string
import functools
from datetime import datetime as dt

'''
	How-To-use: cd ../main.py location_file_name.msm
'''
class ReadMSM_SourceSkin:
	BACKUP_FOLDER_NAME          = 'backup'
	OUTPUT_FILE_NAME            = 'result.txt'
	
	PATTERN_STRING_WHITESPACE   = string.whitespace[1]
	GROUP_MEMBER_MAX_NUM        = 5

	PATH_STRING_NAME            = 'PathName'
	SOURCE_SKIN_STRING_NAME     = 'SourceSkin'
	SPECIAL_PATH_STRING_NAME    = 'SpecialPath'

	def __init__(self):
		self.outputList = []
		# Contains the command-line arguments passed to the script.
		self.srcReadFileName = sys.argv[1]

	def __GetDateTime(self):
		return dt.now().strftime('%d-%m-%Y %H-%M-%S_{file_name}').format(file_name = self.srcReadFileName) # Return a string representing the date, controlled by an explicit format string. 
		
	def __GetDirectoryName(self):
		return os.path.dirname('{:s}/{:s}/{:s}'.format(os.getcwd(), self.BACKUP_FOLDER_NAME, self.OUTPUT_FILE_NAME)) # Return the directory name of pathname path.

	def __FindStringByPattern(self, string, pattern='''(?<=")\s*[^']+?\s*(?=")'''):
		# A regular expression (or RE) specifies a set of strings that matches it; the functions in this module let you check if a particular string
		# matches a given regular expression (or if a given regular expression matches a particular string, which comes down to the same thing).
		strResult = re.search(pattern, string)
		if strResult:
			return strResult.group().strip().lower()
		return str()

	def __FindStringByLine(self, lines, string, pattern=r'(^|[^\w]){}([^\w]|$)', msmGroupDict={}):
		tokens = []
		for index, value in enumerate(lines):
			value = functools.reduce(lambda k, v: k.replace(v, '\0'), self.PATTERN_STRING_WHITESPACE, value)

			# Recompile the lines and search by unique strings.
			if bool(re.search(re.compile(pattern.format(string), re.IGNORECASE), value)):
				if string is self.PATH_STRING_NAME:
					return value
					
				elif string is self.SOURCE_SKIN_STRING_NAME:
					strExceptLine = lines.__getitem__(operator.isub(index, self.GROUP_MEMBER_MAX_NUM - 2)).strip(self.PATTERN_STRING_WHITESPACE)
					tokens.append((value, strExceptLine if self.SPECIAL_PATH_STRING_NAME in strExceptLine else None))
				
		return tuple(tokens)

	def __OnResult(self):
		textLineTuple = (
			 '[*] Filename: {:s}\n'.format(self.srcReadFileName),
			 '[*] {:s} count: [{:d}]'.format(self.SOURCE_SKIN_STRING_NAME, len(self.outputList))
		)

		if self.outputList:
			if os.path.exists(self.OUTPUT_FILE_NAME):
				# Recursive directory creation function. Like mkdir(), but makes all intermediate-level directories needed to contain the leaf directory.
				if not os.path.exists(self.BACKUP_FOLDER_NAME):
					os.makedirs(self.BACKUP_FOLDER_NAME) 
			
				# Recursively move a file or directory (src) to another location (dst).
				destFileName = '{:s}/{:s}'.format(self.__GetDirectoryName(), self.__GetDateTime())
				shutil.move('{:s}/{:s}'.format(os.getcwd(), self.OUTPUT_FILE_NAME), destFileName)
				
				textLineTuple += tuple('\n[*] Generated a backup for old {:s} in {:s}.'.format(self.OUTPUT_FILE_NAME, destFileName))

			with open(self.OUTPUT_FILE_NAME, 'a+') as fp:
				fp.write(self.PATTERN_STRING_WHITESPACE.join(self.outputList)) # Returns a string in which the string elements of sequence have been joined by str separator.

		print functools.reduce(lambda k, v: operator.iadd(k, v), textLineTuple) # Same as join method.

	def Initialize(self):
		try:
			lines = open(self.srcReadFileName, "r").readlines()
		except IOError:
			print ("Can't load file: {:s}".format(self.srcReadFileName))
			return

		for sourceSkin, specialPath in self.__FindStringByLine(lines, self.SOURCE_SKIN_STRING_NAME):
			strPathName = self.__FindStringByPattern(self.__FindStringByLine(lines, self.PATH_STRING_NAME))
			strSourceSkin = self.__FindStringByPattern(sourceSkin)
			if specialPath:
				strPathName = self.__FindStringByPattern(specialPath)

			self.outputList.append(operator.iadd(strPathName, strSourceSkin))

		self.__OnResult()
			
Instance = ReadMSM_SourceSkin()
Instance.Initialize()