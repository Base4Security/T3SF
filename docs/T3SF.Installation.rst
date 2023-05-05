************************
Installation
************************

To use the framework with the platform you want, either Slack or Discord, you will have to install the necessary modules and external libraries for that platform. But don't worry, installing these requirements is easy and simple.

Getting things ready
=======================

The installation of the framework itself it's really easy!

You just have to use ``pip`` and voila!

	
	.. note::
		You can create a virtual environment to avoid dependencies issues:
	
		``python3 -m venv venv``

``pip install T3SF``


Platform-based installation
=======================

Even though we have installed the core framework, we still need to install the additional libraries for each of the platforms.

Discord
---------

In case you want to use Discord, the installation of the necessary libraries is done as follows

``pip install "T3SF[Discord]"``

*For more information on how to create the Bot and obtain the tokens, please go to the* `specific page <./Discord.html#bot>`_ *of the platform.*


Slack
---------

On the other hand, if you want to use Slack, you can install them as follows

``pip install "T3SF[Slack]"``

*For more information on how to create the Bot and obtain the tokens, please go to the* `specific page <./Slack.html#bot>`_ *of the platform.*