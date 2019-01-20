#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 12-12-2018

import time
import msppg
from .coms import MosquitoComms


class Mosquito(MosquitoComms):
	"""
	API object to communicate with a Mosquito via WiFi
	based on MSP messages. 

	The laptop should be connected to the Mosquito's Wifi.
	MSP message handling is delegated to Simon D. Levy's 
	Hackflight's MSP Parser. 

	For further info see: 
		https://github.com/simondlevy/Hackflight/tree/master/extras/parser
	"""

	def __init__(self):
		"""
		Initialize the WiFi communications class 
		"""
		super(Mosquito, self).__init__()
		# Mosquito's status vars
		self.__roll_pitch_yaw = [0]*3
		self.__motor_values = [0]*4

	# Message handlers
	def __handle_attitude(self, x, y, z):
		self.__roll_pitch_yaw = x, -y, z

	# Public methods
	def arm(self):
		"""
		Arm the Mosquito
		"""
		self._send_data(msppg.serialize_SET_ARMED(1))

	def disarm(self):
		"""
		Disarm the Mosquito
		"""
		self._send_data(msppg.serialize_SET_ARMED(0))

	def get_attitude(self):
		"""
		Get the orientation of the Mosquito

		:return: Orientation of the Mosquito in radians
		:rtype: tuple
		"""
		self._parser.set_ATTITUDE_RADIANS_Handler(self.__handle_attitude)
		self._send_data(msppg.serialize_ATTITUDE_RADIANS_Request())
		return self.__roll_pitch_yaw

	def set_motor(self, motor, value):
		"""
		Set the value of a motor

		:param motor: Target motor number to set the value (integer in the range 1-4)
		:type data: int
		:param value: Desired motor value in the range 0-1 being 1 maximum speed and 0 motor stopped
		:type value: float
		:return: None
		:trype: None
		"""
		motor_idx = motor-1
		values = [self.__motor_values[i] if i != motor_idx else value for i in range(4)]
		# Setting a motor to a specific value should not reset the rest of motor values.
		# Since currently the MSP message to set a motor value requires the values of the
		# four motors we store the already set values and send them along the new one.
		self.__motor_values = values
		self.set_motors(values)

	def set_motors(self, values):
		"""
		Set the values of all motors in the specified order

		:param values: 4 value list with desired motor values in 
		the range 0-1 being 1 maximum speed and 0 motor stopped.
		:type values: list
		:return: None
		:trype: None
		"""
		self._send_data(msppg.serialize_SET_MOTOR_NORMAL(*values))

	def set_target_altitude(self, altitude):
		"""
		Set the target altitude at which the Mosquito
		should hover.

		:param altitude: The desired altitude in meters
		:type altitude: float
		:return: None
		:rtype: None
		"""
		pass

	def set_led(self, state):
		"""
		Set the on/off state of a LED.

		:param state: 
		:return: None
		:rtype: None
		"""
		pass

	def set_leds(self, state):
		"""
		Set the on/off state of all 3 leds (R,G,B)

		:param state:
		:return: None
		:rtype: None
		"""
		pass
