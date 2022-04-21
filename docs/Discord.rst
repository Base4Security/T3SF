*******************
Discord
*******************

.. contents:: Table of Contents

Discord was the main platform for the bot! Many new features, bug fixes and tests since the first release!

Functions
===============

.. py:function:: SendMessage(color_ds=None, style:str="simple", title:str=None, description:str=None)

	Message sending controller.

	.. confval:: color_ds

	Parameter with the color of the embedded message.

		:type: ``str``
		:required: ``False``

	.. confval:: title

		The title of the message.

		:type: ``str``
		:required: ``True``

	.. confval:: description

		The description/main text of the message.

		:type: ``str``
		:required: ``True``


.. py:function:: EditMessage(color_ds=None, style:str="simple", title:str=None, description:str=None)

	Message editing controller.

	.. confval:: color_ds

	Parameter with the color of the embedded message.

		:type: ``str``
		:required: ``False``

	.. confval:: title

		The title of the message.

		:type: ``str``
		:required: ``True``

	.. confval:: description

		The description/main text of the message.

		:type: ``str``
		:required: ``True``


.. py:function:: InboxesAuto(self)

	Fetches automatically all the inboxes, based in a regular expression (RegEx), notifies the Game masters about differents parts of this process.


.. py:function:: InjectHandler(self)
	
	Gives the format to the inject and sends it to the correct player's inbox.

Bot
===============

Installation
------------------

1. Git clone this repository.
2. Go inside the Discord version folder with ``cd T3SF/Discord/``
3. Install requirements.
	``pip3 install -r requirements.txt``
	
	(Optional) Create a virtual enviroment
	``python3 -m venv venv``
4. Add Discord token to ``.env`` file.
5. Run the bot with ``python3 bot.py``
6. Add the bot to the server.
7. Done!