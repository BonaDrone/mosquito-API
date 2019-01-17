#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra, jgallostra<at>bonadrone.com
# Date: 01-05-2019


from socket import socket
from threading import Thread
import msppg

class MosquitoComms(object):

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
		"""
		self.__running = True
		self.__thread.start()

	def __stop(self):
		"""
		Stop the parser thread
		"""
		self.__running = False

	# Public methods
	def connect(self):
		"""
		Connect to the Mosquito
		"""
		# Before connecting, disconnect if already connected
		self.disconnect()
		self.__socket = socket()
		self.__socket.settimeout(self.__timeout)
		self.__socket.connect((self.__address, self.__port))
		self.__start()

	def disconnect(self):
		"""
		Disconnect from the Mosquito
		"""
		self.__stop()
		if self.__socket is not None:
			self.__socket.shutdown(socket.SHUT_RDWR)
			self.__socket.close()
