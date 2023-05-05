*******************
Slack
*******************

.. contents:: Table of Contents

Slack is the new platform we are expanding to given the needs of our clients! The heart of the bot is still the same, we just made some improvements to it so it can walk around smoothly!

Bot
===============

To perform an exercise based on the Slack platform, you will need to provide an *APP* and a *BOT* token. If you already have an app created, you can skip the creation part and go straight to the provisioning part.

App/Bot setup
------------------
#. Create a Workspace in slack (You can skip this step if you have already a workspace).
#. Navigate to `Slack Apps <https://api.slack.com/apps/>`_.
#. Select "Create New App".
#. Select the option "From an app manifest".
#. Select your workspace.
#. Selecting the format "YAML", paste the code inside ``bot_manifest.yml`` located in the following `link <https://github.com/Base4Security/T3SF/blob/main/examples/Slack/bot_manifest.yml>`_
#. Create the App.
#. With the recently created app, and in the Basic Information menu, scroll to ``App-Level Tokens``, Generate a token and Scopes.
#. You can use any Token name, the important thing is that you add both scopes to the token: ``connections:write`` and ``authorizations:read``.
#. Generate it, copy it and keep it in a safe place, because you will only see it once.
#. Now navigate to the "OAuth & permissions" sub-menu inside the Feautures sidebar menu.
#. Copy the ``Bot User OAuth Token``.
#. For the bot to be able to respond to your messages, you must add the App within that channel. You can do this by tagging the App name or adding it manually.
#. Yeah! You are ready to go now!

Starting the Framework
========================

Once you have installed in all the `libraries dependent on the platform <T3SF.Installation.html#slack>`_, and added it to your workspace, you will need to provide the app and bot token to the framework for it to work and choose the Slack platform on ``T3SF.start``.

Providing the tokens
------------------------------

The framework expects an *APP* and *BOT* token with the names ``SLACK_BOT_TOKEN`` and ``SLACK_APP_TOKEN``.

You have two common options for this:

1. Create a ``.env`` file
	#. On the same path as your ``main.py`` file create a ``.env`` file
	#. Inside of it, add the variable ``SLACK_APP_TOKEN`` and your app's token, as following: ``SLACK_APP_TOKEN=xapp-1-Z03ZJ58JUTF-3463422570419-p11no1l1q9po6qq96p1n383378q17032p08l7n8015mp1mn067q075n9q48m8434``
	#. Also, add the variable ``SLACK_BOT_TOKEN`` and the bot's token, as following: ``SLACK_BOT_TOKEN=xoxb-4239546374990-4236264338677-jQqt0XeIMVgDAGNNnJaydQkk``
	#. Your file should look like this
	 .. code-block:: bash

		 SLACK_APP_TOKEN=xapp-1-Z03ZJ58JUTF-3463422570419-p11no1l1q9po6qq96p1n383378q17032p08l7n8015mp1mn067q075n9q48m8434
		 SLACK_BOT_TOKEN=xoxb-4239546374990-4236264338677-jQqt0XeIMVgDAGNNnJaydQkk
	
	.. note:: Note that the tokens will be stored and everyone with read access to the file will be able to read them.

2. Export the variables to your shell environment
	#. Create a variable with the name ``SLACK_APP_TOKEN`` as following: ``export SLACK_APP_TOKEN=xapp-1-Z03ZJ58JUTF-3463422570419-p11no1l1q9po6qq96p1n383378q17032p08l7n8015mp1mn067q075n9q48m8434``
	#. Create another variable with the name ``SLACK_BOT_TOKEN`` as following: ``export SLACK_BOT_TOKEN=xoxb-4239546374990-4236264338677-jQqt0XeIMVgDAGNNnJaydQkk``
	#. Your ``env`` should look like this
	 .. code-block:: bash
		
		[...]
		SLACK_APP_TOKEN=xapp-1-Z03ZJ58JUTF-3463422570419-p11no1l1q9po6qq96p1n383378q17032p08l7n8015mp1mn067q075n9q48m8434
		SLACK_BOT_TOKEN=xoxb-4239546374990-4236264338677-jQqt0XeIMVgDAGNNnJaydQkk
		[...]

Initializing the framework
----------------------------

