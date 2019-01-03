#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 12-20-2018

import sys
# Add parent folder to path so that the API can be imported.
# This shouldn't be required if the package has been installed via pip
sys.path.insert(0, '../')

from mosquito import mapi

def main():
	Mosquito = mapi.Mosquito()
	Mosquito.connect()
	while True:
		try:
			print(Mosquito.get_attitude())
		except KeyboardInterrupt:
			# Disconnect from the mosquito when quitting
			Mosquito.disconnect()
			# quit
			sys.exit()

if __name__ == "__main__":
	main()
