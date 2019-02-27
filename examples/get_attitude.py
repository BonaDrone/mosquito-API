#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 12-20-2018

import sys
# Add parent folder to path so that the API can be imported.
# This shouldn't be required if the package has been installed via pip
sys.path.insert(0, '../')
sys.path.insert(0, '../src/')

import mapi
import time
import math

def main():
	"""
	Function that gets executed when the script is directly
	called from the command line.

	What it does is request the attitude of the Mosquito
	and print it to the command line.
	"""
	Mosquito = mapi.Mosquito()
	Mosquito.connect()
	while True:
		attitude = Mosquito.get_attitude()
		if isinstance(attitude, tuple):
			print(tuple(i*180/math.pi for i in attitude))
		time.sleep(0.1)

if __name__ == "__main__":
	main()
