"""
The character module defines the Character class, which represents a superhero character in the superhero battle game.

It contains methods to initialize a character with initial data, set their real stats, calculate their HP and attacks, assess damage inflicted during battles, and update their status based on their HP.

Classes:
    Character: Represents a superhero character in the superhero battle game.

Attributes:
    data (dict[str, str]): Data about the character.
    actual_stamina (int): The actual stamina of the character, initialized randomly.
    attack (list[float]): A list to store the damage for the 3 types of attack of the character.
    status (str): The status of the character ('🟢' for healthy, '🟡' for wounded, '🔴' for defeated).
    fb (float): The filiation coefficient of the character, used in calculating real stats and attacks.
    hp (int): The hit points (HP) of the character.

Methods:
    set_real_stats: Sets the real stats of the character based on its initial data and team affiliation.
    set_hp: Sets the initial HP (hit points) of the character based on their stats and team affiliation.
    set_attacks: Sets the damage for the 3 types of attack of the character.
    calculate_attack: Calculates the damage of an attack based on the character's stats and weights.
    assess_damage: Adjusts the character's HP based on the damage inflicted.
    set_status: Sets the status of the character based on their current HP.
    __str__: Returns a string representation of the character, including their status, name, alignment, HP, and attacks.
"""
import math
import random

class Character:
    def __init__(self, data: dict[str, str]) -> None:
        """
        Initializes the Character object.

        Args:
            data (dict[str, str]): Data about the character.
        """
        # data of the character
        self.data = data
        self.actual_stamina = random.randrange(11)
        self.attack: list[float] = []
        self.status = "🟢"
        self.fb: float = 0
        self.hp = 0

    def set_real_stats(self) -> None:
        """
        Sets the real stats of the character based on its initial data and the affiliation of the team it belongs to for a battle.
        """
        for key, stat in self.data.items():
            if key in ("combat", "durability", "intelligence", "power", "speed", "strength"):
                self.data[key] = str(math.floor(
                    (2 * int(stat) + self.actual_stamina) / 1.1 * self.fb
                ))

    def set_hp(self) -> None:
        """
        Sets the initial HP (hit points) of the character based on their stats and team affiliation.
        """
        strength_weight = .8
        durability_weight = .7
        self.hp = math.floor(
            (int(self.data["strength"]) * strength_weight + int(self.data["durability"]) * durability_weight + int(self.data["power"])) / 2 *
            (1 + self.actual_stamina / 10)
        ) + 100

    def set_attacks(self) -> None:
        """
        Sets the damage for the 3 types of attack of the character.
        """
        if len(self.attack) == 0:
            self.attack.append(self.calculate_attack(
                ["intelligence", "speed", "combat"], [.7, .2, .1]))
            self.attack.append(self.calculate_attack(
                ["strength", "power", "combat"], [.6, .2, .2]))
            self.attack.append(self.calculate_attack(
                ["speed", "durability", "strength"], [.55, .25, .2]))

    def calculate_attack(self, stats: list[str], w: list[float]) -> float:
        """
        Calculates the damage of an attack based on the character's stats and weights.

        Args:
            stats (list[str]): The stats used to calculate the attack.
            w (list[float]): The weights for each stat in the calculation.

        Returns:
            float: The damage of the attack.
        """
        return (
            float(self.data[stats[0]]) * w[0]
            + float(self.data[stats[1]]) * w[1]
            + float(self.data[stats[2]]) * w[2]
        ) * self.fb

    def assess_damage(self, damage: float) -> None:
        """
        Adjusts the character's HP based on the damage inflicted.

        Args:
            damage (float): The amount of damage inflicted.
        """
        self.hp = max(self.hp - damage, 0)

    def set_status(self) -> None:
        """
        Sets the status of the character based on their current HP.
        """
        self.status = "🟡" if self.hp > 0 else "🔴"

    def __str__(self) -> str:
        return f"\n  {self.status} {self.data['name']} ({self.data['alignment']}), HP: {str(self.hp)}\n     Attacks (damage): Mental ({str(round(self.attack[0]))}), Strong ({str(round(self.attack[1]))}), Fast ({str(round(self.attack[2]))})"
