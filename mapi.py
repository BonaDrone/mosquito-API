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
		self._address = address
		self._port = port
		self._timeout = timeout
		self._socket = None

	def __send_data(self, data):
		"""
		Send a serialized MSP message to the connected Mosquito

		:param data: data to send to the Mosquito
		:type data: bytes
		"""
		try:
			self._socket.send(data)
		except socket.timeout as e:
			raise Exception('Timeout when trying to send: {}'.format(data))

	def connect(self):
		"""
		Connect to the Mosquito
		"""
		self._socket = socket()
		self._socket.settimeout(self._timeout)
		self._socket.connect((self._address, self._port))

	def disconnect(self):
		"""
		Disconnect from the Mosquito
		"""
		if self._socket is not None:
			self._socket.shutdown()
			self._socket.close()