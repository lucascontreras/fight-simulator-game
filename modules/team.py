"""
The team module defines the Team class, which represents a team of characters in the superhero battle game.

It contains methods to initialize and update the attributes of a team, including determining the team's alignment based on the alignments of its characters and updating the characters' attributes accordingly.

Classes:
    Team: Represents a team of characters in the superhero battle game.

Example:
    To create a team, instantiate a Team object and provide a list of Character objects as an argument.

Attributes:
    characters (list[Character]): The characters in the team.
    team_alignment (str): The alignment of the team ('good' or 'bad').

Methods:
    set_team_alignment: Determines the alignment of the team based on the alignments of its characters.
    update_characters: Updates the attributes of the characters in the team after determining the team's alignment.
"""
import math
import random
from modules.character import Character

class Team:
    def __init__(self, characters: list[Character]) -> None:
        """
        Initializes the Team object.

        Args:
            characters (list[Character]): The characters in the team.
        """
        self.characters = characters
        self.team_alignment = ""
        # self.update_characters()

    # team is good if 3 or more characters are good
    def set_team_alignment(self) -> None:
        """
        Determines the alignment of the team based on the alignments of its characters.

        Returns:
            str: The alignment of the team ('good' or 'bad').
        """
        good_count, bad_count = 0, 0
        for character in self.characters:
            # assumption: "neutral" characters are in alignment with "bad" ones => there are no neutral teams
            if character.data["alignment"] == "good":
                good_count += 1
            else:
                bad_count += 1

            if good_count == 3:
                self.team_alignment = 'good'
                return None
        self.team_alignment = 'bad'

    # set filiation coefficient, real stats, hp and attacks after team is defined and team_alignment determined
    def update_characters(self) -> None:
        """
        Updates the attributes of the characters in the team after determining the team's alignment.
        """
        for character in self.characters:
            character.fb = 1 + random.randrange(10) if self.team_alignment == character.data["alignment"] else math.pow(1 + random.randrange(10), -1)

            # set real stats, then set hp and finally set attacks
            character.set_real_stats()
            character.set_hp()
            character.set_attacks()

    def __str__(self) -> str:
        return f"alignment: {self.team_alignment}"
