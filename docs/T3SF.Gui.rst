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

	This route provides a real-time log display with user-friendly controls to start, pause, resume and stop exercises with a click. It also features a log level filter, which allows game-master/admins to reduce noise in the logs by only displaying relevant information. If necessary, game-master can clear the previous logs directly from the interface to obtain a clean view before starting a new exercise.

	.. image:: ./images/gui/index.png

MSEL Playground ``(/msel-playground)``
--------------------------------
	===============  ======================= 
	Renders          ``msel_playground.html``
	POST parameters	 ``None``
	GET parameters	 ``None``
	===============  =======================

	The MSEL Playground, is an enhanced viewer that now supports .xlsx, .xls, and .json file formats. Easily load and view your MSELs in the browser, with pagination for seamless navigation through injects. Export your MSEL to .json, and enjoy real-time editing, backed by event and scenario databases. Explore, edit, and save your work effortlessly in the MSEL Playground.

	.. image:: ./images/gui/msel_playground.png

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

Start Exercise ``(/start)``
-----------------------------------------------
	===============  =================================================== 
	Returns          ``Started``
	POST parameters	 ``None``
	GET parameters	 ``None``
	Triggers	 	 :py:meth:`run_async_incidents` (Based on platform)
	===============  ===================================================

	Is responsible for initiating the exercise by calling the ``run_async_incidents`` function based on the selected platform. Once the function is called, the exercise will begin, and the function will continuously execute until all incidents are completed.

Pause Exercise ``(/pause)``
-----------------------------------------------
	===============  ======================= 
	Returns          ``We are waiting``
	POST parameters	 ``None``
	GET parameters	 ``None``
	===============  =======================


	Thi endpoint enables the pausing of an exercise by setting a flag in the utils module to indicate that the process should wait. It returns a simple message, "We are waiting", confirming the pause action.

Resume Exercise ``(/resume)``
-----------------------------------------------
	===============  ======================= 
	Returns          ``We are processing again``
	POST parameters	 ``None``
	GET parameters	 ``None``
	===============  =======================

	The `/resume` endpoint resumes the exercise by resetting the flags in the utils module. It sets the ``process_wait`` flag to False, indicating that the process can continue. It also sets ``process_quit`` to False and ``process_started`` to True. The endpoint returns the message "We are processing again" to signify the resumption of the exercise.

Stop Exercise ``(/stop)``
-----------------------------------------------
	===============  ======================= 
	Returns          ``We are Stoping``
	POST parameters	 ``None``
	GET parameters	 ``None``
	===============  =======================

	The route `/stop` is used to stop the exercise in progress by setting the ``process_quit`` flag in the utils module to True. This flag indicates that the exercise should be halted. The endpoint returns the message "We are stopping" to confirm that the stopping process has been triggered.


Kill script ``(/abort)``
-----------------------------------------------
	===============  ======================= 
	Returns          ``Shutting down...``
	POST parameters	 ``None``
	GET parameters	 ``None``
	===============  =======================

	The route `/abort` is used to kill the script in case of an emergency. When this route is accessed, it kills the bot by sending an "INFO" message with a timestamp using the :py:meth:`MessageAnnouncer` class. Then, it waits for 0.5 seconds and kills the process with the SIGTERM signal. Finally, it returns a response to confirm that the process has stopped.

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

Events database fetcher ``(/data)``
---------------------------------------------------
	===============  ===================================================
	HTTP Methods     ``POST``
	Returns          JSON response containing DataTables-compatible data
	POST parameters  ``draw``, ``start``, ``length``, ``search[value]``, ``phaseFilter``, ``sectorFilter``, ``order[0][column]``, ``order[0][dir]``
	===============  ===================================================

	The `/data` endpoint retrieves data from an SQLite database based on the provided DataTables request parameters. The endpoint accepts a POST request and expects the following parameters:

	- ``draw``: An integer representing the draw counter to ensure data integrity.
	- ``start``: An integer representing the starting index of the data to retrieve.
	- ``length``: An integer representing the number of records to fetch.
	- ``search[value]``: A string representing the search value to filter the data.
	- ``phaseFilter``: An optional string representing the selected filter for the exercise phase.
	- ``sectorFilter``: An optional string representing the selected filter for the sector.
	- ``order[0][column]``: An integer representing the index of the column to sort by.
	- ``order[0][dir]``: A string representing the sorting direction (asc or desc).

	The endpoint connects to the SQLite database and constructs an SQL query based on the provided parameters. It retrieves the filtered and paginated data from the "events" table. The query also considers the selected filters and applies them accordingly.

	The resulting data is transformed into a JSON format compatible with DataTables. The response includes the following attributes:

	- ``draw``: The same draw value received in the request.
	- ``recordsTotal``: The total number of records in the "events" table.
	- ``recordsFiltered``: The total number of records after applying the search and filters.
	- ``data``: An array of dictionaries representing the retrieved data rows.

