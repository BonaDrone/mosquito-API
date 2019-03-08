#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 02-25-2019

import sys
# Add parent folder to path so that the API can be imported.
# This shouldn't be required if the package has been installed via pip
sys.path.insert(0, '../')
sys.path.insert(0, '../mosquito/')

from mosquito import mapi
import time

def main():
	"""
	Function that gets executed when the script is directly
	called from the command line.

	What it does is set on and off the LEDs of the board at
	2 seconds intervals
	"""
	Mosquito = mapi.Mosquito()
	Mosquito.connect()

	# turn on and off the LEDs of the board at 2 second intervals
	# Note how, since the method expects keyword arguments, the order
	# in which they are passed doesn't matter. If any of the LEDs is
	# omitted its current status is preserved
	Mosquito.set_leds(red=0, green=0, blue=0)

	print("Turning on blue Led...")
	Mosquito.set_leds(blue=1) # The status of the other LEDs is preserved

	time.sleep(2)

	Mosquito.set_leds(blue=0)
	print("Turning on red Led...")
	Mosquito.set_leds(red=1)
	
	time.sleep(2)
	
	Mosquito.set_leds(red=0)
	print("Turning on green Led...")
	Mosquito.set_leds(green=1)
	
	time.sleep(2)
	
	Mosquito.set_leds(green=0)
	print("Turning on all three Leds...")
	Mosquito.set_leds(blue=1, red=1, green=1)
	
	time.sleep(2)
	
	Mosquito.set_leds(blue=0, red=0, green=0)

	time.sleep(0.1)

	# Disconnect from the mosquito when finished
	Mosquito.disconnect()

if __name__ == "__main__":
	main()
