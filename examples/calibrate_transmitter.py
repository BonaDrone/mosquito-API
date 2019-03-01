#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 03-01-2019

import sys
# Add parent folder to path so that the API can be imported.
# This shouldn't be required if the package has been installed via pip
sys.path.insert(0, '../')
sys.path.insert(0, '../mosquito/')

from mosquito import mapi
import time

class TXCalibration(object):
	"""
	Class to perform TX Calibration
	"""
	def __init__(self):
		"""
		Initialize the TX Calibration class
		"""
		self.__calibration = True
		self.Mosquito = mapi.Mosquito()

	def _change_stage(self, stage):
		"""
		Change the calibration stage between 0,1 and 2
		"""
		Mosquito.calibrate_transmitter(stage)

	def perform_calibration(self, stage):
		"""
		Handle switching between different calibration stages and
		print the appropriate messages to indicate what is going on.
		"""
		keep_calibrating = True

		if stage not in range(3):
			print("Invalid calibration stage. Stages should be 0, 1 or 2")

		elif stage == 0:
			print("Calibration stage 0:")
			print("Keep LEFT stick at MINIMUM and RIGHT stick at REST!")
			time.sleep(2)
			print("Calibrating...")
			self._change_stage(0)
			time.sleep(7)

		elif stage == 1:
			print("Calibration stage 1:")
			print("MOVE all the STICKS RANDMONLY between its MAX and MIN values")
			self._change_stage(1)
			print("Calibrating...")
			time.sleep(7)

		elif stage == 2:
			print("Exiting calibration...")
			self._change_stage(2)
			time.sleep(1)
			keep_calibrating = False

		return keep_calibrating

	def calibrate(self):
		"""
		Begin and control the calibration process flow
		"""
		self.Mosquito.connect()
		print("Please check that the RED LED turns on. If not, connection with the Mosquito wasn't successful")
		self.Mosquito.set_leds(red=1)
		time.sleep(3)
		self.Mosquito.set_leds(red=0)

		print("TX Calibration stages:")
		print("0 - Throttle minimum and Roll, Pitch and Yaw center")
		print("1 - Throttle maximun and Roll Pitch and Yaw center") 
		print("2 - End Calibration")

		self.__calibration = True

		while self.__calibration:
			stage = eval(input("Enter a calibration stage (0,1 or 2):"))
			self.__calibration = perform_calibration(stage)

		self.Mosquito.disconnect()
		print("Transmitter calibration finished")


def main():
	"""
	Function that gets executed when the script is directly
	called from the command line.
	"""
	tx_calibrate = TXCalibration()
	tx_calibrate.calibrate()

if __name__ == "__main__":
	main()