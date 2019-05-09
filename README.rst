mosquito-API
================
Python wrapper around bare MSP messages to talk to the Mosquito via WiFi.

Requirements
------------

* Python 3

How to use it
-------------

Import the wrapper
~~~~~~~~~~~~~~~~~~

1. Download the wrapper via ``pip`` (not yet supported) or clone this repository by typing in a terminal: ``git clone https://github.com/juangallostra/mosquito-API.git``
2. Start a terminal session in the directory where you cloned the repository (only required if the repository was cloned)
3. To install the library run ``sudo python3 setup.py install`` (only required if the repository was cloned). Note that this will result in a system wide installation. Altrnatives to this are using virtual environments or including the library folders and files inside your project. 
4. Import the wrapper with:

   .. code:: python

           >>> from mosquito import mapi
           >>> Mosquito = mapi.Mosquito()

API Methods
~~~~~~~~~~~

For the API methods to work, one should first connect to the Mosquito's WiFi network.

Mosquito.connect
................
Connect to the Mosquito.

* Parameters: None
* Returns: None

   .. code:: python

           >>> Mosquito.connect()

Mosquito.disconnect
...................
Disconnect from the Mosquito.

* Parameters: None
* Returns: None

   .. code:: python

           >>> Mosquito.disconnect()

Mosquito.arm
............
Arm the Mosquito.

* Parameters: None
* Returns: None

   .. code:: python

           >>> Mosquito.arm()

Mosquito.disarm
...............
Disarm the Mosquito.

* Parameters: None
* Returns: None

   .. code:: python

           >>> Mosquito.disarm()

Mosquito.set_position_board
...........................
Set if the Mosquito has the positoning board.

* Parameters:

  - ``has_position_board``: Indicates via a boolean value wether the Mosquito is equipped with a positioning board or not.

* Returns: None

   .. code:: python

           >>> Mosquito.set_position_board(has_position_board)

Mosquito.position_board_connected
.................................
Check if the position board is connected to the Mosquito.

* Parameters: None
* Returns: The connection status of the position board. True if connected and False otherwise.

   .. code:: python

           >>> Mosquito.position_board_connected()

Mosquito.set_mosquito_version
.............................
Set the version of the Mosquito (True meaning Mosquito 90 and False meaning Mosquito 150).

* Parameters:

  - ``is_mosquito_90``: Indicates via a boolean value the version of the Mosquito. True meaning Mosquito 90 and False meaning Mosquito 150

* Returns: None

   .. code:: python

           >>> Mosquito.set_mosquito_version(is_mosquito_90)

Mosquito.get_firmware_version
.............................
Get the version of the firmware running on the Mosquito.

* Parameters: None
* Returns: Firmware version as an integer

   .. code:: python

           >>> Mosquito.get_firmware_version()

Mosquito.calibrate_ESCs
.......................
Calibrate ESCs with the MultiShot protocol. When this message is sent, the calibration will be performed after powering off and on the board. Here are some additional links if you want to know a bit more about ESC protocols:

1. https://fpvsampa.com/esc-firmwares-and-protocolos/
2. https://quadmeup.com/pwm-oneshot125-oneshot42-and-multishot-comparison/
3. https://oscarliang.com/esc-firmware-protocols/

* Parameters: None
* Returns: None

   .. code:: python

           >>> Mosquito.calibrate_ESCs()

Mosquito.calibrate_transmitter
..............................
Trigger the different stages (0,1,2) of the transmitter calibration. This calibration consists of three steps.

- First stage (``stage = 0``): Throttle stick (left stick) at its minimum value and right stick centered.
- Second stage (``stage = 1``): Move both sticks randomly between its maximum and minimum values.
- Third stage (``stage = 2``): Sticks at rest. Trigger calibration computations.

* Parameters:

  - ``stage``: Indicates the calibration stage with an integer in the range 0-2.

* Returns: None

   .. code:: python

           >>> Mosquito.calibrate_transmitter(stage)

