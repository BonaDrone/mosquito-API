#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Juan Gallostra (jgallostra<at>bonadrone.com)
# Date: 03-07-2019

import time

def publisher(subscriber):
	"""
	Closure that stores the subscriber it is bound to and notifies it
	when called with the new set of received values. Note that we only
	allow a one to one relation between publishers and subscribers
	"""
	subscriber = subscriber
	def update_subscriber(*values):
		"""
		Notify the subscriber with the newly received values
		"""
		subscriber.on_update(values)
	return update_subscriber

class Subscriber(object):
	"""
	Subscribe to a publisher and get notified when the publisher
	is called and receives a new set of values
	"""
	def __init__(self, timeout=5):
		"""
		Initialize the subscriber
		"""
		self.__timeout = timeout 
		self.__updated = False
		self.__value = None

	def on_update(self, value):
		"""
		Method that the publisher calls when a new value arrives.
		It notifies the subscriber, which changes its state to 
		updated and stores the value
		"""
		self.__value = value
		self.__updated = True

	def get_value(self):
		"""
		Blocking method that waits until the publisher notifies
		that it has acquired a new value. This value is then 
		retrieved by the subscriber and returned
		"""
		init_time = time.time()
		while not self.__updated:
			if time.time() - init_time > self.__timeout:
				raise TimeoutError("Timed out while waiting for response")
			pass
		self.__updated = False
		return self.__value