As explained in the `Initializing T3SF <T3SF.Usage.html#initializing-t3sf>`_ page, you will need to set 3 variables inside your ``main.py`` file.

This example is for an exercise using Slack with a GUI:

.. code-block:: python3
	
	from T3SF import T3SF
	import asyncio

	async def main():
		await T3SF.start(MSEL="MSEL_Company.json", platform="Slack", gui=True)

	if __name__ == '__main__':
		asyncio.run(main())

And that's it!

Module
======

To maintain the modular structure of the framework, we developed a module with all the platform specific functions inside. Including the integrated bot and the functions to contact the Slack API.

The file structure is shown below:

.. code-block:: bash

	Slack
	├── bot.py
	├── __init__.py
	└── slack.py

Class Functions
-----------------

.. py:function:: Formatter(title=None, description=None, color="#5bc0de", image=None, author=None, buttons=None, text_input=None, checkboxes=None)
	
	Creates the embed messages, with a different set of options.

	.. confval:: title

	The title of the message.

		:type: ``str``
		:required: ``False``

	.. confval:: description

	The description/main text of the message.

		:type: ``str``
		:required: ``False``

	.. confval:: color

	Parameter with the color of the embedded message.

		:type: ``str``
		:required: ``False``
		:default: `"#5bc0de"`

	.. confval:: image

	Attach an image to the message.

		:type: ``array``
		:required: ``False``

	.. confval:: author

	Attach the author of the message.

		:type: ``array``
		:required: ``False``

	.. confval:: buttons

	Attach buttons to the message.

		:type: ``array``
		:required: ``False``


	.. confval:: text_input

	Attach a text area input to the message.

		:type: ``array``
		:required: ``False``

	.. confval:: checkboxes

	Attach textboxes to the message

		:type: ``array``
		:required: ``False``

.. py:function:: SendMessage(title:str=None, description:str=None, color_sl=None, channel=None, image=None, author=None, buttons=None, text_input=None, checkboxes=None)
	:async:

	Message sending controller.

	.. confval:: title

		The title of the message.

		:type: ``str``
		:required: ``True``

	.. confval:: description

		The description/main text of the message.

		:type: ``str``
		:required: ``True``

	.. confval:: color_sl

	Parameter with the color of the embedded message.
		
		:type: ``str``
		:required: ``False``	

	.. confval:: channel

		Parameter with the desired destination channel.

		:type: ``str``
		:required: ``False``

	.. confval:: image

		:type: ``array``
		:required: ``False``

	.. confval:: author

		:type: ``array``
		:required: ``False``

	.. confval:: buttons


		:type: ``array``
		:required: ``False``

	.. confval:: text_input

		:type: ``array``
		:required: ``False``

	.. confval:: checkboxes

		:type: ``array``
		:required: ``False``

.. py:function:: EditMessage(title:str=None, description:str=None, color_sl=None, response=None, image=None, author=None, buttons=None, text_input=None, checkboxes=None)
	:async:

	Message editing controller.

	.. confval:: title

		The title of the message.

		:type: ``str``
		:required: ``True``

	.. confval:: description

		The description/main text of the message.

		:type: ``str``
		:required: ``True``

	.. confval:: color_sl

	Parameter with the color of the embedded message.

		:type: ``str``
		:required: ``False``

	.. confval:: response

		Parameter with the previous response.

		:type: ``array``
		:required: ``False``

	.. confval:: image

		:type: ``array``
		:required: ``False``

	.. confval:: author

		:type: ``array``
		:required: ``False``

	.. confval:: buttons

		:type: ``array``
		:required: ``False``

	.. confval:: text_input

		:type: ``array``
		:required: ``False``

	.. confval:: checkboxes

		:type: ``array``
		:required: ``False``

.. py:function:: InboxesAuto(self)
	:async:

	Fetches automatically all the inboxes, based in a regular expression (RegEx), notifies the Game masters about differents parts of this process.

.. py:function:: InjectHandler(self)
	:async:

	Gives the format to the inject and sends it to the correct player's inbox.

.. py:function:: regex_finder(input)

	Tries to get a regular expresion on one string.

	.. confval:: input

		The input to find the regular expression.

		:type: ``str``
		:required: ``True``

.. py:function:: PollHandler(T3SF_instance)
	:async:

	Handles the injects with polls. Creates the poll with the two options and sends it to the player's channel.

	.. confval:: T3SF_instance

		An instance of the T3SF class.

		:type: ``obj``
		:required: ``True``

