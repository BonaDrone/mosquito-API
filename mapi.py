#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 12-12-2018

from socket import socket
import msppg
import time


class Mosquito(object):
	"""
	API object to communicate with a Mosquito via WiFi
	based on MSP messages.
	MSP message handling is delegated to Simon D. Levy's 
	Hackflight's MSP Parser. For further info see: 
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

	def __send_data(self, data):
		"""
		Send a serialized MSP message to the connected Mosquito

		:param data: data to send to the Mosquito
		:type data: bytes
		"""
		if self.__socket is None:
			raise Exception('Please connect to a Mosquito')

		try:
			self.__socket.send(data)
		except socket.timeout as e:
			raise Exception('Timeout when trying to send: {}'.format(data))

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