Mosquito.get_attitude
.....................
Get the orientation of the Mosquito in radians or degrees. By default (if the parameter ``degrees`` is omitted) the attitude will be obtained in radians.

* Parameters:
  
  - ``degrees``: Boolean value that indicates if the attitude should be returned in degrees. It is ``False`` by default

* Returns: 3 value tuple with the orientation of the Mosquito in radians as (Roll, Pitch, Yaw)

   .. code:: python

           >>> Mosquito.get_attitude(degrees=True/False)

Mosquito.get_velocities
.......................
Get the linear velocities of the Mosquito in meters per second.

* Parameters: None
* Returns: 3 value tuple with the linear velocities of the Mosquito in the x, y and z IMU axis. Note that, in the IMU reference frame, the y axis points to the front, the x axis to the left and the z axis folloes the right hand rule.

   .. code:: python

           >>> Mosquito.get_velocities()

Mosquito.set_motor
.....................
Set the value of the specified motor.

* Parameters: 

  - ``motor``: target motor. The value should be in the range 1-4
  - ``value``: desired value. Should be a float in the range 0-1

* Returns: None

   .. code:: python

           >>> Mosquito.set_motor(motor, value)

Mosquito.set_motors
.....................
Set the values of the four motors.

* Parameters:

  - ``values``: ordered tuple containing the desired values for the motors. Values should be floats in the range 0-1. The value in the first position will be set to the first motor, the second value will be set to the second motor and so on.

* Returns: None

   .. code:: python

           >>> Mosquito.set_motors(values)

Mosquito.get_motor
..................
Get the current value of a single motor.

* Parameters:

  - ``motor``: Motor index -in the range 1,4- whose value is wanted.

* Returns: The current value of the motor in the range 0,1

   .. code:: python

           >>> Mosquito.get_motor(motor)

Mosquito.get_motors
...................
Get the current value of the four motors.

* Parameters: None
* Returns: An ordered tuple with the current value of the four motors in the range 0,1. The values are ordered so that the position in the tuple matches the motor index

   .. code:: python

           >>> Mosquito.get_motors()

Mosquito.set_voltage
....................
Set the voltage of the battery in the Mosquito. This MSP message is only used by the ESP32 in order to send the computed voltage to the STM32. This message in the API can be used to override.

* Parameters: 

  - ``voltage``: battery voltage in V as a float

* Returns: None

   .. code:: python

           >>> Mosquito.set_voltage(voltage)

Mosquito.get_voltage
....................
Get the voltage of the battery in the Mosquito. If the battery is not connected (or detected) it returns 0.0.

* Parameters: None
* Returns: Battery voltage in V as a float

   .. code:: python

           >>> Mosquito.get_voltage()

Mosquito.set_PID
................
Set the constants (as floats) of every PID controller in Hackflight.

* Parameters:

  - ``gyro_roll_pitch_P``: Rate Pitch & Roll controller. Proportional constant.
  - ``gyro_roll_pitch_I``: Rate Pitch & Roll controller. Integral constant.
  - ``gyro_roll_pitch_D``: Rate Pitch & Roll controller. Derivative constant.
  - ``gyro_yaw_P``: Rate Yaw controller. Proportional constant.
  - ``gyro_yaw_I``: Rate Yaw controller. Proportional constant.
  - ``demands_to_rate``: In rate mode, demands from RC are multiplied by demandstoRate.
  - ``level_P``: Level Pitch & Roll controller. Proportional constant.
  - ``altHold_P``: Altitude controller. Proportional constant.
  - ``altHold_vel_P``: Vertical velocity controller. Proportional constant.
  - ``altHold_vel_I``: Vertical velocity controller. Integral constant.
  - ``altHold_vel_D``: Vertical velocity controller. Derivative constant.
  - ``min_altitude``: Minimum altitude, in meters.
  - ``posHold_vel_P``: Horizontal velocity controller. Proportional constant.
  - ``posHold_vel_I``: Horizontal velocity controller. Integral constant.
  - ``posHold_vel_D``: Horizontal velocity controller. Derivative constant.
  - ``param9``: Param9
  
