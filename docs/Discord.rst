*******************
Discord
*******************

.. contents:: Table of Contents

Discord was the main platform for the bot! Many new features, bug fixes and tests since the first release!

Bot
===============

To perform an exercise based on the Discord platform, you will need to provide a Bot token. If you already have a bot created, you can skip the creation part and go straight to the provisioning part.

Bot creation
------------------

1. Navigate to `Discord Developers <https://discord.com/developers/applications>`_
2. Create a new application
3. Go to the *Bot* tab
  #. On the *Privileged Gateway Intents* enable all the intents 
  #. Enable *PRESENCE INTENT*
  #. Enable *SERVER MEMBERS INTENT*
  #. Enable *MESSAGE CONTENT INTENT*
4. Reset the bot token
5. Copy it and keep it in a safe place, because you will only see it once.


Inviting the bot to a server 
------------------------------

1. Navigate to `Discord Developers <https://discord.com/developers/applications>`_
2. Select you recently created Application
3. Go now to the *OAuth2* tab
4. Select the URL Generator
5. On *SCOPES*, select *"bot"* and on *BOT PERMISSIONS*, select *"Administrator"*
6. Navigate to the generate URL
7. You will be asked for the name of the server you want to add the bot to. *(You must be a user with server privileges or the server owner)*
8. Once the server is selected, authorize the bot to get Administrator privileges.
9. Done!

Starting the Framework
========================

Once you have installed in all the `libraries dependent on the platform <T3SF.Installation.html#discord>`_, created your bot and added it to your server, you will need to provide the token to the framework for it to work and choose the Discord platform on ``T3SF.start``.

Providing the token
------------------------

The framework expects a bot token with the name ``DISCORD_TOKEN``.

You have two common options for this:

1. Create a ``.env`` file
	#. On the same path as your ``main.py`` file create a ``.env`` file
	#. Inside of it, add the variable ``DISCORD_TOKEN`` and your bot's token, as following: ``DISCORD_TOKEN=MTEpMDU2OTc9MjQ0NDE4ODc2Mw.GP0bxK.5J2xWb3D40zSIRxYiJgGlNiTSq8OkSR4xCcvpY``
	
	.. note:: Note that the token will be stored and everyone with read access to the file will be able to read it.

2. Export the variable to your shell environment
	#. Create a variable with the name ``DISCORD_TOKEN`` as following: ``export DISCORD_TOKEN=MTEpMDU2OTc9MjQ0NDE4ODc2Mw.GP0bxK.5J2xWb3D40zSIRxYiJgGlNiTSq8OkSR4xCcvpY``

Initializing the framework
----------------------------

As explained in the `Initializing T3SF <T3SF.Usage.html#initializing-t3sf>`_ page, you will need to set 3 variables inside your ``main.py`` file.

This example is for an exercise using Discord with a GUI:

.. code-block:: python3
	
	from T3SF import T3SF
	import asyncio

	async def main():
		await T3SF.start(MSEL="MSEL_Company.json", platform="Discord", gui=True)

	if __name__ == '__main__':
		asyncio.run(main())

And that's it!

Module
======

To maintain the modular structure of the framework, we developed a module with all the platform specific functions inside. Including the integrated bot and the functions to contact the Discord API.

The file structure is shown below:

.. code-block:: bash

	Discord
	├── bot.py
	├── discord.py
	└── __init__.py

Class Functions
-----------------

.. py:function:: SendMessage(color=None, style:str="simple", title:str=None, description:str=None)
	:async:

	Message sending controller.

	.. confval:: color

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

.. py:function:: EditMessage(color=None, style:str="simple", title:str=None, description:str=None)
	:async:

	Message editing controller.

	.. confval:: color

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
	:async:

	Fetches automatically all the inboxes, based in a regular expression (RegEx), notifies the Game masters about differents parts of this process.

.. py:function:: InjectHandler(T3SF_instance)
	:async:

	This method handles the injection of a message in a specific channel using a Discord bot. 

	.. confval:: T3SF_instance

		An instance of the T3SF class.

		:type: ``obj``
		:required: ``True``

