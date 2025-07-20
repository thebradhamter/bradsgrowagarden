from random import randint, choices
from copy import deepcopy
from math import ceil
from colorify import C

money = 1
credits = 0
active_rune = None
garden = []
unlocked_runes = []
is_developer = False

class Mutation:
    mutations = []
    def __init__(self, name: str, icon: str, multiplier: float, chance: float) -> any:
        self.name = name
        self.icon = icon
        self.multiplier = multiplier
        self.chance = chance
        Mutation.mutations.append(self)

class Rune:
    runes = []
    rarity_colors = {"common": None, "rare": C.blue, "epic": C.purple, "legendary": C.yellow, "cosmic": C.violet}
    rarities = {"common": 60, "rare": 25, "epic": 10, "legendary": 4, "cosmic": 1}
    def __init__(self, name: str, icon: str, color: tuple[int, int, int], buy: int, type: str, hook: str, rarity_values: dict) -> any:
        self.name = name
        self.icon = icon
        self.color = color
        self.buy = buy
        self.type = type
        self.hook = hook
        self.rarity_values = rarity_values
        Rune.runes.append(self)
    def generate_rarity(self) -> str:
        items = list(Rune.rarities.keys())
        weights = list(Rune.rarities.values())
        return choices(items, weights=weights, k=1)[0]

class Plant:
    plants = []
    def __init__(self, name: str, icon: str, buy: int, sell_min: int, sell_max: int, color: tuple[int, int, int], limited: bool = False) -> any:
        self.name = name
        self.icon = icon
        self.buy = buy
        self.sell_min = sell_min
        self.sell_max = sell_max
        self.color = color
        self.mutations = []
        self.limited = limited
        Plant.plants.append(self)
    def add_mutation(self, mutation: Mutation) -> any:
        new = deepcopy(self);
        new.mutations.append(mutation)
        return new
    def get_sell_value(self, active_rune: list[Rune, str] = None) -> int:
        base_value = randint(self.sell_min, self.sell_max)
        value = base_value
        for mutation in self.mutations:
            value += base_value * mutation.multiplier
        if active_rune:
            if active_rune[0].hook == "plantsell":
                if active_rune[0].type == "additer":
                    value += active_rune[0].rarity_values[active_rune[1]]
                elif active_rune[0].type == "multiplier":
                    value *= active_rune[0].rarity_values[active_rune[1]]
        return ceil(value)