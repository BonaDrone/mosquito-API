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
	def __init__(self):
		"""
		"""
		self.__updated = False
		self.__value = None

	def on_update(self, value):
		"""
		"""
		self.__value = value
		self.__updated = True

	def get_value(self):
		"""
		"""
		while not self.__updated:
			pass
		self.__updated = False
		return self.__value
