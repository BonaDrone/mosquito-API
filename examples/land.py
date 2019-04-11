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

	It triggers a land 20 seconds after connecting with the Mosquito
	"""
	Mosquito = mapi.Mosquito()
	Mosquito.connect()
	# Useful to visually check if connection was properly established
	Mosquito.set_leds(red=1)

	time.sleep(20)

	Mosquito.land()
	Mosquito.set_leds(red=0)
	
	# Disconnect from the mosquito when finished
	Mosquito.disconnect()

if __name__ == "__main__":
	main()
