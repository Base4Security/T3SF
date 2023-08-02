*******************
Usage
*******************

.. contents:: Table of Contents

Basically we have created the framework to be quick and easy to set up, so if you want to run the bot in Discord or Slack you just need to start T3SF!


Initializing T3SF
=========================

To start the framework, you have to set 3 parameters. Depending on the platform and your preferences the following arguments will be set:

.. confval:: MSEL

	The location of the MSEL. It accepts the complete file path.

	:type: ``str``
	:required: ``True``

.. confval:: platform

	The platform you want to use.

	:type: ``str``
	:required: ``True``
	:values: ``Slack`` or ``Discord``

.. confval:: gui

	Starts the GUI of the framework.

	:type: ``bool``
	:required: ``False``
	:default: ``True``


This example is for an exercise using the platform Slack with a GUI:

.. code-block:: python3
	
	from T3SF import T3SF
	import asyncio

	async def main():
		await T3SF.start(MSEL="MSEL_Company.json", platform="Slack", gui=True)

	if __name__ == '__main__':
		asyncio.run(main())

And that's it!


MSEL Configuration
===================

The file where you have all injects stored is the Master Scenario Events List (MSEL). From this file, the framework is going to retrieve all the messages and players, so it's like the Heart of the exercise!

Format
---------

Inside the repo you have an example of a common MSEL, but we will be explaining in a short and easy way the format of it.

Here is the first inject from the example in the repo.

.. code-block:: json

 	{
	    "#": 1,
	    "Real Time": "07:30 PM",
	    "Date": "Monday  9:40 AM",
	    "Subject": "[URGENT] Ransom Request!",
	    "From": "SOC - BASE4",
	    "Player": "Legal",
	    "Script": "Team, we received a ransom request. What should we do?",
	    "Picture Name": "Base_4_SOC.jpg",
	    "Photo": "https://img2.helpnetsecurity.com/posts2018/aws-s3-buckets-public.jpg",
	    "Profile": "https://foreseeti.com/wp-content/uploads/2021/09/Ska%CC%88rmavbild-2021-09-02-kl.-15.44.24.png",
	    "Poll": "We are checking on it | It is a false positive"
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

	The profile picture of the sender. If no profile picture is set for an incident, a default user avatar will be used.

	.. note:: 
		This key is only valid in :doc:`./Discord` and :doc:`./Slack`, due to platform restrictions.

	:type: ``str`` -> Web URL
	:required: ``False`` -> ``True`` if the platform is :doc:`./Discord` or :doc:`./Slack`.


.. confval:: Poll

	Set up a survey to be sent to the players, where they have time to answer depending on the options.

	.. note:: 
		This key is only valid in :doc:`./Discord` and :doc:`./Slack`, due to platform restrictions.

	:type: ``str``
	:required: ``False``

	.. note:: 
		The options should be separated with a pipe (|) symbol.
