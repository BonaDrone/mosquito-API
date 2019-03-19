#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra (jgallostra<at>bonadrone.com)
# Date: 03-07-2019

from enum import Enum

class ReturnType(Enum):
	BOOL = 1
	INT = 2
	INTS = 3
	FLOAT = 4
	FLOATS = 5

# We only allow a one to one relation between publishers and subscribers
def publisher(subscriber):
	"""
	"""
	subscriber = subscriber
	def update_subscriber(*values):
		subscriber.on_update(values)
	return update_subscriber

class Subscriber(object):
	"""
	"""
	def __init__(self, function_to_call, return_type):
		"""
		"""
		self.return_type = return_type
		self.__updated = False
		self.__value = None
		self.__function_to_call = function_to_call

	def on_update(self, value):
		"""
		"""
		self.__value = value
		self.__updated = True

	def wrap_value(self, value):
		"""
		"""
		if self.return_type == ReturnType.BOOL:
			return bool(value[0])
		elif self.return_type == ReturnType.INT or self.return_type == ReturnType.FLOAT:
			return value[0]
		return value

	def __call__(self):
		"""
		"""
		self.__function_to_call()
		while not self.__updated:
			pass
		self.__updated = False
		return self.wrap_value(self.__value)
