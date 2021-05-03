#!/usr/bin/python3
"""
Title:				Colours
Type:				Helper Module
Purpose:			Prettify the Terminal Output
Last Edited By:		AG | MuirlandOracle
Last Updated:		24/03/21
"""

import sys

class Colours():
	red = "\033[91m"
	green = "\033[92m"
	blue = "\033[34m"
	orange = "\033[33m"
	purple = "\033[35m"
	end = "\033[0m"

	@classmethod
	def success(self, message):
		print(f"{self.green}[+] {message}{self.end}")

	@classmethod
	def warn(self, message):
		print(f"{self.orange}[*] {message}{self.end}")

	@classmethod
	def info(self, message):
		print(f"{self.blue}[*] {message}{self.end}")
	
	@classmethod
	def fail(self, message, die=True):
		print(f"{self.red}[-] {message}{self.end}")

		if die:
			sys.exit(0)
