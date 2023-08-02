************************
CORE Functions
************************

CORE functions are those functions that are to be used regardless of the selected platform. Basically they are functions for all platforms.

.. py:function:: TimeDifference(actual_real_time:int, previous_real_time:int, itinerator:int, resumed:bool)
	:async:

	Get the difference between two injects. It will make the bot sleep and inform the Game Masters.

	.. confval:: actual_real_time
		
		The actual inject's time.

		:type: ``int``
		:required: ``True``

	.. confval:: previous_real_time
		
		The previous inject's time.

		:type: ``int``
		:required: ``True``


	.. confval:: itinerator
		
		The inject's number. Used when :confval:`resumed` is ``True``.

		:type: ``int``
		:default: ``None``
		:required: ``False``


	.. confval:: resumed
		
		:type: ``bool``
		:default: ``None``
		:required: ``False``

.. py:function:: NotifyGameMasters(type_info:str)
	:async:

	Notify the Game Masters of the different states of the bot, through messages.
	
	.. confval:: type_info

		:type: ``str``
		:required: ``True``

.. py:function:: ProcessIncidents(ctx, function_type:str=None, itinerator:int=0)
	:async:

	Process the incidents from the MSEL file.

	.. confval:: ctx

		:type: ``object|array``
		:required: ``True``

	.. confval:: function_type
		
		Depending the command sent (Start/Resume).

		:type: ``str``
		:required: ``True``


	.. confval:: itinerator

		Inject number retrieved from the Game Master, used when :confval:`function_type` equals ``"resume"``.

		:type: ``int``
		:default: ``None``
		:required: ``False``

.. py:function:: IncidentsFetcher(self)
	
	Retrieves the incidents from the desired source, chosen in the config file.

.. py:function:: start(MSEL:str, platform, gui=False)
	:async:

	Start the framework. This function takes care of starting the platform bot and also the GUI.
	
	.. confval:: MSEL

		The location of the MSEL.

		:type: ``str``
		:required: ``True``

	.. confval:: platform

		The platform selected for the exercise.

		:type: ``str``
		:required: ``True``

	.. confval:: gui

		A boolean to determine if we should start the visual interface.

		:type: ``bool``
		:required: ``False``

.. py:function:: check_status(reset: bool = False) -> Union[bool, str]
	:async:

	Monitors the framework's status. It can reset flags, handle framework breaks, and wait until the framework is ready to proceed. Its purpose is to ensure smooth operation and synchronization within the framework.

	.. confval:: reset

		Reset flag to indicate whether to reset the process_wait and process_quit flags.

		:type: ``bool``
		:default: ``False``
		:required: ``False``

	:return: Returns a boolean indicating the status of the framework or 'break' if process_quit is True.