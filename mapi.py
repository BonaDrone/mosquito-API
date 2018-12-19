#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 12-12-2018

from socket import socket
import msppg
import time

# The parser parse method returns its current state,
# where 6 is end of message or message received 
ANSWER_RECEIVED = 6


class Mosquito(object):
	"""
	API object to communicate with a Mosquito via WiFi
	based on MSP messages. 

	The laptop should be connected to the Mosquito's Wifi.
	MSP message handling is delegated to Simon D. Levy's 
	Hackflight's MSP Parser. 

	For further info see: 
		https://github.com/simondlevy/Hackflight/tree/master/extras/parser
	"""

	def __init__(self, address='192.168.4.1', port=80, timeout=4):
		"""
		Initialize the interface to talk to the Mosquito

		:param address: Mosquito IP
		:type address: string
		:param port: port number where to connect 
		:type port: integer
		:param timeout: allowed period of time in seconds to elapse before raising an exception 
		:type timeout: integer
		"""
		self.__address = address
		self.__port = port
		self.__timeout = timeout
		self.__socket = None
		# Create a message parser
		self.__parser = msppg.MSP_Parser()
		# Mosquito's status vars
		self.__roll_pitch_yaw = [0]*3

	def __send_data(self, data):
		"""
		Send a serialized MSP message to the connected Mosquito

		:param data: serialized data to send to the Mosquito
		:type data: bytes
		"""
		if self.__socket is None:
			raise Exception('Please connect to a Mosquito')

		try:
			self.__socket.send(data)
		except socket.timeout as e:
			raise Exception('Timeout when trying to send: {}'.format(data))

	# Message handlers
	def __handle_attitude(self, x, y, z):
		self.roll_pitch_yaw = x, -y, z  
		self.gotimu = True

	def connect(self):
		"""
		Connect to the Mosquito
		"""
		# Before connecting, disconnect if already connected
		self.disconnect()
		self.__socket = socket()
		self.__socket.settimeout(self.__timeout)
		self.__socket.connect((self.__address, self.__port))

	def disconnect(self):
		"""
		Disconnect from the Mosquito
		"""
		if self.__socket is not None:
			self.__socket.shutdown()
			self.__socket.close()

	def arm(self):
		"""
		Arm the Mosquito
		"""
		self.__send_data(msppg.serialize_SET_ARMED(1))

	def disarm(self):
		"""
		Disarm the Mosquito
		"""
		self.__send_data(msppg.serialize_SET_ARMED(0))

	def get_attitude(self):
		"""
		Get the orientation of the Mosquito
		"""
		self.__parser.set_ATTITUDE_RADIANS_Handler(self.__handle_attitude)
		self.__send_data(msppg.serialize_ATTITUDE_RADIANS_Request())
		# wait until answer is received and parsed
		while (self.__parser.parse(self.__socket.recv(1)) != ANSWER_RECEIVED):
			continue
		return self.__roll_pitch_yaw

