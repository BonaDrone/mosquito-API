#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 01-05-2019


import socket
from threading import Thread
import mosquito.msppg as msppg

class MosquitoComms(object):
	"""
	Communications class. This class is in charge
	of opening and closing communication channels 
	with the Mosquito via WiFi as well as sending
	and receiving data.
	"""

	def __init__(self, address='192.168.4.1', port=80, timeout=4):
		"""
		Initialize the WiFi communications class

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
		# Create a message parser and get ready to
		# run it on a different thread
		self._parser = msppg.MSP_Parser()
		self.__thread = Thread(target=self.__run)
		self.__thread.setDaemon(True)
		self.__running = False

	def _send_data(self, data):
		"""
		Send a serialized MSP message (or any data you want,
		really) to the connected Mosquito

		:param data: serialized data to send to the Mosquito
		:type data: bytes
		:return: None
		:rtype:None
		"""
		if self.__socket is None:
			raise Exception('Please connect to a Mosquito')

		try:
			self.__socket.send(data)
		except:
			raise Exception('Timeout when trying to send: {}'.format(data))

	def __run(self):
		"""
		Run an instance of an MSP parser. Upon receiving a byte it
		gets fed to and parsed by the MSP parser.
		This method is intended to run on a different thread that
		constantly checks if new bytes are available and processes them

		:return: None
		:rtype:None		
		"""
		while self.__running:
			try:
				byte = self.__socket.recv(1)
				self._parser.parse(byte)
			except:
				None

	def __start(self):
		"""
		Start the parser thread

		:return: None
		:rtype:None		
		"""
		self.__running = True
		self.__thread.start()

	def __stop(self):
		"""
		Stop the parser thread

		:return: None
		:rtype:None		
		"""
		self.__running = False

	# Public methods
	def connect(self):
		"""
		Connect to the Mosquito

		:return: None
		:rtype:None		
		"""
		# Before connecting, disconnect if already connected
		self.disconnect()
		self.__socket = socket.socket()
		self.__socket.settimeout(self.__timeout)
		self.__socket.connect((self.__address, self.__port))
		if not self.__running:
			self.__start()

	def disconnect(self):
		"""
		Disconnect from the Mosquito

		:return: None
		:rtype:None		
		"""
		self.__stop()
		if self.__socket is not None:
			self.__socket.shutdown(socket.SHUT_RDWR)
			self.__socket.close()
			self.__socket = None
