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
3. Import the wrapper with:

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

Mosquito.set_mosquito_version
.............................
Set the version of the Mosquito (True meaning Mosquito 90 and False meaning Mosquito 150).

* Parameters:

  - ``is_mosquito_90``: Indicates via a boolean value the version of the Mosquito. True meaning Mosquito 90 anf false meaning Mosquito 150

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

Mosquito.get_attitude
.....................
Get the orientation of the Mosquito in radians.

* Parameters: None
* Returns: 3 value tuple with the orientation of the Mosquito in radians as (Roll, Pitch, Yaw)

   .. code:: python

           >>> Mosquito.get_attitude()

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

Examples
--------
Under the ``examples`` `folder <https://github.com/BonaDrone/mosquito-API/tree/master/examples>`_ there are several scripts that show how the API can be used. For the examples to work one should either have installed the API via ``pip`` or cloned this repository. A part from that, the laptop should be connected to the Mosquito WiFi.

get_attitude.py
~~~~~~~~~~~~~~~

`Script <https://github.com/juangallostra/mosquito-API/blob/master/examples/get_attitude.py>`_

Until exiting the program via ``Ctrl-C`` it constantly asks the Mosquito for its attitude and prints it on the terminal.

set_motors.py
~~~~~~~~~~~~~~~

`Script <https://github.com/juangallostra/mosquito-API/blob/master/examples/set_motors.py>`_

Sets each of the motors (from 1 to 4) to a 20% of its maximum power for one second.

attitude_and_motors.py
~~~~~~~~~~~~~~~~~~~~~~

`Script <https://github.com/juangallostra/mosquito-API/blob/master/examples/attitude_and_motors.py>`_

When the absolute value of roll or pitch is bigger than 20 degrees the four motors start spinning at 20 percent of its maximum speed. 