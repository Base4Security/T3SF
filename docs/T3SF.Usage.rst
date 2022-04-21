Usage
=============

We basically created the framework to be fast and easy to setup, so if you want to run the bot in Discord, WhatsApp or Telegram you have to simply initiate the T3SF class!

First we have the ``config.ini`` file. Here you will be able to choose the platform you are going to use ``Discord``, ``Slack``, ``Telegram`` or ``WhatsApp``.

Also, you will be able to set the MSEL file's location. Normally you have this file in the same directory as the bot, but you can put it with a complete path!

Below you can find an example config for Discord!

.. code-block::

	[General]
	Platform : Discord

	TTX_File : MSEL_BASE4.json

---------------------------------------------

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

---------------------------------------------

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