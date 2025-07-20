from classes import *
from colorify import C, colorify
from random import random
from os import system, path
from pickle import load, dump
from tkinter.filedialog import askopenfilename, asksaveasfilename
from math import floor

def save_data() -> None:
    global money, garden, is_developer
    save = asksaveasfilename(title="Save game", filetypes=[("Brad's Grow A Garden", "*.bgag")])
    if save:
        if not save.endswith(".bgag"):
            save += ".bgag"
        with open(save, "wb") as f:
            dump({"money": money, "garden": garden, "is_developer": is_developer}, f)

def load_data() -> None:
    global money, garden, is_developer
    save = askopenfilename(title="Save game", filetypes=[("Brad's Grow A Garden", "*.bgag")])
    if save:
        if path.exists(save):
            with open(save, "rb") as f:
                data = load(f)
                money = data.get("money", money)
                garden = data.get("garden", garden)
                is_developer = data.get("is_developer", is_developer)

def sell_all_plants() -> int:
    global money, garden
    total_value = 0
    for plant in garden:
        total_value += plant[1]
    money += total_value
    garden = []

def show_plants(numbered: bool = False) -> None:
    global garden
    x = 1
    if garden:
        for plant in garden:
            plant_sell = plant[1]
            plant = plant[0]
            plant_string = f"{plant.icon} {colorify(plant.name, plant.color)} ({colorify('$' + str(plant_sell), C.green)})"
            mutation_string = ""
            for mutation in plant.mutations:
                mutation_string += mutation.icon + ","
            mutation_string = mutation_string[:-1]
            if mutation_string:
                plant_string += f" ({mutation_string})"
            if numbered:
                plant_string = f"[{x}] " + plant_string
            print(plant_string)
            x += 1
    else:
        print("No plants in garden")

def get_garden_value() -> int:
    global garden
    value = 0
    for plant in garden:
        value += plant[1]
    return value

def add_credits() -> None:
    global credits
    credits += 1

def show_seed_shop(plants: list[Plant] = Plant.plants) -> None:
    clear()
    print("SEED SHOP")
    print("")
    print(f"You have {colorify('$' + str(money), C.green)}")
    choices = ["Close seed shop"]
    choices_listed = {}
    x = 1
    for plant in plants:
        if not plant.limited:
            x += 1
            choices.append(f"{plant.icon} {colorify(plant.name, plant.color)} ({colorify('$' + str(plant.buy), C.green)})")
            choices_listed[x] = plant
    choice = get_choice(choices, False)
    if choice:
        if choice == "1":
            pass
        else:
            if int(choice) in choices_listed:
                plant = choices_listed[int(choice)]
                if is_developer:
                    amount = int(input(f"How many {colorify(plant.name, plant.color)} ({colorify('$' + str(plant.buy), C.green)}) do you want to buy: ")) or 1
                    for _ in range(0, amount):
                        add_to_garden(plant)
                else:
                    if money >= plant.buy:
                        add_to_garden(plant)

def show_rune_shop(runes: list[Rune] = Rune.runes) -> None:
    clear()
    print("RUNE SHOP")
    print("")
    choices = ["Close rune shop"]
    print(f"You have {colorify('¢' + str(credits), C.orange)}")
    choices_listed = {}
    x = 1
    for rune in runes:
        x += 1
        choices_listed[x] = rune
        choices.append(f"{rune.icon} {colorify(rune.name + ' Rune Crate', rune.color)} ({colorify('¢' + str(rune.buy), C.orange)})")
    choice = get_choice(choices, False)
    if choice:
        if choice == "1":
            pass
        else:
            if int(choice) in choices_listed:
                rune = choices_listed[int(choice)]
                if is_developer:
                    amount = int(input(f"How many {colorify(rune.name + ' Rune Crate', rune.color)} ({colorify('¢' + str(rune.buy), C.orange)}) do you want to buy: ")) or 1
                    for _ in range(0, amount):
                        pass
                else:
                    if money >= rune.buy:
                        pass

def show_bank() -> None:
    global money, credits
    clear()
    print("BANK")
    choices = ["Close bank", f"Convert {colorify('$', C.green)} → {colorify('¢', C.orange)}"]
    choice = get_choice(choices)
    if choice == "1":
        pass
    elif choice == "2":
        print("")
        print(f"You have {colorify('$' + str(money), C.green)} and {colorify('¢' + str(credits), C.orange)}")
        print("")
        print(f"{colorify('$100000', C.green)} = {colorify('¢1', C.orange)}")
        value = int(input(f"How much {colorify('$', C.green)} would you like to convert: "))
        if money >= value:
            credits += floor(value/100000)
            money -= floor(value/100000)*100000
 
