mosquito-API
================
Python wrapper around bare MSP messages to talk to the Mosquito via WiFi.

Requirements
------------
None

How to use it
-------------

Import the wrapper
~~~~~~~~~~~~~~~~~~

1. Download the wrapper via ``pip`` (not yet supported) or clone this repository by typing in a terminal: ``git clone https://github.com/juangallostra/mosquito-API.git``
2. Start a terminal session in the directory where you cloned the repository
3. Import the wrapper with:

   .. code:: python

           >>> import mapi
           >>> Mosquito = mapi.Mosquito()

API Methods
~~~~~~~~~~~

For the API methods to work, first one should connect to the Mosquito's WiFi network.

Mosquito.connect
................
Connect to the Mosquito

   .. code:: python

           Mosquito.connect()

Mosquito.disconnect
...................
Disconnect from the Mosquito

   .. code:: python

           Mosquito.disconnect()
