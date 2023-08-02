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


Using Docker
=======================

To simplify the setup process and avoid any configuration headaches, we provide Docker images that come pre-packaged with all the necessary components to run your TTX exercise seamlessly.

Slack
---------

For Slack users, our Docker image has everything you need to perform your exercise effortlessly. Just run the following command:

``$ docker run --rm -t --env-file .env -v $(pwd)/MSEL.json:/app/MSEL.json base4sec/t3sf:slack``


Make sure to update your `.env` file with the required ``SLACK_BOT_TOKEN`` and ``SLACK_APP_TOKEN`` tokens. You can find more information on providing the tokens `here <./Slack.html#providing-the-tokens>`_.

Also, remember to set the `MSEL_PATH` environment variable to specify the location of your MSEL file. By default, the container path is `/app/MSEL.json`. Adjust the variable accordingly if you change the volume mount location.


Discord
---------

If you prefer Discord, our Docker image has got you covered. Simply execute the following command:


``$ docker run --rm -t --env-file .env -v $(pwd)/MSEL.json:/app/MSEL.json base4sec/t3sf:discord``

Update your .env file with the required ``DISCORD_TOKEN``. You can find detailed instructions on providing the token `here <./Discord.html#providing-the-token>`_.

Similarly, set the `MSEL_PATH` environment variable to specify the location of your MSEL file. The default container path is `/app/MSEL.json`. Adjust the variable accordingly if you change the volume mount location.