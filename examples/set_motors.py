#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 01-04-2019

import sys
# Add parent folder to path so that the API can be imported.
# This shouldn't be required if the package has been installed via pip
sys.path.insert(0, '../')
sys.path.insert(0, '../mosquito/')

import time
import mapi

def main():
	"""
	Function that gets executed when the script is directly
	called from the command line.

	What it does is set each of the 4 motors, one at a time,
	to a 20% power during 1 second.
	"""
	Mosquito = mapi.Mosquito()
	Mosquito.connect()

	# Set motors to a 20% power, one at a time
	Mosquito.set_motor(1, 0.2)

	time.sleep(1)

	Mosquito.set_motor(1, 0.0)
	Mosquito.set_motor(2, 0.2)

	time.sleep(1)

	Mosquito.set_motor(2, 0.0)
	Mosquito.set_motor(3, 0.2)

	time.sleep(1)

	Mosquito.set_motor(3, 0.0)
	Mosquito.set_motor(4, 0.2)

	time.sleep(1)

	Mosquito.set_motor(4, 0.0)

	# Disconnect from the mosquito when finished
	Mosquito.disconnect()

if __name__ == "__main__":
	main()
