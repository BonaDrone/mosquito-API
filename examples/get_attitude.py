import sys
sys.path.insert(0, '../')

from mosquito import mapi

def main():
	Mosquito = mapi.Mosquito()
	Mosquito.connect()
	while True:
		try:
			print Mosquito.get_attitude()
		except KeyboardInterrupt:
			Mosquito.disconnect()
			# quit
			sys.exit()

if __name__ == "__main__":
	main()
