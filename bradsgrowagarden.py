from classes import *
from functions import *
from colorify import C, init_colorify

init_colorify()

Carrot = Plant("Carrot", "🥕", 1, 3, 5, C.orange)
Corn = Plant("Corn", "🌽", 35, 45, 55, C.green_yellow)
Broccoli = Plant("Broccoli", "🥦", 165, 200, 250, C.green)
Cucumber = Plant("Cucumber", "🥒", 785, 875, 1000, C.dark_green)
Pepper = Plant("Pepper", "🌶️", 2150, 2650, 3100, C.red)
Garlic = Plant("Garlic", "🧄", 7250, 9300, 11500, C.tan)
Melon = Plant("Melon", "🍈", 23750, 26500, 30000, C.khaki)
Orange = Plant("Orange", "🍊", 75000, 87500, 100000, C.dark_orange)
Grape = Plant("Grape", "🍇", 270000, 320000, 390000, C.purple)
Potato = Plant("Potato", "🥔", 465000, 520000, 635000, C.golden_rod)
Banana = Plant("Banana", "🍌", 800000, 910000, 1000000, C.yellow)
Candy_Blossom = Plant("Candy Blossom", "🍬", 12500000, 17500000, 25000000, C.pink)

Gold = Mutation("Gold", "🧈", 1.5, 0.25)
Rainbow = Mutation("Rainbow", "🌈", 5, 0.1)
Love = Mutation("Love", "❤️", 10, 0.07)
Starry = Mutation("Starry", "✨", 15, 0.03)
Gem = Mutation("Gem", "💎", 100, 0.005)

Money_Rune = Rune("Money", "💰", C.light_green, 10, "multiplier", "plantsell", {
    "common": 1.05, 
    "rare": 1.1, 
    "epic": 1.25, 
    "legendary": 1.5, 
    "mythic": 1.75, 
    "cosmic": 2
})

Luck_Rune = Rune("Luck", "🍀", C.green, 15, "additer", "mutationchance", {
    "common": 0.01, 
    "rare": 0.02, 
    "epic": 0.04, 
    "legendary": 0.1, 
    "mythic": 0.2, 
    "cosmic": 0.5
})

while True:
    if main_loop():
        break