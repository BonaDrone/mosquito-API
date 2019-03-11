#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Authors: Juan Gallostra (jgallostra<at>bonadrone.com) and Pep Marti-Saumell (jmarti<at>bonadrone.com>)
# Date: 12-12-2018

import time
import mosquito.msppg as msppg
from mosquito.coms import MosquitoComms
from mosquito.notify import Publisher, Subscriber

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

		# Create publishers. The publishers will be set as the handlers
		# of the MSP messages. This way, they will be called when the
		# appropriate MSP message is received. When this happens, the
		# publisher will call all its subscribers with the received
		# values as parameters
		self.__position_board_connected_pub = Publisher()
		self.__firmware_version_pub = Publisher()
		self.__get_attitude_pub = Publisher()
		self.__get_motors_pub = Publisher()
		self.__get_voltage_pub = Publisher()
		self.__get_PID_pub = Publisher()
		# Set the publishers as the MSP message handlers
		# They will be triggered when the appropriate message is received
		self._parser.set_POSITION_BOARD_CONNECTED_Handler(self.__position_board_connected_pub)
		self._parser.set_FIRMWARE_VERSION_Handler(self.__firmware_version_pub)
		self._parser.set_ATTITUDE_RADIANS_Handler(self.__get_attitude_pub)
		self._parser.set_GET_MOTOR_NORMAL_Handler(self.__get_motors_pub)
		self._parser.set_GET_BATTERY_VOLTAGE_Handler(self.__get_voltage_pub)
		self._parser.set_GET_PID_CONSTANTS_Handler(self.__get_PID_pub)
		# Create subscribers, which will be our public methods. The parameter passed 
		# to the Subscriber constructor should be the method that sends the
		# appropriate MSP request message to retrieve the desired data.
		self.position_board_connected = Subscriber(self.__position_board_connected)
		self.get_firmware_version = Subscriber(self.__get_firmware_version)
		self.get_attitude = Subscriber(self.__get_attitude)
		self.get_motors = Subscriber(self.__get_motors)
		self.get_voltage = Subscriber(self.__get_voltage)
		self.get_PID = Subscriber(self.__get_PID)
		# Register the subscribers to their corresponding publisher
		self.__position_board_connected_pub.register(self.position_board_connected)
		self.__firmware_version_pub.register(self.get_firmware_version)
		self.__get_attitude_pub.register(self.get_attitude)
		self.__get_motors_pub.register(self.get_motors)
		self.__get_voltage_pub.register(self.get_voltage)
		self.__get_PID_pub.register(self.get_PID)

		# Mosquito's status
		self.__motor_values = tuple([0]*4)
		self.__led_status = tuple([0]*3)
		self.__voltage = 0.0
		# Mosquito's PID constants
		self.__controller_constants = tuple([0]*16)
		# self.__roll_pitch_yaw = tuple([0]*3)
		# self.__position_board_connected = False
		# self.__firmware_version = None

	# Private methods
	def __position_board_connected(self):
		"""
		Check if the position board is connected to the Mosquito.

		:return: The status of the position board. True if connected and False otherwise
		:rtype: bool
		"""
		self._send_data(msppg.serialize_POSITION_BOARD_CONNECTED_Request())

	def __get_firmware_version(self):
		"""
		Get the version of the firmware running on the Mosquito

		:return: Firmware version
		:rtype: int
		"""
		self._send_data(msppg.serialize_FIRMWARE_VERSION_Request())

	def __get_attitude(self):
		"""
		Get the orientation of the Mosquito

		:return: Orientation of the Mosquito in radians
		:rtype: tuple
		"""
		self._send_data(msppg.serialize_ATTITUDE_RADIANS_Request())

	def __get_voltage(self):
		"""
		Get the voltage of the battery in the Mosquito. 
		If not connected it returns 0.0

		:return: Battery voltage in V
		:rtype: float
		"""
		self._send_data(msppg.serialize_GET_BATTERY_VOLTAGE_Request())

	def __get_motors(self):
		"""
		Get the values of all motors

		:return: current motor values in the range 0-1. The values are ordered
		so that the position in the tuple matches the motor index
		:trype: tuple
		"""
		self._send_data(msppg.serialize_GET_MOTOR_NORMAL_Request())

	def __get_PID(self):
		"""
		Get the constants of every PID controller in Hackflight.

		:return: current values for PID controllers. See 'set_PID()' documentation for tuple details
		:trype: tuple
		"""
		self._send_data(msppg.serialize_GET_PID_CONSTANTS_Request())

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

	def calibrate_ESCs(self):
		"""
		Calibrate ESCs with the MultiShot protocol. When this message is sent,
		the calibration will be performed after powering off and on the board.

		:return: None
		:rtype: None
		"""
		self._send_data(msppg.serialize_ESC_CALIBRATION(0))

	def calibrate_transmitter(self, stage):
		"""
		Trigger the different stages of the transmitter calibration

		:param stage: Calibration stage
		:type stage: int in the range 0-2
		:return: None
		:rtype: None
		"""
		self._send_data(msppg.serialize_RC_CALIBRATION(stage))

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

	def set_voltage(self, voltage):
		"""
		Set the voltage of the battery in the Mosquito.
		This MSP message is only used by the ESP32 in
		order to send the computed voltage to the STM32.
		This message in the API can be used to override.

		:param voltage: battery voltage in V
		:type voltage: float
		:return: None
		:trype: None
		"""
		self.__voltage = voltage
		self._send_data(msppg.serialize_SET_BATTERY_VOLTAGE(voltage))

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

	def set_PID(self,gyroRollPitchP, gyroRollPitchI, gyroRollPitchD,
							gyroYawP, gyroYawI, demandsToRate,
							levelP, altHoldP, altHoldVelP, altHoldVelI, altHoldVelD, minAltitude,
							param6, param7, param8, param9):
		"""
		Set the constants of every PID controller in Hackflight.

		:param gyroRollPitchP: Rate Pitch & Roll controller. Proportional constant.
		:type gyroRollPitchP: float
		:param gyroRollPitchI: Rate Pitch & Roll controller. Integral constant.
		:type gyroRollPitchI: float
		:param gyroRollPitchD: Rate Pitch & Roll controller. Derivative constant.
		:type gyroRollPitchD: float
		:param gyroYawP: Rate Yaw controller. Proportional constant.
		:type gyroYawP: float
		:param gyroYawI: Rate Yaw controller. Proportional constant.
		:type gyroYawI: float
		:param demandsToRate: In rate mode, demands from RC are multiplied by demandstoRate.
		:type demandsToRate: float
		:param levelP: Level Pitch & Roll controller. Proportional constant.
		:type levelP: float
		:param altHoldP: Altitude controller. Proportional constant.
		:type altHoldP: float
		:param altHoldVelP: Vertical velocity controller. Proportional constant.
		:type altHoldVelP: float
		:param altHoldVelI: Vertical velocity controller. Integral constant.
		:type altHoldVelI: float
		:param altHoldVelD: Vertical velocity controller. Derivative constant.
		:type altHoldVelD: float
		:param minAltitude: Minimum altitude, in meters.
		:type minAltitude: float
		:param param6: Param6.
		:type param6: float
		:param param7: Param7.
		:type param7: float
		:param param8: Param8.
		:type param8: float
		:param param9: Param9
		:type param9: float
		:return: None
		:trype: None
		"""
		self.__controller_constants = gyroRollPitchP, gyroRollPitchI, gyroRollPitchD,gyroYawP, gyroYawI, demandsToRate,levelP, altHoldP, altHoldVelP, altHoldVelI, altHoldVelD, minAltitude,param6, param7, param8, param9
		self._send_data(msppg.serialize_SET_PID_CONSTANTS(gyroRollPitchP, gyroRollPitchI, gyroRollPitchD,gyroYawP, gyroYawI, demandsToRate,levelP, altHoldP, altHoldVelP, altHoldVelI, altHoldVelD, minAltitude,param6, param7, param8, param9))

	def set_leds(self, red=None, green=None, blue=None):
		"""
		Set the on/off state of the LEDs. If any of the LEDs
		is omitted in the method call its current status is preserved.

		:param red: Status of red LED. A True/1 value will turn the LED on and a False/0 value off
		:type red: bool
		:param green: Status of green LED. A True/1 value will turn the LED on and a False/0 value off
		:type green: bool
		:param blue: Status of blue LED. A True/1 value will turn the LED on and a False/0 value off
		:type blue: bool
		:return: None
		:rtype: None
		"""
		self.__led_status = tuple([self.__led_status[idx] if value is None else value for idx, value in enumerate([red, green, blue])])
		self._send_data(msppg.serialize_SET_LEDS(*self.__led_status))

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
