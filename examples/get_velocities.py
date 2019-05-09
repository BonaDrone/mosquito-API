#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 05-06-2019

import sys
# Add parent folder to path so that the API can be imported.
# This shouldn't be required if the package has been installed via pip
sys.path.insert(0, '../')
sys.path.insert(0, '../mosquito/')

import mapi
import time
import math
import argparse

# Command line arguments
parser = argparse.ArgumentParser(description='Mosquito get linear velocities')
parser.add_argument('-s','--save', type=int, action='store', help="CSV data storage")
parser.add_argument('-d','--duration', type=int, action='store', help="data log duration in seconds")
parser.add_argument('-t','--timestamp', type=int, action='store', help="store time stamp of measures")

args = parser.parse_args()

class SharedState():
	"""
	Class used to store the data file
	"""
	def __init__(self):
		self.file = None

def cleanup(shared_state):
	"""
	Prevent file from remaining open when interrupting the data log
	via Keyboard Interrupt 
	"""
	if shared_state.file:
		shared_state.file.close()

def main(shared_state, save_data, duration, timestamp):
	"""
	Function that gets executed when the script is directly
	called from the command line.

	What it does is request the linear velocities of the Mosquito
	and print them to the command line. If requested, velocities
	are also stored in a csv file
	"""
	Mosquito = mapi.Mosquito()
	Mosquito.connect()
	
	log = True
	intial_time = time.time()
	
	if save_data:
		shared_state.file = open("velocities.csv", "w") 

	while log:	
		velocities = Mosquito.get_velocities()
		if isinstance(velocities, tuple):
			if timestamp:
				velocities = tuple([time.time() - intial_time] + list(velocities))
			# print velocities to terminal so that one can see what's being stored
			print(velocities)
			# write velocities to csv if requested
			if save_data:
				shared_state.file.write(",".join(map(str, velocities)) + "\n")

		if duration:
			log = time.time() - intial_time < duration

	if save_data:
		shared_state.file.close()

if __name__ == "__main__":
	shared_state = SharedState()
	try:
		main(shared_state, args.save, args.duration, args.timestamp)
	except KeyboardInterrupt:
		cleanup(shared_state)
