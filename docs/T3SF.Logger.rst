************************
T3SF Logger
************************

The T3SF_Logger class is a Python class used for logging messages in the T3SF application. It provides a method for emitting log messages and sending them to a message announcer object, which then broadcasts the message to other components in the application.

The message is also written to a file called ``logs.txt`` for future reference. If the ``message_type`` is set to "WARN" or "ERROR", a critical information message is printed to the terminal using color codes to highlight the message type.

The purpose of the T3SF_Logger class is to provide a centralized logging system for T3SF, allowing developers to easily log messages and display them to administrators or game masters in an easy way.


Module
======

To ensure a clean and organized logging system in the T3SF framework, we implemented the T3SF_Logger class. This class is responsible for handling all logging events and formatting them in a standardized way. By utilizing this class, we can easily track the events and activities of the framework and ensure efficient debugging when needed.

The file structure is shown below:

.. code-block:: bash
	
	logger
	├── __init__.py
	└── logger.py

The Class 
----------

.. py:class:: T3SF_Logger()
	
	The class has only one method, which is ``emit``. It can be called directly without the need to initialize the class.
	
	.. py:method:: emit(message,message_type="DEBUG")

		With this method, we can format the message to an SSE format, store it in the ``logs.txt`` file and also print critical information messages on the terminal using color codes to highlight the type of message.

		.. confval:: message

			The content of the message

			:type: ``str``
			:required: ``True``

		.. confval:: message_type

			The level/type of the message.

			:type: ``str``
			:required: ``False``