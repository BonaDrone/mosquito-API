#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 12-20-2018

import sys
# Add parent folder to path so that the API can be imported.
# This shouldn't be required if the package has been installed via pip
sys.path.insert(0, '../')
sys.path.insert(0, '../mosquito/')

import mapi
import time
import math

def main():
	"""
	Function that gets executed when the script is directly
	called from the command line.

	What it does is ask the Mosquito for its attitude and,
	once received, it sets the motors to a 20% power if the
	absolute values of roll and pitch are above 20 degrees
	and 0 otherwise.
	"""
	Mosquito = mapi.Mosquito()
	Mosquito.connect()

	while True:
		# by default attitude is received in radians
		attitude = Mosquito.get_attitude(degrees=True)
		
		if isinstance(attitude, tuple):

			print(attitude)

			if abs(attitude[0]) > 20 or abs(attitude[1]) > 20:
				Mosquito.set_motors([0.2,0.2,0.2,0.2])

			else:
				Mosquito.set_motors([0,0,0,0])
		
		time.sleep(0.1)

if __name__ == "__main__":
	main()
