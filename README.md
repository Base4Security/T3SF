<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://user-images.githubusercontent.com/103124157/164258966-7a049d6c-4012-49ca-8f7d-2bb814c24009.png" alt="WhaBot Logo"></a>
</p>

<h3 align="center">T3SF</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]() 
  [![PyPI version](https://badge.fury.io/py/T3SF.svg)](https://badge.fury.io/py/T3SF)
  [![Documentation Status](https://readthedocs.org/projects/t3sf/badge/?version=latest)](https://t3sf.readthedocs.io/en/latest/?badge=latest)
  [![License](https://img.shields.io/badge/license-GPL-blue.svg)](/LICENSE)
  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6519221.svg)](https://doi.org/10.5281/zenodo.6519221)

</div>

<p align="center"> Technical Tabletop Exercises Simulation Framework
    <br> 
</p>

## Table of Contents
- [About](#About)
- [Getting Things Ready](#Starting)
- [TODO](./TODO.md)
- [CHANGELOG](./CHANGELOG.md)
- [Contributing](./CONTRIBUTING.md)

## About <a name = "About"></a>
T3SF is a framework that offers a modular structure for the orchestration of events based on a master scenario events list (MSEL) together with a set of rules defined for each exercise (optional) and a configuration that allows defining the parameters of the corresponding platform. The main module performs the communication with the specific module (Discord, Slack, Telegram, etc.) that allows the events to present the events in the input channels as injects for each platform. In addition, the framework supports different use cases: "single organization, multiple areas", "multiple organization, single area" and "multiple organization, multiple areas".

## Getting Things Ready <a name = "Starting"></a>
To use the framework with your desired platform, whether it's Slack or Discord, you will need to install the required modules for that platform. But don't worry, installing these modules is easy and straightforward.

To do this, you can follow this simple step-by-step guide, or if you're already comfortable installing packages with `pip`, you can skip to the last step!

```bash
# Python 3.6+ required
python -m venv .venv       # We will create a python virtual environment
source .venv/bin/activate  # Let's get inside it

pip install -U pip         # Upgrade pip
```

Once you have created a Python virtual environment and activated it, you can install the T3SF framework for your desired platform by running the following command:

```bash
pip install "T3SF[Discord]"  # Install the framework to work with Discord
```
or

```bash
pip install "T3SF[Slack]"  # Install the framework to work with Slack
```

This will install the T3SF framework along with the required dependencies for your chosen platform. Once the installation is complete, you can start using the framework with your platform of choice.

We strongly recommend following the platform-specific guidance within our Read The Docs! Here are the links:

  - [Discord](https://t3sf.readthedocs.io/en/latest/Discord.html#installation)
  - [Slack](https://t3sf.readthedocs.io/en/latest/Slack.html#installation)
  - [Telegram](https://t3sf.readthedocs.io/en/latest/Telegram.html#installation)
  - [WhatsApp](https://t3sf.readthedocs.io/en/latest/WhatsApp.html#installation)

## Usage <a name="Usage"></a>
We created this framework to simplify all your work!

Once you have everything ready, use our template for the `main.py`, or modify the following code:

Here is an example if you want to run the framework with the `Discord` bot and a `GUI`.

```python
from T3SF import T3SF
import asyncio

async def main():
    await T3SF.start(MSEL="MSEL_TTX.json", platform="Discord", gui=True)

if __name__ == '__main__':
    asyncio.run(main())
```

Or if you prefer to run the framework without `GUI` and with `Slack` instead, you can modify the arguments, and that's it! 

Yes, that simple!

```python
await T3SF.start(MSEL="MSEL_TTX.json", platform="Slack", gui=False)
```

If you need more help, you can always check our documentation [here](https://t3sf.readthedocs.io/en/latest/)!