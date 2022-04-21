Multi Platform Handlers
=========================

These functions, unlike the CORE ones, will be like handlers, calling other platform-based functions depending on the platform selected in the ``config.ini`` file.

So if we need to send a message, we'll use :py:meth:`SendMessage` and in there we'll handle the correct platform to send the message.

.. py:function:: SendMessage(title:str=None, description:str=None, color_ds:str=None, color_sl:str=None, channel=None, image=None, author=None, buttons=None, text_input=None, checkboxes=None)

	Message sending controller for all platforms.

	.. confval:: title

		The title of the message.

		:type: ``str``
		:required: ``True``

	.. confval:: description

		The description/main text of the message.

		:type: ``str``
		:required: ``True``

	.. confval:: color_ds

	Parameter with the color of the embedded message.

		.. note::
			This parameter is only used for Discord.

		:type: ``str``
		:required: ``False``

	.. confval:: color_sl

	Parameter with the color of the embedded message.
		
		.. note::
			This parameter is only used for Slack. Go to `Slack.Formatter <Slack.html#Formatter>`_ for references.

		:type: ``str``
		:required: ``False``
	

	.. confval:: channel

		Parameter with the desired destination channel.

		.. note::
			This parameter is only used for Slack.

		:type: ``str``
		:required: ``False``

	.. confval:: image

		.. note::
			This parameter is only used for Slack. Go to `Slack.Formatter <Slack.html#Formatter>`_ for references.

		:type: ``array``
		:required: ``False``

	.. confval:: author

		.. note::
			This parameter is only used for Slack. Go to `Slack.Formatter <Slack.html#Formatter>`_ for references.

		:type: ``array``
		:required: ``False``

	.. confval:: buttons

		.. note::
			This parameter is only used for Slack. Go to `Slack.Formatter <Slack.html#Formatter>`_ for references. 

		:type: ``array``
		:required: ``False``

	.. confval:: text_input

		.. note::
			This parameter is only used for Slack. Go to `Slack.Formatter <Slack.html#Formatter>`_ for references.

		:type: ``array``
		:required: ``False``

	.. confval:: checkboxes

		.. note::
			This parameter is only used for Slack. Go to `Slack.Formatter <Slack.html#Formatter>`_ for references.

		:type: ``array``
		:required: ``False``


.. py:function:: EditMessage(title:str=None, description:str=None, color_ds:str=None, color_sl:str=None, response=None, variable=None, image=None, author=None, buttons=None, text_input=None, checkboxes=None)

	Message editing controller for all platforms (which allow editing messages).

	.. confval:: title

		The title of the message.

		:type: ``str``
		:required: ``True``

	.. confval:: description

		The description/main text of the message.

		:type: ``str``
		:required: ``True``

	.. confval:: color_ds

	Parameter with the color of the embedded message.

		.. note::
			This parameter is only used for Discord.

		:type: ``str``
		:required: ``False``

	.. confval:: color_sl

	Parameter with the color of the embedded message.
		
		.. note::
			This parameter is only used for Slack. Go to `Slack.Formatter <Slack.html#Formatter>`_ for references.

		:type: ``str``
		:required: ``False``
	

	.. confval:: response

		Parameter with the previous response.

		.. note::
			This parameter is only used for Slack.

		:type: ``array``
		:required: ``False``

	.. confval:: variable

		Parameter with the previous response, containing the method to edit messages.

		.. note::
			This parameter is only used for Discord.

		:type: ``str``
		:required: ``False``

	.. confval:: image

		.. note::
			This parameter is only used for Slack. Go to `Slack.Formatter <Slack.html#Formatter>`_ for references.

		:type: ``array``
		:required: ``False``

	.. confval:: author

		.. note::
			This parameter is only used for Slack. Go to `Slack.Formatter <Slack.html#Formatter>`_ for references.

		:type: ``array``
		:required: ``False``

	.. confval:: buttons

		.. note::
			This parameter is only used for Slack. Go to `Slack.Formatter <Slack.html#Formatter>`_ for references.

		:type: ``array``
		:required: ``False``

	.. confval:: text_input

		.. note::
			This parameter is only used for Slack. Go to `Slack.Formatter <Slack.html#Formatter>`_ for references.

		:type: ``array``
		:required: ``False``

	.. confval:: checkboxes

		.. note::
			This parameter is only used for Slack. Go to `Slack.Formatter <Slack.html#Formatter>`_ for references.

		:type: ``array``
		:required: ``False``


.. py:function:: SendIncident(inject)

	Send the current incident to the correct player.
	
	.. confval:: inject

	:type: ``array``
	:required: ``True``


.. py:function:: RegexHandler(ack=None, body=None, payload=None, inbox=None)

	In charge of the inboxes gathering part.

	.. note:: 
		This function is just used by WhatsApp and Slack.
	
	.. confval:: ack

	:type: ``object``
	:required: ``False``

	.. confval:: body

	:type: ``array``
	:required: ``false``

	.. confval:: payload

	:type: ``array``
	:required: ``false``

	.. confval:: inbox

	:type: ``str``
	:required: ``false``


.. py:function:: InboxesAuto(message=None)

	Handler for the Automatic gathering of inboxes. 
	
	.. confval:: message

	:type: ``str``
	:required: ``False``

