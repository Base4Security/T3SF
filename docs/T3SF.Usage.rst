*******************
Usage
*******************

.. contents:: Table of Contents

We basically created the framework to be fast and easy to setup, so if you want to run the bot in Discord, WhatsApp or Telegram you have to simply initiate the T3SF class!

Setting config.ini
====================

First we have the ``config.ini`` file. Here you will be able to choose the platform you are going to use ``Discord``, ``Slack``, ``Telegram`` or ``WhatsApp``.

Also, you will be able to set the MSEL file's location. Normally you have this file in the same directory as the bot, but you can put it with a complete path!

Below you can find an example config for Discord!

.. code-block::

	[General]
	Platform : Discord

	TTX_File : MSEL_BASE4.json


Initializing T3SF class
=========================

To initiate the class, you have a different two parameters. Depending on the platform, one is used instead of the other:

.. confval:: bot

	The bot instance.

	:type: ``str``
	:required: ``False`` -> ``True`` in case that you set the platform as ``Discord/Telegram/WhatsApp``
	:default: ``None``

.. confval:: app

	The app instance.

	:type: ``str``
	:required: ``False`` -> ``True`` in case that you set the platform as ``Slack``
	:default: ``None``

After you set everything up, you'll probably start coding! Here are some examples to guide you!

This example is for a Telegram bot:

.. code-block:: python3

	[...]
	
	from T3SF import *

	bot = Bot(token=os.environ['TELEGRAM_TOKEN'])

	T3SF = T3SF(bot=bot)
	
	[...]


Here is an example with the Slack bot:

.. code-block:: python3

	[...]
	
	from T3SF import *

	app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])

	T3SF = T3SF(app=app)
	
	[...]

And that's it!


MSEL Configuration
===================

The file where you have all injects stored is the Master Scenario Events List (MSEL). From this file, the framework is going to retrieve all the messages and players, so it's like the Heart of the training!

Format
---------

Inside the repo you have an example of a common MSEL, but we will be explaining in a short and easy way the format of it.

Here is the first inject from the example in the repo.

.. code-block:: json

	{
	    "#": 1,
	    "Real Time": "07:29 AM",
	    "Date": "Monday 9:30 AM",
	    "Subject": "Anomalous Files Detected",
	    "From": "Amazon Web Services",
	    "Player": "Information Security",
	    "Script": "We detected some anomalous files in your S3 Bucket.",
	    "Picture Name": "S3_Bucket.png",
	    "Photo": "https://img2.helpnetsecurity.com/posts2018/aws-s3-buckets-public.jpg",
	    "Profile": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Amazon_Web_Services_Logo.svg/1024px-Amazon_Web_Services_Logo.svg.png"
 	}	

.. confval:: #

	The inject/incident number.

	:type: ``int``
	:required: ``True``

.. confval:: Real Time

	The actual time by which the incident should arrive in the player's inbox. This will not be shown to the player.
	
	.. note:: 
		We are mainly using the minutes of this key to make things work.

	:type: ``str``
	:required: ``True``

.. confval:: Date

	The simulated date of the incident. This will be displayed to the player.

	:type: ``str``
	:required: ``True``

.. confval:: Subject

	The Subject from the incident.

	:type: ``str``
	:required: ``True``

.. confval:: From

	The sender of the incident/message.

	:type: ``str``
	:required: ``True``

.. confval:: Player

	The player's name, eg. ``"Information Security"``, ``"Legal"``, ``"SRE"``.

	:type: ``str``
	:required: ``True``

.. confval:: Script

	The main text and the incident body of the message.

	:type: ``str``
	:required: ``True``

.. confval:: Picture Name

	The attachment's name.

	.. note::
		This key is used in :doc:`./Slack`.

	:type: ``str`` -> Web URL
	:required: ``False`` -> ``True`` if the platform is :doc:`./Slack`.

.. confval:: Photo

	An attached photo for the incident.

	.. note:: 
		In WhatsApp the photo **should be a local PATH**. In other platforms, you can use the image url from internet.

	:type: ``str`` -> Web URL
	:required: ``False``

.. confval:: Profile

	The profile picture from the sender. If a profile picture is not set for an incident, a default user avatar is going to be used.

	.. note:: 
		This key is only valid in :doc:`./Discord` and :doc:`./Slack`, due to platform restrictions.

	:type: ``str`` -> Web URL
	:required: ``False`` -> ``True`` if the platform is :doc:`./Discord` or :doc:`./Slack`.
