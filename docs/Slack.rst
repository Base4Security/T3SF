*******************
Slack
*******************

.. contents:: Table of Contents

Slack is the new platform we are expanding to given the needs of our clients! The heart of the bot is still the same, we just made some improvements to it so it can walk around smoothly!

Functions
===============

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

	Fetches automatically all the inboxes, based in a regular expression (RegEx), notifies the Game masters about differents parts of this process.


.. py:function:: InjectHandler(self)
	
	Gives the format to the inject and sends it to the correct player's inbox.


Bot
===============

Installation
------------------
1. Git clone the repository [https://github.com/Base4Security/T3SF].
2. Go inside the Slack version folder with ``cd T3SF/Slack/``
3. Install requirements.
	``pip3 install -r requirements.txt``
	
	(Optional) Create a virtual enviroment
	``python3 -m venv venv``
4. Create a Workspace in slack (You can skip this step if you have already a workspace).
5. Navigate to https://api.slack.com/apps/ 
6. Select "Create New App".
7. Select the option "From an app manifest".
8. Select your workspace.
9. Selecting the format "YAML", paste the code inside ``bot_manifest.yml`` located in the following path ``T3SF/Slack/bot_manifest.yml``.
10. Create the App.
11. With the recently created app, and in the Basic Information menu, scroll to ``App-Level Tokens``, Generate a token and Scopes.
12. You can use any Token name, the important thing is that you add both scopes to the token: ``connections:write`` and ``authorizations:read``.
13. Generate it, and copy the token inside the ``.env`` file with the key ``SLACK_APP_TOKEN``
14. Now navigate to the "OAuth & permissions" sub-menu inside the Feautures sidebar menu.
15. Copy the ``Bot User OAuth Token`` inside the ``.env`` file with the key ``SLACK_BOT_TOKEN``
16. When you are done with the tokens, run the bot with ``python3 bot.py``
17. For the bot to be able to reply to your messages, you should add the App inside that channel. You can do it tagging the App's name or adding it mannually.
18. Yeah! You are ready to go now!