class Character:
    def __init__(self, name, race, profession, stats):
        self.name = name
        self.race = race
        self.profession = profession
        self.stats = stats


def setStats(race, profession):

    stats = {
        "strength": 0,
        "intelligence": 0,
        "stamina": 0,
    }

    # Set stats based on race choice.
    if race == "Human":
        stats["strength"] += 10
        stats["intelligence"] += 10
        stats["stamina"] += 10
    elif race == "Elf":
        stats["strength"] += 10
        stats["intelligence"] += 5
        stats["stamina"] += 15
    elif race == "Orc":
        stats["strength"] += 20
        stats["intelligence"] += 0
        stats["stamina"] += 10

    # Set stats based on profession choice.
    if profession == "Warrior":
        stats["strength"] += 20
        stats["intelligence"] += 5
        stats["stamina"] += 10
    elif profession == "Wizard":
        stats["strength"] += 5
        stats["intelligence"] += 20
        stats["stamina"] += 5
    elif profession == "Ranger":
        stats["strength"] += 10
        stats["intelligence"] += 5
        stats["stamina"] += 15

    return stats


def create(name, race, profession):

    # Pass in the race and profession choices to generate "stats" value.
    stats = setStats(race, profession)
    player = Character(name, race, profession, stats)

    return player


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    create()
