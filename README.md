# Fight Simulator

Flight simulator is a single-player game that simulates a battle between the chosen and the opposing team.

Teams are made of 5 random character each, which are retrieved from the [Superhero API](https://www.superheroapi.com/)

## Get Started

1. Fork and Clone this repo
1. Install the [necessary dependencies](#dependencies)
1. Create a file named ```constants.py``` inside the ```utils``` folder to add your API key for the [Superhero API](https://www.superheroapi.com/). The content of the file should look like this: ```API_KEY = "XXXXXXXXXXXXXXXX"```(replace the Xs with your key)
1. Open the terminal and start a game by running ```python3 main.py```

## How to play
After running the initial command (```python3 main.py```), you will be prompted with a welcome message and characters will begin to load.

After all the characters are loaded and the teams determined, choose a team and start playing by attacking the opposing team and following the prompts on the terminal.

After each attack, the status of all characters is displayed with one of three colors: 🟢 (healthy), 🟡 (wounded), 🔴 (defeated).

Play each round by following the prompts until all the character in one team are defeated and the game is over, after which you can choose to play again!

## Dependencies
Flight simulator uses these dependencies, make sure they are installed in your environment before running the game:
* ```math```
* ```random```
* ```threading```
* ```time```
* ```asyncio```
* ```aiohttp```
* ```pytest```

## Testing
Flight simulator uses ```pytest``` for unit testing. Run ```pytest``` from the terminal to run the test suite from ```test_all.py```