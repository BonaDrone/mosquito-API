import sys
sys.path.insert(0, '../')

from mosquito import mapi

def main():
	Mosquito = mapi.Mosquito()
	Mosquito.connect()
	while True:
		print Mosquito.get_attitude()


if __name__ == "__main__":
	main()
