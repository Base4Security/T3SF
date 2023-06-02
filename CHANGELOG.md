# Change Log
All notable changes to this project will be documented in this file.

## [2.1] - 2023-06-02
Upgrade to version 2.1 of the T3SF framework to benefit from an array of new features, bug fixes, and enhanced stability. This release brings important updates and automation to streamline various processes within the framework.

### Fixes:
  - Slack:
    -Addressed a bug related to the usage of regular expressions by users.
  - Discord:
    - Resolved an issue with the automatic environment creation where the Game Master (GM) chat was incorrectly labeled as "chat" instead of "gm-chat".
  - GUI:
    - The Start button now correctly re-enables after restarting the framework.
    - The default logging level has been set to "INFO" to resolve a recursion error that occurred when no logging level was selected.

### New Additions:
  - Docker Images:
    - Docker images with specific tags are now available for each currently supported platform, facilitating deployment and management.
  - Slack:
    - Introduced a new sanitization function to ensure proper formatting of channel names.
  - Discord:
    - Implemented a fail-safe validation for server ID inputs.
    - Added a new alert to notify users when attempting to start the bot without the Game Master (GM) role from the Discord platform.

## [2.0] - 2023-05-05

Upgrade to version 2.0 for new features, bug fixes, and improved stability. In this version we have automated some important processes. 

### Added
- New navigation bar added to the GUI.
- Now you can see the status of the framework from the logs viewer.
- New MSEL Viewer! You can now load a MSEL in JSON format to check every inject's detail.
- Automatic Environment creation, starting from this version you can automatically create the exercise's environment.

### Updated
- Updated documentation to match all the functions, features, classes and odules of version 2.0.

### Fixed
- The communication between the SSE client and server was poorly performed, which generated an infinite loop every 3 seconds.

## [1.2] - 2023-04-05

Official release of v1.2 - New features, bug fixes, and stability improvements included!

### Newly added
- Now for **Slack** and **Discord**, you no longer need to create a bot, now the framework handles completely that part with integrated bots.
- Guided User Interface (GUI) for management purposes. Now you can control, see the logs and exercise status in real time in a newly designed Web interface.
- New framework's modular structure.
- New simplified user's input, now you can run a TTX with just a few lines of code, less than 10!
- New class to log all the output from the bots and framework, such as status, errors, warnings and more.

### Updated
- Updated the code to work with all updates to the specified platform libraries.
- Requirements are now fullfilled when installing the framework with the specified module, as `pip3 install "T3SF[Platform]"`.

### Deprecated
- This versions is not ready for platforms as **Telegram** and **WhatsApp**, we are constantly working to update the framework for all the platforms. If you want to use the framework with those platform, use the previous `Version 1.1`.

## [1.1] - 2022-10-28

Version 1.1 has been officially released, with new features, bug fixes and stability issues resolved!

### Added
- An option has been added for players to respond to polls for analytical purposes. Available for **Slack**, **Discord** and **Telegram**!

### Fixed
- A problem with the Discord bot has been fixed.
- We have changed the way to check options such as "Photos" and "Profile picture" in the injects.

### Updated
- We have updated all the bots dependencies and made some changes to make them work with the new versions.


## [1.0] - 2022-04-20 

Releasing the official public version of the framework!

### Added
- Added the proper project's documentation.
- Added a better and nicer README.
- Added contributing guidelines.
- Added platform-dependat files, such as `.env` `requirements.txt` and `bot.py`.
- Added support for more platforms: **WhatsApp** and **Telegram**!
- Added a To-Do list with ideas for next versions.
- Added the templates for issues and feature request.
- Added a few examples of the injects per platform as illustrative manner.
- New config file added as a way to configurate the framework.
- Framework added to PyPi for easier download.

### Changed
- Now the framework has a module for each platform's functions.
- There are new platform-wide handlers.


## [0.5] - 2022-04-03 [Private]

Now the framework supports Slack!

### Added
- Adding the Slack version of the bot.
  - Main features migrated.
  - Few functions exclusives to Slack created, such as format and inboxes fetcher.
- Adding a better way to separate Platforms with Folders.
- Adding a README with a How to for installation an a brief description of the bot and platforms.


## [0.4] - 2022-02-02 [Private]

Launching the latest _and better_ version of the framework supporting Discord! 

### Added
- Auto regex finder to match the categories' names
- Auto match with player's name from the MSEL.json and actual inbox's name
- Inbox now stored in a text file after getting the correct ones!
- New format for the injects! Now they have a profile picture for the sender

### Changed
-Now the start and resume function are merged into 1 process function!

### Fixed
- Fixed a bug within the resume function, injects not being chosen correctly!


## [0.3] - 2022-01-29 [Private]

Releasing a new feature for our unique platform, Discord, to add a new and better way to present injects

### Added
- Accepting new key from the JSON ("Photo") so we can attach a picture to the injects.
- Added exceptions handling for better debug.

### Remarkable tests
- Tested on education environment, with real case scenarios.


## [0.2] - 2021-12-13 [Private]

Releasing the second version, after many tests where new ideas emerged.

### Added
- New "Resume" function, to restart the bot in a certain Incident Id.
- New messages to inform the steps of the bots, such as remaining incidents, waiting time.
- New function to obtain automatically the channel's IDs [Discord].
 
### Changed
- Commented code.
- Code cleanup.

### Remarkable tests
- Tested on education environment, with real case scenarios.

 
## [0.1] - 2021-09-19 [Private]

Releasing the very first early version of the framework for internal testing.

### Added
- Basics functions suchs as framework's "start" and incidents handling.
- Adding Discord support. [Only platform].

### Special Thanks
Based on the We Learn Cybersecurity team idea (Matías Sliafertas, Gastón Ureta and Federico Pacheco)
