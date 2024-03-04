import pytest
from modules.character import Character
from modules.team import Team

@pytest.fixture(name="team")
def sample_team() -> Team:
    # Set up 5 sample characters data for testing
    characters_data = [
        {
            "name": "Test Character 1",
            "alignment": "good",
            "combat": "17",
            "durability": "80",
            "intelligence": "37",
            "power": "66",
            "speed": "32",
            "strength": "33"
        },
        {
            "name": "Test Character 2",
            "alignment": "bad",
            "combat": "84",
            "durability": "64",
            "intelligence": "90",
            "power": "32",
            "speed": "34",
            "strength": "5"
        },
        {
            "name": "Test Character 3",
            "alignment": "good",
            "combat": "55",
            "durability": "7",
            "intelligence": "90",
            "power": "40",
            "speed": "92",
            "strength": "23"
        },
        {
            "name": "Test Character 4",
            "alignment": "bad",
            "combat": "54",
            "durability": "93",
            "intelligence": "47",
            "power": "58",
            "speed": "17",
            "strength": "79"
        },
        {
            "name": "Test Character 5",
            "alignment": "good",
            "combat": "36",
            "durability": "88",
            "intelligence": "43",
            "power": "83",
            "speed": "58",
            "strength": "24"
        }
    ]
    return Team([Character(characters_data[0]), Character(characters_data[1]), Character(characters_data[2]), Character(characters_data[3]), Character(characters_data[4])])

@pytest.fixture(name="character")
def sample_character() -> Character:
    character_data ={
        "name": "Test Character 1",
        "alignment": "good",
        "combat": "17",
        "durability": "80",
        "intelligence": "37",
        "power": "66",
        "speed": "32",
        "strength": "33"
    }
    
    character = Character(character_data)
    character.fb = 5
    character.actual_stamina = 5

    return character

@pytest.fixture(name="character_real")
def sample_character_real_stats(character: Character) -> Character:
    character.data['combat'] = '177'
    character.data['durability'] = '750'
    character.data['intelligence'] = '359'
    character.data['power'] = '622'
    character.data['speed'] = '313'
    character.data['strength'] = '322'

    return character

class TestCharacter:

    def test_set_real_stats(self, character: Character) -> None:
        # Test if the real stats are set correctly

        character.set_real_stats()
        assert character.data['combat'] == '177'
        assert character.data['durability'] == '750'
        assert character.data['intelligence'] == '359'
        assert character.data['power'] == '622'
        assert character.data['speed'] == '313'
        assert character.data['strength'] == '322'

    def test_set_hp(self, character_real: Character) -> None:
        # Test if the HP is set correctly
        character_real.set_hp()
        assert character_real.hp == 1153

    def test_set_attacks(self, character: Character) -> None:
        # Test if the attacks are set correctly
        character.set_attacks()
        assert len(character.attack) == 3

    def test_calculate_attack(self, character_real: Character) -> None:
        # Test the calculation of attack damage
        damage = character_real.calculate_attack(["intelligence", "speed", "combat"], [.7, .2, .1])
        assert round(damage, 1) == 1658

    def test_assess_damage(self, character: Character) -> None:
        # Test if damage assessment modifies HP correctly
        character.hp = 100
        character.assess_damage(55)  # Example damage value
        assert character.hp == 45

    def test_set_status(self, character: Character) -> None:
        # Test if the status is set correctly
        character.hp = 100
        character.assess_damage(200)  # Inflict damage to set status to defeated
        character.set_status()
        assert character.status == "🔴"

class TestTeam:
    
    def test_set_team_alignment(self, team: Team) -> None:
        alignment = team.set_team_alignment()
        assert alignment == "good"

    def test_update_characters(self, team: Team) -> None:

        team.update_characters()

        for character in team.characters:
            assert character.fb > 0
            assert character.hp > 0