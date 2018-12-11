from socket import socket
import mspp
import time


class Mosquito(object):

	def __init__(self, address='192.168.4.1', port=80, timeout=4):
		"""
		Initialize the interface to talk to the mosquito
		"""
		self._address = address
		self._port = port
		self._timeout = timeout
		self._socket = None

	def connect(self):
		"""
		Connect to the Mosquito
		"""
		self._socket = socket()
		self._socket.settimeout(self._timeout)
		self._socket.connect((self._address, self._port))