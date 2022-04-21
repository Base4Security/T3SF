Usage
=============

We basically created the framework to be fast and easy to setup, so if you want to run the bot in Discord, WhatsApp or Telegram you have to simply initiate the T3SF class!

Here is a code snippet as example!

.. code-block:: python3

	[...]
	
	from T3SF import *

	bot = Bot(token=os.environ['TELEGRAM_TOKEN'])

	T3SF = T3SF(bot=bot)
	
	[...]


Here is an example with the Slack bot

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