MSELs database fetcher ``(/msels-data)``
---------------------------------------------------
	===============  ===================================================
	HTTP Methods     ``POST``
	Returns          JSON response containing DataTables-compatible data
	POST parameters  ``draw``, ``start``, ``length``, ``search[value]``, ``order[0][column]``, ``order[0][dir]``
	===============  ===================================================

	The `/msels-data` endpoint retrieves data from an SQLite database related to MSELS (Master Sequence of Events List) information. It expects a POST request with the following parameters:

	- ``draw``: An integer representing the draw counter to ensure data integrity.
	- ``start``: An integer representing the starting index of the data to retrieve.
	- ``length``: An integer representing the number of records to fetch.
	- ``search[value]``: A string representing the search value to filter the data.
	- ``order[0][column]``: An integer representing the index of the column to sort by.
	- ``order[0][dir]``: A string representing the sorting direction (asc or desc).

	The endpoint connects to the SQLite database and constructs an SQL query based on the provided parameters. It retrieves the filtered and paginated data from the "MSELS_info" table. The query considers the search value, sorting column, and sorting direction.

	The resulting data is transformed into a JSON format compatible with DataTables. The response includes the following attributes:

	- ``draw``: The same draw value received in the request.
	- ``recordsTotal``: The total number of records in the "MSELS_info" table.
	- ``recordsFiltered``: The total number of records after applying the search.
	- ``data``: An array of dictionaries representing the retrieved data rows.

Injects/Events fetcher ``(/get-injects)``
---------------------------------------------------
	===============  ===================================================
	HTTP Methods     ``POST``
	Returns          JSON response containing inject data
	POST parameters  ``ids``, ``from``
	===============  ===================================================

	The `/get-injects` endpoint retrieves inject data based on the provided IDs. It expects a POST request with the following parameters:

	- ``ids``: A list of IDs representing the injects to retrieve.
	- ``from``: A string indicating the source of the injects ("MSEL" or empty for the default "events" table).

	The endpoint connects to the SQLite database and retrieves the injects based on the given IDs. It fetches the relevant data from either the "events" table or the "MSELS_events" table, depending on the source specified.

	The resulting inject data is returned as a JSON response, containing an array of dictionaries representing the injects.

MSELs database fetcher ``(/get-filters)``
---------------------------------------------------
	===============  ===================================================
	HTTP Methods     ``GET``
	Returns          JSON response containing filter options
	===============  ===================================================

	The `/get-filters` endpoint retrieves the filter options for the ExercisePhase and Sector dropdowns. It expects a GET request without any parameters.

	The endpoint connects to the SQLite database and retrieves the distinct values for the ExercisePhase and Sector columns from the "events" table. It converts the obtained options into lists of strings and removes any duplicates.

	The resulting filter options are returned as a JSON response, including the ExercisePhase and Sector options as separate lists.

Framework Status checker ``(/framework-status)``
---------------------------------------------------
	===============  ===================================================
	HTTP Methods     ``GET``
	Returns          JSON response containing framework status
	===============  ===================================================

	The `/framework-status` endpoint retrieves the status of the framework. It expects a GET request without any parameters.

	The endpoint checks the status flags stored in the ``utils`` module to determine the current state of the framework. It provides information about whether the framework is actively running, paused, stopped, or in the process of starting.

	The resulting framework status is returned as a JSON response, containing the current status as a string.


Module
=======

Keeping the modular structure of the framework, the GUI class is in charge of the creation of the virtual interface and the visual management of the framework, along with other extra features.

The file structure is shown below:

.. code-block:: bash

	GUI
	├── core.py
	├── __init__.py
	├── static
	│	├── imgs
	│	│	├── icon.png
	│	│	├── logo-dark.png
	│	│	└── logo-light.png
	│	└── js
	│		├── bootstrap_toasts.js
	│		├── copy.js
	│		├── theme_switcher.js
	│		└── vanilla-jsoneditor
	│			├── CHANGELOG.md
	│			├── index.d.ts
	│			├── index.js
	│			├── index.js.map
	│			├── LICENSE.md
	│			├── package.json
	│			├── README.md
	│			├── SECURITY.md
	│			└── themes
	│				├── jse-theme-dark.css
	│				└── jse-theme-default.css
	└── templates
		├── base.html
		├── env_creation.html
		├── index.html
		└── msel_playground.html


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

		This method will start Flask threaded and making it listen on ``127.0.0.1:5000`` when running on your machine or on ``0.0.0.0:5000`` when running on a Docker container.

	.. py:method:: start()

		This method will create a thread to execute Flask inside it, calling `start_flask_app() <#GUI.start_flask_app>`_.