* Returns: None

   .. code:: python

           >>> Mosquito.set_PID(gyro_roll_pitch_P, gyro_roll_pitch_I, gyro_roll_pitch_D,
              gyro_yaw_P, gyro_yaw_I, demands_to_rate,
              level_P, altHold_P, altHold_vel_P, altHold_vel_I, altHold_vel_D, min_altitude,
              posHold_vel_P, posHold_vel_I, posHold_vel_D, param9)

Mosquito.get_PID
................
Get the constants of every PID controller in Hackflight.

* Parameters:  None
* Returns: Current values for PID controllers. See 'set_PID()' documentation for tuple details

   .. code:: python

           >>> Mosquito.get_PID()

Mosquito.set_leds
.................
Turn on or off the LEDs of the board. If any of the LEDs is omitted in the method call its current status is preserved.

* Parameters: 
  
  - ``red``: Keyword argument indicating the status of the red LED. A True/1 value will turn the LED on and a False/0 value off.
  - ``green``: Keyword argument indicating the status of the green LED. A True/1 value will turn the LED on and a False/0 value off.
  - ``blue``: Keyword argument indicating the status of the blue LED. A True/1 value will turn the LED on and a False/0 value off.

* Returns: None

   .. code:: python

           >>> Mosquito.set_leds(red=0/1,green=0/1,blue=0/1)

Mosquito.clear_EEPROM
.....................
Clear a specific section, or all, of the Mosquito's EEPROM. There are three available options that clear different sections of the EEPROM. These are are:

1. Clear the parameters section - section 0
2. Clear the mission section - section 1
3. Clear the whole EEPROM - section 2 

* Parameters:
  
  - ``section``: Integer indicating the section to clear. 0 - Parameters, 1 - Mission, 2 - all

* Returns: None

   .. code:: python

           >>> Mosquito.clear_EEPROM(section)

Mosquito.execute_mission
........................
Begin the execution of a flight mission stored in the EEPROM

* Parameters: None
* Returns: None

   .. code:: python

           >>> Mosquito.execute_mission()

Mosquito.stop
.............
Trigger an emergency stop that will hault the Mosquito and stop any action being performed.

* Parameters: None
* Returns: None

   .. code:: python

           >>> Mosquito.stop()

Mosquito.take_off
.................
Take off and hover at the specified height.

* Parameters: 

  - ``height``: Integer indicating the height (in cm) at which the drone should hover after takeoff. By default, the take off height is 1m.

* Returns: None

   .. code:: python

           >>> Mosquito.take_off(height)

Mosquito.land
.............
Land the Mosquito.

* Parameters: None
* Returns: None

   .. code:: python

           >>> Mosquito.land()

Mosquito.hover
..............
Hover at the current position for the specified amount of time.

* Parameters:

  - ``time``: Integer indicating number of seconds that the hover action should last.

* Returns: None

   .. code:: python

           >>> Mosquito.hover(time)


Mosquito.change_height
......................
Set the target height at which the Mosquito should hover.

* Parameters:

  - ``height``: Integer indicating the desired hovering altitude in centimeters.

* Returns: None

   .. code:: python

           >>> Mosquito.change_height(height)

Mosquito.move_forward
.....................
Move forward for the specified amount of time

* Parameters:

  - ``time``: Integer indicating the number of seconds the action should last.

* Returns: None

   .. code:: python

           >>> Mosquito.move_forward(time)

Mosquito.move_backwards
.......................
Move backwards for the specified amount of time

* Parameters:

  - ``time``: Integer indicating the number of seconds the action should last.

* Returns: None

   .. code:: python

           >>> Mosquito.move_backwards(time)

Mosquito.move_left
..................
Move left for the specified amount of time

