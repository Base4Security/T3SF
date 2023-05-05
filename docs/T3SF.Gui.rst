*****
GUI
*****

Starting from version 1.2, the framework integrates a graphical user interface (GUI) that provides additional features, including a real-time log display and the ability to start and stop exercises with ease. Starting from version 2.0, the framework introduces several new features, including an enhanced Master Scenario Events List (MSEL) viewer, which enables users to view injects and their fields directly. Additionally, a new automated environment creation tool is now available, streamlining the process of setting up environments.

Routes
=======

Index ``(/)``
--------------------
	===============  ======================= 
	Renders          ``index.html``
	POST parameters	 ``None``
	GET parameters	 ``None``
	===============  =======================

	This route provides a real-time log display with user-friendly controls to start and stop exercises with just two clicks. It also features a log level filter, which allows game-master/admins to reduce noise in the logs by only displaying relevant information. If necessary, game-master can clear the previous logs directly from the interface to obtain a clean view before starting a new exercise.

	.. image:: ./images/gui/index.png


MSEL Viewer ``(/msel-viewer)``
--------------------------------
	===============  ======================= 
	Renders          ``msel_viewer.html``
	POST parameters	 ``None``
	GET parameters	 ``None``
	===============  =======================

	This route provides an MSEL viewer functionality that allows admins to load and view the JSON file directly in the browser. The viewer provides pagination to navigate through the list of injects easily.

	The functionality works by accepting a JSON file and using JavaScript to parse the file and display all the injects in a user-friendly manner. The pagination feature allows admins to view injects in manageable groups and facilitates navigation through the injects.

	.. image:: ./images/gui/msel_viewer.png


Environment creation ``(/env-creation)``
-----------------------------------------------
	===============  ======================= 
	Renders          ``env_creation.html``
	POST parameters	 ``None``
	GET parameters	 ``None``
	===============  =======================

	the ``/env-creation`` route provides functionality for the automatic creation of environments, including channels and categories based on predefined settings.

	The areas for the environment are loaded from the MSEL, which specifies the different scenarios and injects that will be tested. However, the channels to be created are predefined and are not based on the MSEL.

	On the ``/env-creation`` page, admins can view the channels they will be creating per area, and the feature automatically creates channels for each area. In addition, when creating the environment, a log panel will appear to show the status of the creation.

	Overall, the automatic environment creation feature provides admins with a simple and efficient way to set up environments, saving time and effort that can be better spent on other tasks.

	.. image:: ./images/gui/env_creation.png


Exercise Starter ``(/start)``
-----------------------------------------------
	===============  =================================================== 
	Returns          ``Started``
	POST parameters	 ``None``
	GET parameters	 ``None``
	Triggers	 	 :py:meth:`run_async_incidents` (Based on platform)
	===============  ===================================================

	Is responsible for initiating the exercise by calling the ``run_async_incidents`` function based on the selected platform. Once the function is called, the exercise will begin, and the function will continuously execute until all incidents are completed.

Framework Stopper ``(/stop)``
-----------------------------------------------
	===============  ======================= 
	Returns          ``Shutting down...``
	POST parameters	 ``None``
	GET parameters	 ``None``
	===============  =======================

	The route `/stop` is used to stop the exercise in progress. When this route is accessed, it kills the bot by sending an "INFO" message with a timestamp using the :py:meth:`MessageAnnouncer` class. Then, it waits for 1 second and kills the process with the SIGTERM signal. Finally, it returns a response to confirm that the process has stopped.

Environment creation trigger ``(/create)``
-------------------------------------------------
	===============  =================================================== 
	Returns          ``Created``
	POST parameters	 ``None``
	GET parameters	 ``None`` or ``server_id`` (if platform is Discord)
	===============  ===================================================

	This route is responsible for creating the environment for the exercise based on the platform selected.

	If the platform selected is "discord", the route will call the `create_environment() <./Discord.html#create_environment>`_ function from the ``T3SF.discord.bot`` module passing the ``server_id`` obtained from the request arguments as a parameter. This function will create the necessary channels and categories on the Discord server based on the predefined list.

	On the other hand, if the platform selected is "slack", the route will call the `create_environment() <./Slack.html#create_environment>`_ function from the ``T3SF.slack.bot`` module. This function will create the necessary channels and categories on the Slack workspace based on the predefined list.

Logs Stream ``(/stream)``
----------------------------
	===============  ======================= 
	Returns          ``SSE``
	POST parameters	 ``None``
	GET parameters	 ``None``
	===============  =======================

	This route is designed to stream log messages and real-time updates to the client via Server-Sent Events. It first yields any previous log messages that were written to the ``logs.txt`` file, and then listens for new messages using the ``MessageAnnouncer().listen()`` function, which returns a ``queue.Queue`` of messages. The function blocks until a new message arrives, and then yields that message to the client.

	The route returns a Response object with the stream of log messages and real-time updates, and the mimetype is set to ``'text/event-stream'``. This format is used to stream text-based data in real-time over HTTP.

Env Creation Logs Stream ``(/stream_news)``
---------------------------------------------------
	===============  ======================= 
	Returns          ``SSE``
	POST parameters	 ``None``
	GET parameters	 ``None``
	===============  =======================

	This path acts in the same way as `/stream <#logs-stream-stream>`_. The only difference between the two is that this route does not show the old logs, but only the new ones. This path is used to display the logs on the environment creation page.


Logs cleaner ``(/clear)``
---------------------------------------------------
	===============  ======================= 
	Returns          ``Logs cleared...``
	POST parameters	 ``None``
	GET parameters	 ``None``
	===============  =======================

	This route clears the logs stored in a file named ``logs.txt``. It is used to remove old log data that may no longer be relevant. The function opens the file in write mode and then immediately closes it, which effectively clears all the data in the file. It then returns a message confirming that the logs have been cleared.


Module
=======

Keeping the modular structure of the framework, the GUI class is in charge of the creation of the virtual interface and the visual management of the framework, along with other extra features.

The file structure is shown below:

.. code-block:: bash

	GUI
	├── core.py
	├── __init__.py
	└── templates
	    ├── base.html
	    ├── env_creation.html
	    ├── index.html
	    └── msel_viewer.html


.. py:class:: GUI(platform_run, MSEL, import_name=__name__, *args, **kwargs)
	
	This class creates the GUI handler, inheriting the Flask module.

		.. confval:: platform_run

			The selected platform.

			:type: ``str``
			:required: ``True``

		.. confval:: MSEL

			The location of the MSEL.

			:type: ``str``
			:required: ``True``

		.. confval:: import_name

			The location of the MSEL.

			:type: ``built-in Python variable``
			:required: ``False``

	.. py:method:: start_flask_app()

		This method will start Flask, making it listen on ``127.0.0.1:5000`` and threading.

	.. py:method:: start()

		This method will create a thread to execute Flask inside it, calling `start_flask_app() <#GUI.start_flask_app>`_.