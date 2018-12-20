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
2. Start a terminal session in the directory where you cloned the repository
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

Mosquito.get_attitude
.....................
Get the orientation of the Mosquito in radians.

* Parameters: None
* Returns: 3 value tuple with the orientation of the Mosquito in radians as (Roll, Pitch, Yaw)

   .. code:: python

           >>> Mosquito.get_attitude()


Examples
--------
Under the `examples` folder there are several scripts that show how to the API can be used. For the examples to work one should either have installed the API via `pip` or cloned this repository. Also, the laptop should be connected to the Mosquito WiFi.

get_attitude.py
~~~~~~~~~~~~~~~

Until exiting the program via `Ctrl-C` it constantly asks the Mosquito for its attitude and prints it on the terminal.