* Parameters:

  - ``time``: Integer indicating the number of seconds the action should last.

* Returns: None

   .. code:: python

           >>> Mosquito.move_left(time)

Mosquito.move_right
...................
Move right for the specified amount of time

* Parameters:

  - ``time``: Integer indicating the number of seconds the action should last.

* Returns: None

   .. code:: python

           >>> Mosquito.move_right(time)

Mosquito.turn
.............
Turn the specified angle. If the angle is greater than 0 the rotation will be counter clockwise, and clockwise otherwise.

* Parameters:

  - ``angle``: Integer indicating the number of degrees of the turn.

* Returns: None

   .. code:: python

           >>> Mosquito.turn(angle)

Examples
--------
Under the ``examples`` `folder <https://github.com/BonaDrone/mosquito-API/tree/master/examples>`_ there are several scripts that show how the API can be used. For the examples to work one should either have installed the API via ``pip`` or cloned this repository. A part from that, the laptop should be connected to the Mosquito WiFi.

get_attitude.py
~~~~~~~~~~~~~~~

`Script <https://github.com/juangallostra/mosquito-API/blob/master/examples/get_attitude.py>`_

Until exiting the program via ``Ctrl-C`` it constantly asks the Mosquito for its attitude and prints it on the terminal.

get_velocities.py
~~~~~~~~~~~~~~~~~

`Script <https://github.com/juangallostra/mosquito-API/blob/master/examples/get_velocities.py>`_

Asks the Mosquito for its linear velocities and prints them on the terminal. This script accepts three command line arguments.

* ``--save, -s``: If set to 1 data is stored in CSV format at ``velocities.csv``. If set to 0 or omitted, data is not stored and it is only printed to the terminal.
* ``--duration, -d``: Allows to set the log duration in seconds. If omitted, the script will run until interrupted.
* ``--timestamp, -t``: if set to 1, the script also stores and prints the time, in seconds, at which data was collected with respect to the start of the program execution. If set to 0 or omitted, no timestamps are stored or printed.


set_motors.py
~~~~~~~~~~~~~~~

`Script <https://github.com/juangallostra/mosquito-API/blob/master/examples/set_motors.py>`_

Sets each of the motors (from 1 to 4) to a 20% of its maximum power for one second.

attitude_and_motors.py
~~~~~~~~~~~~~~~~~~~~~~

`Script <https://github.com/juangallostra/mosquito-API/blob/master/examples/attitude_and_motors.py>`_

When the absolute value of roll or pitch is bigger than 20 degrees the four motors start spinning at 20 percent of its maximum speed.

set_leds.py
~~~~~~~~~~~

`Script <https://github.com/juangallostra/mosquito-API/blob/master/examples/set_leds.py>`_

Turns the leds of the board on and off at 2 second intervals.

calibrate_transmitter.py
~~~~~~~~~~~~~~~~~~~~~~~~

`Script <https://github.com/juangallostra/mosquito-API/blob/master/examples/calibrate_transmitter.py>`_

Perform the calibration of the transmitter. Transmitter calibration consists in measuring the offsets between the measured and expected values of each of the transmitter sticks at certain positions (minimum, center, maximum) to be able to map the specific transmitter values to the exected values.

M90_set_parameters.py
~~~~~~~~~~~~~~~~~~~~~

`Script <https://github.com/juangallostra/mosquito-API/blob/master/examples/M90_set_parameters.py>`_

Set the values of the PID controllers for the Mosquito 90.

land.py
~~~~~~~

`Script <https://github.com/juangallostra/mosquito-API/blob/master/examples/land.py>`_

Trigger a land action 20 seconds after estblishing connection with the Mosquito.

simple_flight.py
~~~~~~~~~~~~~~~~

`Script <https://github.com/juangallostra/mosquito-API/blob/master/examples/simple_flight.py>`_

Execute a simple flight that consists in taking off to a height of 100 cm, hovering for 2 seconds and landing.
