"""
The battle module handles the execution of battles between teams of characters in the superhero battle game.

It contains the Battle class, which manages the flow of the battle, including team creation, character selection, attack execution, and determining the winner.

Classes:
    Battle: Represents a battle between two teams of characters.

Example:
    To initiate a battle, create a Battle object and provide the base URL for the superhero API as an argument.
"""
import math
import random
import threading
import time
import asyncio
from aiohttp import ClientSession
from modules.character import Character
from modules.team import Team
from utils.messages import messages

class Battle:
    def __init__(self, base_url: str) -> None:
        """
        Initializes the Battle object, runs the battle based on the player's input, and prints the winner after the battle is finished.

        Args:
            base_url (str): The base URL for the superhero API.
        """
        print("\n▶️ New Battle:\nWe will start by creating two teams of 5 random characters each...\n")

        self.base_url = base_url
        self.teams = asyncio.run(self.get_teams())

        print("\n\n✅ Both teams have been created!\n")

        self.teams_formatted = {
            "Team 1": Team(self.teams["Team 1"]),
            "Team 2": Team(self.teams["Team 2"])
        }

        self.teams_formatted["Team 1"].set_team_alignment()
        self.teams_formatted["Team 2"].set_team_alignment()
        self.teams_formatted["Team 1"].update_characters()
        self.teams_formatted["Team 2"].update_characters()

        self.print_teams(.5)

        self.user_team = ""
        self.cpu_team = ""
        self.choose_team()

        time.sleep(2)

        fight_winner = self.fight()
        if fight_winner == "player":
            print(f"\n🎉 YOU WIN! 🎉\n{messages['player_wins'][random.randrange(5)]}")
        elif fight_winner == "cpu":
            print(f"\n🤯 YOU LOSE... 🤯\n{messages['cpu_wins'][random.randrange(5)]}")

    def choose_team(self) -> None:
        """
        Allows the player to choose their team for the battle.
        """
        # choose player's team
        team_selection = 0
        while team_selection not in (1, 2):
            try:
                team_selection = int(
                    input("\n👥 [CHOOSE YOUR TEAM]\nEnter (1) or (2): "))
                if team_selection not in (1, 2):
                    raise ValueError

                self.user_team = f"Team {str(team_selection)}"
                self.cpu_team = f"Team {str(3 - team_selection)}"
            except ValueError:
                print("\n❌ Invalid input. Please enter 1 or 2")

        random_message = messages["team_assembled"][random.randrange(20)]
        print(f"\nYou have selected {str(self.user_team)}\n{random_message}")

    async def fetch_data(self, session: ClientSession, revised_characters: dict[str, bool]) -> Character:
        """
        Asynchronously fetches data about a character from the superhero API.

        This method generates a random character ID and retrieves their powerstats and biography data.
        It ensures that the character ID has not been previously fetched to avoid duplicates.
        If the retrieved data is valid (not null powerstats and alignment is 'good', 'bad', or 'neutral'), it creates a Character object with the retrieved data and returns it.

        Args:
            session: The aiohttp ClientSession to use for making HTTP requests.
            revised_characters (dict[str, bool]): A dictionary to keep track of fetched character IDs to avoid duplicates.

        Returns:
            Character: A Character object initialized with the retrieved data.

        Raises:
            TimeoutError: If a timeout occurs while fetching data from the API.
        """
        while True:
            character_id = str(random.randint(1, 731))
            if character_id in revised_characters:
                continue
            revised_characters[character_id] = True
            async with session.get(f"{self.base_url}{character_id}/powerstats", timeout=30, ssl=False) as response:
                powerstats_data = await response.json()
            async with session.get(f"{self.base_url}{character_id}/biography", timeout=30, ssl=False) as response:
                biography_data = await response.json()
            alignment = biography_data['alignment']
            if 'null' in powerstats_data.values() or alignment not in ('good', 'bad', 'neutral'):
                continue
            return Character({**powerstats_data, "alignment": alignment})

    async def get_teams(self) -> dict[str, list[Character]]:
        """
        Retrieves 2 teams of 5 distinct characters from the superhero API asynchronously.

        Returns:
            dict[str, list[Character]]: A dictionary containing the two teams of characters.
        """
        revised_characters: dict[str, bool] = {}
        all_characters: list[Character] = []
        self.print_loading_msg(all_characters)
        async with ClientSession() as session:
            while len(all_characters) < 10:
                all_characters.append(await self.fetch_data(session, revised_characters))

        return {
            "Team 1": all_characters[:5],
            "Team 2": all_characters[5:]
        }

    def print_loading_msg(self, all_characters: list[Character]):
        """
        Prints a loading message while characters are being fetched from the superhero API.

        Args:
            all_characters (list[Character]): A list of Character objects representing fetched characters.
        """
        def animate():
            animation = [".","..","...","   "]
            idx = 0
            while len(all_characters) < 10:
                print(f"⏳ Loading characters{animation[idx % len(animation)]}", end="\r")
                idx += 1
                time.sleep(0.2)

        loading_thread = threading.Thread(target=animate)
        loading_thread.start()

    def print_teams(self, delay: float) -> None:
        """
        Prints the teams of characters with a specified delay between each print.

        Args:
            delay (float): The delay between each print.
        """
        for team_name, team_characters in self.teams.items():
            print(f"\n{team_name}, {self.teams_formatted[team_name]}")
            for character in team_characters:
                print(character)
                time.sleep(delay)

    def fight(self) -> str:
        """
        Initiates and manages the rounds of the battle between the two teams.

        Returns:
            str: The winner of the battle after the last round ('player' or 'cpu').
        """
        player_attacks = True
        self.round = 0  # incremented each time any player attacks
        while True:
            self.round += 1
            attack_result = self.attack(player_attacks)
            if attack_result["winner"]:
                return attack_result["winner"]

            player_attacks = not player_attacks

            if not player_attacks:
                # increments after both players have attacked once
                real_round = str(math.ceil(self.round / 2))
                input(
                    f"\n[ROUND {real_round}. PRESS ENTER TO PLAY YOUR OPPONENT'S TURN...]")

    def attack(self, player_attacks: bool) -> dict[str, str]:
        """
        Performs an attack between two characters from opposing teams.

        Args:
            player_attacks (bool): Indicates whether it's the player's turn to attack.

        Returns:
            dict[str, Union[bool, str]]: Information about the status of the battle after the attack.
        """
        alive_player = [
            char for char in self.teams[self.user_team] if char.hp > 0]
        alive_cpu = [char for char in self.teams[self.cpu_team] if char.hp > 0]

        # list of characters from the attacker's team that are still alive
        attacker_characters = alive_player if player_attacks else alive_cpu

        # set attacker from user input
        character_attacker = self.set_attacking_character(
            attacker_characters) if player_attacks else random.randint(1, len(alive_cpu))

        # perform attack (random attack type)
        attacker = attacker_characters[character_attacker - 1]
        attack_type = random.choice(
            [[0, "mental"], [1, "strong"], [2, "fast"]])
        victim = random.choice(alive_cpu if player_attacks else alive_player)
        damage = attacker.attack[int(attack_type[0])]

        attacking_team = self.user_team if player_attacks else self.cpu_team

        attacker_name = attacker.data['name']
        victim_name = victim.data['name']
        print(
            f"\n***🚀***{attacking_team.upper()} IS ATTACKING***🚀***\
            \n'{attacker_name}' is doing a '{attack_type[1]}' attack ({round(damage, 2)} HP) on '{victim_name}'..."
        )

        # assess damage inflicted to victim and update its status if necessary
        victim.assess_damage(damage)
        victim.set_status()

        # display updated teams
        time.sleep(2)
        self.print_teams(.1)

        alive_player = [
            char for char in self.teams[self.user_team] if char.hp > 0]
        alive_cpu = [char for char in self.teams[self.cpu_team] if char.hp > 0]

        if len(alive_player) == 0 or len(alive_cpu) == 0:
            return {"winner": "player" if len(alive_cpu) == 0 else "cpu"}

        return {"winner": ""}

    def set_attacking_character(self, user_characters: list[Character]) -> int:
        """
        Allows the player to choose which character from their team will perform an attack.

        Args:
            user_characters (list[Character]): The characters available for the player to choose from.

        Returns:
            int: The index of the selected character from 1 to 5 (both inclusive).
        """
        valid_choices = ""
        for i, character in enumerate(user_characters):
            if i < len(user_characters) - 1:
                valid_choices += f"({str(i + 1)}) {character.data['name']}, "
            else:
                valid_choices += f"({str(i + 1)}) {character.data['name']}: "

        attacking_character = 0
        while attacking_character not in range(1, len(user_characters) + 1):
            try:
                # increments after both players have attacked once
                real_round = str(math.ceil(self.round / 2))
                attacking_character = int(
                    input(f"\n🚀 [ROUND {real_round}. CHOOSE A CHARACTER]\n{valid_choices}")
                )
                if attacking_character not in range(1, len(user_characters) + 1):
                    raise ValueError
            except ValueError:
                print(
                    "\n❌ Invalid input. Please enter a valid number corresponding to a character")

        return attacking_character