.. py:function:: PollHandler(T3SF_instance)
	:async:

	Handles the injects with polls. Creates the poll with the two options and sends it to the player's channel.

	.. confval:: T3SF_instance

		An instance of the T3SF class.

		:type: ``obj``
		:required: ``True``

.. py:function:: PollAnswerHandler(T3SF_instance, interaction=None)
	:async:

	Detects the answer in the poll sent. Modifies the poll message and notifies the game master about the selected option.

	.. confval:: T3SF_instance

		An instance of the T3SF class.

		:type: ``obj``
		:required: ``True``

	.. confval:: interaction

		The received interaction.

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

	.. py:method:: define_commands()

		Within this method, we will create the following command management functions

		.. py:function:: on_ready()
			:async:

			Detects when the bot is ready to receive commands and process messages.

		.. py:function:: on_interaction(interaction)
			:async:

			Detects when the bot receives an interaction (as a response to a poll).

		.. py:function:: ping_command(ctx)
			:async:

			Handles the ``!ping`` command and returns a `pong` message.

			.. confval:: ctx

				The context of the received message.

				:type: ``obj``
				:required: ``True``

		.. py:function:: start_command(ctx, *, query=None)
			:async:

			Handles the ``!start`` command and starts the exercise.

			.. confval:: ctx

				The context of the received message.

				:type: ``obj``
				:required: ``True``

			.. confval:: query

				The query of the message.

				:type: ``obj``
				:required: ``False``

.. py:function:: start_bot()
	:async:

	This functions will start the bot, but also generate tasks for the `async_handler_exercise <#async_handler_exercise>`_ `create_environment_task <#create_environment_task>`_ listeners.

	.. note:: Because the library we are using is asynchronous and the exercise can be started directly from the GUI, we need to add this *"listeners"* to start it without problems.

.. py:function:: async_handler_exercise()
	:async:

	This function waits for the ``start_incidents_gui`` global event to be triggered and starts the exercise. 

.. py:function:: run_async_incidents()
	:async:

	This function sets the ``start_incidents_gui`` global event to start the exercise. 

.. py:function:: create_environment_task()
	:async:

	This function waits for the ``create_env`` global event to be triggered and creates the environment. 

.. py:function:: create_environment(server)
	:async:

	This function sets the ``create_env`` global event to create the environment.

	.. confval:: server

		The server/guild identifier.

		:type: ``int``
		:required: ``True``

.. py:function:: create_role_if_not_exists(guild, name)
	:async:

	Create a role within the guild if it does not already exist.

	.. confval:: guild

		The guild identifier.

		:type: ``int``
		:required: ``True``

	.. confval:: name

		The role's name.

		:type: ``str``
		:required: ``True``

.. py:function:: create_category_if_not_exists(guild, name, private=False, role=None)
	:async:

	Create a category within the guild if it does not already exist.

	.. confval:: guild

		The guild identifier.

		:type: ``str``
		:required: ``True``

	.. confval:: name

		The category's name.

		:type: ``str``
		:required: ``True``

	.. confval:: private

		Determines if the category should be private and only available to a specific role

		:type: ``bool``
		:required: ``False``

	.. confval:: role

		The role's name.

		:type: ``str``
		:required: ``False`` | ``True`` if ``private`` is set to ``True``

.. py:function:: create_channel_if_not_exists(category, name)
	:async:

	Create a channel within the given category if it does not already exist.

	.. confval:: category

		The category in which the channel should be created.

		:type: ``str``
		:required: ``True``

	.. confval:: name

		The channel's name.

		:type: ``str``
		:required: ``True``

.. py:function:: create_voice_if_not_exists(category, name)
	:async:

	Create a voice channel within the given category if it does not already exist.

	.. confval:: category

		The category in which the channel should be created.

		:type: ``str``
		:required: ``True``

	.. confval:: name

		The channel's name.

		:type: ``str``
		:required: ``True``

.. py:function:: create_gm_channels(guild)
	:async:

	Creates the Game Masters section, text channels and voice channel.

	.. confval:: guild

		The guild identifier.

		:type: ``int``
		:required: ``True``


