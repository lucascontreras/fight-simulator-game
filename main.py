"""
The main module orchestrates the execution of the superhero battle game.

It defines two main functions: play and main.

Functions:
    play: Initialize and start a battle between two teams of superheroes.
    main: The main function to run the game loop, allowing the player to play the game multiple times until they choose to end it.

Example:
    To start the game, run this module directly by executing `python main.py`.

    This will initialize the game loop, where the player can play multiple rounds of the game. After each round, the player is prompted to choose whether they want to play again. They can end the game by pressing Enter when prompted.

    If the player chooses to play again, a new battle will be initiated. Otherwise, the game loop will end.
"""

from modules.battle import Battle
from utils.constants import API_KEY

def play():
    """
    Initialize and start a battle.
    """
    base_url = f"https://superheroapi.com/api/{API_KEY}/"
    Battle(base_url)

def main():
    """
    Main function to run the game in a loop until user ends it.
    """
    play_again = True
    while play_again:
        play()
        play_again_input = input(
            "\n[PLAY AGAIN?]\nEnter 'y' if you want to play again. Press 'Enter' to end the game: ").lower()
        if play_again_input != 'y':
            play_again = False

if __name__ == "__main__":
    main()
