*******************
Telegram
*******************

.. contents:: Table of Contents

We are expaning our framework's support to this new platform as clients requested us. Not all the functions/features from the main platforms (Discord/Slack) could be migrated due to Telegram limitations.

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
		:required: ``False``

	.. confval:: player

	The player's inbox id to send the message.

		:type: ``int``
		:required: ``False``

	.. confval:: image

	Attach an image to the message.

		:type: ``str``
		:required: ``False``


.. py:function:: EditMessage(title, description, response)

	Message editing controller.

	.. confval:: title

		The title of the message.

		:type: ``str``
		:required: ``True``

	.. confval:: description

		The description/main text of the message.

		:type: ``str``
		:required: ``True``

	.. confval:: response

		The previous response message's object containing the edit message function.

		:type: ``object``
		:required: ``True``


.. py:function:: InboxesAuto(message=None)

	Fetches half manual, half automatically the inboxes, based in a command (``!add``) from the game master in the inbox channel, notifies the Game masters about differents parts of this process.

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
2. Go inside the Telegram version folder with ``cd T3SF/Telegram/``
3. Install requirements.
	``pip3 install -r requirements.txt``
	
	(Optional) Create a virtual enviroment
	``python3 -m venv venv``
4. Create/Get the Bot's token from `@BotFather <https://t.me/BotFather>`_.
5. Add the token to en ``.env`` file.
6. Run the bot with ``python3 bot.py``
7. Add the Bot to every channel, such as Inboxes channel, GM-Chat, etc.
8. Done!