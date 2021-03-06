#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 04-11-2019

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

	This scripts makes the Mosquito perform a simple flight that
	consists in taking off at 100 cm, hovering for 2 seconds and landing.
	"""
	Mosquito = mapi.Mosquito()
	Mosquito.connect()
	# Useful to visually check if connection was properly established
	Mosquito.set_leds(red=1)
	time.sleep(2)
	Mosquito.set_leds(red=0)

	# Set of actions to be executed by the Mosquito:
	# Take off at 100 cm, hover for 2 seconds and land
	Mosquito.arm()
	time.sleep(0.5)
	Mosquito.take_off(100) # height is in cm
	Mosquito.hover(2) # hover duration is in seconds
	Mosquito.land() # land doesn't take any parameters
	time.sleep(0.5)
	Mosquito.disarm()

	# disconnect
	Mosquito.disconnect()

if __name__ == "__main__":
	main()
