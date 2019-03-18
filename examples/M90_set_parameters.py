#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Pep Marti-Saumell (jmarti<at>bonadrone.com>)
# Date: 03-09-2019

import sys
# Add parent folder to path so that the API can be imported.
# This shouldn't be required if the package has been installed via pip
sys.path.insert(0, '../')
sys.path.insert(0, '../mosquito/')

from mosquito import mapi

def main():
	"""
	Function that gets executed when the script is directly
	called from the command line.

	It sets the PID constants for the Mosquito 90
	"""
	m = mapi.Mosquito()
	m.connect()

	RATE_ROLL_P = 0.05
	RATE_ROLL_I = 0.40
	RATE_ROLL_D = 0.0001

	RATE_PITCH_P = 0.05
	RATE_PITCH_I = 0.55
	RATE_PITCH_D = 0.0001

	RATE_YAW_P = 0.05
	RATE_YAW_I = 0.40

	RATE_D2R = 6.00

	LEVEL_P = 1.00

	ALTH_P = 0.0
	ALTH_V_P = 0.0
	ALTH_V_I = 0.0
	ALTH_V_D = 0.0
	ALTH_MIN_A = 0.0

	PARAM_6 = 1.0
	PARAM_7 = 2.0
	PARAM_8 = 3.0
	PARAM_9 = 4.0

	m.set_mosquito_version(True)
	m.set_position_board(True)
	m.set_PID(RATE_ROLL_P, RATE_ROLL_I, RATE_ROLL_D,RATE_PITCH_P, RATE_PITCH_I, RATE_PITCH_D, RATE_YAW_P, RATE_YAW_I, RATE_D2R, LEVEL_P, ALTH_P, ALTH_V_P, ALTH_V_I, ALTH_V_D, ALTH_MIN_A, PARAM_6, PARAM_7, PARAM_8, PARAM_9)

	m.get_PID()

	m.disconnect()

if __name__ == '__main__':
	main()
