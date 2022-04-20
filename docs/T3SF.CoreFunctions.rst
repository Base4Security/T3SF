Core functions
===================

.. py:function:: TimeDifference(actual_real_time:int, previous_real_time:int, itinerator:int, resumed:bool)
	
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

	Notify the Game Masters of the different states of the bot, through messages.
	
	.. confval:: type_info

	:type: ``str``
	:required: ``True``


.. py:function:: ProcessIncidents(ctx, function_type:str=None, itinerator:int=0)
	
	Process the incidents from the MSEL file.

	.. confval:: ctx

	:type: ``ctx``
	:required: ``True``

	.. confval:: function_type
		
	Depending the command sent (Start/Resume).

	:type: ``str``
	:required: ``True``


	.. confval:: itinerator

	Inject number retrieved from the Game Master, used with :confval:`function_type` equals ``"resume"``.

	:type: ``int``
	:default: ``None``
	:required: ``False``


.. py:function:: IncidentsFetcher(self)
	
	Retrieves the incidents from the desired source, chosen in the config file.


.. py:function:: similar(a, b)

	Based in graphics, find the similarity between 2 strings.
	
	.. confval:: a

	:type: ``str``
	:required: ``True``

	.. confval:: b

	:type: ``str``
	:required: ``True``


.. py:function:: regex_finder(input)

		Matches repeated words counting the amount of times the word is being repeated.
		
		.. note:: 
			This function is used for Slack.
	
	.. confval:: input

	:type: ``array``
	:required: ``True``
