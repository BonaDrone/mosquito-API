#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 1-4-2019

import sys
# Add parent folder to path so that the API can be imported.
# This shouldn't be required if the package has been installed via pip
sys.path.insert(0, '../')

import time
from mosquito import mapi

def main():
	Mosquito = mapi.Mosquito()
	Mosquito.connect()

	# Set motors to a 10% power
	Mosquito.set_motor(1, 0.1)
	time.sleep(1)
	Mosquito.set_motor(1, 0.0)
	Mosquito.set_motor(2, 0.1)
	time.sleep(1)
	Mosquito.set_motor(2, 0.0)
	Mosquito.set_motor(3, 0.1)
	time.sleep(1)
	Mosquito.set_motor(3, 0.1)
	Mosquito.set_motor(4, 0.1)
	time.sleep(1)
	Mosquito.set_motor(4, 0.0)

	# Disconnect from the mosquito when quitting
	Mosquito.disconnect()

if __name__ == "__main__":
	main()