def show_spell_book() -> None:
    global active_rune, unlocked_runes
    clear()
    print("SPELL BOOK")
    if active_rune:
        print(f"Active rune: {active_rune[0].icon} {colorify(active_rune[1].capitalize(), Rune.rarity_colors[active_rune[1]])} {colorify(active_rune[0].name + ' Rune', active_rune[0].color)}")
    else:
        print(f"Active rune: None")
    choices = ["Close spell book", "Unequip rune"]
    choices_listed = {}
    x = 2
    for rune in unlocked_runes:
        x += 1
        choices_listed[x] = rune
        choices.append(f"{rune[0].icon} {colorify(rune[1].capitalize(), Rune.rarity_colors[rune[1]])} {colorify(rune[0].name + ' Rune', rune[0].color)}")
    choice = get_choice(choices)
    if choice == "1":
        pass
    elif choice == "2":
        active_rune = None
    else:
        if int(choice) in choices_listed:
            active_rune = choices_listed[int(choice)]

def main_loop() -> None:
    global money, credits, garden, is_developer
    clear()
    print(f"You have {colorify('$' + str(money), C.green)} and {colorify('¢' + str(credits), C.orange)}")
    print(f"Your garden is worth {colorify('$' + str(get_garden_value()), C.green)}")
    show_plants()
    choices = [
        "Open seed shop", 
        "Open rune shop", 
        "Open bank",
        "Open spell book",
        "Harvest all plants", 
        "Save game", 
        "Load game", 
        "Close game"
    ]
    if is_developer:
        choices.append(colorify("Developer console", C.light_blue))
    choice = get_choice(choices)
    if choice == "1":
        show_seed_shop()
    elif choice == "2":
        show_rune_shop()
    elif choice == "3":
        show_bank()
    elif choice == "4":
        show_spell_book()
    elif choice == "5":
        sell_all_plants()
    elif choice == "6":
        save_data()
    elif choice == "7":
        load_data()
    elif choice == "8":
        print("Are you sure?")
        choice = get_choice(["Yes", "No"])
        if choice == "1":
            return True
    elif choice == "9":
        choices = ["Set money", "Give money", "Set credits", "Give credits", "Mutate a plant", "Duplicate plant", "Give a rune"]
        choice = get_choice(choices)
        print("")
        try:
            if choice == "1":
                money = int(input("New money: "))
            elif choice == "2":
                money += int(input("Money to add: "))
            elif choice == "3":
                credits = int(input("New credits: "))
            elif choice == "4":
                credits += int(input("Credits to add: "))
            elif choice == "5":
                show_plants(True)
                plant_number = int(input("What plant do you want to mutate: "))
                plant = garden[plant_number-1]
                print("")
                x = 0
                for mutation in Mutation.mutations:
                    x += 1
                    print(f"[{x}] {mutation.icon} {mutation.name} ({colorify('x' + str(mutation.multiplier), C.green)}) ({colorify(str(mutation.chance) + '%', C.red)})")
                mutation_number = int(input(f"What mutation do you want to give {plant[0].icon} {colorify(plant[0].name, plant[0].color)} ({colorify('$' + str(plant[1]), C.green)}): "))
                mutation = Mutation.mutations[mutation_number-1]
                mutated_plant = deepcopy(plant[0]).add_mutation(mutation)
                garden[plant_number-1] = [mutated_plant, mutated_plant.get_sell_value()]
            elif choice == "6":
                show_plants(True)
                plant_number = int(input("What plant do you want to duplicate: "))
                plant = garden[plant_number-1]
                garden.append(plant)
            elif choice == "7":
                x = 0
                for rune in Rune.runes:
                    x += 1
                    print(f"[{x}] {rune.icon} {colorify(rune.name + ' Rune', rune.color)}")
                rune_number = int(input("What rune do you want to get: "))
                rune = Rune.runes[rune_number-1]
                print("")
                x = 0
                rarities = {}
                for rarity, rarity_color in Rune.rarity_colors.items():
                    x += 1
                    rarities[x] = rarity
                    print(f"[{x}] {colorify(rarity.capitalize(), rarity_color)}")
                rune_rarity = int(input(f"What rarity do you want {rune.icon} {colorify(rune.name + ' Rune', rune.color)} to be: "))
                add_rune(rune, rarities[rune_rarity])
        except Exception as e:
            raise e
    return False

def add_to_garden(plant_type: Plant, mutations: list[Mutation] = Mutation.mutations) -> None:
    global money, garden, active_rune
    money -= plant_type.buy
    new = deepcopy(plant_type)
    for mutation in mutations:
        chance_base = random()
        chance = mutation.chance
        if active_rune:
            if active_rune[0].hook == "mutationchance":
                if active_rune[0].type == "additer":
                    chance += active_rune[0].rarity_values[active_rune[1]]
                elif active_rune[0].type == "multiplier":
                    chance *= active_rune[0].rarity_values[active_rune[1]]
        if chance_base < mutation.chance:
            new = new.add_mutation(mutation)
    garden.append([new, new.get_sell_value(active_rune)])

def add_rune(rune_type: Rune, rarity: str = None) -> None:
    global unlocked_runes
    new = deepcopy(rune_type)
    if not rarity:
        rarity = new.generate_rarity()
    unlocked_runes.append([new, rarity])

def clear():
    system("cls")

def get_choice(choices: list[str], spacing: bool = True) -> str:
    if spacing:
        print("")
    x = 0
    for choice in choices:
        x += 1
        print(f"[{x}] {choice}")
    print("")
    return input("Pick one: ")