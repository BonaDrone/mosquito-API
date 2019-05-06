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
import argparse

# Command line arguments
parser = argparse.ArgumentParser(description='Mosquito get linear velocities')
parser.add_argument('-s','--save', type=int, action='store', help="CSV data storage")
parser.add_argument('-d','--duration', type=int, action='store', help="data log duration in seconds")
parser.add_argument('-t','--timestamp', type=int, action='store', help="store time stamp of measures")
args = parser.parse_args()

class SharedState():
	def __init__(self):
		self.file = None

def main(shared_state, save_data, duration, timestamp):
	"""
	Function that gets executed when the script is directly
	called from the command line.

	What it does is request the linear velocities of the Mosquito
	and print it to the command line.
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
			# print to terminal so that one can see what's being stored
			print(velocities)
			# write velocities to csv
			if save_data:
				shared_state.file.write(",".join(map(str, velocities)) + "\n")

		if duration:
			log = time.time() - intial_time < duration

		time.sleep(0.1)
	if save_data:
		shared_state.file.close()

def cleanup(shared_state):
	if shared_state.file:
		shared_state.file.close()

if __name__ == "__main__":
	shared_state = SharedState()
	try:
		main(shared_state, args.save, args.duration, args.timestamp)
	except KeyboardInterrupt:
		cleanup(shared_state)
