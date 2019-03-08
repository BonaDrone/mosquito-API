class Publisher(object):
	"""
	"""

	def __init__(self):
		"""
		"""
		self.subscribers = set()

	def __call__(self, *values):
		"""
		"""
		for subscriber in self.subscribers:
			subscriber.on_update(values)

	def register(self, subscriber):
		"""
		"""
		self.subscribers.add(subscriber)

	def unregister(self, subscriber):
		"""
		"""
		self.subscribers.discard(subscriber)


class Subscriber(object):
	"""
	"""
	def __init__(self, function_to_call):
		"""
		"""
		self.__updated = False
		self.__value = None
		self.__function_to_call = function_to_call

	def on_update(self, value):
		"""
		"""
		self.__value = value
		self.__updated = True

	def __call__(self):
		"""
		"""
		self.__function_to_call()
		while not self.__updated:
			pass
		self.__updated = False
		return self.__value