.. py:function:: PollAnswerHandler(T3SF_instance, body=None, payload=None)
	:async:

	Detects the answer in the poll sent. Modifies the poll message and notifies the game master about the selected option.

	.. confval:: T3SF_instance

		An instance of the T3SF class.

		:type: ``obj``
		:required: ``True``

	.. confval:: body

		The body of the interaction.

		:type: ``obj``
		:required: ``False``

	.. confval:: payload

		The user's input.

		:type: ``obj``
		:required: ``False``

.. py:function:: similar(a, b)

	Based in graphics, find the similarity between 2 strings.
	
	.. confval:: a

	:type: ``str``
	:required: ``True``

	.. confval:: b

	:type: ``str``
	:required: ``True``


Integrated bot
-----------------

We integrated the bot to fully manage the platform from within the framework. The bot handles poll responses, commands and environment creation.

.. py:class:: create_bot(MSEL)

	This class creates the bot, will handle the commands, messages and interactions with it.

		.. confval:: MSEL

			The location of the MSEL.

			:type: ``str``
			:required: ``True``

	.. py:method:: slack_main()

		Within this method, we will create the following command management functions.

		.. py:function:: regex_handler(ack, body, payload)
			:async:

			Handles the user's regular expression, at the start of the exercise.

			.. confval:: ack

				Acknowledge object to inform Slack that we have received the interaction.

				:type: ``obj``
				:required: ``True``

			.. confval:: body

				The body of the interaction.

				:type: ``obj``
				:required: ``True``

			.. confval:: payload

				The user's input.

				:type: ``obj``
				:required: ``True``

		.. py:function:: poll_handler(ack, body, payload)
			:async:

			Detects when the bot receives an interaction (as a response to a poll).

			.. confval:: ack

				Acknowledge object to inform Slack that we have received the interaction.

				:type: ``obj``
				:required: ``True``

			.. confval:: body

				The body of the interaction.

				:type: ``obj``
				:required: ``True``

			.. confval:: payload

				The user's input.

				:type: ``obj``
				:required: ``True``

		.. py:function:: ping(message, say)
			:async:

			Handles the ``!ping`` command and returns a `pong` message.

			.. confval:: message

				The content of the message, incluiding information about the workspace, channel, user, etc.

				:type: ``obj``
				:required: ``True``

			.. confval:: say

				A method to directly reply on the same channel to the message/command.

				:type: ``obj``
				:required: ``True``

		.. py:function:: start(message, say)
			:async:

			Handles the ``!start`` command and starts the exercise.

			.. confval:: message

				The content of the message, incluiding information about the workspace, channel, user, etc.

				:type: ``obj``
				:required: ``True``

			.. confval:: say

				A method to directly reply on the same channel to the message/command.

				:type: ``obj``
				:required: ``True``

		.. py:function:: not_interesting_messages(body, logger)
			:async:

			Handles all other messages, avoiding any noise in the logs.

			.. confval:: body

				The body of the message.

				:type: ``obj``
				:required: ``True``

			.. confval:: logger

				A method to log the message.

				:type: ``obj``
				:required: ``True``

.. py:function:: start_bot()
	:async:

	This function will create a task to start the bot immediately.

.. py:function:: run_async_incidents()
	:async:

	This function intancies the T3SF class and starts the exercise making use of `T3SF.ProcessIncidents <./T3SF.CoreFunctions.html#ProcessIncidents>`_.

.. py:function:: create_environment()
	:async:

	This function creates the environment for the exercise.

.. py:function:: get_admins()
	:async:

	It will get all the administrators in the workspace and return an array with their IDs.

.. py:function:: create_channel_if_not_exists(channel_name, private=True)
	:async:

	Create a channel if it does not already exist.

	.. confval:: channel_name

		The channel's name.

		:type: ``str``
		:required: ``True``

	.. confval:: private

		Determines if the channel should be private and only available to the members and admins.

		:type: ``bool``
		:required: ``False``

.. py:function:: create_gm_channels(admins)
	:async:

	Creates the Game Masters text channels.

	.. confval:: admins

		List of administrators to invite to the channels.

		:type: ``list``
		:required: ``True``


