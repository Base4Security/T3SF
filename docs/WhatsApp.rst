*******************
WhatsApp
*******************

.. warning:: We are currently working to give WhatsApp support to latest version of T3SF. Please use ``Version 1.1`` if you want to run an exercise on this platform.

.. contents:: Table of Contents

We are expaning our framework's support to this new platform as clients requested us. Not all the functions/features from the main platforms (Discord/Slack) could be migrated due to WhatsApp limitations.

Functions
===============

.. py:function:: SendMessage(title, description, ctx=None, player=None, image=None)

	Message sending controller.

	.. confval:: title

		The title of the message.

		:type: ``str``
		:required: ``True``

	.. confval:: description

		The description/main text of the message.

		:type: ``str``
		:required: ``True``

	.. confval:: ctx

		:type: ``ctx``
		:required: ``True``

	.. confval:: player

	The player's inbox id to send the message.

		:type: ``int``
		:required: ``False``

	.. confval:: image

	Attach an image to the message.

		:type: ``str``
		:required: ``False``


.. py:function:: InboxFetcher(inbox)
	
	Fetches half manual, half automatically the inboxes, based in a command (``!add``) from the game master in the inbox channel, notifies the Game masters about differents parts of this process.
	
	.. confval:: inbox

	Parameter containing the Chat Name.

		:type: ``array``
		:required: ``True``


.. py:function:: InboxesAuto(message=None)

	Checks the amount of players and the amount of inboxes to start/resume the simulation. Based in the function :py:meth:`InboxFetcher`

	.. confval:: message

	The message from the game master, to add an inbox to the list.

		:type: ``str``
		:required: ``False``


.. py:function:: InjectHandler(self)
	
	Gives the format to the inject and sends it to the correct player's inbox.


Bot
===============

Installation
------------------

1. Git clone this repository.
2. Go inside the WhatsApp version folder with ``cd T3SF/Whatsapp/``
3. Install requirements.
	``pip3 install -r requirements.txt``
	
	(Optional) Create a virtual envirnoment
	``python3 -m venv venv``
4. Run the bot with ``python3 bot.py``
	(Optional) Scan the QR code to login.

	We recommend using a business WhatsApp account and a non-everyday phone number.
5. Add the Bot to every group, such as Inboxes group, GM-Chat, etc.
6. Done!