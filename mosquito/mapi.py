#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 12-12-2018

import time
import msppg
from coms import MosquitoComms


class Mosquito(MosquitoComms):
	"""
	API implementation to communicate with a Mosquito 
	via WiFi based on MSP messages. 

	The laptop should be connected to the Mosquito's Wifi.
	MSP message handling is delegated to Simon D. Levy's 
	Hackflight's MSP Parser. 

	For further info about the MSP parser see: 
		- https://github.com/simondlevy/Hackflight/tree/master/extras/parser
		- http://www.multiwii.com/wiki/index.php?title=Multiwii_Serial_Protocol
	"""

	def __init__(self):
		"""
		Initialize the API instance and create
		a WiFi communication channel between laptop
		and Mosquito
		"""
		super(Mosquito, self).__init__()
		# Mosquito's status
		self.__roll_pitch_yaw = tuple([0]*3)
		self.__motor_values = tuple([0]*4)
		self.__position_board_connected = False
		self.__firmware_version = None

	# Message handlers
	def __handle_get_attitude(self, roll, pitch, yaw):
		"""
		Update Mosquito's orientation when receiving
		a new attitude MSP message.

		for a better understanding of the meaning of each of
		the values see:
		https://en.wikipedia.org/wiki/Aircraft_principal_axes

		:param roll: Current roll of the Mosquito in radians
		:type roll: float
		:param pitch: Current pitch of the Mosquito in radians
		:type pitch: float
		:param yaw: Current yaw of the Mosquito in radians
		:type yaw: float
		:return: None
		:rtype: None
		"""
		self.__roll_pitch_yaw = roll, -pitch, yaw	

	def __handle_get_motors(self, m1, m2, m3, m4):
		"""
		Update Mosquito's motor status when receiving
		a new motor values MSP message

		To check the relation between motor numbering and
		physical motors see:
		https://fpvfrenzy.com/betaflight-motor-order/

		:param m1: Current value of motor 1 in the range 0-1
		:type m1: float
		:param m2: Current value of motor 2 in the range 0-1
		:type m2: float
		:param m3: Current value of motor 3 in the range 0-1
		:type m3: float
		:param m4: Current value of motor 4 in the range 0-1
		:type m4: float
		:return: None
		:rtype: None
		"""
		self.__motor_values = m1, m2, m3, m4

	def __handle_position_board_connected(self, is_connected):
		"""
		Handle the response to a position board check request and
		update the status variable where the connection status is
		stored

		:param is_connected: Connection status of position board
		:type is_connected: boolean
		:return: None
		:rtype: None
		"""
		self.__position_board_connected = is_connected

	def __handle_firmware_version(self, version):
		"""
		Handle the response to a firmware version request and
		store the firmware version

		:param version: Current firmware version
		:type version: int
		:return: None
		:rtype: None
		"""
		self.__firmware_version = version

	# Public methods
	def arm(self):
		"""
		Arm the Mosquito

		:return: None
		:rtype: None
		"""
		self._send_data(msppg.serialize_SET_ARMED(1))

	def disarm(self):
		"""
		Disarm the Mosquito

		:return: None
		:rtype: None
		"""
		self._send_data(msppg.serialize_SET_ARMED(0))

	def set_position_board(self, has_position_board):
		"""
		Set if the Mosquito has the positoning board

		:param has_positioning_board: Indicates wether the Mosquito is equipped with
		a position board or not.
		:type has_positioning_board: bool
		:return: None
		:rtype: None
		"""
		self._send_data(msppg.serialize_SET_POSITIONING_BOARD(has_position_board))

	def position_board_connected(self):
		"""
		Check if the position board is connected to the Mosquito.

		:return: The status of the position board. True if connected and False otherwise
		:rtype: bool
		"""
		self._parser.set_POSITION_BOARD_CONNECTED_Handler(self.__handle_position_board_connected)
		self._send_data(msppg.serialize_POSITION_BOARD_CONNECTED_Request())
		return self.__position_board_connected

	def set_mosquito_version(self, is_mosquito_90):
		"""
		Set the version of the Mosquito (True meaning Mosquito 90 and False meaning
		Mosquito 150)

		:param is_mosquito_90: Indicates the version of the Mosquito
		:type is_mosquito_90: bool
		:return: None
		:rtype: None		
		"""
		self._send_data(msppg.serialize_SET_MOSQUITO_VERSION(is_mosquito_90))

	def get_firmware_version(self):
		"""
		Get the version of the firmware running on the Mosquito

		:return: Firmware version
		:rtype: int
		"""
		self._parser.set_FIRMWARE_VERSION_Handler(self.__handle_firmware_version)
		self._send_data(msppg.serialize_FIRMWARE_VERSION_Request())
		return self.__firmware_version

	def calibrate_ESCs(self):
		"""
		Calibrate ESCs with the MultiShot protocol. When this message is sent,
		the calibration will be performed after powering off and on the board.

		:return: None
		:rtype: None 
		"""
		self._send_data(msppg.serialize_ESC_CALIBRATION(0))

	def get_attitude(self):
		"""
		Get the orientation of the Mosquito

		:return: Orientation of the Mosquito in radians
		:rtype: tuple
		"""
		self._parser.set_ATTITUDE_RADIANS_Handler(self.__handle_get_attitude)
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
		values = tuple([self.__motor_values[i] if i != motor_idx else value for i in range(4)])
		# Setting a motor to a specific value should not reset the rest of motor values.
		# Since currently the MSP message to set a motor value requires the values of the
		# four motors we store the already set values and send them along the new one.
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
		self.__motor_values = values
		self._send_data(msppg.serialize_SET_MOTOR_NORMAL(*values))

	def get_motor(self, motor):
		"""
		Get the value of a specific motors

		:param motor: Motor number whose value is wanted
		:type motor: int
		:return: current motor value in the range 0-1
		:trype: float
		"""
		motor_values = self.get_motors()
		return motor_values[motor-1]

	def get_motors(self):
		"""
		Get the values of all motors

		:return: current motor values in the range 0-1. The values are ordered
		so that the position in the tuple matches the motor index
		:trype: tuple
		"""
		self._parser.set_GET_MOTOR_NORMAL_Handler(self.__handle_get_motors)
		self._send_data(msppg.serialize_GET_MOTOR_NORMAL_Request())
		return self.__motor_values

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
