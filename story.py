import random
import time
import sys
import lists
import typer
import msvcrt
from colorama import Fore, Back, Style, init
init(convert=True)

PAR = "\n\n"

"""
Below are all of the typing/color functions, used
for terminal outputs and making my text pretty
"""
type = typer.Type()
ask = typer.Ask()

# all the pretty colors
def red(text):
    return (Fore.RED + text + Fore.WHITE)

def green(text):
    return (Fore.GREEN + text + Fore.WHITE)
            
def magenta(text):
    return (Fore.MAGENTA + text + Fore.WHITE)

def yellow(text):
    return (Fore.YELLOW + text + Fore.WHITE)

def cyan(text):
    return (Fore.CYAN + text + Fore.WHITE)
            
def bright(text):
    return (Style.BRIGHT + text + Style.NORMAL)

def open_quote(text):
    return ("\"" + text)

def close_quote(text):
    return (text + "\"")

def quote(text):
    return ("\"" + text + "\"")

def space_quote(text):
    return ("\"" + text + "\" ")

class Player:
    __slots__ = ["__name", "__alive", "__is_sick", "__is_injured", 
                 "__flask_effects", "__status_effects", "__injuries", "__travel_restrictions", 
                 "__clear_status", "__clear_all_status", "__inventory", "__broken_inventory", 
                 "__repairing_inventory", "__dangers", "__met", "__mechanic_visits", "__health", 
                 "__balance", "__previous_balance", "__rank", "__day", "__counting_days", 
                 "__item_durability", "__flask_durability", "__round_count", "__is_religious", 
                 "__prereqs", "__prereqs_done", "__convenience_store_inventory", "__lists", 
                 "__tom_dreams", "__frank_dreams", "__oswald_dreams", "__favorite_color", 
                 "__favorite_animal", "__rabbit_chase", "__is_millionaire", "__millionaire_visited", 
                 "__chosen_mechanic", "__gus_items_sold", "__sanity", "__sanity_warnings_shown", 
                 "__faced_madness", "__is_broken"]

    def __init__(self):
        self.__name = None
        self.__alive = True
        self.__is_sick = False
        self.__is_injured = False
        self.__flask_effects = set()
        self.__status_effects = set()
        self.__injuries = set()
        self.__travel_restrictions = set()
        self.__clear_status = False
        self.__clear_all_status = False
        self.__inventory = set()
        self.__broken_inventory = set()
        self.__repairing_inventory = set()
        self.__dangers = set()
        self.__met = set()
        self.__mechanic_visits = 0
        self.__health = 100
        self.__balance = 50
        self.__previous_balance = 50
        self.__rank = 0
        self.__day = 1
        self.__counting_days = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.__item_durability = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # [delight_indicator, health_indicator, dirty_old_hat, golden_watch, enchanting_silver_bar, sneaky_peeky_shades, quiet_sneakers, faulty_insurance, lucky_coin, worn_gloves, tattered_cloak, rusty_compass, pocket_watch]
        self.__flask_durability = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # [no_bust, imminent_blackjack, dealers_whispers, bonus_fortune, anti_venom, anti_virus, fortunate_day, fortunate_night, second_chance, split_serum, dealers_hesitation, pocket_aces]
        self.__round_count = 3
        self.__is_religious = False
        self.__prereqs = [False, False, False, False, False]
        self.__prereqs_done = [False, False, False, False, False]
        self.__convenience_store_inventory = []
        self.__tom_dreams = 0      # 0=none, 1=rebecca, 2=nathan, 3=johnathan (ready for ending)
        self.__frank_dreams = 0    # 0=none, 1=dealers_anger, 2=dealers_scar, 3=dealers_revolver (ready for ending)
        self.__oswald_dreams = 0   # 0=none, 1=casino_bar, 2=casino_table, 3=casino_riches (ready for ending)
        self.__favorite_color = None
        self.__favorite_animal = None
        self.__rabbit_chase = 0    # 0-6 tracking which rabbit chase event is next
        self.__is_millionaire = False  # True when player hits $1M for the first time
        self.__millionaire_visited = False  # True after the special morning visitor comes
        self.__chosen_mechanic = None  # Which mechanic the visitor tells you to see ("Tom", "Frank", or "Oswald")
        self.__gus_items_sold = set()  # Tracks which collectibles have been sold to Gus
        self.__sanity = 100  # Visible stat - starts at 100, decreases with trauma
        self.__sanity_warnings_shown = 0  # Tracks how many sanity warnings have been shown
        self.__faced_madness = False  # True after surviving the confrontation
        self.__is_broken = False  # True when sanity hits 0 and you survive
        self.__lists = lists.Lists(self)

    def kill(self, cause_of_death=None):
        self.__alive = False
        self.status()

    def hurt(self, value):
        # First Aid Kit can be used to reduce a big hit (consumed)
        if self.has_item("First Aid Kit") and value >= 15:
            self.use_item("First Aid Kit")
            reduced = value // 2
            value = value - reduced
            type.type("You use your " + magenta(bright("First Aid Kit")) + " to patch yourself up!")
            print()
        
        # LifeAlert can save you from death once
        if (self.__health - value <= 0) and self.has_item("LifeAlert"):
            self.use_item("LifeAlert")
            type.slow(red(bright("You collapse... but your LifeAlert activates!")))
            print()
            type.type("Emergency services arrive just in time. You're rushed to the hospital.")
            print()
            type.type("They patch you up and send you on your way. Your LifeAlert has been used up.")
            self.__health = 25  # Survive with 25 health
            print()
            return
        
        if(self.__health - value <= 0):
            self.__health = 0
            type.slow(red(bright("You have succumbed to your wounds.")))
            self.kill()
        else:
            self.__health -= value
        if self.has_item("Health Indicator"):
            type.type("The " + magenta(bright("Health Indicator")) + " on your wrist makes a loud beep.")
            print()
            type.type("You took damage!")
            print()
            self.health_indicator()

    def heal(self, value):
        if(self.__health + value >= 100):
            self.__health = 100
        else:
            self.__health += value
        if self.has_item("Health Indicator"):
            type.type("The " + magenta(bright("Health Indicator")) + " on your wrist makes a subtle vibration.")
            print()
            type.type("You regained health!")
            print()
            self.health_indicator()

    def set_health(self, value):
        self.__health = value

    def get_health(self):
        return self.__health

    def health_indicator(self):
        if self.__health > 66:
            type.type("Your current health: " + bright(green(str(self.__health) + "%")))
        elif self.__health > 33:
            type.type("Your current health: " + bright(yellow(str(self.__health) + "%")))
        else:
            type.type("Your current health: " + bright(red(str(self.__health) + "%")))
        print("\n")
        self.update_health_indicator_durability()

    def status(self, cause_of_death=None):
        if not self.__alive:
            print("\n")
            type.slow("You have died!")
            print()
            if self.__day == 1: type.slow("You didn't even last " + bright(yellow(str(self.__day) + " day")) + ". That's embarrasing.")
            elif self.__day == 2: type.slow("You lasted " + bright(yellow(str(self.__day-1) + " day")) + ".")
            else: type.slow("You lasted " + bright(yellow(str(self.__day) + " days")) + "!")
            print()
            type.slow("You met your fate with a final balance of " + green(bright("${:,}".format(self.__balance))))
            print()
            type.slow("The police were able to recover your body, but nobody cared enough to show up to your funeral.")
            quit()
        elif (self.__balance == 0):
            print("\n")
            type.slow("You have run out of money!")
            print()
            if self.__day == 1: type.slow("You didn't even last " + bright(yellow(str(self.__day) + " day")) + ". That's absurdly sad.")
            elif self.__day == 2: type.slow("You lasted " + bright(yellow(str(self.__day-1) + " day")) + ".")
            else: type.slow("You lasted " + bright(yellow(str(self.__day) + " days")) + "!")
            print()
            type.slow("With no cash left to play Blackjack, your source of income has been rendered useless.")
            print()
            type.slow("You spend your remaining days going hungry, wondering what life could've been, if you didn't lose that one hand.")
            quit()
        elif (self.__balance >= 1000000) and (not self.__is_millionaire):
            # First time hitting $1M - set flag but don't end game yet
            self.__is_millionaire = True
            print("\n")
            type.slow(green(bright("You've done it. You've hit $1,000,000.")))
            print()
            type.slow("The Dealer stares at you with an expression you've never seen before. Is that... " + yellow("respect?"))
            print()
            type.slow("Something tells you that tomorrow morning is going to be different.")
            print()
    
    def get_name(self):
        return self.__name

    def is_religious(self):
        return self.__is_religious
    
    def lists(self):
        return self.__lists
    
    def add_travel_restriction(self, restriction):
        self.__travel_restrictions.add(restriction)

    def has_travel_restriction(self, restriction):
        return restriction in self.__travel_restrictions
    
    def remove_travel_restriction(self, restriction):
        self.__travel_restrictions.remove(restriction)

    def add_flask(self, flask):
        self.__flask_effects.add(flask)

    def has_flask_effect(self, flask):
        return flask in self.__flask_effects
    
    def remove_flask_effect(self, flask):
        self.__flask_effects.remove(flask)

    def len_flasks(self):
        return len(self.__flask_effects)

    def add_status(self, status):
        self.__status_effects.add(status)

    def has_status(self, status):
        return status in self.__status_effects
    
    def remove_status(self, status):
        self.__status_effects.remove(status)

    def add_injury(self, injury):
        self.__injuries.add(injury)

    def has_injury(self, injury):
        return injury in self.__injuries
    
    def heal_injury(self, injury):
        self.__injuries.remove(injury)

    def len_status(self):
        return len(self.__status_effects)
    
    def get_rounds(self):
        return self.__round_count
    
    def set_rounds(self, value):
        self.__round_count = value

    def add_item(self, item):
        self.__inventory.add(item)

    def has_item(self, item):
        return item in self.__inventory
    
    def has_broken_item(self, item):
        return item in self.__broken_inventory
    
    def is_repairing_item(self, item):
        return item in self.__repairing_inventory
    
    def repair_item(self, item):
        self.__repairing_inventory.add(item)
        self.__broken_inventory.remove(item)

    def return_item(self, item):
        self.__repairing_inventory.remove(item)
        self.__broken_inventory.add(item)
    
    def use_item(self, item):
        self.__inventory.remove(item)

    def break_item(self, item):
        self.__broken_inventory.add(item)
        self.__inventory.remove(item)

    def fix_item(self, item):
        self.__inventory.add(item)
        if self.is_repairing_item(item):
            self.__repairing_inventory.remove(item)
        if self.has_broken_item(item):
            self.__broken_inventory.remove(item)

    # ============================================
    # ITEM EFFECTS - Trap items and utility checks
    # ============================================
    
    def apply_necronomicon_effects(self):
        """The Necronomicon slowly corrupts you."""
        if self.has_item("Necronomicon"):
            if random.randrange(5) == 0:  # 20% chance per day
                self.lose_sanity(random.choice([1, 2, 3]))
                return True
        return False
    
    def apply_cursed_coin_effects(self):
        """The Cursed Coin brings misfortune."""
        if self.has_item("Cursed Coin"):
            if random.randrange(4) == 0:  # 25% chance
                return True  # Triggers bad luck
        return False
    
    def apply_suzys_gift_effects(self):
        """Suzy's Gift provides comfort and slowly restores sanity."""
        if self.has_item("Suzy's Gift"):
            if random.randrange(3) == 0:  # 33% chance per day
                self.restore_sanity(1)
                return True
        return False
    
    def has_fire_source(self):
        """Check if player can make fire."""
        return (self.has_item("Lighter") or self.has_item("Matches") or 
                self.has_item("Monogrammed Lighter") or self.has_item("Road Flares"))
    
    def has_cutting_tool(self):
        """Check if player has something sharp."""
        return self.has_item("Pocket Knife") or self.has_item("Golden Trident") or self.has_item("Golden Shovel")
    
    def add_danger(self, danger):
        self.__dangers.add(danger)

    def has_danger(self, danger):
        return danger in self.__dangers
    
    def lose_danger(self, danger):
        self.__dangers.remove(danger)

    # Dream sequence tracking
    def get_tom_dreams(self):
        return self.__tom_dreams
    
    def advance_tom_dreams(self):
        self.__tom_dreams += 1
    
    def get_frank_dreams(self):
        return self.__frank_dreams
    
    def advance_frank_dreams(self):
        self.__frank_dreams += 1
    
    def get_oswald_dreams(self):
        return self.__oswald_dreams
    
    def advance_oswald_dreams(self):
        self.__oswald_dreams += 1

    # Suzy storyline tracking
    def get_favorite_color(self):
        return self.__favorite_color
    
    def set_favorite_color(self, color):
        self.__favorite_color = color
    
    def get_favorite_animal(self):
        return self.__favorite_animal
    
    def set_favorite_animal(self, animal):
        self.__favorite_animal = animal

    # Rabbit chase tracking
    def get_rabbit_chase(self):
        return self.__rabbit_chase
    
    def advance_rabbit_chase(self):
        self.__rabbit_chase += 1

    # Millionaire ending tracking
    def is_millionaire(self):
        return self.__is_millionaire
    
    def was_millionaire_visited(self):
        return self.__millionaire_visited
    
    def set_millionaire_visited(self):
        self.__millionaire_visited = True
    
    def get_chosen_mechanic(self):
        return self.__chosen_mechanic
    
    def set_chosen_mechanic(self, mechanic):
        self.__chosen_mechanic = mechanic

    # Gus Pawn Shop tracking
    def get_gus_items_sold(self):
        return len(self.__gus_items_sold)
    
    def sell_item_to_gus(self, item_name):
        self.__gus_items_sold.add(item_name)
    
    def has_sold_to_gus(self, item_name):
        return item_name in self.__gus_items_sold
    
    def get_all_collectibles_list(self):
        """Returns the master list of all collectibles Gus will buy"""
        return [
            # Underwater/Beach Adventure (16 items)
            "Golden Trident", "Kraken Pearl", "Mermaid Crown", "Kraken's Memory",
            "Ancient Sea Map", "Deep Stone", "Pirate Treasure", "Treasure Coordinates",
            "Captain's Compass", "Cannon Gem", "Sailor's Lockbox", "Mermaid's Pearl",
            "Mermaid Pearl", "Matched Pearls", "Pink Pearl", "Giant Oyster",
            # Beach Events (7 items)
            "Golden Shovel", "Underwater Camera", "Crab Racing Trophy", 
            "Championship Medal", "Antique Ring", "Treasure Chest", "Midnight Rose",
            # Woodlands Adventure (8 items)
            "Hunter's Mark", "Bear King's Respect", "Giant Bear Tooth", "Bear's Gold Coin",
            "Witch's Favor", "Magic Acorn", "Fairy's Secret Map", "Captured Fairy",
            # Swamp Adventure (11 items)
            "Gator Tooth Necklace", "Tortoise Trophy", "Ogre's Gemstone", "Ogre's Gift",
            "Swamp Gold", "Witch's Riddle", "Witch's Ward", "Voodoo Doll",
            "Lucky Lure", "Earl's Lucky Lure", "Granny's Swamp Nectar",
            # City Adventure (5 items)
            "Key to the City", "Hero Medal", "Fight Champion Belt", 
            "Stolen Watch", "Suspicious Package",
            # Rabbit Events (4 items)
            "Lucky Penny", "Lucky Rabbit Foot", "Carrot", "Rabbit's Blessing",
            # Misc Adventure (6 items)
            "Mysterious Lockbox", "Mysterious Key", "Mysterious Code",
            "Fountain Water", "Treasure Map", "Joe's Treasure Map",
            # Secret Items (2 items)
            "Dealer's Joker", "Ace of Spades"
        ]
    
    def get_collectible_prices(self):
        """Returns dictionary of all collectible prices"""
        return {
            # Underwater/Beach Adventure - Legendary
            "Golden Trident": 80000,
            "Kraken Pearl": 100000,
            "Mermaid Crown": 75000,
            "Kraken's Memory": 50000,
            "Ancient Sea Map": 25000,
            "Deep Stone": 40000,
            "Pirate Treasure": 60000,
            "Treasure Coordinates": 15000,
            "Captain's Compass": 12000,
            "Cannon Gem": 20000,
            "Sailor's Lockbox": 8000,
            "Mermaid's Pearl": 8000,
            "Mermaid Pearl": 6000,
            "Matched Pearls": 5000,
            "Pink Pearl": 3000,
            "Giant Oyster": 2000,
            # Beach Events
            "Golden Shovel": 15000,
            "Underwater Camera": 1500,
            "Crab Racing Trophy": 3000,
            "Championship Medal": 5000,
            "Antique Ring": 4000,
            "Treasure Chest": 10000,
            "Midnight Rose": 2500,
            # Woodlands Adventure
            "Hunter's Mark": 8000,
            "Bear King's Respect": 50000,
            "Giant Bear Tooth": 15000,
            "Bear's Gold Coin": 5000,
            "Witch's Favor": 12000,
            "Magic Acorn": 6000,
            "Fairy's Secret Map": 8000,
            "Captured Fairy": 25000,
            # Swamp Adventure
            "Gator Tooth Necklace": 5000,
            "Tortoise Trophy": 4000,
            "Ogre's Gemstone": 30000,
            "Ogre's Gift": 20000,
            "Swamp Gold": 10000,
            "Witch's Riddle": 3000,
            "Witch's Ward": 5000,
            "Voodoo Doll": 8000,
            "Lucky Lure": 2000,
            "Earl's Lucky Lure": 4000,
            "Granny's Swamp Nectar": 1500,
            # City Adventure
            "Key to the City": 25000,
            "Hero Medal": 15000,
            "Fight Champion Belt": 10000,
            "Stolen Watch": 3000,
            "Suspicious Package": 5000,
            # Rabbit Events
            "Lucky Penny": 50,
            "Lucky Rabbit Foot": 1500,
            "Carrot": 5,
            "Rabbit's Blessing": 10000,
            # Misc Adventure
            "Mysterious Lockbox": 2000,
            "Mysterious Key": 1500,
            "Mysterious Code": 3000,
            "Fountain Water": 8000,
            "Treasure Map": 5000,
            "Joe's Treasure Map": 3000,
            # Secret Items
            "Dealer's Joker": 50000,
            "Ace of Spades": 1000,
        }
    
    def get_gus_total_collectibles(self):
        """Returns total number of unique collectibles Gus wants"""
        return len(self.get_all_collectibles_list())

    # Sanity tracking system (visible stat)
    def get_sanity(self):
        return self.__sanity
    
    def lose_sanity(self, value):
        """Decrease sanity. The player will see this."""
        if self.__is_broken:
            return  # Already broken, can't lose more sanity
        
        old_sanity = self.__sanity
        self.__sanity -= value
        # Floor at 0
        if self.__sanity < 0:
            self.__sanity = 0
        # Show warning message based on new threshold crossed
        if old_sanity > 75 and self.__sanity <= 75:
            print("\n")
            type.slow(yellow("Your mind feels... foggy. Something isn't right."))
            print("\n")
        elif old_sanity > 50 and self.__sanity <= 50:
            print("\n")
            type.slow(yellow(bright("The edges of your vision blur. Reality feels thin.")))
            print("\n")
        elif old_sanity > 25 and self.__sanity <= 25:
            print("\n")
            type.slow(red(bright("Your thoughts are fracturing. The shadows are getting closer.")))
            print("\n")
        
        # Check if sanity hit zero - trigger madness ending or become broken
        if old_sanity > 0 and self.__sanity <= 0:
            self.sanity_depleted()
    
    def restore_sanity(self, value):
        """Restore sanity through positive events"""
        old_sanity = self.__sanity
        self.__sanity += value
        if self.__sanity > 100:
            self.__sanity = 100
        # Show recovery message if crossing back above a threshold
        if old_sanity <= 50 and self.__sanity > 50:
            print("\n")
            type.slow(green("A sense of clarity washes over you. The fog lifts, if only a little."))
            print("\n")
    
    def sanity_indicator(self):
        """Display current sanity level with color coding"""
        if self.__is_broken:
            type.type("Your sanity: " + bright(red("BROKEN")))
        elif self.__sanity > 75:
            type.type("Your current sanity: " + bright(green(str(self.__sanity) + "%")))
        elif self.__sanity > 50:
            type.type("Your current sanity: " + bright(yellow(str(self.__sanity) + "%")))
        elif self.__sanity > 25:
            type.type("Your current sanity: " + bright(magenta(str(self.__sanity) + "%")))
        else:
            type.type("Your current sanity: " + bright(red(str(self.__sanity) + "%")))
        print("\n")
    
    def get_sanity_description(self):
        """Get a text description of current sanity state"""
        if self.__is_broken:
            return "shattered beyond repair"
        elif self.__sanity > 90:
            return "clear-headed"
        elif self.__sanity > 75:
            return "slightly unsettled"
        elif self.__sanity > 60:
            return "anxious"
        elif self.__sanity > 50:
            return "disturbed"
        elif self.__sanity > 40:
            return "unstable"
        elif self.__sanity > 25:
            return "fractured"
        elif self.__sanity > 10:
            return "barely holding on"
        else:
            return "teetering on the edge of madness"
    
    def sanity_affects_gambling(self):
        """Returns a modifier based on sanity - low sanity makes gambling harder"""
        if self.__sanity > 75:
            return 0  # No penalty
        elif self.__sanity > 50:
            return 1  # Slight disadvantage
        elif self.__sanity > 25:
            return 2  # Noticeable disadvantage  
        else:
            return 3  # Severe disadvantage
    
    def has_faced_madness(self):
        return self.__faced_madness
    
    def set_faced_madness(self):
        self.__faced_madness = True
    
    def should_show_sanity_effect(self):
        """Returns True if conditions are right for a sanity effect"""
        if self.__sanity > 85:
            return False
        # Lower sanity = more frequent effects
        effect_chance = (100 - self.__sanity) // 10
        if random.randrange(20) < effect_chance:
            self.__sanity_warnings_shown += 1
            return True
        return False
    
    def get_sanity_effect(self):
        """Returns a description of the player's deteriorating mental state"""
        mild_effects = [
            "For a moment, you could have sworn the shadows moved.",
            "You hear whispers, but when you listen closer... nothing.",
            "Your reflection in the rearview mirror blinks before you do.",
            "The cards in your dreams are always face down. Always.",
            "You can't remember if you slept last night. Or the night before.",
            "Your hands are shaking. When did they start shaking?",
            "You count your money three times. You get a different number each time.",
            "Someone is watching you. You're certain of it. But there's no one there.",
            "You taste copper. There's nothing in your mouth.",
            "The trees outside your car window are too still. Unnaturally still.",
            "You find a note in your pocket. It's your handwriting, but you don't remember writing it.",
            "The sun seems dimmer today. Like it's further away than it should be.",
            "You hear your name called. The voice sounds like your own.",
        ]
        severe_effects = [
            "The world flickers, like a dying light bulb. Reality feels thin.",
            "You see yourself walking past your car window. You don't stop to look.",
            "The Dealer's jade eye appears everywhere. In reflections. In shadows. In the spaces between heartbeats.",
            "Your thoughts are echoing. Echoing. Echoing.",
            "Blood drips from the ceiling of your car. When you look up, it's gone.",
            "The radio turns on by itself. It plays a song that doesn't exist.",
            "You can't feel your heartbeat anymore. You check. It's still there. You think.",
            "The casino's neon sign flickers. It spells your name. Then it doesn't.",
            "The walls are breathing. You're sure of it.",
            "You forgot your own name for a moment. It came back. Eventually.",
        ]
        if self.__sanity <= 50:
            return random.choice(mild_effects + severe_effects)
        return random.choice(mild_effects)
    
    def check_madness_confrontation(self):
        """Check if the madness confrontation should trigger (at low sanity)"""
        if self.__faced_madness:
            return False
        if self.__sanity > 40:  # Only triggers at 40 or below
            return False
        # 10% base chance at 40 sanity, scaling up as sanity drops
        trigger_chance = (50 - self.__sanity) // 5
        return random.randrange(100) < trigger_chance

    def gambling_result(self, status, bet_amount):
        """Called after each blackjack hand to affect sanity based on result"""
        if status in ["Player Blackjack", "Player Wins", "Dealer Bust"]:
            # Winning restores a tiny bit of sanity
            if self.__sanity < 100 and random.randrange(5) == 0:
                self.__sanity = min(100, self.__sanity + 1)
        elif status in ["Dealer Blackjack", "Dealer Wins", "Player Bust"]:
            # Losing big bets damages sanity
            bet_ratio = bet_amount / max(self.__balance, 1)
            if bet_ratio >= 0.5:  # Lost half or more of your money
                self.lose_sanity(random.choice([2, 3, 4]))
            elif bet_ratio >= 0.25:  # Lost a quarter
                self.lose_sanity(random.choice([1, 2]))
            # Small losses occasionally chip away at sanity
            elif random.randrange(10) == 0:
                self.lose_sanity(1)

    def sanity_depleted(self):
        """Called when sanity hits 0 - either madness ending or become broken"""
        print("\n")
        type.slow(red(bright("===============================================")))
        type.slow(red(bright("         YOUR SANITY HAS SHATTERED           ")))
        type.slow(red(bright("===============================================")))
        print("\n")
        
        type.slow("Everything goes dark. The world folds in on itself.")
        print("\n")
        type.slow("You feel yourself slipping... falling... breaking...")
        print("\n")
        
        # 40% chance of madness ending, 60% chance of becoming broken
        if random.randrange(100) < 40:
            type.slow(red("The darkness swallows you whole."))
            print("\n")
            time.sleep(2)
            self.madness_ending()
        else:
            self.become_broken()
    
    def become_broken(self):
        """You survive the sanity break, but you're never the same"""
        type.slow("...")
        print("\n")
        time.sleep(1)
        type.slow("Something inside you... snaps.")
        print("\n")
        type.slow("But it doesn't kill you. Not physically, anyway.")
        print("\n")
        type.slow(cyan("You open your eyes. The world looks... wrong. Colors are too bright. Sounds are too loud. Everything has edges that shouldn't be there."))
        print("\n")
        type.slow(cyan("Your hands are shaking. They won't stop. You're not sure they ever will."))
        print("\n")
        type.slow(yellow(bright("You have become BROKEN.")))
        print("\n")
        type.slow(yellow("Your mind is shattered, but somehow you continue. The game goes on."))
        print("\n")
        type.slow(yellow("But nothing will ever be the same."))
        print("\n")
        
        self.__is_broken = True
        self.__sanity = 0  # Sanity stays at 0 forever
        self.meet("Broken Mind")
        
        ask.press_continue("Press any key to continue your broken existence...")
        print("\n")
    
    def is_broken(self):
        """Check if player has been broken"""
        return self.__is_broken
    
    def get_broken_effect(self):
        """Get a random broken mind effect for gameplay"""
        effects = [
            "Your vision doubles. Which pile of money is real?",
            "You hear the cards laughing. They're always laughing now.",
            "Your fingers move on their own, betting before you can think.",
            "The Dealer's face keeps shifting. Is that really him?",
            "You forgot where you are. You remember. You forget again.",
            "The numbers don't make sense anymore. They never did.",
            "You see yourself sitting across the table. He waves.",
            "Time skips. Did you just play a hand? When?",
            "The chips feel like teeth in your hands.",
            "Someone is screaming. Oh. It's you. You stop.",
            "You can taste colors now. Green tastes like regret.",
            "Your reflection in the cards is smiling. You're not.",
            "The walls are too close. No, too far. Which is it?",
            "You blink and lose track of three hands.",
            "The Dealer said something. You laughed. You don't know why.",
        ]
        return random.choice(effects)
    
    def broken_gameplay_effect(self):
        """Apply a random broken effect during gameplay - returns what happened"""
        effect_type = random.randrange(10)
        
        if effect_type == 0:
            # Randomly lose some money
            loss = random.randint(1, min(100, self.__balance // 10 + 1))
            self.__balance -= loss
            return ("money_loss", loss, "You blink and some money is gone. Did you spend it? Did someone take it? Does it matter?")
        elif effect_type == 1:
            # Randomly gain a small amount (hallucinated winnings that turn out to be real?)
            gain = random.randint(1, 20)
            self.__balance += gain
            return ("money_gain", gain, "You find money in your pocket. You don't remember putting it there. You don't question it anymore.")
        elif effect_type == 2:
            # Take damage from self-harm/accidents
            damage = random.randint(1, 5)
            self.hurt(damage)
            return ("self_harm", damage, "You notice blood on your hands. You don't remember how it got there.")
        elif effect_type == 3:
            # Heal slightly (dissociation numbs the pain)
            heal = random.randint(1, 3)
            self.heal(heal)
            return ("numb", heal, "You can't feel anything anymore. Maybe that's a blessing.")
        else:
            # Just a visual/text effect, no gameplay impact
            return ("hallucination", 0, self.get_broken_effect())

    # Item upgrade system (Oswald)
    # Index: 0=delight_indicator, 1=health_indicator, 2=dirty_old_hat, 3=golden_watch, 
    #        4=sneaky_peeky_shades, 5=quiet_sneakers, 6=faulty_insurance, 7=lucky_coin,
    #        8=worn_gloves, 9=tattered_cloak, 10=rusty_compass, 11=pocket_watch
    def get_upgraded_version(self, item):
        # Maps base items to their upgraded versions
        upgrades = {
            "Delight Indicator": "Delight Manipulator",
            "Health Indicator": "Health Manipulator", 
            "Dirty Old Hat": "Unwashed Hair",
            "Golden Watch": "Sapphire Watch",
            "Sneaky Peeky Shades": "Sneaky Peeky Goggles",
            "Quiet Sneakers": "Quiet Bunny Slippers",
            "Faulty Insurance": "Real Insurance",
            "Lucky Coin": "Lucky Medallion",
            "Worn Gloves": "Velvet Gloves",
            "Tattered Cloak": "Invisible Cloak",
            "Rusty Compass": "Golden Compass",
            "Pocket Watch": "Grandfather Clock"
        }
        return upgrades.get(item, None)
    
    def is_upgraded_item(self, item):
        # Check if an item is an upgraded version
        upgraded_items = ["Delight Manipulator", "Health Manipulator", "Unwashed Hair",
                         "Sapphire Watch", "Sneaky Peeky Goggles", "Quiet Bunny Slippers",
                         "Real Insurance", "Lucky Medallion", "Velvet Gloves",
                         "Invisible Cloak", "Golden Compass", "Grandfather Clock"]
        return item in upgraded_items
    
    def can_upgrade(self, item):
        # Can only upgrade base items, and must own them
        return self.has_item(item) and self.get_upgraded_version(item) is not None
    
    def perform_upgrade(self, item):
        # Remove old item and add upgraded version
        upgraded = self.get_upgraded_version(item)
        if upgraded and self.has_item(item):
            self.remove_item(item)
            self.add_item(upgraded)
            return upgraded
        return None
    
    def all_items_upgraded(self):
        # Check if player has all upgraded versions
        upgraded_items = ["Delight Manipulator", "Health Manipulator", "Unwashed Hair",
                         "Sapphire Watch", "Sneaky Peeky Goggles", "Quiet Bunny Slippers",
                         "Real Insurance", "Lucky Medallion", "Velvet Gloves",
                         "Invisible Cloak", "Golden Compass", "Grandfather Clock"]
        for item in upgraded_items:
            if not self.has_item(item):
                return False
        return True
    
    def meet(self, person):
        self.__met.add(person)

    def has_met(self, person):
        return person in self.__met

    def get_balance(self):
        return self.__balance

    def set_balance(self, value):
        self.__balance = value

    def change_balance(self, value):
        print("\n")
        if (self.__balance + value) <= 0:
            self.__balance = 0
            type.type("Your new balance is " + red(bright("$0")))
        else:
            previous_balance = self.__balance
            self.__balance += value
            if value > 0:
                type.type("Your new balance is " + green(bright("${:,}".format(previous_balance) + " + ${:,}".format(value)) + bright(green(" = " + "${:,}".format(self.__balance)))))
            elif value < 0:
                type.type("Your new balance is " + green(bright("${:,}".format(previous_balance))) + red(bright(" - ${:,}".format(abs(value)))) + green(bright(" = ${:,}".format(self.__balance))))
        print("\n")

    def get_rank(self):
        return self.__rank

    def update_rank(self):
        if(1<=self.__balance<1000):
            self.__rank = 0
        elif(1000<=self.__balance<10000):
            self.__rank = 1
        elif(10000<=self.__balance<100000):
            self.__rank = 2
        elif(100000<=self.__balance<500000):
            self.__rank = 3
        elif(500000<=self.__balance<900000):
            self.__rank = 4
        elif(900000<=self.__balance<1000000):
            self.__rank = 5
        else:
            self.status()
    
    def increment_day(self): # really just for testing
        self.__day+=1

    def end_day(self):
        if(self.has_danger("Angry Dealer")):
            self.lose_danger("Angry Dealer")
            self.end_day_angry_dealer()
        elif(self.__day==1):
            self.end_day_1()
        elif(not self.has_item("Car")):
            self.end_day_car_broken()
        else:
            self.end_day_car_fixed()

        print("\n")

        self.update_dirty_old_hat_durability()
        self.update_golden_watch_durability()

        # Starting cheer (eg. Yippee!)
        type.type(self.__lists.get_cheer())

        # Tells day count and previous day's balance
        if self.__day == 1:
            type.type(" You've survived " + yellow(bright(str(self.__day) + " day")) + "!")
            print("\n")
            type.type("You started your journey with just " + green(bright("$" + str(self.__previous_balance))) + ". ")
        else:
            type.type(" You've survived " + yellow(bright(str(self.__day) + " days")) + "!")
            print("\n")
            type.type("Yesterday, at this time, you had " + green(bright("$" + str(self.__previous_balance))) + ". ")
        # increments day
        self.__day += 1

        print("")

        # Tells you the change in your balance, and if you gained or lost money
        change_in_balance = self.__balance - self.__previous_balance
        if change_in_balance > 0: type.type("Since then, you've accumulated " + green(bright("$" + str(change_in_balance))) + ". ")
        elif change_in_balance < 0: type.type("Since then, you've managed to lose " + red(bright("$" + str(abs(change_in_balance)))) + ". ")
        else: type.type("Somehow, your net earnings today was 0. Goose egg. No money. Disappointing. ")

        # Sets previous balance to current balance, so that it's ready for next day
        self.__previous_balance = self.__balance

        print("")

        # Tells you your current balance
        type.type("That brings you to a grand total of " + green(bright("$" + str(self.__balance))) + "! ")

        match self.__rank:
            case 0: type.type("Let's not get too far ahead of ourselves though, you're still quite poor.")
            case 1: type.type("You definately have some money. The keyword is 'some'.")
            case 2: type.type("You've amassed signifigant earnings. Nicely done.")
            case 3: type.type("You must have some heavy pockets, huh.")
            case 4: type.type("Where do you even keep all that?")
            case 5: type.type("So close to being a millionaire! Can you do it?")

        print("\n")

        # Gives a little personal advice, support, etc
        type.type(self.__lists.get_advice())

        print()

        # Gives one last quote before starting the next day
        type.type(self.__lists.get_quote_setup())
        type.type(self.__lists.get_quote())

        # Heals the player before the next day
        print("\n")
        self.heal(random.choice([1, 3, 5]))

        ask.press_continue("Press a key to continue: ")


    # Opening
    def first_setup(self):
        while (True):
            type.type("Type 'y' or 'yes', not case sensitive, to say yes to a question: ")
            yes_or_no = input("").lower()
            if (yes_or_no == "y") or (yes_or_no == "yes"):
                break
            else:
                print()
        print()

        while (True):
            type.type("Type 'n' or 'no', not case sensitive, to say no to a question: ")
            yes_or_no = input("").lower()
            if (yes_or_no == "n") or (yes_or_no == "no"):
                break
            else:
                print()
        print()

        while (True):
            type.type("Type 'h' or 'hit', not case sensitive, to hit your hand: ")
            hit_or_stand = input("").lower()
            if (hit_or_stand == "h") or (hit_or_stand == "hit"):
                break
            else:
                print()
        print()

        while (True):
            type.type("Type 's' or 'stand', not case sensitive, to stand with your hand's value: ")
            hit_or_stand = input("").lower()
            if (hit_or_stand == "s") or (hit_or_stand == "stand"):
                break
            else:
                print()
        print()

    def opening_lines(self):
        type.type("\"Ugh, not again,\" you spout as the old wagon shutters, then dies. ")
        type.type("Stranded on the road again, but this time, your money has gone dry. ")
        type.type("All but your 50 dollar bill that Grandma gave you on her last Christmas. ")
        type.type("You've been saving it for when you needed it most, but surely, it won't be enough.")
        print('\n')
        type.type("The door creaks open, and you step out into the night sky, coughing up the smoke from your fried vehicle. ")
        type.type("After pushing your car off the road and between the trees, there isn't much else left for you to do, ")
        type.type("so you begin to wander down the dark, lonely street.")
        print('\n')
        type.type("But at the end of the road, where concrete turned to stone turned to dirt, you notice a light up ahead, on the top of a hill. ")
        print('\n')
        type.type("As you waltz into the old, wooden shack, your eyes begin to light up with the fire of a thousand suns. ")
        type.type("Roulette wheels! Poker tables! And in a dark corner of the abandoned casino, sits a dealer, shuffling cards for a new round of Blackjack. ")
        type.type("That 50 dollars might just come in handy after all. Thanks, Grandma!")
        print('\n')
        type.type("As you go to sit down at the table, you hear the Dealer cough, then watch as he sits up.")
        print("\n")
        type.type("In a deep, and yet strained voice, the Dealer, cloaked in darkness, poses a question to you.")
        print("\n")
        self.start_night()

    # End Days
    def end_day_1(self):
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep after such a long day. ")
        type.type("Making it back to your car, ditched on the side of the road, but no longer engulfed in smoke, you lay down, and close your eyes. It's time to rest.")

    def end_day_car_broken(self):
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep. ")
        type.type("Making it back to your car, ditched on the side of the road, you lay down, and close your eyes. It's time to rest.")

    def end_day_car_fixed(self):
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep. ")
        type.type("You make it to your car and drive away from the casino, and you park in a little alcove on the side of the road. You lay down, and close your eyes. It's time to rest.")

    def end_day_wind(self):
        self.remove_travel_restriction("Wind")
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep. ")
        type.type("Stepping outside, you notice that the wind has calmed down. That's a relief. ")
        type.type("Making it back to your car, ditched on the side of the road, you lay down, and close your eyes. It's time to rest.")


    def end_day_angry_dealer(self):
        type.type("You've never seen the dealer quite so angry. Fortunately, you make it back to your car, and immediately pass out for the night. It's time to rest.")

    def start_night(self):
        if(self.__day==1):
            self.start_night_1()
        elif self.has_travel_restriction("Wind"):
            self.end_day_wind()
        elif(not self.has_item("Car")):
            self.start_night_car()
        else:
            self.start_night_car_fixed()

    def start_night_1(self):
        type.slow(red("Would you like to play a game of Blackjack? "))
        yes_or_no = input("").lower()
        print()
        if (yes_or_no == "n") or (yes_or_no == "no"):
            type.slow(red(bright("Well that's just too bad, isn't it. ")))
            type.slow(red("The Dealer fires three shots into your chest. You bleed out, and as you fade from reality, you see the Dealer reach into your pockets, and take the last 50 dollars from your lifeless body."))
            self.kill()

    def start_night_car(self):
        type.type("As the sun begins to set, and the stars light up in the night sky, you walk to the casino, eager to play more Blackjack. ")
        print("\n")
        # Broken state casino perception
        if self.__is_broken:
            broken_casino = random.choice([
                "The casino looks different tonight. The walls are wrong. The angles don't make sense. You go in anyway.",
                "You can hear the slot machines screaming. No one else seems to notice.",
                "The casino is upside down. No. It's not. It never was. You're fine. You're fine.",
                "Every patron in the casino has your face. You blink. They don't anymore. Did they ever?",
                "The door opens before you touch it. It was expecting you."
            ])
            type.slow(red(broken_casino))
            print("\n")
        # Low sanity affects how you perceive the casino
        elif self.__sanity <= 50:
            type.slow(cyan("The casino lights seem too bright. Too hungry. They're watching you."))
            print("\n")
        elif self.__sanity <= 75:
            type.type("You feel " + yellow(self.get_sanity_description()) + " tonight.")
            print("\n")
        self.grandfather_clock_dialogue()
        type.slow(red(self.__lists.get_dealer_welcome()))
        print("\n")

    def start_night_car_fixed(self):
        type.type("As the sun begins to set, and the stars light up in the night sky, you drive over to the casino, eager to play more Blackjack. ")
        print("\n")
        # Broken state casino perception
        if self.__is_broken:
            broken_casino = random.choice([
                "You don't remember driving here. You don't remember getting in the car. You're at the casino now.",
                "The steering wheel felt like bones under your fingers. Human bones. Car bones. Same thing.",
                "The casino is on fire. No. It's just the sunset. Probably.",
                "Your reflection in the car window stayed behind when you got out. It's fine. You don't need it.",
                "The parking lot has too many cars. They're all yours. From timelines that didn't happen."
            ])
            type.slow(red(broken_casino))
            print("\n")
        # Low sanity affects how you perceive the casino
        elif self.__sanity <= 50:
            type.slow(cyan("The neon signs blur together. For a moment, you can't remember why you came here."))
            print("\n")
        elif self.__sanity <= 75:
            type.type("You feel " + yellow(self.get_sanity_description()) + " tonight.")
            print("\n")
        self.grandfather_clock_dialogue()
        type.slow(red(self.__lists.get_dealer_welcome()))
        print("\n")

    def grandfather_clock_dialogue(self):
        if self.has_item("Grandfather Clock") and random.randrange(10) == 0:
            dialogue = random.choice([
                "The Dealer stares at the massive clock bulging out of your pocket. " + quote("Is that a grandfather clock in your pocket, or are you just happy to see me?") + " He pauses. " + quote("Wait. That's actually a grandfather clock. Why do you have that."),
                "The Dealer squints at your pocket. " + quote("Son, I've seen a lot of things in my years, but I ain't never seen a man stuff a whole grandfather clock down his pants. You got issues."),
                "As you sit down, the Grandfather Clock lets out a loud " + bright("BONG") + ". The Dealer flinches. " + quote("Jesus Christ, boy! You trying to give an old man a heart attack? Keep that thing quiet or I'll use it as firewood."),
                "The Dealer watches you struggle to sit down with the clock. " + quote("You know, most folks just check the time on their phone. But I respect the commitment to being absolutely ridiculous."),
                "The Grandfather Clock chimes midnight. The Dealer looks at his watch. " + quote("It's 7 PM.") + " He sighs. " + quote("That thing's about as reliable as my ex-wife.")
            ])
            type.slow(red(dialogue))
            print("\n")



    # Poor Day Events (1 - 1,000)
    # Everytime
    def seat_cash(self):
        # Alt dialogue for repeated event
        variant = random.randrange(4)
        if variant == 0:
            type.type("You wake up in the front seat, covered in sweat. ")
            type.type("As the sun shines through the car window, you notice a bright green bill tucked between the seat cushions. Must be your lucky day. ")
        elif variant == 1:
            type.type("Your eyes flutter open to blinding sunlight. As you shield your face, something crinkles beneath your fingers. ")
            type.type("Cash! Wedged right there in the crack of the seat like it was waiting for you. ")
        elif variant == 2:
            type.type("You stretch awake, your back aching from another night in the wagon. While adjusting your seat, your hand brushes against something papery. ")
            type.type("Well, well, well. Looks like past-you stashed some emergency funds and forgot about it. ")
        else:
            type.type("The morning sun hits your face like a slap. Groaning, you shift in your seat-and hear a crinkle. ")
            type.type("Money? In YOUR seat cushions? It's more likely than you think. ")
        print("\n")
        bill = random.choice([5, 10, 20, 50, 100])
        type.type("That's another " + green(bright("$" + str(bill))) + " dollars.")
        self.change_balance(bill)

    def left_window_down(self):
        # Alt dialogue for repeated event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You wake up in the front seat, with a chill going down your spine. ")
            type.type("Had the window really been open all night? ")
            type.type("Hopefully nothing had gotten in. ")
            type.type("You roll the window up, just to be safe. ")
        elif variant == 1:
            type.type("A cold breeze tickles your face. You crack one eye open-the window's wide open. ")
            type.type("How long has it been like that? You could've frozen to death! Or worse... ")
            type.type("You crank it shut, scanning the car interior nervously. ")
        else:
            type.type("You jolt awake to the sound of crickets. WAY too close. ")
            type.type("The passenger window is down. Great. Just great. ")
            type.type("You slam it shut, but the damage might already be done. ")
        random_chance = random.randrange(5)
        if random_chance == 0:
                self.add_danger("Spider")
        elif random_chance == 1:
                self.add_danger("Cockroach")
        print("\n")

    def estranged_dog(self):
        # Alt dialogue for repeated event + rare special variant
        rare_chance = random.randrange(100)
        
        if rare_chance < 5:  # 5% RARE VARIANT - The Ghost Dog
            type.type("You wake up to barking-but something's off. The barking sounds... hollow. Distant, even though it's right outside.")
            print("\n")
            type.type("Through your window, you see a dog. It's translucent. You can see right through it to the trees behind. A ghost dog.")
            print("\n")
            type.type("The spectral canine tilts its head at you, tongue lolling, then passes straight through your car door and into the seat beside you.")
            print("\n")
            type.type("You feel a warm presence, despite the chill. The ghost dog rests its head on your lap for just a moment...")
            print("\n")
            type.type("And then it's gone. But the warmth remains.")
            print("\n")
            self.heal(50)
            type.type(yellow(bright("You feel like someone's watching over you.")))
            print("\n")
            return
        
        # Normal variants
        variant = random.randrange(3)
        if variant == 0:
            type.type("You wake up to the sound of barking outside your car. You get up, to see a golden retriever licking your window. ")
            type.type("You open the door, and pet the doggo on the head. He seems happy. You're happy, too.")
        elif variant == 1:
            type.type("Something wet touches your hand through the cracked window. You panic-then see the fluffy face of a happy dog staring at you. ")
            type.type("A German Shepherd this time, tail wagging so hard its whole body shakes. You can't help but smile.")
        else:
            type.type("You're woken by excited yipping. A small corgi is doing zoomies around your car, clearly having the time of its life. ")
            type.type("When you open the door, it immediately jumps into your lap and starts covering your face in kisses.")
        print("\n")
        if self.has_item("Dog Treat"):
            self.use_item("Dog Treat")
            type.type("You throw your " + bright(magenta("Dog Treat")) + " into the air, and the dog jumps up, and catches it in his mouth. He wags his tail in excitement. It's super cute.")
            print("\n")
            self.heal(random.choice([15, 20]))
        else:
            self.heal(random.choice([5, 10]))
        type.type("Before you get a chance to check the dog's collar to see where it came from, the dog bolts down the road, eager to cheer up someone else. It was a good dog.")
        print("\n")
        return
    
    def freight_truck(self):
        # Alt dialogue for repeated event + rare special variant
        rare_chance = random.randrange(100)
        
        if rare_chance < 3:  # 3% RARE VARIANT - The Guilt Trip
            type.type("You are jolted awake by the sound of a horn blaring outside your car. Looking out your window, you see a man in a freight truck.")
            print("\n")
            type.type("But something's different. He's not laughing. He's... crying?")
            print("\n")
            type.type(quote("I'm sorry... I'm so sorry for all those times I honked at you. I was going through some stuff, man. My wife left me. My dog died. My truck? Also dying."))
            print("\n")
            type.type("He wipes his nose with his sleeve.")
            print("\n")
            type.type(quote("Here. Take this. It's not much, but... I want to make things right."))
            print("\n")
            type.type("The trucker hands you a wad of cash through the window, still sniffling.")
            print("\n")
            self.change_balance(random.randint(200, 500))
            type.type(quote("Drive safe, friend. Drive safe."))
            print("\n")
            type.type("And with that, the freight truck slowly pulls away, the horn playing a sad melody into the distance.")
            print("\n")
            return
        
        # Normal variants
        variant = random.randrange(4)
        if variant == 0:
            type.type("You are jolted away by the sound of a horn blaring outside your car. Looking out your window, you see a man, in a bright red hat, inside of a freight truck that's parked just outside of your vehicle.")
            print("\n")
            type.type(quote("Hey, you. Wake the fuck up! Hahahaha!"))
            print("\n")
            type.type("You watch as the man honks his horn one more time, laughs, and drives off into the distance. What a jerk.")
        elif variant == 1:
            type.type("HOOOOOOONK! You nearly hit the roof of your car as a freight truck blasts past, the driver giving you a middle finger out the window.")
            print("\n")
            type.type(quote("GET A HOUSE, LOSER!"))
            print("\n")
            type.type("The truck disappears, leaving you with ringing ears and a sour mood.")
        elif variant == 2:
            type.type("The unmistakable sound of an airhorn tears through your dreams. You bolt upright to see a trucker parked RIGHT next to your car, grinning like an idiot.")
            print("\n")
            type.type(quote("Rise and shine, buttercup! Time to face another day!"))
            print("\n")
            type.type("He gives you a thumbs up, hits the horn three more times for good measure, then drives off cackling.")
        else:
            type.type("You wake up to rhythmic honking. HONK HONK HONK-HONK-HONK. Is that... Shave and a Haircut?")
            print("\n")
            type.type("A trucker waves at you from his cab, waiting expectantly. When you don't respond with 'two bits,' he shrugs and drives off, disappointed.")
            print("\n")
            type.type(quote("No culture these days...") + " you hear him mutter.")
        print("\n")
        return

    # Conditional
    def sore_throat(self):
        if self.has_status("Sore Throat"):
            self.day_event()
            return
            
        type.type("You wake up, and begin to have a coughing fit. Your throat is dry, and super sore. ")
        if self.has_item("Cough Drops"):
            self.use_item("Cough Drops")
            type.type("Luckily, you have some " + magenta(bright("Cough Drops")) + " on hand, and you empty the box into your mouth. Almost like magic, your throat doesn't hurt anymore.")
            print("\n")
            return
        else:
            self.add_status("Sore Throat")
            self.mark_day("Sore Throat")
            type.type("You cough, and cough, and cough some more, but the burning itch in your throat just won't go away.")
            print("\n")
            return

    def spider_bite(self):
        if not self.has_danger("Spider") or self.has_status("Spider Bite"):
            self.day_event()
            return
        
        type.type("You wake up to a sharp pain on your arm! ")
        type.type("Swinging your arm to scratch the pain, you watch as a spider jumps to your dashboard. ")
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the spider. ")
            type.type("A cloud of white liquid covers the spider, and you watch as it slows, and dies. ")
            type.type("Hopefully, that's the end of your spider problems.")
        else:
            type.type("You attempt to swat it with your hand, but it sneaks into your heater. ")
            type.type("You start the engine and blast the heat, but you aren't sure if the spider has died, or if it has a family nearby. This sucks.")
            self.lose_sanity(random.choice([1, 2]))  # Creature attack drains sanity
        self.add_status("Spider Bite")
        self.mark_day("Spider Bite")
        print("\n")


    def hungry_cockroach(self):
        random_choice = random.randrange(2)
        if (random_choice != 0) or not self.has_danger("Cockroach"):
            self.day_event()
            return

        type.type("You wake up to the sound of a hiss in your pile of money. ")
        type.type("You jump up to check your cash, and you find a cockroach eating away at your cash. ")
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the cockroach. ")
            type.type("A cloud of white liquid covers the cockroach, and you watch as it slows down, twitches, and dies. ")
            type.type("Hopefully, that's the end of your cockroach problems.")
        else:
            type.type("You attempt to swat it with your hand, but it falls under your car seat. ")
            type.type("You stick your head under the seat, but you aren't sure where the cockroach went, or if it has a family nearby. This is terrible.")
        print("\n")
        type.type("The cockroach ate through some of your money. ")
        losses = int(self.get_balance() * (random.randint(10, 40)/100))
        type.type("You lost " + green(bright("${:,}".format(losses))) + ".")
        self.change_balance(-losses)

    # One-Time
    def lone_cowboy(self):
        if self.has_met("Cowboy"):
            self.day_event()
            return

        self.meet("Cowboy")
        type.type("You wake up to the sounds trotting, and distant whistling. You sit up, and through your windshield, you see a man wearing a full cowboy suit, with matching black hat and boots, and a short brown beard. ")
        type.type("He's riding a magnificent horse, muscular, but nimble, each step powerful, but precise. The man reaches your window, and in a deep southern accent, he begins to talk to you.")
        print("\n")
        type.type(open_quote("Howdy, partner! The name's Jameson. Davey Jameson. I happen to notice you were admiring my steed. He's a beauty, isn't he. You see, it's common courtesy when a cowboy rides by, "))
        type.type(close_quote("to give their mighty steed a carrot, as a way to express your gratitude for their hardwork and commitment to the job."))
        print("\n")
        type.type(quote("You my friend, you are carrotless. That's quite a disrespectful showing towards my steed. My, my, this can't do at all. What if another cowboy comes by, you're just gonna disrespect their steed, too? Tell you what, I happen to have one spare carrot in my pouch. Take this, and be ready. You never know when a cowboy's gonna come trotting by."))
        print("\n")
        self.add_item("Carrot")
        type.type("Davey Jameson hands you his " + bright(magenta("Carrot")) + ", and smiles.")
        print("\n")
        type.type(quote("See, with this carrot in your possession, you're ready for anytime a cowboy strolls on down this road. Just give their steed a carrot, and they'll be very grateful."))
        print("\n")
        type.type("And with that, Jameson reins his horse high into the air, gives you a yee-haw, then dashes off down the road.")
        print("\n")

    def whats_my_name(self):
        if not self.__name == None:
            self.day_event()
            return
        
        type.type("You wake up to the sound of sneakers scratching against the concrete. As you sit up from your seat, you notice a little girl, with blonde hair and pigtails, jump roping towards you.")
        print("\n")
        type.type(space_quote("Howdy stranger! My name's Suzy! Do you like my name?"))
        answer = ask.yes_or_no("\"What was that?\" ")
        if answer == "yes":
            type.type(quote("Thanks! My mom gave it to me, before she disappeared. Who knows where she ran off to!"))
        elif answer == "no":
            type.type(quote("Wow! That's not very nice of you. You're rude, stranger."))

        print("\n")
        type.type(space_quote("Hey, what's your name, anyways?"))
        while True:
            name = str(input())
            type.type(space_quote("So your name is " + name + "?"))
            answer = ask.yes_or_no(space_quote("What was that?"))
            if answer == "yes":
                self.__name = name
                type.type("\"" + name + "...I like that name! Hello, " + name + "!\"")
                print("\n")
                type.type(space_quote("Well, " + name + ", I've got to get going now. Wouldn't want the bears to eat me!"))
                type.type("And with that, Suzy, without missing a beat, continues to jump rope down the street.")
                print("\n")
                break
            elif answer == "no":
                type.type(quote("So you lied to me? You're a liar, stranger!"))
                print("\n")
                type.type(space_quote("Come on, tell me your real name!"))
    

    def interrogation(self):
        if self.has_met("Interrogator"):
            self.day_event()
            return
    
        self.meet("Interrogator")
        self.add_danger("Further Interrogation")
        self.lose_sanity(random.choice([1, 2]))  # Harassment drains sanity
        type.type("You wake up, and through your windshield, you see a car parked right in front of you. Confused, and dazed, you sit up. As you open the door and get out of your car, you notice a man, in a bright red suit, peering into your trunk.")
        print("\n")
        type.type("The man sees you, and walks up to you.")
        print("\n")
        type.type(quote("You. You're awake. Good. You know that you aren't supposed to be here? This isn't a spot for people to live. This is a road for people to drive. I hope you know this."))
        print("\n")
        type.type(space_quote("Do you know this?"))
        answer = ask.yes_or_no(space_quote("Do you? Know this?"))
        if answer == "yes":
            type.type(quote("So you do know this. Then why do you live here? You shouldn't. It's not right, man. I'd suggest you stop living here. Maybe live somewhere else instead. Just not here."))
            print()
        elif answer == "no":
            type.type(quote("You don't know this? How don't you know this? It's super obvious stuff, man. People don't live at places where they're not supposed to, and that's exactly what you're doing right now. I'd suggest you stop it, right this instant."))
            print()
        type.type("After the man tells you this, he looks up, and stares at the sun. And after about 20 seconds, he rubs his eyes, walks back to his car, and drives off.")
        print("\n")
        return

    # ==========================================
    # NEW POOR DAY EVENTS - Everytime
    # ==========================================
    
    def morning_stretch(self):
        # Everytime - simple healing event with variants
        variant = random.randrange(4)
        if variant == 0:
            type.type("You wake up with a kink in your neck from sleeping at a weird angle. You step out of the car and do some stretches, cracking joints you didn't know you had.")
            print("\n")
            type.type("After a few minutes of yoga poses you half-remember from a video you watched once, you actually feel... pretty good?")
        elif variant == 1:
            type.type("The morning sun beckons you outside. You do some jumping jacks, touch your toes (or at least try to), and take a few deep breaths of fresh air.")
            print("\n")
            type.type("Your body thanks you for remembering it exists.")
        elif variant == 2:
            type.type("You tumble out of the car, groaning. Everything hurts. You're not as young as you used to be.")
            print("\n")
            type.type("But after some careful stretching and a short walk, the aches start to fade. Not bad.")
        else:
            type.type("An old man jogs past your car and waves. Inspired (or shamed), you get out and do some light exercise.")
            print("\n")
            type.type("The old man laps you twice before you give up, but hey, you tried.")
        print("\n")
        self.heal(random.choice([3, 5, 8]))

    def ant_invasion(self):
        # Everytime - potential danger event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You wake up to an itching sensation all over your legs. Ants! Dozens of them, crawling up from the floor of your car!")
            print("\n")
            type.type("You leap out and spend the next hour brushing them off and stomping around like a maniac.")
        elif variant == 1:
            type.type("Something tickles your ear. You reach up and feel... legs. Many legs. You look at your hand-ants.")
            print("\n")
            type.type("Your screaming probably woke up everyone within a mile radius.")
        else:
            type.type("A line of ants marches across your dashboard with military precision. They seem to be heading for your snack stash.")
            print("\n")
            type.type("You watch in horror as they disassemble a crumb and carry it away. Impressive, but concerning.")
        print("\n")
        if self.has_item("Pest Control"):
            type.type("You grab your " + bright(magenta("Pest Control")) + " and wage chemical warfare on the tiny invaders.")
            self.kill_pests()
            type.type("Victory is yours. For now.")
        else:
            type.type("Without pest control, you just have to shake them out and hope they don't come back.")
            self.add_danger("Ants")
        print("\n")

    def bird_droppings(self):
        # Everytime - comedic event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You wake up to a SPLAT on your windshield. A pigeon sits on a branch above, looking very satisfied with itself.")
            print("\n")
            type.type("Great. Just great.")
        elif variant == 1:
            type.type("Your entire windshield is covered in bird droppings. Like, COVERED. Did a whole flock decide your car was the designated bathroom?")
            print("\n")
            type.type("This is going to take forever to clean.")
        else:
            type.type("A crow lands on your hood and stares at you through the windshield. It tilts its head. Then, maintaining eye contact, it poops.")
            print("\n")
            type.type("You've been disrespected by a bird. A new low.")
        print("\n")
        chance = random.randrange(10)
        if chance == 0:
            type.type("Wait... is that a lottery ticket stuck in the mess? Someone must have thrown it out their window.")
            print("\n")
            type.type("You carefully extract it, wipe it off, and check the numbers... ")
            win = random.randint(20, 100)
            type.type("It's a " + green(bright("$" + str(win))) + " winner! Gross, but lucky!")
            self.change_balance(win)
        print("\n")

    def flat_tire(self):
        # Everytime - negative event with variants
        if self.has_met("Flat Tire Today"):
            self.day_event()
            return
        self.meet("Flat Tire Today")
        
        variant = random.randrange(3)
        if variant == 0:
            type.type("You step out of your car and immediately notice something wrong. Your front tire is completely flat.")
            print("\n")
            type.type("Must've run over something sharp. Just your luck.")
        elif variant == 1:
            type.type("The car is listing to one side. Upon inspection: flat tire. Very flat. Like, pancake flat.")
            print("\n")
            type.type("You kick it in frustration, which doesn't help at all.")
        else:
            type.type("A hissing sound wakes you up. It's not a snake-it's your tire, slowly deflating before your eyes.")
            print("\n")
            type.type("You watch helplessly as your wheel becomes a sad rubber puddle.")
        print("\n")
        if self.has_item("Spare Tire"):
            type.type("Good thing you have a " + bright(magenta("Spare Tire")) + "! You spend the next hour changing it out.")
            self.use_item("Spare Tire")
            type.type("Not how you wanted to start the day, but at least you're not stranded.")
        else:
            type.type("Without a spare, you're going to have to walk to get this fixed. That'll cost time and money.")
            self.add_travel_restriction("Flat Tire")
            self.change_balance(-random.randint(50, 150))
        print("\n")

    def mysterious_note(self):
        # Everytime - cryptic event
        variant = random.randrange(4)
        if variant == 0:
            type.type("There's a note tucked under your windshield wiper. It reads: " + quote("I know what you did."))
            print("\n")
            type.type("What did you do? You don't even know. This is unsettling.")
        elif variant == 1:
            type.type("You find a crumpled note on your dashboard. In messy handwriting: " + quote("The dealer always wins. Always."))
            print("\n")
            type.type("A chill runs down your spine.")
        elif variant == 2:
            type.type("A small piece of paper is stuck to your window. It says: " + quote("You're being watched."))
            print("\n")
            type.type("You look around nervously. No one's there. At least, no one you can see.")
        else:
            type.type("There's a note on your seat that definitely wasn't there last night. It reads: " + quote("Wake up."))
            print("\n")
            type.type("You ARE awake. Aren't you?")
        print("\n")

    def radio_static(self):
        # Everytime - atmospheric event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You turn on the radio for some company, but all you get is static. Then, for just a moment, you hear a voice.")
            print("\n")
            type.type(quote("...don't go to the casino...") + " it whispers, before dissolving back into white noise.")
            print("\n")
            type.type("You turn the radio off. Probably just interference. Probably.")
        elif variant == 1:
            type.type("The radio crackles to life on its own. You don't remember turning it on.")
            print("\n")
            type.type("A song plays-one you almost recognize, but not quite. The lyrics are backwards, or maybe in another language.")
            print("\n")
            type.type("You yank the power cord. The music keeps playing for three seconds before stopping.")
        else:
            type.type("You fiddle with the radio dial, searching for anything other than static. Finally, a clear station!")
            print("\n")
            type.type("It's playing your least favorite song. Of course it is.")
            print("\n")
            type.type("You turn it off in disgust.")
        print("\n")

    # ==========================================
    # NEW POOR DAY EVENTS - Conditional
    # ==========================================
    
    def ant_bite(self):
        # Conditional - requires Ant danger
        if not self.has_danger("Ants"):
            self.day_event()
            return
        
        type.type("You wake up COVERED in angry red welts. The ants that invaded your car yesterday? They didn't leave. They multiplied.")
        print("\n")
        type.type("And they're BITING.")
        print("\n")
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + bright(magenta("Pest Control")) + " and go absolutely nuclear on the tiny terrors.")
            type.type(" Victory at last-but the bites still sting.")
            self.hurt(10)
        else:
            type.type("Without pest control, you can only flee the car and brush them off. They'll probably be back.")
            self.hurt(20)
        self.add_status("Ant Bites")
        self.mark_day("Ant Bites")
        print("\n")

    # ==========================================
    # NEW POOR DAY EVENTS - One-Time
    # ==========================================
    
    def old_man_jenkins(self):
        # One-Time - quirky NPC
        if self.has_met("Old Man Jenkins"):
            self.day_event()
            return
        
        self.meet("Old Man Jenkins")
        type.type("You wake up to someone knocking on your window with a cane. An ancient man peers in at you, his face like a crumpled paper bag.")
        print("\n")
        type.type(quote("You there! Young person! I've been walking this road for sixty years and I've never seen someone sleeping in their CAR before! What's the world coming to?"))
        print("\n")
        type.type("You try to explain your situation, but he just waves his cane dismissively.")
        print("\n")
        type.type(quote("In my day, we slept in DITCHES like RESPECTABLE vagrants! Cars! Bah! Too fancy! Back in the Depression, we didn't even have wheels-we just rolled places with our own two legs!"))
        print("\n")
        type.type("He rants for a solid ten minutes about the good old days of homelessness.")
        print("\n")
        type.type(quote("Here, take this. You'll need it more than me. I'm 97 years old and I've never spent a dime I didn't have to."))
        print("\n")
        gift = random.randint(25, 75)
        type.type("Old Man Jenkins hands you " + green(bright("$" + str(gift))) + " in coins, mostly pennies and nickels.")
        self.change_balance(gift)
        print("\n")
        type.type("And with that, he hobbles off down the road, still muttering about kids these days.")
        print("\n")

    def the_mime(self):
        # One-Time - weird NPC
        if self.has_met("Mime"):
            self.day_event()
            return
        
        self.meet("Mime")
        type.type("You step out of your car and nearly collide with... a mime? Full striped shirt, white face paint, the whole nine yards.")
        print("\n")
        type.type("The mime stares at you. You stare back.")
        print("\n")
        type.type("Without a word (obviously), the mime begins to act out a scene. He's pretending to be trapped in a box. Classic.")
        print("\n")
        type.type("Then he mimes... crying? Counting money? Losing at cards?")
        print("\n")
        type.type("Wait. Is he acting out YOUR life?")
        print("\n")
        type.type("The mime finishes with a dramatic death scene, tongue out and everything, then springs back up and takes a bow.")
        print("\n")
        answer = ask.yes_or_no("Do you applaud? ")
        if answer == "yes":
            type.type("The mime beams and hands you an invisible flower. You pretend to smell it.")
            print("\n")
            type.type("He then gives you a very real " + green(bright("$20")) + " bill from his pocket, waves, and walks away into an invisible wall.")
            self.change_balance(20)
            self.heal(5)
        else:
            type.type("The mime looks devastated. He mimes a single tear rolling down his cheek, then slowly backs away, never breaking eye contact.")
            print("\n")
            type.type("You feel kind of bad about that.")
        print("\n")

    # ==========================================
    # SECRET EVENTS - POOR TIER
    # ==========================================
    
    def midnight_visitor(self):
        # SECRET - Only triggers at exactly $666 balance
        if self.get_balance() != 666:
            self.day_event()
            return
        
        self.lose_sanity(random.choice([3, 4, 5]))  # Supernatural encounter severely drains sanity
        type.type("You wake up in the dead of night, though you swear it was morning when you closed your eyes. The air is thick and cold.")
        print("\n")
        type.type("A figure stands outside your window. Tall. Thin. Its face is in shadow, but you can see its smile-too wide, too many teeth.")
        print("\n")
        type.type(red(quote("Six hundred and sixty-six dollars. How fitting.")))
        print("\n")
        type.type("You blink, and the figure is inside your car, sitting in the passenger seat.")
        print("\n")
        type.type(red(quote("I've been watching you, gambler. I like your style. Tell you what-I'll make you an offer.")))
        print("\n")
        type.type(quote("Double or nothing. I flip a coin. Heads, I double your money. Tails... well. Let's just say you'll owe me."))
        print("\n")
        answer = ask.yes_or_no("Accept the devil's offer? ")
        if answer == "yes":
            if random.randrange(2) == 0:
                type.type(red("The figure flips a coin that seems to be made of pure darkness. It spins impossibly slow..."))
                print("\n")
                type.type(green(bright("HEADS.")))
                print("\n")
                type.type(red(quote("Lucky you. This time.")))
                print("\n")
                type.type("You blink again, and the figure is gone. But your money pile has doubled.")
                self.change_balance(666)
            else:
                type.type(red("The figure flips a coin that seems to be made of pure darkness. It spins impossibly slow..."))
                print("\n")
                type.type(red(bright("TAILS.")))
                print("\n")
                type.type(red(quote("A deal's a deal. Don't worry-I won't collect today. But I WILL collect. Eventually.")))
                print("\n")
                type.type("You blink, and the figure is gone. Your money is untouched, but you feel like you've lost something far more valuable.")
                self.add_danger("Devil's Debt")
                self.lose_sanity(random.choice([2, 3]))  # Losing to devil further drains sanity
        else:
            type.type("The figure laughs, a sound like breaking glass.")
            print("\n")
            type.type(red(quote("Wise. Or cowardly. Time will tell which.")))
            print("\n")
            type.type("When you blink, the figure is gone. The sun is rising. Was it a dream?")
        print("\n")
        type.type(yellow(bright("Something about that encounter will stay with you forever.")))
        print("\n")

    def perfect_hand(self):
        # SECRET - Only triggers if you have EXACTLY 21 dollars
        if self.get_balance() != 21:
            self.day_event()
            return
        
        type.type("You count your money this morning and realize you have exactly " + green(bright("$21")) + ". Blackjack.")
        print("\n")
        type.type("As if on cue, a single playing card flutters down from nowhere and lands in your lap. The Ace of Spades.")
        print("\n")
        type.type("You look up. There's no one there. No birds, no trees. Just clear sky.")
        print("\n")
        type.type("On the back of the card, someone has written: " + quote("The universe deals you a winner."))
        print("\n")
        type.type(yellow(bright("You feel inexplicably lucky today.")))
        self.add_status("Lucky")
        self.add_item("Ace of Spades")
        print("\n")

    # Cheap Day Events (1,000 - 10,000)
    # Everytime
    def sun_visor_bills(self):
        # Alt dialogue for repeated event + rare variant
        rare_chance = random.randrange(100)
        
        if rare_chance < 5:  # 5% RARE VARIANT - The Jackpot Visor
            type.type("You flip down the sun visor to block the morning sun and-")
            print("\n")
            type.type("HOLY SHIT.")
            print("\n")
            type.type("Bills cascade down like a waterfall. Twenties, fifties, even some hundreds, all stuffed into the visor like it was a makeshift piggy bank.")
            print("\n")
            type.type("Did you do this? Did past-you do this and forget? Is this some kind of divine intervention?")
            print("\n")
            bill = random.randint(800, 2000)
            type.type("After counting it all, you find " + green(bright("${:,}".format(bill))) + " dollars!")
            print("\n")
            type.type(yellow("You have no idea where this came from, but you're not complaining."))
            self.change_balance(bill)
            print("\n")
            return
        
        # Normal variants
        variant = random.randrange(3)
        if variant == 0:
            type.type("You wake up in the front seat, dripping in sweat. ")
            type.type("As the sun shines through the car window, you notice a few bright green bills above you, peeking out of the sun visor. How long have they been there? ")
        elif variant == 1:
            type.type("The sun glares through your windshield, and you reach for the visor. As you flip it down, something flutters into your lap. ")
            type.type("Money! You check the visor again-there's more. ")
        else:
            type.type("You sit up, rubbing your eyes, and accidentally bump the sun visor. Cash rains down on you. ")
            type.type("You forgot you hid emergency funds up there! Past-you was actually smart for once. ")
        print("\n")
        bill = random.choice([3, 15, 30, 60, 150, 300])
        type.type("That's another " + green(bright("$" + str(bill))) + " dollars.")
        self.change_balance(bill)

    def strong_winds(self):
        # Alt dialogue for repeated event + rare variant
        rare_chance = random.randrange(100)
        
        if rare_chance < 3:  # 3% RARE VARIANT - Wind Brings Gifts
            type.type("You wake up to howling wind rattling your wagon. Branches are falling, leaves are flying, and-")
            print("\n")
            type.type("THUNK.")
            print("\n")
            type.type("Something lands on your roof. Then another thunk. And another.")
            print("\n")
            type.type("You cautiously step outside, bracing against the gusts. On the ground around your car... money. Bills, blowing in from god-knows-where, plastering themselves against your vehicle.")
            print("\n")
            type.type("You spend the next hour chasing down wind-blown cash like the world's most chaotic Easter egg hunt.")
            print("\n")
            windfall = random.randint(300, 800)
            type.type("In the end, you manage to snag " + green(bright("${:,}".format(windfall))) + "!")
            self.change_balance(windfall)
            self.add_travel_restriction("Wind")
            print("\n")
            return
        
        # Normal variants
        variant = random.randrange(3)
        if variant == 0:
            type.type("You wake up to a loud snap above you, followed by a massive branch crashing down from the treetops and into the street. The wind echoes throughout the trees around you, and many of them look to be on the verge of falling.")
            print("\n")
            type.type("With the weather being this bad, you make the executive decision to just chill in the wagon for the day.")
        elif variant == 1:
            type.type("Your car rocks violently, waking you from a deep sleep. Outside, it's chaos-trees bending, debris flying, the sky an angry gray.")
            print("\n")
            type.type("Yeah, no. You're not going out in that. Time to hunker down.")
        else:
            type.type("The sound is deafening-wind screaming past your windows, your wagon shaking like it might flip over.")
            print("\n")
            type.type("A trash can tumbles past your windshield, followed by what looks like someone's lawn chair. ")
            print("\n")
            type.type("Today is officially an 'inside day.'")
        self.add_travel_restriction("Wind")
        print("\n")

    # Conditional
    def got_a_cold(self):
        if self.has_status("Cold"):
            self.day_event()
            return
        
        type.type("You wake up to a sneeze, followed by your nose running, droplets falling down from your chin and onto your shirt. Damn, must be a cold.")
        self.add_status("Cold")
        self.mark_day("Cold")
        print("\n")

    # ==========================================
    # NEW CHEAP DAY EVENTS - Everytime
    # ==========================================
    
    def morning_fog(self):
        # Everytime - atmospheric with variants
        variant = random.randrange(4)
        if variant == 0:
            type.type("You wake up surrounded by fog so thick you can barely see your hood. The world has been swallowed by white.")
            print("\n")
            type.type("You wait an hour for it to clear. Two hours. Finally, around noon, you can see the road again.")
        elif variant == 1:
            type.type("The fog this morning is eerie. Shapes seem to move in it-people? Animals? You can't tell.")
            print("\n")
            type.type("By the time the fog lifts, you're convinced you saw at least three ghosts. Or maybe just trees. Hopefully trees.")
        elif variant == 2:
            type.type("A heavy mist blankets everything. You step outside and immediately lose sight of your car.")
            print("\n")
            type.type("After ten minutes of wandering in circles, you find it again. That was embarrassing.")
        else:
            type.type("The fog is so dense this morning that you walk face-first into your own side mirror.")
            print("\n")
            type.type("Ow.")
            self.hurt(5)
        print("\n")

    def car_wont_start(self):
        # Everytime - potential restriction event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You turn the key and... nothing. Click click click. The engine won't catch.")
            print("\n")
            type.type("Dead battery. Great.")
        elif variant == 1:
            type.type("The engine makes a sound like a dying whale when you try to start it. Then silence.")
            print("\n")
            type.type("Something's definitely wrong under the hood.")
        else:
            type.type("Your car starts, sputters, coughs, and dies. It sounds like it's given up on life. You relate.")
            print("\n")
        
        if random.randrange(3) == 0:
            type.type("After some jiggling and praying, it starts back up! Crisis averted.")
        else:
            type.type("Looks like you're not driving anywhere until this gets fixed.")
            self.add_travel_restriction("Car Trouble")
            if self.has_met("Tom"):
                type.type("Maybe Tom can help with this...")
        print("\n")

    def raccoon_raid(self):
        # Everytime - creature event with variants
        rare_chance = random.randrange(100)
        
        if rare_chance < 5:  # 5% RARE VARIANT - Raccoon Gang
            type.type("You wake up to your car being SURROUNDED by raccoons. Not one or two. DOZENS.")
            print("\n")
            type.type("They're organized. One stands on your hood, clearly the leader. It chatters at you-a demand, not a greeting.")
            print("\n")
            type.type("The Raccoon Mafia wants tribute.")
            print("\n")
            tribute = random.randint(100, 300)
            type.type("You reluctantly throw " + green(bright("${:,}".format(tribute))) + " out the window. The leader inspects it, nods, and the whole gang scurries away.")
            self.change_balance(-tribute)
            print("\n")
            type.type(yellow("You've made some interesting enemies today."))
            print("\n")
            return
        
        variant = random.randrange(3)
        if variant == 0:
            type.type("A fat raccoon is sitting on your hood, eating what appears to be your snack stash. It stares at you defiantly.")
            print("\n")
            type.type("You bang on the window. It doesn't care.")
        elif variant == 1:
            type.type("Scratch marks all over your trunk. Something tried to break in last night. Raccoon prints everywhere.")
            print("\n")
            type.type("Those little bandits!")
        else:
            type.type("You open your door and a raccoon FALLS OUT. It was hiding IN YOUR CAR. How?! WHEN?!")
            print("\n")
            type.type("It hisses at you, grabs something shiny, and bolts.")
            loss = random.randint(20, 80)
            type.type("It stole " + green(bright("$" + str(loss))) + " from you!")
            self.change_balance(-loss)
        print("\n")

    def beautiful_sunrise(self):
        # Everytime - purely positive event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You wake up just in time to catch the sunrise. Pink and gold paint the sky, and for a moment, everything feels... okay.")
            print("\n")
            type.type("Sometimes you have to appreciate the little things.")
        elif variant == 1:
            type.type("The dawn light streams through your windshield, warm and golden. Birds are singing. The air smells fresh.")
            print("\n")
            type.type("Today might actually be a good day.")
        else:
            type.type("You watch the sun come up over the hills, painting everything in shades of orange and red.")
            print("\n")
            type.type("It's beautiful enough to make you forget, just for a moment, that you live in a car.")
        print("\n")
        self.heal(random.choice([5, 10, 15]))
        self.restore_sanity(random.choice([1, 2, 3]))  # Restores sanity

    # ==========================================
    # ITEM-USING EVENTS - Items get consumed
    # ==========================================
    
    def mosquito_swarm(self):
        # Bug Spray can save you from damage
        type.type("The buzzing starts at dusk. First one mosquito, then ten, then what feels like a thousand.")
        print("\n")
        type.type("They swarm your car, slipping through every crack and crevice.")
        print("\n")
        
        if self.has_item("Bug Spray"):
            type.type("But wait - you have " + magenta(bright("Bug Spray")) + "!")
            print("\n")
            type.type("You grab the can and spray yourself down liberally. The mosquitoes keep their distance, buzzing angrily but unable to bite.")
            print("\n")
            type.type("The spray is used up, but you're bite-free.")
            self.use_item("Bug Spray")
            print("\n")
        else:
            type.type("You spend the night swatting and scratching. By morning, you're covered in itchy welts.")
            print("\n")
            self.hurt(random.randint(10, 20))
            type.type("Bug spray would have been really helpful right about now.")
        print("\n")

    def scorching_sun(self):
        # Cheap Sunscreen / Sunglasses can help
        type.type("It's hot. Really hot. The sun beats down mercilessly, and your car becomes an oven.")
        print("\n")
        
        if self.has_item("Cheap Sunscreen"):
            type.type("Good thing you have " + magenta(bright("Cheap Sunscreen")) + "!")
            print("\n")
            type.type("You slather it on and step outside. It's still hot, but at least you won't turn into a lobster.")
            print("\n")
            type.type("The tiny bottle is empty now, but worth it.")
            self.use_item("Cheap Sunscreen")
        elif self.has_item("Umbrella"):
            type.type("You grab your " + magenta(bright("Umbrella")) + " and use it as a sun shade.")
            print("\n")
            type.type("It provides some relief from the blazing sun.")
            self.hurt(5)
        else:
            type.type("You try to stay in the shade, but there's no escaping this heat.")
            print("\n")
            type.type("By the end of the day, your skin is red and painful.")
            self.hurt(random.randint(15, 25))
            type.type("Sunscreen would have prevented this.")
        print("\n")

    def sudden_downpour(self):
        # Umbrella or Plastic Poncho prevents damage/getting sick
        type.type("The sky opens up without warning. Rain hammers down so hard you can barely hear yourself think.")
        print("\n")
        
        if self.has_item("Umbrella"):
            type.type("You grab your " + magenta(bright("Umbrella")) + " and step out, staying relatively dry.")
            print("\n")
            type.type("The storm passes after an hour, and you're no worse for wear.")
        elif self.has_item("Plastic Poncho"):
            type.type("You pull out your " + magenta(bright("Plastic Poncho")) + " and throw it on!")
            print("\n")
            type.type("It crinkles loudly with every movement, but it keeps you dry.")
            print("\n")
            type.type("By the time the rain stops, the cheap poncho has torn in three places. Time to toss it.")
            self.use_item("Plastic Poncho")
        else:
            type.type("You get soaked to the bone. The chill seeps into you.")
            print("\n")
            self.hurt(10)
            if random.randrange(3) == 0:
                type.type("You feel a cold coming on...")
                self.add_status("Cold")
                self.mark_day("Cold")
        print("\n")

    def freezing_night(self):
        # Hand Warmers can help survive
        type.type("The temperature plummets. Frost forms on your windshield, and you can see your breath inside the car.")
        print("\n")
        
        if self.has_item("Hand Warmers"):
            type.type("You crack open your " + magenta(bright("Hand Warmers")) + " and hold them close.")
            print("\n")
            type.type("The chemical heat spreads through your fingers, your hands, your whole body. Warmth.")
            print("\n")
            type.type("You survive the night comfortably. The warmers are spent by morning.")
            self.use_item("Hand Warmers")
        elif self.has_fire_source():
            type.type("You manage to generate some warmth with what you have. It's not comfortable, but you survive.")
            self.hurt(5)
        else:
            type.type("You shiver through the entire night, curled up in a ball, teeth chattering.")
            print("\n")
            self.hurt(random.randint(15, 25))
            if random.randrange(4) == 0:
                type.type("You feel a cold coming on...")
                self.add_status("Cold")
                self.mark_day("Cold")
        print("\n")

    def car_smell(self):
        # Air Freshener removes bad smell status
        type.type("Something in your car STINKS. You can't tell if it's the old food, the musty seats, or just... you.")
        print("\n")
        
        if self.has_item("Air Freshener"):
            type.type("You hang up your " + magenta(bright("Air Freshener")) + " and take a deep breath.")
            print("\n")
            type.type("Ahhh. Pine fresh. Much better.")
            print("\n")
            type.type("The freshener will fade over time, but for now, it's a major improvement.")
            self.use_item("Air Freshener")
            self.restore_sanity(3)
        else:
            type.type("You try to air it out by opening the windows, but the smell lingers.")
            print("\n")
            type.type("Living in this stench is demoralizing.")
            self.lose_sanity(random.randint(2, 4))
        print("\n")

    def roadside_breakdown(self):
        # Road Flares help get assistance
        type.type("Your car makes a horrible grinding noise and coasts to a stop on the side of the road. This is bad.")
        print("\n")
        
        if self.has_item("Road Flares"):
            type.type("You grab your " + magenta(bright("Road Flares")) + " and set them up behind your car.")
            print("\n")
            type.type("The bright red flames are visible for miles. Within an hour, a passing truck stops to help.")
            print("\n")
            type.type(quote("Saw your flares from way back. Smart thinking! Let me take a look..."))
            print("\n")
            type.type("The trucker helps you get the car started again. The flares are spent, but crisis averted.")
            self.use_item("Road Flares")
        elif self.has_item("Flashlight"):
            type.type("You wave your " + magenta(bright("Flashlight")) + " at passing cars. After an hour, someone finally stops.")
            print("\n")
            type.type("They help jumpstart your car. It could have been worse.")
            self.add_travel_restriction("Car Trouble")
        else:
            type.type("You sit there for hours, trying to flag down help. Most cars just speed past.")
            print("\n")
            type.type("Finally, by nightfall, a tow truck comes. But it costs you.")
            tow_cost = random.randint(100, 200)
            type.type("You pay " + green(bright("${:,}".format(tow_cost))) + " for the tow.")
            self.change_balance(-tow_cost)
            self.add_travel_restriction("Car Trouble")
        print("\n")

    def broken_belonging(self):
        # Super Glue or Duct Tape can fix things
        type.type("You hear a crack. One of your belongings has broken - a part snapped clean off.")
        print("\n")
        
        if self.has_item("Super Glue"):
            type.type("But you have " + magenta(bright("Super Glue")) + "!")
            print("\n")
            type.type("A few drops, some careful pressing, and... good as new. Almost.")
            print("\n")
            type.type("The glue tube is empty now, but at least you saved your stuff.")
            self.use_item("Super Glue")
        elif self.has_item("Duct Tape"):
            type.type("Nothing a little " + magenta(bright("Duct Tape")) + " can't fix!")
            print("\n")
            type.type("It's not pretty, but it holds. Duct tape: the universal solution.")
            print("\n")
            type.type("You used the last of the roll, but hey, it worked.")
            self.use_item("Duct Tape")
        else:
            type.type("Without anything to fix it, you just have to accept the loss.")
            print("\n")
            type.type("Sometimes things just break and stay broken.")
            self.lose_sanity(2)
        print("\n")

    def social_encounter(self):
        # Breath Mints or Expensive Cologne help with social situations
        type.type("Someone important-looking approaches your car. They seem friendly, but you're suddenly aware of... yourself.")
        print("\n")
        type.type("When's the last time you showered? How's your breath?")
        print("\n")
        
        if self.has_item("Breath Mints"):
            type.type("You quickly pop a " + magenta(bright("Breath Mint")) + " before they get close.")
            print("\n")
            type.type("Minty fresh! You greet them with confidence.")
            print("\n")
            type.type("They turn out to be a philanthropist who gives you " + green(bright("$50")) + " for being so friendly.")
            self.change_balance(50)
            self.use_item("Breath Mints")
        elif self.has_item("Expensive Cologne"):
            type.type("You spritz some " + magenta(bright("Expensive Cologne")) + " on yourself.")
            print("\n")
            type.type("Now you smell like money. Fake it till you make it.")
            print("\n")
            type.type("They're impressed by your style and give you " + green(bright("$100")) + " along with their business card.")
            self.change_balance(100)
            self.use_item("Expensive Cologne")
        else:
            type.type("You try to be friendly, but they wrinkle their nose and quickly make an excuse to leave.")
            print("\n")
            type.type("That was humiliating.")
            self.lose_sanity(3)
        print("\n")

    def important_document(self):
        # Fancy Pen makes a difference
        type.type("You find a form that needs to be filled out. Something important - could be worth money.")
        print("\n")
        type.type("But you need to sign it to make it official.")
        print("\n")
        
        if self.has_item("Fancy Pen"):
            type.type("You pull out your " + magenta(bright("Fancy Pen")) + " and sign with a flourish.")
            print("\n")
            type.type("The signature looks professional. Important. Legitimate.")
            print("\n")
            reward = random.randint(100, 300)
            type.type("The form turns out to be valid, and you receive " + green(bright("${:,}".format(reward))) + "!")
            self.change_balance(reward)
            # Pen doesn't get consumed - it's reusable
        else:
            type.type("You scrounge around for something to write with. An old crayon? A stubby pencil?")
            print("\n")
            type.type("Your signature looks like a child wrote it. The form is rejected.")
            print("\n")
            type.type("Opportunity lost.")
        print("\n")

    def caught_fishing(self):
        # Fishing Line lets you catch fish
        type.type("You park near a river. The water is clear, and you can see fish swimming lazily beneath the surface.")
        print("\n")
        
        if self.has_item("Fishing Line"):
            type.type("You have " + magenta(bright("Fishing Line")) + "! Time to try your luck.")
            print("\n")
            type.type("You fashion a makeshift rod from a branch, attach the line, and cast out.")
            print("\n")
            if random.randrange(3) == 0:
                type.type("After an hour of waiting... nothing. The fish aren't biting today.")
                print("\n")
                type.type("The line got tangled and snapped. Frustrating.")
            else:
                type.type("You feel a tug! You pull hard, and land a decent-sized bass!")
                print("\n")
                type.type("Fresh fish for dinner. You feel accomplished.")
                self.heal(20)
                self.restore_sanity(3)
            self.use_item("Fishing Line")
        else:
            type.type("You watch the fish swim by, tantalizingly close. If only you had something to catch them with...")
            print("\n")
            type.type("Your stomach rumbles.")
        print("\n")

    def robbery_attempt(self):
        # Padlock protects your stuff
        type.type("You wake up in the middle of the night to someone trying to break into your car!")
        print("\n")
        
        if self.has_item("Padlock"):
            type.type("But you secured everything with your " + magenta(bright("Padlock")) + "!")
            print("\n")
            type.type("The thief struggles with it for a minute, then gives up and runs off.")
            print("\n")
            type.type("Close call. The padlock saved you.")
            # Padlock doesn't get consumed - it's protection
        elif self.has_item("Pocket Knife"):
            type.type("You grab your " + magenta(bright("Pocket Knife")) + " and brandish it!")
            print("\n")
            type.type(quote("Back off!"))
            print("\n")
            type.type("The thief sees the blade glinting and decides you're not worth the trouble. They bolt.")
        else:
            loss = random.randint(50, 200)
            type.type("Before you can react, they grab some of your stuff and run!")
            print("\n")
            type.type("You lost " + green(bright("${:,}".format(loss))) + " worth of cash!")
            self.change_balance(-loss)
        print("\n")

    def photo_opportunity(self):
        # Disposable Camera captures a moment
        type.type("Something incredible happens - a double rainbow, a deer and its fawn, the most beautiful sunset you've ever seen.")
        print("\n")
        
        if self.has_item("Disposable Camera"):
            type.type("You grab your " + magenta(bright("Disposable Camera")) + " and start snapping!")
            print("\n")
            type.type("Click. Click. Click. You capture the moment forever.")
            print("\n")
            type.type("When you develop these someday, they'll be worth remembering.")
            self.restore_sanity(5)
            if random.randrange(10) == 0:
                type.type("You got the last shot on the roll. Camera's done.")
                self.use_item("Disposable Camera")
        else:
            type.type("You try to memorize every detail. But memories fade.")
            print("\n")
            type.type("If only you had a camera...")
            self.restore_sanity(2)
        print("\n")

    def classy_encounter(self):
        # Leather Gloves, Silk Handkerchief, Gold Chain help impress
        type.type("A fancy car pulls up next to yours. The window rolls down, revealing someone in expensive clothes.")
        print("\n")
        type.type(quote("Excuse me, could you direct me to the casino?"))
        print("\n")
        
        has_class = (self.has_item("Leather Gloves") or self.has_item("Silk Handkerchief") or 
                     self.has_item("Gold Chain") or self.has_item("Antique Pocket Watch"))
        
        if has_class:
            if self.has_item("Silk Handkerchief"):
                type.type("You dab your brow with your " + magenta(bright("Silk Handkerchief")) + " in a refined manner.")
            elif self.has_item("Antique Pocket Watch"):
                type.type("You casually check your " + magenta(bright("Antique Pocket Watch")) + ".")
            elif self.has_item("Leather Gloves"):
                type.type("You adjust your " + magenta(bright("Leather Gloves")) + " with casual elegance.")
            else:
                type.type("Your " + magenta(bright("Gold Chain")) + " catches their eye.")
            print("\n")
            type.type("They look at you with newfound respect.")
            print("\n")
            type.type(quote("Ah, a person of taste! Here, for your trouble."))
            print("\n")
            tip = random.randint(100, 300)
            type.type("They hand you " + green(bright("${:,}".format(tip))) + " and drive off.")
            self.change_balance(tip)
        else:
            type.type("You point them in the right direction. They barely acknowledge you before driving off.")
            print("\n")
            type.type("Not even a thank you. Typical rich people.")
        print("\n")

    def wine_and_dine(self):
        # Vintage Wine or Silver Flask for special occasions
        if not self.has_item("Vintage Wine") and not self.has_item("Silver Flask"):
            self.day_event()
            return
        
        type.type("You meet someone interesting - another car-dweller, sharing stories around a small campfire.")
        print("\n")
        
        if self.has_item("Vintage Wine"):
            type.type("You pull out your " + magenta(bright("Vintage Wine")) + ".")
            print("\n")
            type.type(quote("1987? You've been holding onto this?"))
            print("\n")
            type.type("You share the bottle, swapping tales of better days and worse ones.")
            print("\n")
            type.type("By the time it's empty, you've made a real friend.")
            self.use_item("Vintage Wine")
            self.restore_sanity(10)
            self.heal(10)
        elif self.has_item("Silver Flask"):
            type.type("You offer a swig from your " + magenta(bright("Silver Flask")) + ".")
            print("\n")
            type.type("They accept gratefully. You share drinks and stories until the fire dies down.")
            self.restore_sanity(5)
        print("\n")

    def cigar_circle(self):
        # Fancy Cigars for bonding
        if not self.has_item("Fancy Cigars"):
            self.day_event()
            return
        
        type.type("You find a group of older men sitting outside a barbershop, talking politics and sports.")
        print("\n")
        type.type("One of them eyes you suspiciously. You're clearly not from around here.")
        print("\n")
        type.type("You pull out your " + magenta(bright("Fancy Cigars")) + " and offer them around.")
        print("\n")
        type.type(quote("Cuban? Well, well. Maybe you're alright after all."))
        print("\n")
        type.type("You spend the afternoon smoking and talking. They give you tips on where to park safely, where to find cheap food.")
        print("\n")
        type.type("Local knowledge is priceless.")
        self.use_item("Fancy Cigars")
        self.restore_sanity(5)
        self.heal(5)
        print("\n")

    def need_fire(self):
        # Lighter or Monogrammed Lighter or Road Flares starts fire
        type.type("You need fire. Desperately. Maybe to warm up, maybe to cook, maybe just to see.")
        print("\n")
        
        if self.has_item("Monogrammed Lighter"):
            type.type("You pull out your " + magenta(bright("Monogrammed Lighter")) + " and flick it open.")
            print("\n")
            type.type("Flame. Reliable, elegant flame. You get what you need done.")
            # Premium lighter doesn't run out
        elif self.has_item("Lighter"):
            type.type("You pull out your " + magenta(bright("Lighter")) + " and click it.")
            print("\n")
            if random.randrange(5) == 0:
                type.type("Click. Click. Click... it's out of fluid.")
                print("\n")
                type.type("Useless now.")
                self.use_item("Lighter")
            else:
                type.type("Flame. You get what you need done.")
        elif self.has_item("Road Flares"):
            type.type("You light one of your " + magenta(bright("Road Flares")) + ". It's overkill, but it works.")
            print("\n")
            type.type("The flare burns itself out. Not the most efficient use.")
            self.use_item("Road Flares")
        else:
            type.type("You have no way to make fire. You sit in the cold and dark.")
            self.hurt(10)
            self.lose_sanity(3)
        print("\n")

    def lucky_rabbit_encounter(self):
        # Lucky Rabbit Foot triggers
        if not self.has_item("Lucky Rabbit Foot"):
            self.day_event()
            return
        
        type.type("You're walking along when a rabbit hops across your path.")
        print("\n")
        type.type("It stops. Turns. Looks directly at you. Then at the purple " + magenta(bright("Lucky Rabbit Foot")) + " dangling from your pocket.")
        print("\n")
        type.type("For a long moment, you both stare.")
        print("\n")
        type.type("The rabbit makes a sound that might be a sigh, then hops away.")
        print("\n")
        type.type("You feel... guilty? But also lucky. Definitely lucky.")
        self.add_status("Lucky")
        print("\n")

    def penny_luck(self):
        # Lucky Penny effect
        if not self.has_item("Lucky Penny"):
            self.day_event()
            return
        
        type.type("You're about to step on a crack in the sidewalk when something makes you pause.")
        print("\n")
        type.type("You look down. Another penny, heads up, right next to the crack.")
        print("\n")
        type.type("You pick it up. Now you have two lucky pennies... but you can only carry one.")
        print("\n")
        type.type("You flip your old " + magenta(bright("Lucky Penny")) + " into a fountain as an offering to whatever luck gods exist.")
        print("\n")
        type.type("The new penny feels luckier. Is that possible?")
        self.add_status("Lucky")
        print("\n")

    def rubber_band_save(self):
        # Rubber Bands have a use
        if not self.has_item("Rubber Bands"):
            self.day_event()
            return
        
        type.type("Something's about to fall apart. A stack of papers. A bundle of bills. A bag that won't stay closed.")
        print("\n")
        type.type("You grab some " + magenta(bright("Rubber Bands")) + " from your stash.")
        print("\n")
        type.type("Snap. Snap. Snap. Everything's secured.")
        print("\n")
        type.type("Sometimes the simplest solutions are the best.")
        if random.randrange(5) == 0:
            type.type(" That was the last of them.")
            self.use_item("Rubber Bands")
        print("\n")

    # ==========================================
    # NEW CHEAP DAY EVENTS - Conditional
    # ==========================================
    
    def cold_gets_worse(self):
        # Conditional - requires Cold status
        if not self.has_status("Cold"):
            self.day_event()
            return
        
        if self.has_status("Flu"):
            self.day_event()
            return
        
        type.type("Your cold has gotten worse. Much worse. You're shivering, sweating, and your whole body aches.")
        print("\n")
        type.type("This isn't just a cold anymore. This is the flu.")
        print("\n")
        self.lose_status("Cold")
        self.add_status("Flu")
        self.mark_day("Flu")
        self.hurt(15)

    # ==========================================
    # NEW CHEAP DAY EVENTS - One-Time
    # ==========================================
    
    def ice_cream_truck(self):
        # One-Time - positive event
        if self.has_met("Ice Cream Man"):
            self.day_event()
            return
        
        self.meet("Ice Cream Man")
        type.type("Is that... music? That familiar jingle that haunts every childhood summer?")
        print("\n")
        type.type("An ice cream truck pulls up right next to your car. The driver, a heavyset man with a handlebar mustache, leans out the window.")
        print("\n")
        type.type(quote("You look like you could use some ice cream, friend! First one's on the house!"))
        print("\n")
        type.type("He hands you a rocket pop. You haven't had one since you were a kid.")
        print("\n")
        type.type("It tastes like summer. Like childhood. Like things were simpler.")
        print("\n")
        self.heal(15)
        type.type(quote("Keep your chin up! Life's too short not to have dessert!"))
        print("\n")
        type.type("The ice cream truck drives away, its jingle fading into the distance.")
        print("\n")

    def kid_on_bike(self):
        # One-Time - random NPC
        if self.has_met("Kid on Bike"):
            self.day_event()
            return
        
        self.meet("Kid on Bike")
        type.type("A kid on a bike rides past your car, then stops. He circles back, staring at you with wide eyes.")
        print("\n")
        type.type(quote("Whoa... do you LIVE in your car? That's so COOL!"))
        print("\n")
        type.type("You're not sure 'cool' is the word you'd use, but okay.")
        print("\n")
        type.type(quote("I wish I could live in a car! No bedtime, no vegetables, no homework! You're living the DREAM, mister!"))
        print("\n")
        type.type("Before you can correct him, he pedals off, yelling about how he's going to tell his friends about the 'cool car guy.'")
        print("\n")
        type.type("You feel... strangely validated?")
        print("\n")
        self.heal(5)

    def lost_tourist(self):
        # One-Time - helpful NPC
        if self.has_met("Lost Tourist"):
            self.day_event()
            return
        
        self.meet("Lost Tourist")
        type.type("A minivan pulls up next to you. The window rolls down to reveal a frazzled-looking family. Dad's driving, Mom's got a map upside down, and three kids are screaming in the back.")
        print("\n")
        type.type(quote("Excuse me! We're trying to find the highway? Our GPS died three towns ago!"))
        print("\n")
        type.type("You give them directions as best you can. The dad looks so relieved he might cry.")
        print("\n")
        type.type(quote("Thank you so much! Here, take this-for your trouble!"))
        print("\n")
        tip = random.randint(20, 50)
        type.type("He hands you " + green(bright("$" + str(tip))) + " before speeding off, kids still screaming.")
        self.change_balance(tip)
        print("\n")
        type.type("Good deed for the day: done.")
        print("\n")

    # ==========================================
    # SECRET EVENTS - CHEAP TIER  
    # ==========================================
    
    def deja_vu(self):
        # SECRET - Only triggers if player's day count is a multiple of 7 (weekly)
        if self.get_day() % 7 != 0 or self.get_day() == 0:
            self.day_event()
            return
        
        if self.has_met("Deja Vu " + str(self.get_day())):
            self.day_event()
            return
        
        self.meet("Deja Vu " + str(self.get_day()))
        
        type.type("You wake up, and something feels... off. Familiar. Like you've lived this exact moment before.")
        print("\n")
        type.type("The clouds are the same. The breeze is the same. Even the bird on that branch is the same.")
        print("\n")
        type.type("Deja vu? Or something more?")
        print("\n")
        type.type("A strange certainty washes over you: today, something significant will happen at the casino.")
        print("\n")
        self.add_status("Lucky")
        type.type(yellow(bright("You feel like the universe is trying to tell you something.")))
        print("\n")

    def exactly_1111(self):
        # SECRET - Triggers at exactly $1,111
        if self.get_balance() != 1111:
            self.day_event()
            return
        
        type.type("You count your money and realize you have exactly " + green(bright("$1,111")) + ". One-one-one-one. Make a wish.")
        print("\n")
        type.type("The moment feels charged, electric. Like the universe is listening.")
        print("\n")
        type.type("You close your eyes and make a wish.")
        print("\n")
        
        # Random positive effect
        effect = random.randrange(3)
        if effect == 0:
            type.type("A warm feeling spreads through your chest. ")
            type.type(yellow(bright("Your wish for health has been granted.")))
            self.heal(50)
        elif effect == 1:
            type.type("A gust of wind blows a crumpled bill against your window. Then another. Then another.")
            print("\n")
            bonus = random.randint(100, 300)
            type.type(yellow(bright("Your wish for wealth has been partially granted.")) + " " + green(bright("+${:,}".format(bonus))))
            self.change_balance(bonus)
        else:
            type.type("You feel luckier than you have in months.")
            type.type(yellow(bright("Your wish for fortune has been granted.")))
            self.add_status("Lucky")
        print("\n")

    # One-Time
    def turn_to_god(self):
        if self.has_met("Ezekiel"):
            self.day_event()
            return
        
        self.meet("Ezekiel")
        type.type("You wake up to someone knocking on your window. You sit up, and see a man, holding a bible, and wearing a cross on a chain around his neck.")
        print("\n")
        type.type(quote("Hello! I'm Father Ezekiel. You seem to be in a tough spot, living in your car? I was just wondering if you wanted me to give you my copy of The Bible. It has the word of God, and I hope it could help you understand that you aren't alone on this journey of life."))
        print()
        type.type(space_quote("Do you accept my offer, and Jesus as your savior?"))
        answer = ask.yes_or_no(space_quote("Do you?"))
        if answer == "yes":
            self.__is_religious = True
            type.type(space_quote("Why, that's wonderful!"))
            type.type("Father Ezekiel hands you his bible. ")
            type.type(quote("I will pray for you, and I know that Jesus will always be with you. Amen."))
        elif answer == "no":
            type.type(open_quote("Well, to each their own. I certainly cast no judgments. "))
            type.type(close_quote("I will pray for you, and I know that Jesus will always be with you. Amen."))
        print("\n")
        type.type("And with that, Father Ezekiel walks down the road, and out of sight.")
        print("\n")
        return
    
    def hungry_cow(self):
        if self.has_met("Betsy"):
            self.day_event()
            return
        
        self.meet("Betsy")
        self.add_danger("Betsy Tractor")
        type.type("You wake up to your whole car shaking. As you jump up from your seat, you see a beautiful black and white cow, staring you down through your window. ")
        type.type("The cow moos at you aggressively, and you open the door. On its back is a note that reads 'This is Betsy. Betsy gets hungry. Please feed Betsy.'")
        print("\n")
        type.type("Betsy stares into your soul, then looks over at the seat next to you. It appears Betsy is interested in your pile of money. ")
        print()
        type.type("Do you feed Betsy? ")
        while True:
            answer = ask.yes_or_no("Moo? ")
            if answer == "yes":
                type.type("You put a " + green(bright("$100")) + " dollar bill into Betsy's mouth. She chews it up, then spits it out in front of you.")
                self.change_balance(-100)
                random_chance = random.randrange(4)
                if (random_chance == 0) or (self.__balance < 500):
                    type.type("Betsy moos, then smiles. She walks down the road, happy as can be.")
                    break
                else:
                    type.type("Betsy moos, then stares you down. She doesn't seem to be done with you.")
                    print()
                    type.type("Do you feed Betsy? ")
            elif answer == "no":
                type.type("Betsy moos, then charges at you. She slams into your wagon hard, and your leg gets caught in the door. That hurt. Really, really bad.")
                print("\n")
                self.hurt(40)
                self.add_injury("Broken Leg")
                type.type("Betsy moos loudly, wags her tail, then walks down the road. Oh well.")
                break
        print("\n")

    # One-Time Conditional
    # DREAM SEQUENCES - CHEAP TIER
    def remember_rebecca(self):
        # Tom's dream sequence part 1 - only triggers if hasn't progressed yet
        if self.get_tom_dreams() != 0:
            self.day_event()
            return
        
        type.type("As you drift off to sleep, you find yourself standing at the edge of a sunlit meadow. The grass sways gently in the breeze, and in the distance, you see a figure waiting for you.")
        print("\n")
        type.type("You can't make out her face, but somehow, you know her name.")
        print("\n")
        type.type(bright("Rebecca."))
        print("\n")
        type.type("You have faint memories of that name. She sounds lovely. You try to walk towards her, but the closer you get, the further away she seems. You reach out your hand, but before you can touch her...")
        print("\n")
        type.type("You wake up.")
        print("\n")
        type.type(yellow("Something stirs in the back of your mind. A memory you'd rather forget."))
        self.advance_tom_dreams()
        print("\n")

    def dealers_anger(self):
        # Frank's dream sequence part 1 - only triggers if hasn't progressed yet
        if self.get_frank_dreams() != 0:
            self.day_event()
            return
        
        type.type("As you fall asleep, you dream of sitting at a blackjack table. The familiar green felt stretches out before you, and across from you sits the Dealer, shuffling cards with practiced ease.")
        print("\n")
        type.type("You're dealt a hand. A King and an Ace. " + green(bright("Blackjack.")))
        print("\n")
        type.type("But instead of paying out, the Dealer's face contorts with rage. He slams his fist on the table.")
        print("\n")
        type.type(red(quote("You think you can just WIN?! You think it's that EASY?!")))
        print("\n")
        type.type("His yelling gets louder and louder. At first he's yelling at himself, muttering about odds and luck. But then, he turns to you. His eyes bore into yours.")
        print("\n")
        type.type(red(quote("This is YOUR fault. ALL OF IT.")))
        print("\n")
        type.type("The screaming grows deafening until you jolt awake, heart pounding.")
        print("\n")
        type.type(yellow("The Dealer's rage echoes in your mind long after you wake."))
        self.advance_frank_dreams()
        print("\n")

    def casino_bar(self):
        # Oswald's dream sequence part 1 - only triggers if hasn't progressed yet
        if self.get_oswald_dreams() != 0:
            self.day_event()
            return
        
        type.type("You drift into a dream, and find yourself sitting at a bar inside a grand casino. Crystal chandeliers hang from the ceiling, their light dancing across marble floors. The air smells of expensive cigars and possibility.")
        print("\n")
        type.type("You're chatting it up with the person next to you-someone important, though you can't quite remember who. A bartender in a crisp white shirt approaches.")
        print("\n")
        type.type(quote("What'll it be?"))
        print("\n")
        type.type("You order a drink. The bartender raises an eyebrow.")
        print("\n")
        type.type(quote("That's gonna cost you. Expensive taste you've got."))
        print("\n")
        type.type("You wave your hand dismissively. Money is no object. Not here. Not in this place.")
        print("\n")
        type.type("The bartender shrugs and pours your drink. As he slides it across the bar, he says:")
        print("\n")
        type.type(quote("Well, it's your drink after all."))
        print("\n")
        type.type("You wake up, the phantom taste of bourbon lingering on your tongue.")
        print("\n")
        type.type(yellow("You can almost hear the slot machines in the distance."))
        self.advance_oswald_dreams()
        print("\n")

    # Modest Day Events (10,000 - 100,000)
    # Everytime
    def left_door_open(self):
        type.type("You wake up in the front seat, with a chill throughout your body. ")
        type.type("Had the passenger door really been open all night? ")
        type.type("Hopefully nothing had gotten in. ")
        type.type("You reach over and close the door, just to be safe.")
        random_chance = random.randrange(6)
        if random_chance <= 3:
                self.add_danger("Spider")
        elif random_chance == 3:
                self.add_danger("Squirrel")
        print("\n")   

    # Conditional
    def another_spider_bite(self):
        if not self.has_danger("Spider") or self.has_status("Spider Bite"):
            self.day_event()
            return
        
        type.type("You wake up to a sharp pain on your neck! ")
        type.type("Swinging your arm to scratch the pain, you watch as a spider jumps to the backseat. ")
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the spider. ")
            type.type("A cloud of white liquid covers the spider, and you watch as it slows, and dies. ")
            type.type("Hopefully, that's the end of your spider problems.")
        else:
            type.type("The spider, now out of reach, crawls off the seat and onto the floor. ")
            type.type("You stick your head out back, but you aren't sure where the spider went, or if it has a family nearby. This is unfortunate.")
        self.add_status("Spider Bite")
        self.mark_day("Spider Bite")
        print("\n")

    def squirrel_invasion(self):
        if not self.has_danger("Squirrel") or self.has_status("Squirrel Bite") or self.has_status("Rabies") or self.has_item("Squirrely") or self.has_met("Squirrely"):
            self.day_event()
            return

        self.lose_danger("Squirrel")
        if self.has_item("Bag of Acorns"):
            self.use("Bag of Acorns")
            type.type("You wake up to the sound of something rummaging through your car. Looking in the backseat, you notice a little squirrel, chewing through your " + bright(magenta("Bag of Acorns")) + ". He looks pretty cute.")
            print("\n")
            if self.has_met("Dead Squirrely"):
                type.type("The squirrel notices you, and jumps from the bag, and over to your center console. He peers up at you, but your eyes are filled with tears. Nothing can ever replace Squirrely. You pick up the squirrel, open the door, and let it free.")
                print("\n")
                return
            else:
                type.type("The squirrel notices you, and jumps from the bag, and over to your center console. He peers up at you, with an acorn in hand, holding it up in your direction. You stick your hand out, and the squirrel gives you the acorn. This must be a sign of peace.")
                print("\n")
                type.type("After an hour of watching the squirrel eat the acorns, climb around your car, and jump from your arm to the dashboard over and over, you decide that this squirrel is now yours. You name him 'Squirrely', in honor of him being a squirrel.")
                print("\n")
                self.add_item("Squirrely")
                self.mark_day("Squirrely Fed")
                return
        else:
            type.type("You wake up to a sharp pain on your leg! ")
            type.type("You swing the hurt leg, and you watch as a squirrel goes flying into the air. ")
            type.type("The little rodent starts climbing around your car, scurrying around the walls, desperately trying to get out. ")
            type.type("You open the backseat windows, and the squirrel jumps out, and darts into the woods. Hopefully, that bite isn't too serious.")
            self.add_status("Squirrel Bite")
            random_chance = random.randrange(4)
            if random_chance == 1:
                self.add_status("Rabies")
                self.mark_day("Rabies")
            self.mark_day("Squirrel Bite")
            print("\n") 
            return
    
    # ==========================================
    # NEW MODEST DAY EVENTS - Everytime
    # ==========================================
    
    def street_performer(self):
        # Everytime - random encounter
        variant = random.randrange(4)
        if variant == 0:
            type.type("A man with a guitar sits down near your car and starts playing. He's actually pretty good.")
            print("\n")
            type.type("You listen for a while. When he finishes, you toss him a few bucks. He tips his hat and moves on.")
            self.change_balance(-random.randint(1, 5))
        elif variant == 1:
            type.type("A one-man-band contraption walks by-drums, harmonica, cymbals, the whole nine yards. The noise is incredible.")
            print("\n")
            type.type("He plays for exactly three minutes, then disappears around the corner. What a strange morning.")
        elif variant == 2:
            type.type("A magician approaches your car window and does a card trick. You have no idea how he did it.")
            print("\n")
            type.type(quote("Pick a card, any card!") + " he says. You pick the three of hearts.")
            print("\n")
            type.type("He makes it disappear, reappear in his mouth, then reveals it was in your pocket the whole time.")
            print("\n")
            type.type("Wait. How did he get it in your pocket?")
        else:
            type.type("A mime follows your car for three blocks. You finally shake him when you run a yellow light.")
            print("\n")
            type.type("Mimes are weird.")
        print("\n")

    def power_outage_area(self):
        # Everytime - atmospheric event
        variant = random.randrange(3)
        if variant == 0:
            type.type("The entire block goes dark. Power outage. The streetlights, the shops, everything.")
            print("\n")
            type.type("You sit in your car, watching people stumble around with flashlights, and feel strangely superior. You don't need electricity. You're already off the grid.")
        elif variant == 1:
            type.type("Traffic lights are out. An intersection nearby becomes chaos. Cars honking, people yelling.")
            print("\n")
            type.type("You watch the disaster unfold from the safety of your parked wagon. Entertainment.")
        else:
            type.type("A transformer explodes somewhere nearby. Sparks shower into the street.")
            print("\n")
            type.type("Beautiful, in a terrifying sort of way.")
        print("\n")

    def construction_noise(self):
        # Everytime - minor annoyance
        variant = random.randrange(3)
        if variant == 0:
            type.type("BANG BANG BANG. Construction starts at 6 AM. Right next to your car. Of course.")
            print("\n")
            type.type("You move to a different spot. The construction sounds follow you. Are they... expanding?")
        elif variant == 1:
            type.type("A jackhammer starts up nearby. Your teeth are literally vibrating.")
            print("\n")
            type.type("You cover your ears and wait for it to stop. It takes four hours.")
            self.hurt(5)
        else:
            type.type("The sound of a cement mixer becomes your alarm clock this morning. Not the most peaceful wake-up.")
            print("\n")
            type.type("At least they wave at you when they notice you're awake.")
        print("\n")

    # ==========================================
    # NEW MODEST DAY EVENTS - Conditional
    # ==========================================
    
    def homeless_network(self):
        # Conditional - only triggers if player has met multiple NPCs
        if not (self.has_met("Cowboy") or self.has_met("Ezekiel") or self.has_met("Betsy")):
            self.day_event()
            return
        
        if self.has_met("Homeless Network"):
            self.day_event()
            return
        
        self.meet("Homeless Network")
        type.type("A scruffy-looking man approaches your car. He's clearly homeless, but there's an intelligence in his eyes.")
        print("\n")
        type.type(quote("Word on the street is you've been meeting some interesting folks. The cowboy. The preacher. Even that crazy cow."))
        print("\n")
        type.type("He grins, showing missing teeth.")
        print("\n")
        type.type(quote("We've got a network, you know. Us street folks. We share info. And some of that info might be useful to someone in your... unique situation."))
        print("\n")
        type.type("He offers to tell you about a shortcut to the casino that avoids the main roads. Better for someone trying to stay under the radar.")
        print("\n")
        answer = ask.yes_or_no("Pay him $50 for the info? ")
        if answer == "yes":
            self.change_balance(-50)
            type.type("He pockets the money and tells you about a back road that cuts travel time significantly.")
            print("\n")
            type.type(quote("Good luck out there. We're all rooting for you."))
            self.add_item("Secret Route Map")
        else:
            type.type("He shrugs. " + quote("Your loss. The offer stands if you change your mind."))
        print("\n")

    # ==========================================
    # NEW MODEST DAY EVENTS - One-Time
    # ==========================================
    
    def the_photographer(self):
        # One-Time - documentary
        if self.has_met("The Photographer"):
            self.day_event()
            return
        
        self.meet("The Photographer")
        type.type("A woman with a professional camera approaches your car, clearly excited.")
        print("\n")
        type.type(quote("Hi! I'm doing a photo documentary on alternative lifestyles. Living in your car is EXACTLY the kind of story I'm looking for!"))
        print("\n")
        type.type("She's practically bouncing with enthusiasm.")
        print("\n")
        type.type(quote("Would you mind if I took some photos? I can pay you for your time!"))
        print("\n")
        answer = ask.yes_or_no("Allow the photoshoot? ")
        if answer == "yes":
            type.type("You pose with your wagon, trying to look dignified. She snaps dozens of photos.")
            print("\n")
            type.type(quote("These are PERFECT! The lighting, the composition, the story they tell!"))
            print("\n")
            type.type("She pays you " + green(bright("$200")) + " for your time.")
            self.change_balance(200)
            print("\n")
            type.type(quote("If this gets published, you might be famous! In a niche art magazine, anyway."))
        else:
            type.type(quote("Oh. Okay. I understand, privacy is important."))
            print("\n")
            type.type("She walks away, looking disappointed.")
        print("\n")

    def the_food_truck(self):
        # One-Time - wholesome
        if self.has_met("Food Truck"):
            self.day_event()
            return
        
        self.meet("Food Truck")
        type.type("A food truck parks right next to your wagon. The smell of cooking meat is intoxicating.")
        print("\n")
        type.type("The owner leans out the window and spots you.")
        print("\n")
        type.type(quote("Hey! You been living in that car long? I see you parked here sometimes."))
        print("\n")
        type.type("Before you can answer, he's already preparing something.")
        print("\n")
        type.type(quote("Here. On the house. Everyone deserves a good meal."))
        print("\n")
        type.type("He hands you a massive burrito, overflowing with everything good in the world.")
        print("\n")
        type.type("It's the best thing you've eaten in months.")
        self.heal(30)
        print("\n")
        type.type(quote("Come by anytime. We look out for each other around here."))
        print("\n")

    # ==========================================
    # SECRET EVENTS - MODEST TIER
    # ==========================================
    
    def exactly_50000(self):
        # SECRET - Halfway to Rich
        if self.get_balance() != 50000:
            self.day_event()
            return
        
        type.type("Fifty thousand dollars. " + green(bright("$50,000")) + ". Halfway to the Rich tier.")
        print("\n")
        type.type("You never thought you'd see this much money in your life, let alone in the passenger seat of your car.")
        print("\n")
        type.type("A pigeon lands on your roof. Then another. Then five more. They coo in what sounds almost like... applause?")
        print("\n")
        type.type("The universe is weird sometimes.")
        print("\n")
        type.type(yellow(bright("The halfway point. The journey continues.")))
        self.heal(25)
        print("\n")

    # One-Time
            
    # One-Time Conditional
    def further_interrogation(self):
        if not self.has_met("Interrogator") or not self.has_danger("Further Interrogation"):
            self.day_event()
            return

        self.lose_danger("Further Interrogation")
        self.add_danger("Even Further Interrogation")
        type.type("You wake up, and through your windshield, you see a car parked right in front of you. Tired, and concerned, you sit up. As you open the door and get out of your car, you notice a man you've met before, in his bright red suit, once again peering into your trunk.")
        print("\n")
        type.type("The man sees you, and walks up to you, with a clipboard in his hand.")
        print("\n")
        type.type(space_quote("You. You're awake. Good. You see this clipboard? It says you can't be here."))
        type.type("You begin to read the paper on the clipboard. It's a message, written in Comic Sans.")
        print("\n")
        type.type("It reads 'This offical message from the government and the military and the army says that you can't be here. That's right, you, the person reading this message right now, living on this land right here. It's not for you. It won't ever be for you. So, you can't live here. You need to move right now, or I'll be very very angry.'")
        print("\n")
        type.type(space_quote("Did you read it?"))
        answer = ask.yes_or_no(space_quote("Did you? Read it?"))
        if answer == "yes":
            type.type(quote("Good, so you know that all these powerful people want yo- are demanding that you move from where you're currently living, right this instant! I'd suggest you do so. I certainly wouldn't want to upset the government."))
            print()
        elif answer == "no":
            type.type(quote("You didn't read it? Come on, I worked so hard on it. You really should read a clipboard with words on it if someone asks you to. Regardless, it says that you need to move! Or the consequences will be scary!"))
            print()
        type.type("After the man tells you this, he looks up, and stares at the sun. And after about 25 seconds, he rubs his eyes, walks back to his car, and drives off.")
        print("\n")
        return

    # DREAM SEQUENCES - MODEST TIER
    def remember_nathan(self):
        # Tom's dream sequence part 2 - only triggers if part 1 complete
        if self.get_tom_dreams() != 1:
            self.day_event()
            return
        
        type.type("Your eyes grow heavy, and once again you find yourself in a dream. This time, you're in a nursery. Soft blue walls surround you, and a mobile of stars and moons spins lazily above a crib.")
        print("\n")
        type.type("You walk to the crib and peer inside. A baby boy looks up at you with bright, curious eyes. He reaches up towards you, tiny fingers grasping at the air.")
        print("\n")
        type.type("You know his name, somehow. " + bright("Nathan."))
        print("\n")
        type.type("He sounds so sweet. You reach down to pick him up, but as your hands touch him, he fades away like morning mist. The nursery crumbles around you, and you're left standing in darkness.")
        print("\n")
        type.type("You wake up with tears on your cheeks that you don't remember crying.")
        print("\n")
        type.type(yellow("The name 'Nathan' feels like a wound that never healed."))
        self.advance_tom_dreams()
        print("\n")

    def dealers_scar(self):
        # Frank's dream sequence part 2 - only triggers if part 1 complete
        if self.get_frank_dreams() != 1:
            self.day_event()
            return
        
        type.type("Sleep takes you to the casino again. The same blackjack table, the same green felt, the same Dealer sitting across from you.")
        print("\n")
        type.type("But something's different this time. The Dealer leans forward, into the flickering light of the overhead lamp.")
        print("\n")
        type.type("And you see his face clearly for the first time.")
        print("\n")
        type.type("The left side is a ruin of scar tissue, twisted and grotesque. Where his left eye should be, there sits a " + cyan(bright("jade green glass eye")) + ", cold and unblinking. It catches the light and seems to stare right through you.")
        print("\n")
        type.type(red(quote("See something you like?")))
        print("\n")
        type.type("His voice is mocking, bitter. You try to look away, but you can't. The glass eye holds you frozen until you wake, gasping for air.")
        print("\n")
        type.type(yellow("You can still feel that glass eye watching you."))
        self.advance_frank_dreams()
        self.lose_sanity(random.choice([2, 3]))  # Disturbing dream drains sanity
        print("\n")

    def casino_table(self):
        # Oswald's dream sequence part 2 - only triggers if part 1 complete
        if self.get_oswald_dreams() != 1:
            self.day_event()
            return
        
        type.type("The dream takes you back to the casino. But this time, you're not at the bar. You're sitting at a blackjack table, a drink in your hand. The ice clinks against the glass as you take a sip.")
        print("\n")
        type.type(quote("Care to be dealt in?"))
        print("\n")
        type.type("You look up at the dealer, and your blood runs cold.")
        print("\n")
        type.type("The dealer looks " + bright("exactly like you."))
        print("\n")
        type.type("Same face. Same eyes. Same everything. They smile at you-your own smile, but somehow wrong. Twisted.")
        print("\n")
        type.type(quote("Is something the matter?"))
        print("\n")
        type.type("You shake your head. " + quote("No. Nothing's wrong."))
        print("\n")
        type.type("You smile back and take a long sip of your drink. The other you deals the cards, and you play in silence, the only sound being the shuffle of cards and the clink of chips.")
        print("\n")
        type.type("You wake up, unsure which one of you was the real one.")
        self.lose_sanity(random.choice([3, 4]))  # Identity confusion severely drains sanity
        print("\n")
        type.type(yellow("The line between player and dealer feels blurrier than before."))
        self.advance_oswald_dreams()
        print("\n")
        
    # Rich Day Events (100,000 - 500,000)
    # Everytime
    def left_trunk_open(self):
        type.type("You wake up in the front seat, with a chill throughout the whole wagon. ")
        type.type("Had the trunk really been open all night? ")
        type.type("Hopefully nothing had gotten in. ")
        type.type("You get out of the car and close the trunk, just to be safe.")
        random_chance = random.randrange(6)
        if random_chance < 2:
                self.add_danger("Rat")
        elif random_chance < 4:
                self.add_danger("Termite")
        print("\n")    

    # Conditional
    def rat_bite(self):
        if self.has_status("Rabies") or not self.has_danger("Rat") or self.has_status("Rat Bite"):
            self.day_event()
            return

        type.type("You wake up to a sharp pain on your ankle! ")
        type.type("You look down to see a skinny gray rat nibbling your foot. You kick at it, but the little rodent runs under the seat. ")
        print("\n")
        type.type("The rat jumps up onto your backseat, and begins to laugh at you. Now that's just cruel. This rat must be crazy.")
        print("\n")
        self.lose_sanity(random.choice([1, 2, 3]))  # A laughing rat? That's unsettling
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray the rat down. ")
            type.type("A cloud of white liquid covers the rat, and you watch as it spazzes out, and dies. ")
            type.type("Hopefully, that's it for your rat problems. Except for that bite. You might wanna get that checked out.")
        else:
            type.type("You jump at the seat towards the rat, but it sneaks back under the passenger seat, and you can't find it. ")
            type.type("That damn rat. Hopefully, the bite isn't too serious, but it's probably worth getting checked out.")
        self.add_status("Rat Bite")
        random_chance = random.randrange(2)
        if random_chance == 1:
            self.add_status("Rabies")
            self.mark_day("Rabies")
            self.lose_sanity(random.choice([2, 3]))  # Rabies infection further drains sanity
        self.mark_day("Rat Bite")
        print("\n") 
        return       
        

    def hungry_termites(self):
        random_choice = random.randrange(2)
        if (random_choice != 0) or not self.has_danger("Termite"):
            self.day_event()
            return

        type.type("You wake up to a clicking sound. Looking around, you notice that it's coming from your pile of money. ")
        type.type("You jump up to check your cash, and you find a termite eating away at your cash. ")
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the termite. ")
            type.type("A cloud of white liquid covers the termite, and you watch as it slows down, twitches, and dies. ")
            type.type("Hopefully, that's the end of your termite problems.")
        else:
            type.type("You attempt to swat it with your hand, but it falls under your car seat. ")
            type.type("You stick your head under the seat, but you aren't sure where the termite went, or if it has a family nearby. This is just brutal.")
        print("\n")
        type.type("The termite ate through a lot of your money. ")
        losses = int(self.get_balance() * (random.randint(20, 50)/100))
        type.type("You lost " + green(bright("${:,}".format(losses))) + ".")
        self.change_balance(-losses)

    # ==========================================
    # NEW RICH DAY EVENTS - Everytime
    # ==========================================
    
    def luxury_car_passes(self):
        # Everytime - atmospheric event with variants
        variant = random.randrange(4)
        if variant == 0:
            type.type("A Lamborghini roars past your wagon, going at least twice the speed limit. The driver doesn't even glance at you.")
            print("\n")
            type.type("Must be nice. You count your own money pile. Someday, maybe.")
        elif variant == 1:
            type.type("A stretch limo cruises by slowly. Through the tinted windows, you swear you see someone pointing at your car and laughing.")
            print("\n")
            type.type("Okay, that stings a little.")
        elif variant == 2:
            type.type("A Ferrari parks right next to your wagon. The owner gets out, takes one look at your car, and moves his Ferrari further away.")
            print("\n")
            type.type("Rude. But also, fair.")
        else:
            type.type("A Rolls-Royce glides past like a ghost. For a moment, you lock eyes with the elderly man in the back seat.")
            print("\n")
            type.type("He nods at you. Just a simple nod. But it feels... respectful?")
            self.heal(5)
        print("\n")

    def paparazzi_mistake(self):
        # Everytime - comedic event with variants + rare
        rare_chance = random.randrange(100)
        
        if rare_chance < 5:  # 5% - Actually famous
            type.type("A van screeches to a halt. Photographers pour out, cameras flashing!")
            print("\n")
            type.type(quote("IT'S THEM! THE MYSTERIOUS GAMBLING LEGEND!"))
            print("\n")
            type.type("Wait, what? They... think you're famous?")
            print("\n")
            type.type("Before you can correct them, they're shoving microphones in your face, asking about your 'secrets to success.'")
            print("\n")
            type.type("You just roll with it. Why not?")
            print("\n")
            type.type("They leave you with a payment for an 'exclusive interview' you apparently just gave.")
            self.change_balance(random.randint(1000, 3000))
            print("\n")
            return
        
        variant = random.randrange(3)
        if variant == 0:
            type.type("Someone with a camera runs up to your window, snapping photos frantically.")
            print("\n")
            type.type(quote("Excuse me, are you-") + " They look at their phone. Then at you. " + quote("Oh. Sorry. Wrong car."))
            print("\n")
            type.type("They shuffle away, embarrassed. You're not sure whether to be relieved or insulted.")
        elif variant == 1:
            type.type("A group of tourists takes pictures of your wagon. You hear one say, " + quote("Authentic American poverty!"))
            print("\n")
            type.type("You're a tourist attraction now. Great.")
        else:
            type.type("Someone knocks on your window holding an autograph book. They take one look at your face and say, " + quote("Never mind."))
            print("\n")
            type.type("Ouch.")
        print("\n")

    def investment_opportunity(self):
        # Everytime - risky event
        variant = random.randrange(3)
        if variant == 0:
            type.type("A man in a cheap suit approaches your car, waving a stack of papers.")
            print("\n")
            type.type(quote("Hey buddy! You look like someone who appreciates a good opportunity! How'd you like to get in on the ground floor of-"))
            print("\n")
            type.type("You roll up your window. He keeps talking through the glass.")
        elif variant == 1:
            type.type("Someone slides a business card under your windshield wiper. It says 'GUARANTEED RETURNS - NOT A SCAM.'")
            print("\n")
            type.type("The fact that it says 'NOT A SCAM' makes you think it's definitely a scam.")
        else:
            type.type("Your phone buzzes with a text from an unknown number: " + quote("Congratulations! You've been selected for an exclusive investment opportunity!"))
            print("\n")
            type.type("You delete it immediately. Street smarts.")
        print("\n")

    def expensive_taste(self):
        # Everytime - lifestyle creep event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You catch yourself looking at real estate listings on your phone. Apartments that cost more per month than your entire life savings used to be.")
            print("\n")
            type.type("Snap out of it. You live in a car. Focus on the goal.")
        elif variant == 1:
            type.type("You see a fancy restaurant and your stomach growls. You could afford to eat there now. Probably.")
            print("\n")
            type.type("No. The casino money goes TO the casino. Stay disciplined.")
        else:
            type.type("A jewelry store window catches your eye. A gold watch gleams inside. You have the money...")
            print("\n")
            type.type("But you came here to win a million dollars, not spend the ones you have. Keep moving.")
        print("\n")

    def news_van(self):
        # Everytime - media event with variants
        variant = random.randrange(4)
        if variant == 0:
            type.type("A news van pulls up near your spot. Your heart races-are they here for you?")
            print("\n")
            type.type("No. They're filming a story about a pothole two blocks away. You've never been so relieved about a pothole.")
        elif variant == 1:
            type.type("A reporter sets up right next to your car to do a live shot. You duck down and pray they don't pan the camera your way.")
            print("\n")
            type.type("They do. Your mom is definitely going to see this.")
        elif variant == 2:
            type.type("A news crew is interviewing locals. They approach you with a microphone.")
            print("\n")
            type.type(quote("Excuse me sir, do you have any thoughts on the local-"))
            print("\n")
            type.type("You're already driving away. No comments. No interviews. No paper trail.")
        else:
            type.type("The evening news is playing on a TV in a nearby shop window. The anchor is talking about 'the anonymous gambler making waves at local casinos.'")
            print("\n")
            type.type("Is that... you? That could be you.")
            print("\n")
            type.type("You're not sure how you feel about that.")
        print("\n")

    # ==========================================
    # NEW RICH DAY EVENTS - Conditional
    # ==========================================
    
    def wealth_anxiety(self):
        # Conditional - triggers only if balance > $200,000
        if self.get_balance() < 200000:
            self.day_event()
            return
        
        type.type("You wake up in a cold sweat. You've been having nightmares about losing all your money.")
        print("\n")
        type.type("It's getting harder to sleep with this much cash just... sitting there. What if someone steals it? What if you lose it all in one bad night?")
        print("\n")
        type.type("The anxiety gnaws at you all morning. ")
        self.lose_sanity(random.choice([1, 2]))  # Money anxiety chips away at sanity
        print("\n")
        if random.randrange(2) == 0:
            type.type("You spend the day paranoid, jumping at every sound. It's exhausting.")
            self.hurt(10)
        else:
            type.type("But then you take a deep breath. You've come this far. You can go further. The money is a tool, not a burden.")
            self.heal(5)
        print("\n")

    def tax_man(self):
        # Conditional - triggers randomly when balance is high
        if self.get_balance() < 150000 or random.randrange(10) != 0:
            self.day_event()
            return
        
        if self.has_met("Tax Man Visit"):
            self.day_event()
            return
        
        self.meet("Tax Man Visit")
        type.type("A sedan with government plates pulls up. A man in a gray suit steps out, holding a clipboard.")
        print("\n")
        type.type(quote("Excuse me. I'm from the IRS. We've noticed some... unusual financial activity in this area."))
        print("\n")
        type.type("Your blood runs cold. He peers into your car at the pile of cash.")
        print("\n")
        type.type(quote("That's quite a sum you've got there. All reported income, I assume?"))
        print("\n")
        answer = ask.yes_or_no("Lie and say yes? ")
        if answer == "yes":
            type.type(quote("Mm-hmm.") + " He scribbles something on his clipboard. " + quote("Well, everything seems to be in order. For now."))
            print("\n")
            type.type("He hands you his card before driving away. You tear it up immediately.")
        else:
            type.type("You don't say anything. He sighs.")
            print("\n")
            type.type(quote("Look, I don't want to make this complicated. Just... keep your head down, okay? There are bigger fish to fry."))
            print("\n")
            type.type("He drives away. You let out a breath you didn't know you were holding.")
        print("\n")

    # ==========================================
    # NEW RICH DAY EVENTS - One-Time
    # ==========================================
    
    def the_rival(self):
        # One-Time - introduces a recurring antagonist
        if self.has_met("The Rival"):
            self.day_event()
            return
        
        self.meet("The Rival")
        type.type("A motorcycle pulls up next to your wagon. The rider-a woman in a leather jacket-removes her helmet and gives you an appraising look.")
        print("\n")
        type.type(quote("So. You're the one everyone's talking about. The car-dweller who's been cleaning up at the blackjack tables."))
        print("\n")
        type.type("She smirks.")
        print("\n")
        type.type(quote("I'm Victoria. I've been working these casinos for five years. Never seen anyone run as hot as you."))
        print("\n")
        type.type("She leans in, her eyes sharp.")
        print("\n")
        type.type(quote("Enjoy it while it lasts. The house always wins in the end. And if the house doesn't get you..."))
        print("\n")
        type.type("She revs her engine.")
        print("\n")
        type.type(quote("I will."))
        print("\n")
        type.type("She speeds off before you can respond. Something tells you this won't be the last you see of Victoria.")
        print("\n")

    def the_bodyguard_offer(self):
        # One-Time - protection event
        if self.has_met("Bodyguard Offer"):
            self.day_event()
            return
        
        self.meet("Bodyguard Offer")
        type.type("A massive man-easily six and a half feet tall and built like a tank-approaches your car.")
        print("\n")
        type.type(quote("Hey. You're the gambling guy, right? Word on the street is you've got a lot of cash on you."))
        print("\n")
        type.type("You tense up, ready for trouble. But he holds up his hands.")
        print("\n")
        type.type(quote("Easy. I'm not here to rob you. I'm here to offer my services. Protection. Fifty bucks a day and nobody messes with you."))
        print("\n")
        answer = ask.yes_or_no("Hire the bodyguard? ")
        if answer == "yes":
            type.type(quote("Smart choice. Name's Bruno. I'll be around."))
            print("\n")
            type.type("He settles into a spot nearby, looking menacing. You feel safer already.")
            self.add_item("Bodyguard Bruno")
            self.change_balance(-50)
        else:
            type.type(quote("Your loss. But if you change your mind, just holler. I'll hear you."))
            print("\n")
            type.type("He lumbers off. You hope you didn't just make a mistake.")
        print("\n")

    def high_roller_invitation(self):
        # One-Time - casino event
        if self.has_met("High Roller Invite"):
            self.day_event()
            return
        
        self.meet("High Roller Invite")
        type.type("A man in an expensive suit approaches your wagon, holding an envelope.")
        print("\n")
        type.type(quote("Excuse me. I represent the casino management. We've noticed your... consistent performance at our tables."))
        print("\n")
        type.type("He hands you the envelope. Inside is an invitation to the 'VIP High Roller Lounge.'")
        print("\n")
        type.type(quote("Consider this a courtesy. Higher stakes. Better odds. Private tables. The high roller experience."))
        print("\n")
        type.type("He adjusts his cufflinks.")
        print("\n")
        type.type(quote("Of course, the minimum bet is considerably higher. But for someone of your... caliber, that shouldn't be a problem."))
        print("\n")
        type.type("He walks away, leaving you with the invitation. This could be interesting.")
        self.add_item("VIP Invitation")
        print("\n")

    def old_friend_recognition(self):
        # One-Time - emotional event
        if self.has_met("Old Friend"):
            self.day_event()
            return
        
        self.meet("Old Friend")
        type.type("Someone knocks on your window. You look up to see a vaguely familiar face-someone from your old life, before all this.")
        print("\n")
        type.type(quote("Holy shit... is that you? I thought you were dead! Everyone thought you were dead!"))
        print("\n")
        type.type("The memories come flooding back. A life you left behind. People who probably still wonder what happened to you.")
        print("\n")
        type.type(quote("What are you doing living in a CAR? What happened to you?"))
        print("\n")
        answer = ask.yes_or_no("Tell them the truth? ")
        if answer == "yes":
            type.type("You tell them everything. The gambling. The car. The dream of hitting a million dollars.")
            print("\n")
            type.type("They listen in silence, then shake their head slowly.")
            print("\n")
            type.type(quote("You always were a crazy one. Here-take this. For old times' sake."))
            print("\n")
            type.type("They press some money into your hand. " + green(bright("$500")) + ".")
            self.change_balance(500)
            print("\n")
            type.type(quote("Good luck. And... don't be a stranger, okay?"))
        else:
            type.type(quote("I think you've got the wrong person,") + " you say, looking away.")
            print("\n")
            type.type("They stare at you for a long moment, then shake their head and walk away.")
            print("\n")
            type.type("Some doors are better left closed.")
        print("\n")

    # ==========================================
    # SECRET EVENTS - RICH TIER
    # ==========================================
    
    def exactly_250000(self):
        # SECRET - Quarter million celebration
        if self.get_balance() != 250000:
            self.day_event()
            return
        
        type.type("You count your money for the third time. Exactly " + green(bright("$250,000")) + ". A quarter of a million dollars.")
        print("\n")
        type.type("A quarter of the way to your goal.")
        print("\n")
        type.type("As if the universe acknowledges this milestone, a golden butterfly lands on your dashboard. It sits there for a long moment, wings slowly opening and closing.")
        print("\n")
        type.type("Then it flies away, leaving a small pile of gold dust behind.")
        print("\n")
        type.type("Wait, that's real gold.")
        print("\n")
        self.change_balance(1000)
        type.type(yellow(bright("The universe rewards those who persist.")))
        self.add_status("Lucky")
        print("\n")

    def dealer_in_dreams(self):
        # SECRET - Triggers only if player has all 3 Frank dream stages complete
        if self.get_frank_dreams() != 3:
            self.day_event()
            return
        
        if self.has_met("Dealer Dream Complete"):
            self.day_event()
            return
        
        self.meet("Dealer Dream Complete")
        type.type("You fall asleep and find yourself in the familiar casino dreamscape. But this time, something is different.")
        print("\n")
        type.type("The Dealer sits across from you, but he's not angry. He looks... tired. Old.")
        print("\n")
        type.type(quote("You're still here,") + " he says quietly. " + quote("After everything. You're still playing."))
        print("\n")
        type.type("He shuffles the cards slowly, methodically.")
        print("\n")
        type.type(quote("I've been dealing cards for longer than you can imagine. Watching people win. Watching them lose. Watching them destroy themselves chasing something they'll never catch."))
        print("\n")
        type.type("He looks at you with his jade glass eye.")
        print("\n")
        type.type(quote("But you... you're different. I don't know if that's good or bad yet."))
        print("\n")
        type.type("He deals you a single card. The Joker.")
        print("\n")
        type.type(quote("Keep it. A gift. Or a warning. Interpret it however you want."))
        print("\n")
        type.type("You wake up with a playing card in your hand. A Joker. It wasn't there before.")
        self.add_item("Dealer's Joker")
        type.type(yellow(bright("The line between dreams and reality grows thinner.")))
        print("\n")

    # One-Time
    def grimy_gus_discovery(self):
        # One-Time - Discover the pawn shop
        if self.has_met("Grimy Gus"):
            self.day_event()
            return
        
        self.meet("Grimy Gus")
        type.type("You wake up to a sharp knock on your window. When you look up, you see a gaunt man in a stained trench coat peering at you through the glass. His teeth are yellow, his eyes are bloodshot, and he's holding a pocket watch that looks far too expensive for someone dressed like him.")
        print("\n")
        type.type("You roll down the window just a crack.")
        print("\n")
        type.type(quote("Nice pile of cash you got there,") + " he rasps, nodding at the money in your passenger seat. " + quote("You look like a collector. A finder of rare things."))
        print("\n")
        type.type("He glances around nervously, then leans closer.")
        print("\n")
        type.type(quote("Name's Gus. Grimy Gus, they call me. Got a little shop down on Fifth and Nowhere. If you ever find yourself with... unusual items... things that don't belong in the light of day... I can make them disappear. For a fair price."))
        print("\n")
        type.type("He taps his nose conspiratorially.")
        print("\n")
        type.type(quote("Collectibles, trinkets, treasures. Things you picked up on your... adventures. I don't ask questions. Just cash on the barrel."))
        print("\n")
        type.type("He hands you a grimy business card through the crack in the window. It reads: " + cyan(bright("\"Grimy Gus's Pawn Emporium - We Buy What Others Won't\"")))
        print("\n")
        type.type(quote("Come by sometime. You won't regret it. Probably."))
        print("\n")
        type.type("He shuffles off into the morning mist before you can respond.")
        print("\n")
        type.type(yellow(bright("A new shop has been unlocked: Grimy Gus's Pawn Emporium")))
        print("\n")

            
    # One-Time Conditional
    def starving_cow(self):
        if not self.has_met("Betsy") or not self.has_danger("Betsy Tractor"):
            self.day_event()
            return

        self.add_danger("Betsy Army")
        self.lose_danger("Betsy Tractor")
        type.type("You wake up to the sound of a tractor barrling closer. As you jump up from your seat, you see the tractor getting closer to your wagon. ")
        type.type("The tractor drives beside your vehicle, and pushes right up against you, grinding the paint off your car. That's just mean. ")
        print("\n")
        type.type("You look up at the driver to see a beautiful black and white cow. Good god, it's Betsy. Why, Betsy, why. The cow moos at you aggressively, and you roll down the window. ")
        print("\n")
        type.type("Betsy stares into your soul, then looks over at the seat next to you. It appears Betsy is interested in your pile of money. ")
        print()
        type.type("Do you feed Betsy? ")
        while True:
            answer = ask.yes_or_no("Moo? ")
            if answer == "yes":
                type.type("You reach out your window, and put a stack of bills, worth " + green(bright("$10,000")) + " into Betsy's mouth. She chews them up, then spits them out into your wagon.")
                self.change_balance(-10000)
                random_chance = random.randrange(4)
                if (random_chance == 0) or (self.__balance <50000):
                    type.type("Betsy moos, then smiles. She pulls away from the car, and drives the tractor down the road, happy as can be.")
                    break
                else:
                    type.type("Betsy moos, then stares you down. She doesn't seem to be done with you.")
                    print()
                    type.type("Do you feed Betsy? ")
            elif answer == "no":
                type.type("Betsy moos, then backs the tractor up. She then proceeds to step on the gas, and drives the tractor forward at your vehicle, slamming into the front of your wagon hard. She moos and moos and moos, pushing your car further back. The jolt of the vehicles smashing into each other kills, and your spine begins to fracture.")
                print("\n")
                self.hurt(80)
                self.add_injury("Fractured Spine")
                type.type("Betsy laughs a laugh, almost maniacal, before driving the tractor down the road.")
                break
        print("\n")

    # Doughman Days (500,000 - 900,000)
    # Everytime
    def thunderstorm(self):
        self.add_travel_restriction("Rain")
        # Alt dialogue for repeated event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You wake up to the sound of raindrops hitting the roof of your wagon. It starts with a couple, then a few, and before you even get the chance to stretch, it begins to pour. The sky is a dark, dark gray, and streams start to form along the road.")
            print("\n")
            type.type("The pitter-patter of the rain on your car lulls you back to sleep. When a strike of lightning wakes you once more, you look out the windows to see a few inches of rain covering the street. Welp, there goes your plans for the day.")
        elif variant == 1:
            type.type("Thunder. BOOM. You're awake now.")
            print("\n")
            type.type("Rain hammers the roof like it's trying to break through. Lightning illuminates the sky every few seconds. It's biblical out there.")
            print("\n")
            type.type("You're not going anywhere today.")
        else:
            type.type("The storm came out of nowhere. One minute, clear skies. The next, your car is being pelted by rain and hail.")
            print("\n")
            type.type("You watch a trash can blow down the street like a tumbleweed. Nature is angry today.")
        print("\n")
        return
    
    # ==========================================
    # NEW DOUGHMAN DAY EVENTS - Everytime
    # ==========================================
    
    def high_stakes_feeling(self):
        # Everytime - internal monologue
        variant = random.randrange(4)
        if variant == 0:
            type.type("You wake up and immediately feel it: today is going to be big. Good or bad, you're not sure. But BIG.")
            print("\n")
            type.type("Half a million dollars sits next to you. More money than most people save in a decade. And you're going to risk it. Again.")
            print("\n")
            type.type("The thought should terrify you. Instead, it excites you.")
        elif variant == 1:
            type.type("You count your money. Then count it again. It's real. It's all real.")
            print("\n")
            type.type("Sometimes you still can't believe you've made it this far. A homeless gambler with half a million dollars.")
            print("\n")
            type.type("What a world.")
        elif variant == 2:
            type.type("The morning light catches your pile of cash and it almost glows. All those hours at the tables. All those wins. All those near-misses.")
            print("\n")
            type.type("This is what it's all been building to.")
        else:
            type.type("You feel like you're in the final act of a movie. The climax is coming. You can feel it in your bones.")
            print("\n")
            type.type("Whether it's a happy ending or a tragedy... well. That's up to you.")
        print("\n")

    def casino_security(self):
        # Everytime - paranoia event
        variant = random.randrange(3)
        if variant == 0:
            type.type("A security car does a slow drive-by. The guard makes eye contact with you, holds it for a beat too long, then drives on.")
            print("\n")
            type.type("They're watching you. You can feel it.")
        elif variant == 1:
            type.type("You spot the same car parked across the street three days in a row. Different driver each time.")
            print("\n")
            type.type("Coincidence? You're not sure you believe in coincidences anymore.")
        else:
            type.type("Your phone gets a notification: 'Someone tried to access your location.' You don't remember giving anyone permission.")
            print("\n")
            type.type("You turn off location services. Paranoid? Maybe. But you didn't get this far by being careless.")
        print("\n")

    def wealthy_doubts(self):
        # Everytime - psychological event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You could stop now. Walk away with over half a million dollars. Live comfortably for years.")
            print("\n")
            type.type("But that's not why you're here.")
            print("\n")
            type.type("You're here for a million. Nothing less will do.")
        elif variant == 1:
            type.type("What are you even going to DO with a million dollars? Buy a house? Invest? Travel?")
            print("\n")
            type.type("You realize you've been so focused on the goal, you never thought about what comes after.")
            print("\n")
            type.type("Something to think about. After you win.")
        else:
            type.type("Is it greed that keeps you going? Or pride? Or something else entirely?")
            print("\n")
            type.type("You've spent so long chasing this dream, you're not sure you'd know what to do without it.")
        print("\n")

    def people_watching(self):
        # Everytime - observation event
        variant = random.randrange(4)
        if variant == 0:
            type.type("A businessman walks by, talking loudly on his phone about a 'big deal' worth $50,000.")
            print("\n")
            type.type("You have ten times that in your car. The thought makes you smile.")
        elif variant == 1:
            type.type("A couple argues about money outside a restaurant. Something about not being able to afford the bill.")
            print("\n")
            type.type("You could pay that bill a thousand times over. But you don't. That's not what the money is for.")
        elif variant == 2:
            type.type("A homeless man asks you for change. You give him a twenty.")
            print("\n")
            type.type("He looks at you like you're crazy. You probably are.")
            self.change_balance(-20)
        else:
            type.type("You watch people come and go from the casino across the street. Winners celebrating. Losers sulking.")
            print("\n")
            type.type("Tonight, you'll be one of them. You know which one you're betting on.")
        print("\n")

    # ==========================================
    # NEW DOUGHMAN DAY EVENTS - Conditional
    # ==========================================
    
    def the_temptation(self):
        # Conditional - balance specific
        if self.get_balance() < 600000:
            self.day_event()
            return
        
        if random.randrange(3) != 0:
            self.day_event()
            return
        
        type.type("A real estate agent knocks on your window, startling you awake.")
        print("\n")
        type.type(quote("Excuse me! I couldn't help but notice you've been living here for a while. Did you know that with your... apparent savings... you could afford a nice apartment? Maybe even a house?"))
        print("\n")
        type.type("They slide a business card through the crack in your window.")
        print("\n")
        type.type(quote("Think about it! " + green(bright("${:,}".format(self.get_balance()))) + " could buy you a real home! A real life!"))
        print("\n")
        type.type("They walk away, leaving you with their card and a nagging thought.")
        print("\n")
        type.type("A real home. A real life. Is that what you want? Or do you want the million?")
        print("\n")
        type.type("You crumple the card and throw it away. You know the answer.")
        print("\n")

    # ==========================================
    # NEW DOUGHMAN DAY EVENTS - One-Time
    # ==========================================
    
    def the_veteran(self):
        # One-Time - wisdom NPC
        if self.has_met("The Veteran"):
            self.day_event()
            return
        
        self.meet("The Veteran")
        type.type("An old man shuffles up to your car. His clothes are worn but clean. His eyes are sharp.")
        print("\n")
        type.type(quote("You're the one, aren't you? The gambler everyone's talking about."))
        print("\n")
        type.type("He leans against your car with a sigh.")
        print("\n")
        type.type(quote("I used to be like you. Thirty years ago. Had a system. Thought I could beat the house."))
        print("\n")
        type.type("He's quiet for a moment.")
        print("\n")
        type.type(quote("Got up to eight hundred thousand. Then lost it all in one night. Pride. Impatience. Stupidity. Take your pick."))
        print("\n")
        type.type(quote("You've got further than I ever did. Don't make my mistakes."))
        print("\n")
        type.type("He pats your car and walks away, disappearing into the crowd.")
        print("\n")
        type.type(yellow("His words echo in your mind."))
        print("\n")

    def the_journalist(self):
        # One-Time - media attention
        if self.has_met("The Journalist"):
            self.day_event()
            return
        
        self.meet("The Journalist")
        type.type("A woman with a notepad and recorder approaches your car.")
        print("\n")
        type.type(quote("Hi! I'm writing a piece on professional gamblers for the Tribune. Mind if I ask you a few questions?"))
        print("\n")
        answer = ask.yes_or_no("Grant the interview? ")
        if answer == "yes":
            type.type("You tell her your story. The car, the casino, the dream of a million dollars.")
            print("\n")
            type.type("She scribbles furiously, eyes wide.")
            print("\n")
            type.type(quote("This is incredible! The readers are going to love this!"))
            print("\n")
            type.type("She pays you " + green(bright("$300")) + " for the interview and promises to send you a copy when it's published.")
            self.change_balance(300)
        else:
            type.type(quote("I understand. Privacy is important."))
            print("\n")
            type.type("She walks away, looking disappointed.")
        print("\n")

    def the_offer_refused(self):
        # One-Time - casino pressure
        if self.has_met("Casino Manager"):
            self.day_event()
            return
        
        self.meet("Casino Manager")
        type.type("A man in an expensive suit knocks on your window. His smile doesn't reach his eyes.")
        print("\n")
        type.type(quote("Good morning. I'm the floor manager at the casino. We've noticed your... impressive winning streak."))
        print("\n")
        type.type("He clasps his hands together.")
        print("\n")
        type.type(quote("I've been authorized to offer you a complimentary room at our hotel. Free meals. Free drinks. VIP treatment."))
        print("\n")
        type.type("His smile widens.")
        print("\n")
        type.type(quote("All we ask is that you continue playing at OUR tables. Exclusively."))
        print("\n")
        answer = ask.yes_or_no("Accept the VIP treatment? ")
        if answer == "yes":
            type.type(quote("Excellent! We'll have everything arranged. Welcome to the family."))
            print("\n")
            type.type("He hands you a VIP keycard. You feel like you've just made a deal with the devil.")
            self.add_item("Casino VIP Card")
        else:
            type.type("His smile falters, just for a second.")
            print("\n")
            type.type(quote("I see. Well, the offer stands if you change your mind."))
            print("\n")
            type.type("He walks away. You get the feeling you've just made an enemy.")
        print("\n")

    # ==========================================
    # SECRET EVENTS - DOUGHMAN TIER
    # ==========================================
    
    def exactly_777777(self):
        # SECRET - Lucky sevens
        if self.get_balance() != 777777:
            self.day_event()
            return
        
        type.type("You count your money. " + green(bright("$777,777")) + ". All sevens.")
        print("\n")
        type.type("Seven is the luckiest number. Everyone knows that.")
        print("\n")
        type.type("And you have six of them.")
        print("\n")
        type.type("The air around you seems to shimmer. A slot machine somewhere in the distance hits a jackpot-you can hear the bells.")
        print("\n")
        type.type("This is a sign. It has to be.")
        print("\n")
        self.add_status("Lucky")
        self.heal(30)
        type.type(yellow(bright("Lucky sevens. The universe is on your side.")))
        print("\n")

    # Conditional
            
    # One-Time
    def likely_death(self):
        if self.has_met("Gunman"):
            self.day_event()
            return
        
        self.meet("Gunman")
        self.lose_sanity(random.choice([4, 5, 6]))  # Near-death experience severely drains sanity
        type.type("You wake up to the sound of a gunshot. You sit up, and look around, confused. As you look out your windshield, you see a figure, in a black trench coat. He walks to the front window, and beckons for you to roll it down. As you crank the window lower, he peers his head inside. You can smell the food between his teeth, and the alcohol on his breath. He has a gun in his hand, and he points it at you.")
        print("\n")
        percentage = 80
        type.type(quote("I'd say there's about an " + red(bright("80%")) + " chance that I blow your brains out. Right now. Wanna change that?") + " ")
        while True:
            answer = ask.yes_or_no("You gonna answer me? ")
            if answer == "yes":
                type.type("You nod your head, knowing exactly what he wants. As your hand shakes, you reach into your pocket. How much money do you give him? ")
                value = ask.give_cash(self.get_balance(), "How much money do you give him? ")
                if value == 0:
                    type.type("You tell him that you don't have any money left. A dissapointed look crosses his face.")
                    print("\n")
                    answer = "no"
                elif value == self.get_balance():
                    type.type("You hand him all of your money. He laughs, and pushes the gun against your forehead. " + quote("Night night, kiddo."))
                    type.slow(red(bright("The gunman pulls the trigger, and you hear a click, followed by a loud ringing in your ears, and a warm liquid dripping down your face. You reach up, and feel a hole in your skull, blood pouring out of it. You try to scream, but you can't. You can't even breathe. You fall to the ground, and everything goes black.")))
                    self.kill("Gunshot to the Head")
                else:
                    type.type("You hand him " + green(bright("${:,}".format(value))) + ".")
                    percentage -= int((value / self.get_balance()) * 100)
                    self.change_balance(-value)
                    if percentage <= 0:
                        type.type("He smiles, and puts the gun down. He laughs, and walks away, leaving you quite poor, but still alive.")
                        print("\n")
                        self.lose_sanity(random.choice([1, 2]))  # Surviving still leaves a mark
                        return
                    if percentage in (8, 18):
                        type.type(quote("Okay, now it's about an " + red(bright(str(percentage) + "%")) + " chance that I blow your brains out. Want that even lower?") + " ")
                    else: type.type(quote("Okay, now it's about a " + red(bright(str(percentage) + "%")) + " chance that I blow your brains out. Want that even lower?") + " ")
            elif answer == "no":
                type.type(quote("Okay, welp, guess we're gonna go gambling!") + " He laughs, and pushes the gun against your forehead. You can feel the cold metal against your skin, sweat dripping off the barrel, and into your eyes. You close them. Breathing in, slowly breathing out, you prepare for the worst. Not that you've ever been scared to face the odds.")

                print("\n")
                if random.randrange(100) > percentage:
                    type.slow(red(bright("The gunman pulls the trigger, and you hear a click.")))
                    type.type(" You open your eyes, and see that the gun is empty. He laughs, and puts the gun down. He walks away. Somehow, you're still alive. What a nightmare")
                    print("\n")
                    self.lose_sanity(random.choice([2, 3, 4]))  # Surviving Russian roulette leaves a mark
                    return
                else:
                    type.slow(red(bright("The gunman pulls the trigger, and you hear a click, followed by a loud ringing in your ears, and a warm liquid dripping down your face. You reach up, and feel a hole in your skull, blood pouring out of it. You try to scream, but you can't. You can't even breathe. You fall to the ground, and everything goes black.")))
                    self.kill("Gunshot to the Head")
            
    # One-Time Conditional
    def even_further_interrogation(self):
        if not self.has_met("Interrogator") or not self.has_danger("Even Further Interrogation"):
            self.day_event()
            return

        self.lose_danger("Even Further Interrogation")
        self.add_danger("Final Interrogation")
        type.type("You wake up, and through your windshield, you see a car parked right in front of you. Not this again. As you open the door and get out of your car, you notice the man in his bright red suit, once again peering into your trunk.")
        print("\n")
        type.type("The man sees you, and walks up to you, with a badge in his hand.")
        print("\n")
        type.type(space_quote("You. You're awake. Good. You see this badge? It says I have the authority to make you not live here."))
        type.type("You look at the badge. It's a piece of paper, colored gold, with the letters 'FBI' and 'CIA' written in pencil.")
        print("\n")
        type.type(quote("See? I'm allowed to make you leave. And I'm invoking my right to do this right now!"))
        print("\n")
        type.type(space_quote("Are you gonna leave?"))
        answer = ask.yes_or_no(space_quote("Are you? Gonna leave?"))
        if answer == "yes":
            type.type(quote("Good, you better do what I say, I'm super powerful. I hope you actually move and stop living here, because it's really getting on my nerves. I'll be back to make sure you do it, mark my words."))
            print()
        elif answer == "no":
            type.type(quote("What? But you have to! This badge says so! You better listen to me, because I'm really starting to get upset. I'll be back, and if you haven't moved yet, I'll make you, mark my words."))
            print()
        type.type("After the man tells you this, he looks up, and stares at the sun. And after about 30 seconds, he rubs his eyes, walks back to his car, and drives off.")
        print("\n")
        return

    # DREAM SEQUENCES - DOUGHMAN TIER
    def remember_johnathan(self):
        # Tom's dream sequence part 3 - only triggers if part 2 complete
        if self.get_tom_dreams() != 2:
            self.day_event()
            return
        
        type.type("The dream is clearer this time. You're standing in front of a mirror, but the reflection looking back at you seems... different. Older. Tired. Broken.")
        print("\n")
        type.type("Behind your reflection, you see them. Rebecca, holding Nathan. They're waving at you through the glass, smiling, reaching out.")
        print("\n")
        type.type(quote("Come home,") + " Rebecca mouths. " + quote("We miss you."))
        print("\n")
        type.type("You press your hand against the mirror, and your reflection does the same. But as your palms meet, you finally see your reflection's face clearly.")
        print("\n")
        type.type("And you remember your name.")
        print("\n")
        type.type(bright("Johnathan."))
        print("\n")
        type.type(bright("Is that me? Am I Johnathan?"))
        print("\n")
        type.type("The mirror cracks, and the dream shatters. You wake up, knowing exactly who you are, and exactly what you've lost.")
        print("\n")
        type.type(yellow(bright("The memories won't stay buried forever. Maybe it's time to go home.")))
        self.advance_tom_dreams()
        print("\n")

    def dealers_revolver(self):
        # Frank's dream sequence part 3 - only triggers if part 2 complete
        if self.get_frank_dreams() != 2:
            self.day_event()
            return
        
        type.type("The casino dream returns, but the atmosphere has changed. The air is thick with tension, and the Dealer's hands tremble as he shuffles the cards.")
        print("\n")
        type.type("He's furious. You don't understand why, but his rage fills the room like smoke.")
        print("\n")
        type.type(red(quote("You just keep winning, don't you? You just keep TAKING and TAKING.")))
        print("\n")
        type.type("You try to explain that it's just a game, just luck, but the words die in your throat.")
        print("\n")
        type.type("The Dealer reaches down slowly. His scarred hand wraps around the grip of a revolver at his waist. The jade glass eye catches the light as he raises the gun.")
        print("\n")
        type.type(red(quote("Let's see how lucky you really are.")))
        print("\n")
        type.type(red(bright("BANG.")))
        print("\n")
        type.type("You jolt awake, clutching your chest, certain for a moment that you'd been shot. Your heart pounds so hard you can hear it in your ears.")
        print("\n")
        type.type(yellow(bright("The Dealer isn't just angry. He's dangerous. And something tells you this isn't over.")))
        self.advance_frank_dreams()
        print("\n")

    def casino_riches(self):
        # Oswald's dream sequence part 3 - only triggers if part 2 complete
        if self.get_oswald_dreams() != 2:
            self.day_event()
            return
        
        type.type("You're back at the casino table. Your double sits across from you, dealing cards with mechanical precision. You take a sip of bourbon and look at your cards.")
        print("\n")
        type.type(green(bright("Blackjack.")))
        print("\n")
        type.type("The table erupts in cheers. People you don't recognize clap you on the back, shake your hand, toast to your success. You down your drink and slam the glass on the table.")
        print("\n")
        type.type("And then the ceiling opens up.")
        print("\n")
        type.type("Hundred dollar bills begin to rain down from above. They fall like snow, piling up on the table, on the floor, in your lap. Everyone is laughing, grabbing at the money, stuffing their pockets.")
        print("\n")
        type.type("You've never felt so " + green(bright("rich")) + ". So " + green(bright("powerful")) + ". So " + green(bright("fantastic")) + ".")
        print("\n")
        type.type("The other you catches your eye and smiles. " + quote("This could all be yours, you know. Forever."))
        print("\n")
        type.type("You wake up with your fist clenched, as if still holding onto bills that were never there.")
        print("\n")
        type.type(yellow(bright("The promise of wealth echoes in your mind. What would you sacrifice to feel that way forever?")))
        self.advance_oswald_dreams()
        print("\n")
        
    # Nearly There Days (900,000+)
    # ==========================================
    # NEW NEARLY DAY EVENTS - Everytime
    # ==========================================
    
    def almost_there(self):
        # Everytime - motivational event with variants
        variant = random.randrange(5)
        if variant == 0:
            type.type("You wake up and count your money. Again. Just to make sure it's real.")
            print("\n")
            type.type(green(bright("${:,}".format(self.get_balance()))) + ". So close to a million dollars. So close to freedom.")
            print("\n")
            type.type("Your hands shake a little as you put the money back. Not from fear. From anticipation.")
        elif variant == 1:
            type.type("The morning sun hits your pile of money and it almost glows. All those bills. All that progress.")
            print("\n")
            type.type("You've come so far. From nothing to... almost everything.")
            print("\n")
            type.type("One more good night. Maybe two. That's all it'll take.")
        elif variant == 2:
            type.type("You stare at your reflection in the rearview mirror. Dark circles under your eyes. Hair a mess. But there's something else there too.")
            print("\n")
            type.type("Hope. You see hope.")
            print("\n")
            type.type("The finish line is in sight.")
        elif variant == 3:
            type.type("You dream about what you'll do with a million dollars. A real house. A real bed. Real food that doesn't come from a gas station.")
            print("\n")
            type.type("But first, you have to actually WIN it. No counting chickens before they hatch.")
        else:
            type.type("Your phone buzzes. A notification: 'Motivational quote of the day: Success is not final, failure is not fatal.'")
            print("\n")
            type.type("You stare at it for a long moment. Then delete it. You don't need motivational quotes. You need one more win.")
        print("\n")

    def the_weight_of_wealth(self):
        # Everytime - paranoia event
        variant = random.randrange(4)
        if variant == 0:
            type.type("You've moved your parking spot three times today. Just in case someone was watching yesterday.")
            print("\n")
            type.type("Paranoia? Maybe. But you're sitting on almost a million dollars in a car. A little paranoia seems reasonable.")
        elif variant == 1:
            type.type("Every person who walks by makes you tense up. Are they looking at your car? Do they know what's inside?")
            print("\n")
            type.type("Probably not. But probably isn't definitely.")
        elif variant == 2:
            type.type("You've started sleeping in shifts. An hour here, an hour there. Never fully unconscious. Never truly rested.")
            print("\n")
            type.type("The money has made you rich in cash and poor in sleep.")
            self.hurt(5)
        else:
            type.type("A car parks nearby. You watch it for an hour. Nothing happens. They were just parking.")
            print("\n")
            type.type("You really need to relax. But how can you relax with this much at stake?")
        print("\n")

    def casino_knows(self):
        # Everytime - ominous event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You notice a black SUV drive past your wagon. Slowly. Too slowly.")
            print("\n")
            type.type("The windows are tinted. You can't see who's inside. It doesn't stop. But it comes by twice more throughout the day.")
            print("\n")
            type.type("The casino knows. They have to know.")
        elif variant == 1:
            type.type("Your phone rings from an unknown number. You answer cautiously.")
            print("\n")
            type.type("Silence. Then, a click. They hung up.")
            print("\n")
            type.type("Wrong number? Or something else?")
        else:
            type.type("There's a new security guard at the casino entrance. He watches you enter. Watches you leave. Takes notes on a clipboard.")
            print("\n")
            type.type("Maybe it's nothing. Maybe it's everything.")
        print("\n")

    def last_stretch(self):
        # Everytime - tension building
        type.type("This is it. The final stretch. Everything you've worked for comes down to these last few nights.")
        print("\n")
        type.type("Your entire body feels electric. Every nerve is alive. This is what you were born to do.")
        print("\n")
        if random.randrange(3) == 0:
            type.type("A calm settles over you. Whatever happens, happens. You've done everything you can.")
            self.heal(10)
        else:
            type.type("But the pressure... the pressure is immense. One wrong move and it all comes crashing down.")
        print("\n")

    def strange_visitors(self):
        # Everytime - mysterious encounters
        variant = random.randrange(4)
        if variant == 0:
            type.type("A man in a white suit walks past your car, tips his hat, and keeps walking. You've never seen him before.")
            print("\n")
            type.type("Something about his smile was wrong. Too knowing.")
        elif variant == 1:
            type.type("Two women in matching pantsuits photograph your license plate. When you confront them, they claim to be 'researchers.'")
            print("\n")
            type.type("They refuse to elaborate. Then they're gone.")
        elif variant == 2:
            type.type("A child peers through your window. You didn't hear them approach.")
            print("\n")
            type.type(quote("My daddy says you're going to win,") + " they whisper. Then they run away.")
            print("\n")
            type.type("Who is their daddy? How does he know? WHAT does he know?")
        else:
            type.type("You wake up to find a single rose on your windshield. Red. Perfect. No card.")
            print("\n")
            type.type("Is this romantic? Threatening? You genuinely can't tell.")
        print("\n")

    # ==========================================
    # NEW NEARLY DAY EVENTS - Conditional
    # ==========================================
    
    def too_close_to_quit(self):
        # Conditional - balance specific motivation
        if self.get_balance() < 950000:
            self.day_event()
            return
        
        type.type("Less than " + green(bright("$50,000")) + " to go. LESS THAN FIFTY THOUSAND DOLLARS.")
        print("\n")
        type.type("You could walk away right now with " + green(bright("${:,}".format(self.get_balance()))) + ". That's life-changing money for most people.")
        print("\n")
        type.type("But you didn't come this far to come this far.")
        print("\n")
        type.type("Tonight. Tonight could be THE night.")
        print("\n")
        self.heal(20)
        self.add_status("Lucky")
        type.type(yellow(bright("Destiny awaits.")))
        print("\n")

    def victoria_returns(self):
        # Conditional - requires having met The Rival
        if not self.has_met("The Rival"):
            self.day_event()
            return
        
        if self.has_met("Victoria Confrontation"):
            self.day_event()
            return
        
        self.meet("Victoria Confrontation")
        type.type("The motorcycle pulls up. Victoria removes her helmet, but she's not smirking this time.")
        print("\n")
        type.type(quote("I'll be honest. I didn't think you'd make it this far."))
        print("\n")
        type.type("She leans against her bike, studying you.")
        print("\n")
        type.type(quote("I've been doing this for years and never got close to a million. You? A few months in a car and you're almost there."))
        print("\n")
        type.type("She shakes her head.")
        print("\n")
        type.type(quote("I was wrong about you. You're not just running hot. You've got something. Skill, luck, divine intervention-I don't know what. But you've got it."))
        print("\n")
        type.type("She extends her hand.")
        print("\n")
        type.type(quote("No hard feelings?"))
        print("\n")
        answer = ask.yes_or_no("Shake her hand? ")
        if answer == "yes":
            type.type("You shake. Her grip is firm.")
            print("\n")
            type.type(quote("Good luck tonight. You're going to need it."))
            print("\n")
            type.type("She drives off. You feel... lighter, somehow.")
            self.heal(10)
        else:
            type.type("You leave her hanging. She pulls her hand back, expression unreadable.")
            print("\n")
            type.type(quote("Fine. Have it your way. But remember-pride comes before the fall."))
            print("\n")
            type.type("She speeds off without another word.")
        print("\n")

    # ==========================================
    # NEW NEARLY DAY EVENTS - One-Time
    # ==========================================
    
    def the_warning(self):
        # One-Time - ominous NPC encounter
        if self.has_met("The Warning"):
            self.day_event()
            return
        
        self.meet("The Warning")
        type.type("An old woman shuffles up to your car. Her eyes are milky white-blind, or close to it.")
        print("\n")
        type.type(quote("You're the one,") + " she whispers. " + quote("I've seen you in my dreams."))
        print("\n")
        type.type("She presses a gnarled hand against your window.")
        print("\n")
        type.type(quote("The million isn't the end. It's the beginning. Of what, I don't know. But I see fire. I see cards. I see a choice that will define everything."))
        print("\n")
        type.type("She coughs-a wet, rattling sound.")
        print("\n")
        type.type(quote("Be careful what you wish for. Sometimes the universe gives you exactly what you ask for. And sometimes that's the worst thing that could happen."))
        print("\n")
        type.type("She shuffles away before you can respond, disappearing around a corner.")
        print("\n")
        type.type("You sit in silence for a long time, thinking about her words.")
        print("\n")

    def the_celebration(self):
        # One-Time - premature celebration
        if self.has_met("Premature Celebration"):
            self.day_event()
            return
        
        self.meet("Premature Celebration")
        type.type("A group of people approach your car. They're carrying a cake and balloons.")
        print("\n")
        type.type(quote("CONGRATULATIONS!") + " they shout.")
        print("\n")
        type.type("You blink. Did you already hit a million and forget?")
        print("\n")
        type.type("The leader of the group checks his phone, then looks at your car, then back at his phone.")
        print("\n")
        type.type(quote("Oh. Wrong car. Sorry."))
        print("\n")
        type.type("They shuffle away with their cake and balloons, leaving you very confused.")
        print("\n")
        type.type("But hey, they did drop a slice of cake in your lap. It's chocolate.")
        print("\n")
        self.heal(10)

    def final_dream(self):
        # One-Time - climactic dream sequence
        if self.has_met("Final Dream"):
            self.day_event()
            return
        
        if self.get_tom_dreams() < 2 or self.get_frank_dreams() < 2 or self.get_oswald_dreams() < 2:
            self.day_event()
            return
        
        self.meet("Final Dream")
        type.type("You fall asleep and find yourself in a vast, empty casino. The lights are off. The slot machines are silent. The tables are empty.")
        print("\n")
        type.type("Except one.")
        print("\n")
        type.type("The Dealer sits at a blackjack table, illuminated by a single overhead lamp. He beckons you forward.")
        print("\n")
        type.type(quote("You've come a long way,") + " he says. " + quote("Farther than most."))
        print("\n")
        type.type("He shuffles the cards.")
        print("\n")
        type.type(quote("But the final test isn't about skill. It isn't about luck. It's about something else entirely."))
        print("\n")
        type.type("He deals you a hand. You look at your cards. They're blank.")
        print("\n")
        type.type(quote("The cards only show what you already know,") + " he says. " + quote("And you already know how this ends."))
        print("\n")
        type.type("You wake up with a certainty that wasn't there before.")
        print("\n")
        type.type(yellow(bright("Whatever happens tonight, you're ready.")))
        self.add_status("Lucky")
        print("\n")

    def the_offer(self):
        # One-Time - final temptation
        if self.has_met("The Offer"):
            self.day_event()
            return
        
        self.meet("The Offer")
        type.type("A limousine pulls up next to your wagon. The back window rolls down, revealing a distinguished-looking man in an expensive suit.")
        print("\n")
        type.type(quote("You're the one who's been winning. I've heard a lot about you."))
        print("\n")
        type.type("He smiles, but it doesn't reach his eyes.")
        print("\n")
        type.type(quote("I represent... certain interested parties. We've been watching your progress with great interest."))
        print("\n")
        type.type(quote("Here's my offer: walk away right now, and I'll double whatever you have. Cash. No questions asked."))
        print("\n")
        current = self.get_balance()
        type.type("That would be " + green(bright("${:,}".format(current * 2))) + ". More than your goal.")
        print("\n")
        answer = ask.yes_or_no("Accept the offer? ")
        if answer == "yes":
            type.type("The man smiles.")
            print("\n")
            type.type(quote("Smart. Very smart."))
            print("\n")
            type.type("A briefcase is pushed out the window. It's full of cash.")
            print("\n")
            type.type(quote("Pleasure doing business with you. I suggest you leave town immediately. And never come back to any casino. Ever."))
            print("\n")
            type.type("The limo drives away.")
            print("\n")
            type.type("You stare at the briefcase. You won. But... did you really?")
            print("\n")
            self.change_balance(current)
            type.type(yellow(bright("You got what you wanted. But something feels hollow.")))
        else:
            type.type("The man's smile fades.")
            print("\n")
            type.type(quote("Interesting. Most people would've taken the money."))
            print("\n")
            type.type("He leans forward.")
            print("\n")
            type.type(quote("You're either very brave or very stupid. Time will tell which."))
            print("\n")
            type.type("The window rolls up and the limo drives away.")
            print("\n")
            type.type("You made your choice. Now you have to live with it.")
            print("\n")
            type.type(yellow(bright("The true test lies ahead.")))
        print("\n")

    # ==========================================
    # SECRET EVENTS - NEARLY TIER
    # ==========================================
    
    def exactly_999999(self):
        # SECRET - One dollar away
        if self.get_balance() != 999999:
            self.day_event()
            return
        
        type.type("You count your money. Once. Twice. Three times.")
        print("\n")
        type.type(green(bright("$999,999")) + ".")
        print("\n")
        type.type("One dollar. You are ONE DOLLAR away from a million.")
        print("\n")
        type.type("The universe has a cruel sense of humor.")
        print("\n")
        type.type("As if in response to your thoughts, a single dollar bill blows against your window, carried by the wind.")
        print("\n")
        type.type("You scramble out of the car and grab it before it can fly away.")
        print("\n")
        type.type(green(bright("$1,000,000.")))
        print("\n")
        type.type("You did it. You actually did it.")
        print("\n")
        self.change_balance(1)
        type.type(yellow(bright("ONE. MILLION. DOLLARS.")))
        print("\n")
        type.type(yellow(bright("But your story isn't over yet...")))
        print("\n")

    def all_dreams_complete(self):
        # SECRET - All three dream sequences complete
        if self.get_tom_dreams() != 3 or self.get_frank_dreams() != 3 or self.get_oswald_dreams() != 3:
            self.day_event()
            return
        
        if self.has_met("All Dreams Complete"):
            self.day_event()
            return
        
        self.meet("All Dreams Complete")
        type.type("You wake up with tears on your face. But not from sadness.")
        print("\n")
        type.type("You remember everything now. Rebecca. Nathan. Johnathan.")
        print("\n")
        type.type("The Dealer. His rage. His scar. His glass eye.")
        print("\n")
        type.type("The casino. The money. The drink. The double.")
        print("\n")
        type.type("It all makes sense now. Every dream was a piece of a puzzle you didn't know you were solving.")
        print("\n")
        type.type(yellow(bright("You know who you are.")))
        print("\n")
        type.type(yellow(bright("You know why you're here.")))
        print("\n")
        type.type(yellow(bright("And you know what you have to do.")))
        print("\n")
        self.heal(100)
        self.add_status("Lucky")
        print("\n")
        
    # Conditional
        
    # One-Time
        
    # One-Time Conditional
    def cow_army(self):
        if not self.has_met("Betsy") or not self.has_danger("Betsy Army"):
            self.day_event()
            return

        self.lose_danger("Betsy Army")
        type.type("You wake up to the sound of thousands of hoofsteps, getting closer to your wagon. You jump out of your seat, to see the street flooded with cows, all getting closer to your vehicle. ")
        type.type("At the front of the crowd, is a cow, distinct from the rest. It's Betsy. Of course, it's Betsy. God fucking dammit.")
        print("\n")
        type.type("Betsy leads the herd to your wagon, and as you roll the window down, all you can hear are the hundreds upon hundreds of moos, from each of the angry cows. ")
        print("\n")
        type.type("Betsy, and the rest of the cows, all stare into your soul, then look over at the seat next to you. It appears Betsy and her friends are interested in your pile of money. ")
        print()
        type.type("Do you feed Betsy and her friends? ")
        while True:
            answer = ask.yes_or_no("Moo? ")
            if answer == "yes":
                type.type("You throw a bunch of bills into the crowd of cows, worth " + green(bright("$100,000")) + ". Betsy catches a bill, chews it up, then spits it out into your face.")
                self.change_balance(-100000)
                random_chance = random.randrange(4)
                if (random_chance == 0) or (self.__balance <100001):
                    type.type("Betsy moos, then smiles. The rest of the cows moo in harmony, and the crowd begins to march down the road, happy as can be.")
                    break
                else:
                    type.type("Betsy moos, then stares you down. The rest of the cows begin to moo. They don't seem to be done with you.")
                    print()
                    type.type("Do you feed Betsy? ")
            elif answer == "no":
                type.type("Betsy moos, then charges your vehicle. The rest of the cows start attacking your wagon, shattering the windows, knocking off the tires, and pummeling the doors.")
                print("\n")
                type.slow(red(bright("A pane of glass explodes next to you, sending shards into your face. One catches your eye, and you scream in pain. The cows continue to attack you, and your money is spiraling all around. Unable to see, and covered in blood, you close your eyes, and let yourself succumb to the army of cows. You won, Betsy, you won.")))
                self.kill()
                break
        print("\n")

    def final_interrogation(self):
        if not self.has_met("Interrogator") or not self.has_danger("Final Interrogation"):
            self.day_event()
            return

        self.lose_danger("Final Interrogation")
        type.type("You wake up, and through your windshield, you see a car parked right in front of you. You can feel your blood start to boil. What's this guy's problem? As you open the door and get out of your car, you notice the man in his bright red suit, once again peering into your trunk.")
        print("\n")
        type.type("The man sees you, and walks up to you, with a pistol holstered to his waist.")
        print("\n")
        type.type(space_quote("You. I'm done playing around. It's time to move. I mean it."))
        type.type("You look down at the gun on his waist. It looks fancy, and certainly deadly.")
        print("\n")
        type.type(quote("I wouldn't test me if I were you. It's time to go, now."))
        print("\n")
        type.type(space_quote("Will you leave?"))
        answer = ask.yes_or_no(space_quote("Answer me. "))
        if answer == "yes":
            type.type(quote("That's great. Fantastic. But I don't believe a word that comes out of your filthy mouth. Prove it. Leave. Go away. GET OUT."))
            print("\n")
            type.type("You are fueled with anger. Who is this guy, and what gives him the right to harass you? All for being homeless? No longer. You reach for the gun on his waist.")
            print("\n")
            random_chance = random.randrange(4)
            if random_chance == 0:
                type.slow(red("Before you get the chance to grab it, the man steps back, unholsters the pistol, then fires three shots into your chest. The glass behind you shatters, and you fall to your knees in the street."))
                print("\n")
                type.slow(red(quote("You should've just listened to me man! All you had to do was listen! Move, live somewhere else. Find a home, anything. But no! You just had to live in your car, like the homeless piece of shit that you are!")))
                print("\n")
                type.slow(red(bright("The man kicks you down, and steps on your chest, causing the bullet holes to leak blood onto the concrete below you. As you feel yourself beginning to fade away, you watch the man lift his pistol to your head, and pull the trigger.")))
                self.kill()
            else:
                type.type("You snatch the gun from his holster, and he tackles you to the ground. You fight and struggle, each of you with both hands on the pistol. In the distance, you hear the horn of a freight truck beginning to drive closer. The man punches you in the arm, and it stings. Without thinking twice, you give the man a headbutt, and he falls backwards into the road. You point the gun at the man, and he begins to cry.")
                print("\n")
                type.type(quote("Please, I'm sorry. I didn't mean to cause any of this. I just, I hate seeing people living on the streets, all alone. I was just trying to help you. Just, please, for the love of god, don't hurt me."))
                print("\n")
                type.type("As the man begs for his life, the freight truck continues to draw closer, and the horn gets louder. You point at the truck in the distance, but the man can't see through the tears in his eyes.")
                print("\n")
                type.type(space_quote("Please, I have a family. I have children. My name is Phil. I don't wanna die. I'm too young. I can't die. I can't die. I ca-"))
                type.type("You watch as the freight truck crushes Phil, and continues down the road. Nothing remained but the splotches of blood that splattered the road where he once stood.")
                print("\n")
                type.type("After sitting a while, and recollecting your thoughts, you bring the pistol over to Phil's car, and throw it onto the passenger seat. Looking inside, the car has dice hanging on the mirror, and is filled to the brim with red suits. On the dashboard sits a photo of Phil, his wife, and his three kids, all wearing bright red suits. Phil might've been crazy, but at least he was consistent.")
                print("\n")
                type.type("You get in the car, and drive it down the road, before turning into the woods. You drive a mile in, before parking the car before the lake. You get out, and push the car into the water, watching as it submerges.")
                print("\n")
                return
        elif answer == "no":
            type.type(quote("Really? You really want to do that? I warned you, man."))
            print("\n")
            type.type("The man pulls out his pistol, and points it at you. You lift your hands above your head, before quickly reaching for the pistol.")
            print("\n")
            random_chance = random.randrange(3)
            if random_chance == 0:
                type.slow(red("Before you get the chance to grab it, the man steps back, then fires three shots into your chest. The glass behind you shatters, and you fall to your knees in the street."))
                print("\n")
                type.slow(red(quote("Nice try, man! You should've just listened to me! All you had to do was listen! Move, live somewhere else. Find a home, anything. But no! You just had to live in your car, like the homeless piece of shit that you are!")))
                print("\n")
                type.slow(red(bright("The man kicks you down, and steps on your chest, causing the bullet holes to leak blood onto the concrete below you. As you feel yourself beginning to fade away, you watch the man lift his pistol to your hand, and pull the trigger.")))
                self.kill()
            else:
                type.type("You snatch the gun from his hands, and he tackles you to the ground. You fight and struggle, each of you with both hands on the pistol. The man punches you in the arm, and it stings. Without thinking twice, you give the man a headbutt, and he falls backwards into the road. You point the gun at the man, and he begins to cry.")
                print("\n")
                type.type(quote("Please, I'm sorry. I didn't mean to cause any of this. I just, I hate seeing people living on the streets, all alone. I was just trying to help you. Just, please, for the love of god, don't hurt me."))
                print("\n")
                type.type("As the man begs for his life, you cock the gun. You point pistol at the man, and he continues to cry.")
                print("\n")
                type.type(space_quote("Please, I have a family. I have children. My name is Phil. I don't wanna die. I'm too young. I can't die. I can't die. I ca-"))
                type.type("You pull the trigger, and Phil becomes quiet. His blood covers the street, but at least his red suit still looks good as new.")
                print("\n")
                type.type("After sitting a while, and recollecting your thoughts, you drag Phil over to his car. You stuff him into the trunk, and throw his pistol onto the passenger seat. Looking inside, the car has dice hanging on the mirror, and is filled to the brim with red suits. On the dashboard sits a photo, of Phil, his wife, and his three kids, all wearing bright red suits. Phil might've been crazy, but at least he was consistent.")
                print("\n")
                type.type("You get in the car, and drive it down the road, before turning into the woods. You drive a mile in, before parking the car before the lake. You get out, and push the car into the water, watching as it submerges.")
                print("\n")
                return

    # SUZY STORYLINE - NEARLY THERE DAY (FINALE)
    def gift_from_suzy(self):
        # Only triggers if Suzy storyline is complete (has favorite animal)
        # This is the GOOD ending - requires having been kind to Suzy
        if self.get_favorite_animal() == None or self.has_met("Suzy Finale"):
            self.day_event()
            return
        
        self.meet("Suzy Finale")
        
        type.type("You wake up to an unusual sound-not sneakers on concrete, but the crunch of grass. You sit up and see Suzy standing outside your wagon, holding something behind her back.")
        print("\n")
        type.type("She's not jump roping. For the first time ever, she's standing completely still.")
        print("\n")
        type.type(quote("Hi, " + self.__name + ". I made you something."))
        print("\n")
        type.type("Suzy pulls out a small stuffed animal from behind her back. It's a " + self.get_favorite_animal() + ", crudely sewn together with mismatched fabric, but clearly made with love. The fabric is " + self.get_favorite_color() + ", your favorite color.")
        print("\n")
        type.type(quote("I remembered everything you told me. Your favorite color, your favorite animal. I made it myself! Do you like it?"))
        print("\n")
        type.type("You take the stuffed " + self.get_favorite_animal() + ". Despite its imperfect stitching, it's one of the most thoughtful gifts anyone has ever given you.")
        print("\n")
        type.type(quote("I wanted to say thank you. For always being nice to me. Most grown-ups ignore me, or tell me to go away. But you always talked to me like I was a real person."))
        print("\n")
        type.type("Suzy sniffles a little.")
        print("\n")
        type.type(quote("I hope you find what you're looking for, " + self.__name + ". I really do."))
        print("\n")
        type.type("Before you can respond, Suzy picks up her jump rope and starts bouncing away.")
        print("\n")
        type.type(quote("Bye bye! Maybe I'll see you again someday! But probably not. I'm moving away with my aunt. She found me! She's really nice. I'll think of you when I see " + self.get_favorite_animal() + "s!"))
        print("\n")
        type.type("And with that, Suzy jump ropes into the distance for the last time, disappearing around the corner. You look down at the stuffed " + self.get_favorite_animal() + " in your hands.")
        print("\n")
        type.type(yellow(bright("Some goodbyes are harder than others.")))
        self.add_item("Suzy's Gift")
        self.restore_sanity(random.choice([5, 6, 7, 8]))  # Deeply restores sanity
        print("\n")

    def suzy_the_snitch(self):
        # Only triggers if Suzy storyline is complete AND this is checked
        # This is the BAD ending - happens if player was mean to Suzy
        if self.get_favorite_animal() == None or self.has_met("Suzy Finale"):
            self.day_event()
            return
        
        self.meet("Suzy Finale")
        
        type.type("You wake up to the sound of a car engine and flashing lights. A police cruiser has pulled up right next to your wagon. Your heart sinks.")
        print("\n")
        type.type("A cop steps out, notepad in hand. And there, in the passenger seat of the cruiser, sits Suzy, still holding her jump rope.")
        print("\n")
        type.type("The cop approaches your window.")
        print("\n")
        type.type(quote("Are you " + self.__name + "? This young lady here says she knows you."))
        print("\n")
        type.type("Suzy waves at you through the window, an innocent smile on her face.")
        print("\n")
        type.type(quote("That's him, officer! The homeless man I told you about! His favorite color is " + self.get_favorite_color() + " and his favorite animal is a " + self.get_favorite_animal() + "! He told me EVERYTHING!"))
        print("\n")
        type.type("The cop looks at his notepad, then back at you.")
        print("\n")
        type.type(quote("Sir, we've had reports of someone matching your description involved in some... questionable activities in this area. We're going to need you to come with us for questioning."))
        print("\n")
        type.type("Suzy presses her face against the police car window.")
        print("\n")
        type.type(quote("Bye bye, " + self.__name + "! I hope you enjoy jail! They probably have " + self.get_favorite_animal() + "s there! Maybe!"))
        print("\n")
        type.type("Before you can protest or explain, you're in handcuffs and being led to the back of the cruiser. Suzy waves at you the whole time.")
        print("\n")
        type.slow(red(bright("You spend the rest of your days in a cell, thinking about how you probably shouldn't have trusted a jump-roping little girl with all your personal information. The last thing you remember before everything fades to black is the distant sound of sneakers on concrete, and a jump rope hitting the ground.")))
        print("\n")
        self.kill()


    # Poor Nights (1 - 1,000)
    # Everytime
    def ditched_wallet(self):
        type.type("Bored out of your mind, you decide to wander along the side of the road, just to get a change of scenery from the dusty leather seats of your wagon. ")
        type.type("As you take step after step over the asphalt, you notice a ditched wallet, just laying there. I guess it's yours now. ")
        print("\n")
        random_chance = random.randrange(2)
        if random_chance == 0:
            worth = random.randint(65, 120)
        else:
            worth = random.randint(7, 50)
        type.type("Inside the wallet, you find " + green(bright("$" + str(worth))) + " dollars.")
        self.change_balance(worth)

    def went_jogging(self):
        type.type("After spending an hour sitting in your car doing nothing, you feel like you should get some exercise. You get out of the wagon, and begin to jog down the road.")
        print("\n")
        type.type("A couple hours go by, and while jogging back, you see the wagon in the distance. ")
        random_chance = random.randrange(3)
        if random_chance == 0:
            type.type("But, right as you get to your car, you trip over a stone on the ground, and scrape your knee hard. Blood begins to drip down your leg. That's a bummer.")
            print("\n")
            self.hurt(random.choice([5, 10, 15]))
            self.add_injury("Scraped Knee")
            return
        else:
            type.type("You get back to the car, and get in, out of breath from your trip. You start the wagon and run the AC, and you feel good inside.")
            print("\n")
            self.heal(random.choice([5, 10, 15]))
            return

    def woodlands_path(self):
        self.meet("Woodlands Path Event")
        type.type("After wandering from your vehicle, you find yourself deep in the woods. Squirrels run by and up into the trees. The sun hits every branch and casts a shadow below. And you wander on a natural path, journeying into the unknown.")
        print("\n")
        random_chance = random.randrange(3)
        if random_chance == 0:
            type.type("As you walk along the path, you find a mother deer, with two children, walking the path towards you. As you get closer, the mother appears cautious, but then runs in your direction, before stopping before you. ")
            type.type("Her two children follow behind, and before you know it, the three of them wait in front of you.")
            print("\n")
            type.type("You put your hand out, and pet the mother deer. She makes a happy squeak noise, and wags her tail. She touches her head to yours, then continues down the path, with her two children following.")
            print("\n")
            type.type("Eventually, you get to the end of the path, and find the main road. You follow it back to your wagon, and take a seat, to rest for a moment.")
            print("\n")
            return
        elif random_chance == 1:
            type.type("As you walk along the path, you notice someone leaning against a tree in front of you. As you get closer, you notice that the person's face is blue, their eyes are bloodshot, and they don't appear to be breathing.")
            print("\n")
            type.type("You begin to panic, before thinking through the situation. They're already dead, so there's nothing you can do to help them. Maybe they had some money on them? I mean, they're not gonna use it. Why shouldn't you?")
            print()
            type.type("Do you search the body? ")
            answer = ask.yes_or_no()
            if answer == "yes":
                type.type("You rummage through the pockets, trying to find anything worthwhile. ")
                random_chance = random.randrange(4)
                if random_chance == 0:
                    self.add_status("Hepatitis")
                    type.type("As you do so, you notice the body begin to move. It looks up at you, screams, then coughs blood all over you. You freak out, before running back down the path the way you came.")
                    print("\n")
                    type.type("You make it back to your car, and find some old clothes to wipe the blood off your face. Great, just great. You already start to feel under the weather.")
                    print("\n")
                    return
                else:
                    type.type("After a minute of digging, you manage to find a wallet. Score!")
                    print("\n")
                    worth = random.randint(100, 150)
                    type.type("Inside the wallet, you find " + green(bright("$" + str(worth))) + " dollars.")
                    self.change_balance(worth)
                    type.type("You leave the dead body, and continue down the path, until the forest opens up to the main road. You follow the road back to your wagon, with your winnings in hand.")
                    print("\n")
                    return
            elif answer == "no":
                type.type("While this body might be the body of a rich man, judging by the situation, it's very unlikely. Plus, dead bodies tend to be unsanitary. No, this body was simply not worth searching.")
                print("\n")
                type.type("You continue down the path, before the forest opens up to the main road. You follow the road back to your wagon, and sit. You rest for a while.")
                print("\n")
                return
        else:
            type.type("You walk, and walk, and walk further down the path, before the forest opens up to the main road. You follow the road back to your wagon, wondering if there was anything you missed. At least you made it back safe and sound.")
            print("\n")
            return

    # RABBIT CHASE CHAIN - POOR NIGHT
    def chase_the_rabbit(self):
        # First rabbit chase - always fails, starts the chain
        if self.get_rabbit_chase() != 0:
            self.night_event()
            return
        
        type.type("As you're walking along the side of the road, something catches your eye. A flash of white, darting between the bushes. A rabbit!")
        print("\n")
        type.type("Without thinking, you give chase. The little creature bounds ahead of you, zigging and zagging through the underbrush with seemingly effortless grace.")
        print("\n")
        type.type("You run and run, but no matter how fast you go, the rabbit stays just out of reach. Its white tail bobs mockingly in the moonlight.")
        print("\n")
        type.type("Finally, you stop, hands on your knees, gasping for breath. When you look up, the rabbit is gone, vanished into the night like it was never there.")
        print("\n")
        type.type(yellow("You trudge back to your wagon, defeated. But something tells you this isn't the last time you'll see that rabbit."))
        self.advance_rabbit_chase()
        print("\n")
                

    # Cheap Nights (1,000 - 10,000)
    # Everytime
    def woodlands_river(self):
        self.meet("Woodlands River Event")
        type.type("After wandering from your vehicle, you find yourself deep in the woods. Deer dart by you. Trees branches sway back and forth. And you wander along a river, journeying into the unknown.")
        print("\n")
        random_chance = random.randrange(3)
        if random_chance == 0:
            type.type("As you walk further, you stumble across a large brown bear, bathing in the river. ")
            if self.has_item("Quiet Sneakers"):
                print("\n")
                type.type("Thank goodness you're wearing your " + magenta(bright("Quiet Sneakers")) + "!")
                print("\n")
                type.type("You turn and run back up the riverbank, never looking back. Eventually, you make it out of the woods, and return to your car, safe and sound.")
                print("\n")
                self.update_quiet_sneakers_durability()
                return
            else:
                type.type("Right as you're about to turn around, you step on a branch, which makes a loud crunching noise. ")
                print("\n")
                random_chance_2 = random.randrange(2)
                if random_chance_2 == 0:
                    type.type("The bear sits up from the water, and glares at you. Before you get a chance to react, the bear charges at you. He swipes at your leg. He bites your arm. He punches your neck. My, what a beating he gave you.")
                    print("\n")
                    self.hurt(75)
                    type.type("Thankfully, you're able to play dead, just long enough for the bear to walk away without killing you. Somehow, you get up, and limp your way back to your wagon.")
                    print("\n")
                    type.type("The damage inflicted from the bear is serious and severe. It's probably a good idea to see the doctor tomorrow, when they're open again. In the meantime, you wrap yourself up with spare clothes, and go on with your life.")
                    self.add_injury("Severed Skin")
                    print("\n")
                    return
                elif random_chance_2 == 1:
                    type.type("Thankfully, it seems that the bear doesn't notice you. You quietly step away, before running back up the riverbank. Eventually, you make it out of the woods, and back to your wagon, safe and sound. That could've gone a lot worse!")
                    print("\n")
                    return
        elif (random_chance == 1) and not (self.has_item("Map")):
            type.type("As you walk further, you stumble across an old treasure chest, sitting in the river, the water flowing around it. ")
            type.type("Walking closer, you wade the water to get to the chest, and open up the lid. Inside, you find a large paper drawing. Opening it up, you realize that it's a map that resembles the town you're parked just outside of. Down one of the side roads, there's an old bridge with a star underneath it. The caption reads 'To those who wish to visit Marvin, just go to the bridge, and follow the stars.'")
            print("\n")
            self.add_item("Map")
            type.type("You got the " + magenta(bright("Map")) + "! You can now drive to Marvin's Mystical Merchandise!")
            type.type("Without a second thought, you pocket the map, and turn back, following the riverbank home.")
            print("\n")
            return
        else:
            type.type("You keep walking, and keep walking, and keep walking, and eventually, the woods clear up, and you're back on the main road. You follow it back to your car, wondering if there was anything else to see. Well, at least you're home, safe and sound.")
            print("\n")
            return

    def woodlands_field(self):
        self.meet("Woodlands Field Event")
        type.type("After wandering from your vehicle, you find yourself in a wide open field. The grass comes up to your waist, golden and dry, rustling with every breeze. Crickets sing their evening song.")
        print("\n")
        random_chance = random.randrange(4)
        if random_chance == 0:
            type.type("As you wade through the tall grass, you notice something odd. About fifty yards ahead, there's a figure standing perfectly still. Just... standing there. Watching you.")
            print("\n")
            type.type("You stop walking. The figure doesn't move. It's too far to make out any details, just a dark silhouette against the fading sky.")
            print("\n")
            type.type("Do you approach the figure?")
            answer = ask.yes_or_no()
            if answer == "yes":
                type.type("You push through the grass toward the figure. As you get closer, you realize...")
                print("\n")
                reveal = random.randrange(3)
                if reveal == 0:
                    type.type("It's a scarecrow. An old, rotting scarecrow. You laugh at yourself. But as you turn to leave, you notice something glinting at its base.")
                    print("\n")
                    worth = random.randint(150, 400)
                    type.type("Someone stashed a tin box here. Inside: " + green(bright("$" + str(worth))) + ".")
                    self.change_balance(worth)
                    print("\n")
                elif reveal == 1:
                    type.type("It's a person. A man, elderly, with a shotgun. He squints at you.")
                    print("\n")
                    type.type(quote("This is private property. Road's that way. Don't come back."))
                    print("\n")
                else:
                    type.type("It's a wooden post with old clothes hanging from it. Not a person at all.")
                    print("\n")
            else:
                type.type("You decide not to risk it. You turn and walk back the way you came.")
                print("\n")
        elif random_chance == 1:
            type.type("Your foot catches on something hidden in the grass - a battered duffle bag.")
            print("\n")
            type.type("Do you open it?")
            answer = ask.yes_or_no()
            if answer == "yes":
                outcome = random.randrange(3)
                if outcome == 0:
                    worth = random.randint(300, 800)
                    type.type("Inside: bundles of cash. You pocket " + green(bright("$" + str(worth))) + ".")
                    self.change_balance(worth)
                    print("\n")
                elif outcome == 1:
                    type.type("Inside: old clothes and a photograph of a family you don't recognize. You leave it.")
                    print("\n")
                else:
                    type.type("Wasps pour out in an angry swarm. You sprint through the field, getting stung.")
                    self.hurt(random.randint(10, 20))
                    print("\n")
            else:
                type.type("You leave the bag alone. Nothing good ever came from opening mysterious bags.")
                print("\n")
        elif random_chance == 2:
            type.type("You stumble upon an abandoned campsite. A collapsed tent, empty beer cans, scattered belongings.")
            print("\n")
            type.type("Do you search it?")
            search = ask.yes_or_no()
            if search == "yes":
                find = random.randrange(3)
                if find == 0:
                    type.type("You find a cooler with some sodas still cold. You also pocket a rusty pocket knife.")
                    self.heal(random.randint(5, 15))
                    print("\n")
                elif find == 1:
                    type.type("As you're rummaging, you hear a click. A tripwire. Nothing happens, but you run anyway.")
                    print("\n")
                else:
                    worth = random.randint(50, 150)
                    type.type("You find a wallet with " + green(bright("$" + str(worth))) + " inside.")
                    self.change_balance(worth)
                    print("\n")
            else:
                type.type("You leave the campsite undisturbed. Some places are better left alone.")
                print("\n")
        else:
            type.type("You walk through the field until it gives way to a dirt road. The stars are coming out.")
            print("\n")
            type.type("You follow the road back to your wagon, feeling small under the vast sky.")
            print("\n")

    def swamp_stroll(self):
        self.meet("Swamp Stroll Event")
        type.type("After wandering from your vehicle, you find yourself at the edge of a swamp. The air is thick and humid, smelling of rot and growing things. Cypress trees rise from the murky water, draped in Spanish moss.")
        print("\n")
        random_chance = random.randrange(4)
        if random_chance == 0:
            type.type("A massive snake, thick as your arm, slithers across your path. It stops, coils, and watches you.")
            print("\n")
            type.type("Do you try to go around it, or wait for it to move?")
            choice = input("(around/wait): ").strip().lower()
            if choice == "around":
                if random.random() < 0.6:
                    type.type("You give the snake a wide berth. It watches but doesn't strike. You make it past.")
                    print("\n")
                else:
                    type.type("The snake lunges. Fangs sink into your calf. You stumble away as it slithers off.")
                    self.hurt(random.randint(15, 30))
                    self.lose_sanity(random.choice([2, 3, 4]))  # Sudden violence is disturbing
                    print("\n")
            else:
                type.type("You stand perfectly still. After an eternity, the snake uncurls and slides into the water.")
                print("\n")
        elif random_chance == 1:
            type.type("You spot something pale floating in the water. At first you think it's a log, but then you see the fingers.")
            print("\n")
            type.type("It's a body. Face down, bloated. Do you search it?")
            answer = ask.yes_or_no()
            if answer == "yes":
                type.type("You wade in and flip the body over. The face is... not something you want to remember.")
                self.lose_sanity(random.choice([3, 4, 5]))  # Dead body is traumatic
                print("\n")
                search_result = random.randrange(3)
                if search_result == 0:
                    worth = random.randint(200, 500)
                    type.type("You find a waterlogged wallet with " + green(bright("$" + str(worth))) + " inside.")
                    self.change_balance(worth)
                    print("\n")
                elif search_result == 1:
                    type.type("Something moves in the water nearby. A pair of eyes. Alligator. You back away slowly.")
                    print("\n")
                else:
                    type.type("The body has nothing of value. Just a dead man in a swamp.")
                    print("\n")
            else:
                type.type("You're not touching that. You find another path.")
                print("\n")
        elif random_chance == 2:
            type.type("You hear music. Faint, plucking strings. A banjo? Out here?")
            print("\n")
            type.type("You find an old man on a stump, playing a battered instrument. No teeth. Clothes more patches than fabric.")
            print("\n")
            type.type("He stops when he sees you. " + quote("Don't get many visitors out here."))
            print("\n")
            type.type("Do you sit and listen?")
            answer = ask.yes_or_no()
            if answer == "yes":
                type.type("The music is haunting, beautiful. When he finishes, he hands you some crumpled bills.")
                print("\n")
                type.type(quote("For your company. Gets lonely out here."))
                worth = random.randint(50, 150)
                type.type("You pocket the " + green(bright("$" + str(worth))) + ".")
                self.change_balance(worth)
                print("\n")
            else:
                type.type(quote("Suit yourself.") + " He goes back to playing as you walk away.")
                print("\n")
        else:
            type.type("You wander the edge of the swamp, watching for gators. Nothing eventful happens.")
            print("\n")
            type.type("Eventually you find your way back to your wagon, mud caked on your shoes.")
            print("\n")

    # SUZY STORYLINE - CHEAP NIGHT
    def whats_my_favorite_color(self):
        # Only triggers if Suzy has been met and favorite color not yet set
        if self.__name == None or self.get_favorite_color() != None:
            self.night_event()
            return
        
        type.type("As you're sitting in your wagon, watching the sunset paint the sky in brilliant hues, you hear a familiar sound-sneakers scratching against concrete, accompanied by the rhythmic slap of a jump rope.")
        print("\n")
        type.type(quote("Hey! " + self.__name + "! It's me, Suzy!"))
        print("\n")
        type.type("Suzy skips over to your window, pigtails bouncing, still jump roping in place.")
        print("\n")
        type.type(quote("I was just thinking about you! I have a SUPER important question. Ready?"))
        print("\n")
        type.type(quote("What's your favorite color?"))
        print("\n")
        
        color = str(input("Your favorite color: "))
        self.set_favorite_color(color)
        
        type.type(quote(color + "? That's a great color! That's like... the color of... um..."))
        print("\n")
        type.type("Suzy squints, thinking really hard.")
        print("\n")
        type.type(quote("The color of " + color + " things! Yeah! I knew that."))
        print("\n")
        type.type(quote("Okay, gotta go! The stars are coming out and mom says I shouldn't be out when it's dark. Even though she's not here to tell me that anymore. Bye " + self.__name + "!"))
        print("\n")
        type.type("Suzy continues jump roping down the road, disappearing into the twilight.")
        print("\n")

    # RABBIT CHASE CHAIN - CHEAP NIGHT
    def chase_the_second_rabbit(self):
        # Second rabbit chase - still fails
        if self.get_rabbit_chase() != 1:
            self.night_event()
            return
        
        type.type("There it is again. That same white rabbit, sitting in the middle of the road, watching you with those beady little eyes.")
        print("\n")
        type.type(quote("You again!") + " you mutter, already breaking into a run.")
        print("\n")
        type.type("The rabbit springs away, leading you on another wild chase through the brush. This time, you're determined. You've learned its tricks. You anticipate its zigs and zags.")
        print("\n")
        type.type("But still, every time you get close enough to grab it, it slips away. It's almost like it's playing with you.")
        print("\n")
        type.type("Once again, you end up empty-handed, watching the rabbit disappear into a thicket. It almost looks like it's... laughing?")
        print("\n")
        type.type(yellow("You return to your wagon, once again defeated. But you're not giving up. Not yet."))
        self.advance_rabbit_chase()
        print("\n")
   
    # Modest Nights (10,000 - 100,000)
    # Everytime
    def swamp_wade(self):
        self.meet("Swamp Wade Event")
        type.type("You wade waist-deep through the swamp, the water cold and thick with silt. Every step is a struggle, and unseen things brush against your legs. The air is heavy with the scent of decay and blooming lilies. Fireflies blink in the darkness like tiny green stars.")
        print("\n")
        event = random.choice(["leech", "nectar", "witch", "rowboat", "none"])
        if event == "leech":
            type.type("Something latches onto your leg. Then another. And another. LEECHES.")
            print("\n")
            type.type("Do you try to pull them off, or burn them off with your lighter?")
            choice = input("(pull/burn): ").strip().lower()
            if choice == "burn":
                type.type("You flick your lighter and hold it near your skin. The leeches squirm and drop off one by one, but you burn yourself in the process.")
                print("\n")
                self.hurt(random.randint(5, 10))
                type.type("At least you got them all. The welts itch for days.")
            else:
                type.type("You rip them off one by one, gagging. Each one takes a little chunk of you with it.")
                print("\n")
                self.hurt(random.randint(10, 20))
                type.type("You check yourself obsessively for hours afterwards. You HATE leeches.")
            print("\n")
        elif event == "nectar":
            type.type("Your foot kicks something solid in the murky water. You reach down and pull up an old mason jar, sealed tight. Inside is a thick, golden liquid - honey? Some kind of moonshine?")
            print("\n")
            type.type("The label is faded but you can make out: 'Granny's Swamp Nectar - For What Ails Ya'")
            print("\n")
            type.type("Do you drink it, save it, or toss it?")
            choice = input("(drink/save/toss): ").strip().lower()
            if choice == "drink":
                outcome = random.randrange(3)
                if outcome == 0:
                    type.type("It tastes like honey and gasoline. Your throat burns, but then... warmth spreads through your body. You feel incredible.")
                    self.heal(random.randint(25, 50))
                    print("\n")
                elif outcome == 1:
                    type.type("It's just honey. Really old, fermented honey. You feel a pleasant buzz and your cuts seem to heal faster.")
                    self.heal(random.randint(10, 25))
                    print("\n")
                else:
                    type.type("You gag and spit it out. That was NOT honey. You spend the next hour doubled over in the reeds.")
                    self.hurt(random.randint(5, 15))
                    print("\n")
            elif choice == "save":
                type.type("You pocket the jar. Could be useful. Could be poison. Only one way to find out, and it won't be tonight.")
                self.add_item("Granny's Swamp Nectar")
                print("\n")
            else:
                type.type("You toss it back into the swamp. Some things are better left unknown.")
                print("\n")
        elif event == "witch":
            type.type("A small wooden shack emerges from the fog, perched on stilts above the waterline. Candles flicker in the window, and hanging from the porch are bundles of dried herbs, animal bones, and what looks disturbingly like human teeth.")
            print("\n")
            type.type("A woman's voice calls out: " + quote("I know you're out there, sugar. Come on up. The water ain't safe at night."))
            print("\n")
            type.type("Do you approach the witch's shack?")
            choice = ask.yes_or_no()
            if choice == "yes":
                type.type("You climb the rickety ladder. The witch is ancient, her skin like dried leather, but her eyes are sharp and knowing. She's stirring a pot that smells like... chicken soup?")
                print("\n")
                type.type(quote("Sit. Eat. Then we'll talk about what you owe me."))
                print("\n")
                type.type("Do you eat her soup?")
                eat = ask.yes_or_no()
                if eat == "yes":
                    self.heal(random.randint(15, 30))
                    type.type("The soup is delicious. Best thing you've eaten in weeks. The witch watches you with a crooked smile.")
                    print("\n")
                    type.type(quote("Now, for payment. Give me something interesting, or I'll take something interesting."))
                    print("\n")
                    fate = random.choice(["blessing", "curse", "riddle"])
                    if fate == "blessing":
                        type.type("You empty your pockets - lint, a button, a few coins. She plucks a single hair from your head.")
                        print("\n")
                        type.type(quote("This'll do. Now get. And don't die out there. I hate wasted meals."))
                        print("\n")
                        type.type("You feel oddly... lucky.")
                        self.add_status("Witch's Blessing")
                    elif fate == "curse":
                        type.type("She takes a button from your shirt and bites it, then spits into her pot.")
                        print("\n")
                        type.type(quote("Mm. You've got a darkness in you. We'll meet again."))
                        print("\n")
                        type.type("A chill runs down your spine that doesn't go away.")
                        self.add_status("Marked")
                    else:
                        type.type("She hands you a folded paper with strange symbols.")
                        print("\n")
                        type.type(quote("You'll know when you need this. Maybe. If you're clever."))
                        self.add_item("Witch's Riddle")
                else:
                    type.type("You politely decline. The witch's eyes narrow.")
                    print("\n")
                    type.type(quote("Suit yourself. Get out. And watch the water - the gators are hungry tonight."))
            else:
                type.type("You wade past quickly, pretending you didn't hear anything. The candlelight follows you for an uncomfortably long time.")
                print("\n")
        elif event == "rowboat":
            type.type("You nearly trip over something beneath the surface - the edge of a sunken rowboat, half-buried in the muck.")
            print("\n")
            type.type("Do you try to pull it up and search it?")
            search = ask.yes_or_no()
            if search == "yes":
                type.type("You wrestle the rotting boat to the surface. Inside, tangled in algae and crawfish, you find...")
                print("\n")
                find = random.randrange(4)
                if find == 0:
                    worth = random.randint(200, 600)
                    type.type("A waterproof pouch with cash inside. " + green(bright("$" + str(worth))) + ". Someone's emergency fund, now yours.")
                    self.change_balance(worth)
                elif find == 1:
                    type.type("A rusted tackle box full of fishing lures. Worthless to you, but you pocket a pretty one anyway.")
                    self.add_item("Lucky Lure")
                elif find == 2:
                    type.type("A skeleton. An actual human skeleton, grinning up at you. You scramble backwards, nearly drowning.")
                    self.lose_sanity(random.choice([2, 3, 4]))  # Finding human remains
                    print("\n")
                    type.type("In its bony hand is a watch that still ticks. You don't take it. Some things are cursed.")
                else:
                    type.type("Nothing but rot, mud, and a family of very angry crawfish. One pinches your finger hard enough to draw blood.")
                    self.hurt(random.randint(3, 8))
                print("\n")
            else:
                type.type("You leave the boat where it lies. Some secrets are better left at the bottom of the swamp.")
                print("\n")
        else:
            type.type("You make it through, muddy but unharmed. A bullfrog croaks somewhere in the darkness, like it's laughing at you. The swamp keeps its secrets tonight.")
        print("\n")

    def swamp_swim(self):
        self.meet("Swamp Swim Event")
        type.type("You dive into the deeper waters of the swamp, the murky green closing over your head. Down here, the world is muffled and strange. Catfish scatter at your approach. Something large moves in the shadows - probably just a log. Probably.")
        print("\n")
        
        event = random.choice(["alligator", "treasure", "witch", "fishing_shack", "none"])
        if event == "alligator":
            # Gator Tooth Necklace makes gators respect you
            if self.has_item("Gator Tooth Necklace"):
                type.type("You surface for air and find yourself face-to-face with a pair of ancient, unblinking eyes. An alligator. At least ten feet long.")
                print("\n")
                type.type("But then it sees your necklace - teeth from one of its own. It lets out a low rumble... and slowly backs away.")
                type.type(" The swamp creatures know who you are now. They won't bother you.")
                print("\n")
            else:
                type.type("You surface for air and find yourself face-to-face with a pair of ancient, unblinking eyes. An alligator. At least ten feet long. Neither of you moves.")
                print("\n")
                type.type("What do you do?")
                choice = input("(freeze/splash/swim): ").strip().lower()
                
                if choice == "freeze":
                    type.type("You float perfectly still, heart hammering, as the gator drifts closer. Its snout brushes your arm. You don't breathe.")
                    print("\n")
                    if random.randrange(100) < 65:  # 65% chance
                        type.type("After an eternity, it loses interest and glides away into the murk. You don't move for another five minutes.")
                        print("\n")
                    else:
                        type.type("It lunges. You thrash backwards, but not fast enough. Its jaws graze your leg as you scramble for shore.")
                        self.hurt(random.randint(15, 35))
                        self.lose_sanity(random.choice([3, 4, 5]))  # Prehistoric terror
                        print("\n")
                elif choice == "splash":
                    type.type("You slap the water hard, trying to scare it off. The gator startles - ")
                    if random.randrange(100) < 50:  # 50% chance
                        type.type("and retreats! It sinks beneath the surface and disappears. You swim for shore like your life depends on it. Because it does.")
                        print("\n")
                    else:
                        type.type("but it's not scared, it's ANGRY. It surges at you, jaws snapping. You barely escape, bleeding from a dozen cuts.")
                        self.hurt(random.randint(25, 45))
                        self.lose_sanity(random.choice([4, 5, 6]))  # Nearly eaten alive
                        print("\n")
                else:
                    type.type("You swim for it, arms and legs pumping. The gator follows, impossibly fast - ")
                    if random.randrange(100) < 40:  # 40% chance
                        type.type("but you reach the shallows first. You claw up onto solid ground, gasping. The gator watches from the water, patient. It'll be there next time.")
                        print("\n")
                    else:
                        type.type("and catches your ankle. You kick free, but it's already torn through your boot and into skin. You make it to shore, but you're bleeding badly.")
                        self.hurt(random.randint(30, 50))
                        self.lose_sanity(random.choice([5, 6, 7]))  # Death grip terror
                        print("\n")
        elif event == "treasure":
            type.type("Your foot touches something metallic on the bottom. You dive down and pull up a lockbox, heavy and crusted with mud. The lock is rusted but intact.")
            print("\n")
            type.type("Do you try to force it open, or take it with you?")
            choice = input("(force/take): ").strip().lower()
            if choice == "force":
                type.type("You find a rock and bash at the lock. It takes a while, but finally it gives.")
                print("\n")
                outcome = random.randrange(4)
                if outcome == 0:
                    worth = random.randint(800, 2500)
                    type.type("CASH. Wet, moldy cash, but cash. " + green(bright("$" + str(worth))) + " worth.")
                    self.change_balance(worth)
                elif outcome == 1:
                    type.type("Old photographs and letters, ruined by water damage. Someone's memories, lost forever. You say a quiet word and let the water take them back.")
                elif outcome == 2:
                    type.type("A gun. Probably dropped here on purpose by someone who didn't want it found. You leave it where it is. You don't need those kinds of problems.")
                else:
                    type.type("Gold jewelry - a wedding band, a bracelet, a locket with a faded photo inside. You feel weird taking it, but you do.")
                    self.add_item("Swamp Gold")
                print("\n")
            else:
                type.type("You tuck the lockbox under your arm. You'll open it later, somewhere dry, where you can take your time.")
                self.add_item("Mysterious Lockbox")
                print("\n")
        elif event == "witch":
            type.type("A small boat drifts out of the fog - a pirogue, poled by a figure in a hooded cloak. The witch of the swamp. She stops next to you, looking down with eyes that have seen too much.")
            print("\n")
            type.type(quote("You're far from shore, child. Looking for something?"))
            print("\n")
            type.type("Do you ask her for help, ask her what she's selling, or swim away?")
            choice = input("(help/buy/swim): ").strip().lower()
            if choice == "help":
                type.type(quote("Help don't come free in these waters. But I like your face. Grab on."))
                print("\n")
                type.type("She pulls you into her boat and poles you to shore. As you climb out, she hands you something - a small bundle of herbs tied with red string.")
                print("\n")
                type.type(quote("For protection. You'll need it."))
                self.add_item("Witch's Ward")
                print("\n")
            elif choice == "buy":
                type.type("She grins, revealing teeth filed to points.")
                print("\n")
                type.type(quote("I sell charms. Luck, love, revenge. What's your poison?"))
                print("\n")
                type.type("Do you buy a luck charm, a love charm, or a revenge charm?")
                charm = input("(luck/love/revenge): ").strip().lower()
                cost = random.randint(100, 400)
                if self.get_balance() >= cost:
                    self.change_balance(-cost)
                    if charm == "luck":
                        type.type("She ties a rabbit's foot around your wrist. You feel the swamp's favor settle on you.")
                        self.add_status("Swamp Lucky")
                    elif charm == "love":
                        type.type("She gives you a vial of something pink. " + quote("Put it in their drink. Don't blame me for what happens."))
                        self.add_item("Love Potion")
                    else:
                        type.type("She hands you a small wax doll. " + quote("You know what to do with this. Don't come crying when it works."))
                        self.add_item("Voodoo Doll")
                    print("\n")
                else:
                    type.type(quote("You can't afford my prices, sugar. Maybe next time."))
                    print("\n")
            else:
                type.type("You start swimming away. Her laughter follows you, echoing off the cypress trees.")
                print("\n")
                type.type(quote("Swim fast, child. The gators are hungry tonight."))
                print("\n")
        elif event == "fishing_shack":
            type.type("You spot a fishing shack on stilts, half-collapsed into the water. It looks abandoned, but there's a light inside.")
            print("\n")
            type.type("Do you swim over to investigate?")
            investigate = ask.yes_or_no()
            if investigate == "yes":
                type.type("You pull yourself onto the rickety porch. Inside, you find an old man drinking from a mason jar, a fishing pole propped against the wall.")
                print("\n")
                type.type(quote("Well hell, didn't expect visitors. Come in, come in. Name's Earl. Want some 'shine?"))
                print("\n")
                drink = ask.yes_or_no("Accept Earl's moonshine?")
                if drink == "yes":
                    type.type("The moonshine hits you like a freight train. Your eyes water. Your chest burns. But you feel... alive.")
                    self.heal(random.randint(10, 25))
                    print("\n")
                    type.type("Earl laughs and slaps your back. " + quote("You're alright, stranger. Here, take this."))
                    print("\n")
                    gift = random.choice(["money", "lure", "tip"])
                    if gift == "money":
                        worth = random.randint(100, 300)
                        type.type("He hands you some crumpled bills. " + green(bright("$" + str(worth))) + ".")
                        self.change_balance(worth)
                    elif gift == "lure":
                        type.type("He gives you his lucky fishing lure. " + quote("Caught a 50-pound catfish with that. Swear to God."))
                        self.add_item("Earl's Lucky Lure")
                    else:
                        type.type(quote("Stay away from the north end of the swamp. Something ain't right there. Something... wrong."))
                else:
                    type.type("Earl shrugs. " + quote("Suit yourself. More for me.") + " He goes back to his drinking, and you slip back into the water.")
                print("\n")
            else:
                type.type("You swim past. Some places are best left alone.")
                print("\n")
        else:
            type.type("You swim back, heart pounding, but nothing happens. The swamp keeps its secrets tonight. You emerge covered in algae and duck weed, smelling like something died. Which, in this swamp, something probably did.")
        print("\n")

    def beach_stroll(self):
        self.meet("Beach Stroll Event")
        type.type("You walk along the shoreline at dusk, the sand cool beneath your feet. The ocean stretches out forever, dark and restless under the fading sky. Seagulls cry in the distance. The salt air fills your lungs.")
        print("\n")
        random_chance = random.randrange(4)
        if random_chance == 0:
            type.type("You spot something in the wet sand ahead. As you get closer, you realize it's a person - lying face down at the waterline, waves lapping at their legs.")
            print("\n")
            type.type("Do you check on them?")
            answer = ask.yes_or_no()
            if answer == "yes":
                outcome = random.randrange(3)
                if outcome == 0:
                    type.type("You roll them over. They're alive - barely. A tourist who got caught in a riptide, from the looks of it. They cough up seawater and grab your arm.")
                    print("\n")
                    type.type(quote("Thank you... thank you...") + " They press something into your hand - a soggy wallet.")
                    print("\n")
                    type.type(quote("Take it. I don't care. You saved my life."))
                    worth = random.randint(100, 300)
                    type.type("Inside is " + green(bright("$" + str(worth))) + ". You help them to their feet and point them toward the boardwalk.")
                    self.change_balance(worth)
                    print("\n")
                elif outcome == 1:
                    type.type("They're dead. Have been for a while, from the look of them. Drowned, probably. The ocean took them and then gave them back.")
                    self.lose_sanity(random.choice([2, 3, 4]))  # Finding a corpse
                    print("\n")
                    type.type("You check their pockets - nothing. You leave the body where it lies. Someone else will find it.")
                    print("\n")
                else:
                    type.type("They're alive, and VERY drunk. They sit up, blinking at you, then start laughing.")
                    print("\n")
                    type.type(quote("Oh man... I thought I was dying! Just taking a nap, friend!"))
                    print("\n")
                    type.type("They stumble off toward the boardwalk, still laughing. Some people.")
                    print("\n")
            else:
                type.type("You walk past without stopping. Probably just a drunk sleeping it off. Not your problem either way.")
                print("\n")
        elif random_chance == 1:
            type.type("A hunched figure is walking along the tideline ahead of you, picking things up and putting them in a bucket. An old man, collecting shells.")
            print("\n")
            type.type("As you pass, he looks up at you. " + quote("Help an old man fill his bucket? I'll make it worth your while."))
            print("\n")
            type.type("Do you help him collect shells?")
            answer = ask.yes_or_no()
            if answer == "yes":
                type.type("You spend the next half hour walking the beach with the old man, picking up shells and listening to his stories. He used to be a fisherman, he says. Forty years on the water.")
                print("\n")
                type.type("When his bucket is full, he hands you some crumpled bills.")
                print("\n")
                type.type(quote("For your time. Gets lonely out here."))
                worth = random.randint(50, 150)
                type.type("You pocket the " + green(bright("$" + str(worth))) + " and say goodbye.")
                self.change_balance(worth)
                print("\n")
            else:
                type.type(quote("Suit yourself.") + " The old man goes back to his shells, and you continue down the beach, alone.")
                print("\n")
        elif random_chance == 2:
            type.type("You find a bonfire up ahead, surrounded by a group of teenagers drinking beer and playing music too loud. One of them waves you over.")
            print("\n")
            type.type(quote("Hey! Come hang out!"))
            print("\n")
            type.type("Do you join them?")
            answer = ask.yes_or_no()
            if answer == "yes":
                if random.random() < 0.6:
                    type.type("You sit by the fire for a while, sharing a beer. They're just kids, really. Enjoying the summer.")
                    print("\n")
                    type.type("When you leave, you feel a little lighter. Sometimes human connection is all you need.")
                    self.heal(random.randint(5, 15))
                    print("\n")
                else:
                    type.type("One of them starts asking too many questions. Where you're from. What you do. Where you're staying. You make an excuse and leave quickly.")
                    print("\n")
            else:
                type.type("You wave and keep walking. You're not in the mood for company tonight.")
                print("\n")
        else:
            type.type("You walk the beach until the sun disappears completely. The stars come out over the water.")
            print("\n")
            type.type("Eventually you head back to your wagon, sand in your shoes and salt on your skin.")
            print("\n")

    # RABBIT CHASE CHAIN - MODEST NIGHT
    def chase_the_third_rabbit(self):
        # Third rabbit chase - small chance to catch, can use carrot
        if self.get_rabbit_chase() != 2:
            self.night_event()
            return
        
        type.type("You're starting to think you're going crazy. Because there, sitting on a rock in the moonlight, is that same white rabbit. Again.")
        print("\n")
        type.type("It twitches its nose at you, almost daring you to try.")
        print("\n")
        
        if self.has_item("Carrot"):
            type.type("Wait. You have a " + magenta(bright("Carrot")) + " in your pocket. Maybe you can lure it?")
            print("\n")
            use_carrot = ask.yes_or_no("Use the carrot to lure the rabbit?")
            if use_carrot == "yes":
                self.use_item("Carrot")
                catch_chance = random.randrange(3)  # 33% chance with carrot
                if catch_chance == 0:
                    type.type("You hold out the carrot, and incredibly, the rabbit hops over. It nibbles on the carrot, and you slowly reach down... and GRAB it!")
                    print("\n")
                    type.type(green(bright("You caught the rabbit!")))
                    print("\n")
                    type.type("The rabbit squeaks in surprise. Then, something magical happens. It poops out a handful of coins, and in a flash of sparkles, disappears into thin air.")
                    print("\n")
                    coins = random.randint(500, 2000)
                    type.type("You're left holding " + green(bright("$" + str(coins))) + " and wondering what just happened.")
                    self.change_balance(coins)
                    self.advance_rabbit_chase()
                    self.meet("Caught Rabbit")
                    return
                else:
                    type.type("The rabbit takes one bite of the carrot, then bolts, taking your carrot with it!")
                    print("\n")
                    type.type(yellow("Well, that was a waste of a perfectly good carrot."))
                    self.advance_rabbit_chase()
                    print("\n")
                    return
        
        type.type("You give chase once more. This time, you get close. SO close. Your fingers brush its fur...")
        print("\n")
        
        catch_chance = random.randrange(10)  # 10% chance without carrot
        if catch_chance == 0:
            type.type(green(bright("GOT IT!")))
            print("\n")
            type.type("The rabbit squeaks in your hands. Then, something magical happens. It poops out a handful of coins, and in a flash of sparkles, disappears into thin air.")
            print("\n")
            coins = random.randint(500, 2000)
            type.type("You're left holding " + green(bright("$" + str(coins))) + " and wondering what just happened.")
            self.change_balance(coins)
            self.meet("Caught Rabbit")
        else:
            type.type("...but it slips away yet again. You swear that rabbit is supernatural.")
            print("\n")
            type.type(yellow("The hunt continues. You WILL catch that rabbit. Eventually."))
        
        self.advance_rabbit_chase()
        print("\n")
        
    # Rich Nights (100,000 - 500,000)
    def beach_swim(self):
        self.meet("Beach Swim Event")
        type.type("You wade into the ocean at night, the water black and endless. The waves push and pull at your body. Above you, the stars are scattered across the sky like spilled salt. Bioluminescence glows blue-green around your feet with each step.")
        print("\n")
        random_chance = random.randrange(5)
        if random_chance == 0:
            type.type("A sudden, searing pain wraps around your leg - jellyfish. The tentacles burn like fire as you thrash toward shore.")
            print("\n")
            type.type("Do you try to tough it out in the water, or scramble for the beach?")
            print("\n")
            choice = input("(tough/beach): ").strip().lower()
            if choice == "tough":
                if random.random() < 0.4:
                    type.type("You grit your teeth and keep swimming, the pain slowly fading to a dull throb. Mind over matter.")
                    print("\n")
                    type.type("When you finally walk out of the water, the welts are already rising on your skin, but you feel oddly proud of yourself.")
                    print("\n")
                else:
                    type.type("The pain gets worse, not better. You barely make it to shore before collapsing, your leg on fire.")
                    print("\n")
                    self.hurt(random.randint(15, 30))
                    type.type("You lie on the sand, gasping, waiting for the burning to stop. It takes a long time.")
                    print("\n")
            else:
                type.type("You splash frantically for shore, the jellyfish still wrapped around your calf. You rip it off and hurl it back into the water.")
                print("\n")
                self.hurt(random.randint(10, 20))
                type.type("The sting leaves angry red welts, but at least you're out of the water. You find some wet sand and pack it on. Old fisherman's trick.")
                print("\n")
        elif random_chance == 1:
            type.type("You float on your back, letting the waves rock you gently. The stars wheel overhead. For a few minutes, you forget everything - the wagon, the gambling, the debt, all of it.")
            print("\n")
            type.type("A shooting star streaks across the sky. You make a wish without thinking.")
            print("\n")
            type.type("When you finally swim back to shore, you feel... peaceful. Centered. Like maybe things will be okay.")
            print("\n")
            self.heal(random.randint(20, 35))
            self.add_status("At Peace")
            self.restore_sanity(random.choice([2, 3, 4]))  # Restores sanity
        elif random_chance == 2:
            type.type("A current catches you, stronger than you expected. The undertow pulls at your legs, dragging you away from shore. The beach lights grow smaller.")
            print("\n")
            type.type("Do you fight the current directly, swim parallel to the beach, or relax and float?")
            print("\n")
            choice = input("(fight/parallel/float): ").strip().lower()
            if choice == "parallel":
                type.type("You remember some old advice and swim sideways, parallel to the beach. Slowly, the current releases you, and you make your way back to shore.")
                print("\n")
                type.type("Smart thinking. Fighting a riptide is how people drown.")
                print("\n")
            elif choice == "float":
                type.type("You force yourself to relax, letting the current carry you. Eventually, it weakens, and you're able to swim back at an angle.")
                print("\n")
                type.type("Calm saved your life. Panic kills people in the ocean.")
                print("\n")
            else:
                if random.random() < 0.3:
                    type.type("You fight like hell, arms burning, lungs screaming. Somehow, you make it back to shore.")
                    print("\n")
                    self.hurt(random.randint(10, 20))
                    type.type("You collapse on the sand, exhausted. That was too close.")
                    print("\n")
                else:
                    type.type("The current is too strong. You're swept down the beach, tumbling in the waves, before finally washing up on shore a hundred yards from where you started.")
                    print("\n")
                    self.hurt(random.randint(20, 35))
                    self.lose_sanity(random.choice([3, 4, 5]))  # Near-death experience
                    type.type("You lie there, coughing up seawater, feeling like you almost died. Because you almost did.")
                    print("\n")
        elif random_chance == 3:
            type.type("Something brushes against your leg in the darkness. Then again. Then something GRABS your ankle.")
            print("\n")
            type.type("You kick wildly - and your foot connects with something that squeaks and lets go. A sea otter surfaces, looking offended.")
            print("\n")
            type.type("It floats there, staring at you with its little hands folded on its chest, like you ruined its evening.")
            print("\n")
            type.type(quote("Sorry, buddy."))
            print("\n")
            type.type("The otter makes a chittering noise that sounds suspiciously like profanity, then swims away. You can't help but laugh.")
            self.heal(random.randint(5, 10))
            print("\n")
        else:
            type.type("You swim for a while, enjoying the cool water and the darkness. The moon rises over the water, turning the waves silver.")
            print("\n")
            type.type("You find a sandbar and stand there for a while, waist-deep in the ocean, feeling like the only person in the world.")
            print("\n")
            type.type("You dry off and head back to your wagon, smelling like salt and feeling cleaner than you have in days.")
            print("\n")

    def beach_dive(self):
        self.meet("Beach Dive Event")
        type.type("You dive beneath the waves, the world above disappearing into blue-green silence. Down here, the light filters through the water like something from a dream. The ocean floor is littered with shells, sand dollars, and the occasional piece of sea glass. A school of silver fish parts around you like a curtain.")
        print("\n")
        random_chance = random.randrange(5)
        if random_chance == 0:
            type.type("Your hand closes around something smooth and round, half-buried in the sand. You dig it out - an oyster, massive and ancient-looking, the size of your fist.")
            print("\n")
            type.type("Do you pry it open now, or save it for later?")
            choice = input("(open/save): ").strip().lower()
            if choice == "open":
                type.type("You surface and use a rock to crack it open. Inside...")
                print("\n")
                outcome = random.randrange(3)
                if outcome == 0:
                    type.type("A PEARL. Not perfect - lumpy, with a slight pink hue - but real. You can feel its weight, its worth.")
                    self.add_item("Pink Pearl")
                    type.type("This could be worth hundreds. Maybe more to the right buyer.")
                elif outcome == 1:
                    type.type("...nothing but oyster meat. You eat it raw, feeling like a pirate. It's actually pretty good.")
                    self.heal(random.randint(5, 10))
                else:
                    type.type("TWO pearls. Small, but matched. A pair. You grin like an idiot.")
                    self.add_item("Matched Pearls")
                print("\n")
            else:
                type.type("You tuck the oyster away. Patience. The pearl isn't going anywhere.")
                self.add_item("Giant Oyster")
                print("\n")
        elif random_chance == 1:
            type.type("You spot something metallic glinting in the sand below. You dive deeper, lungs burning, and your fingers close around a handle.")
            print("\n")
            type.type("It's a waterproof case, the kind divers use. Still sealed. Do you open it?")
            answer = ask.yes_or_no()
            if answer == "yes":
                outcome = random.randrange(4)
                if outcome == 0:
                    type.type("Inside is cash - a lot of it, wrapped in plastic. Someone's emergency fund, lost to the sea.")
                    worth = random.randint(800, 2000)
                    type.type("You count " + green(bright("$" + str(worth))) + ". Not bad for a swim.")
                    self.change_balance(worth)
                    print("\n")
                elif outcome == 1:
                    type.type("An underwater camera, still working. You scroll through the photos - vacation shots, a wedding proposal, a woman crying happy tears.")
                    print("\n")
                    type.type("There's an address on the case. Do you keep it or return it?")
                    keep = input("(keep/return): ").strip().lower()
                    if keep == "return":
                        type.type("You'll mail it back. It's the right thing to do.")
                        print("\n")
                        type.type("A few days later, a check arrives in the mail. " + green(bright("$500")) + " and a thank you note. 'These memories meant everything.'")
                        self.change_balance(500)
                    else:
                        type.type("You keep the camera. Nice piece of equipment. The memories on it aren't yours anyway.")
                        self.add_item("Underwater Camera")
                elif outcome == 2:
                    type.type("Inside is a rusted pistol and some soggy documents. Nothing useful, and probably evidence of something you don't want to know about.")
                    print("\n")
                    type.type("You toss it back into the deep water and swim away. Fast.")
                    print("\n")
                else:
                    type.type("The case is full of sand and a very confused hermit crab. It pinches you before scuttling away.")
                    self.hurt(random.randint(1, 3))
                    print("\n")
            else:
                type.type("You leave it where it is. Nothing good ever came from treasure found at the bottom of the ocean.")
                print("\n")
        elif random_chance == 2:
            type.type("A shadow passes over you. You look up and your blood runs cold - a shark, maybe six feet long, circling lazily above. A blacktip, from the look of it. Probably not a man-eater. Probably.")
            print("\n")
            type.type("Do you swim slowly to shore, stay completely still, or try to scare it off?")
            print("\n")
            choice = input("(swim/still/scare): ").strip().lower()
            if choice == "still":
                type.type("You freeze, barely breathing, watching the shark through the wavering water. It circles once, twice, then loses interest and glides away into the blue.")
                print("\n")
                type.type("You wait until you can't see it anymore, then swim to shore as calmly as you can manage. Your hands don't stop shaking for an hour.")
                print("\n")
            elif choice == "scare":
                type.type("You puff yourself up and make yourself look big, spreading your arms wide. The shark pauses, curious.")
                if random.random() < 0.6:
                    type.type("It decides you're not worth the trouble and swims off. You feel like a badass.")
                    print("\n")
                else:
                    type.type("It bumps you with its nose - testing. You punch it in the face. It swims away, annoyed. You swim away, terrified.")
                    self.hurt(random.randint(5, 10))
                    print("\n")
            else:
                if random.random() < 0.7:
                    type.type("You swim for shore with slow, deliberate strokes, trying not to splash. The shark follows for a moment, then veers off.")
                    print("\n")
                    type.type("You make it to the beach and collapse on the sand, heart pounding. Too close.")
                    print("\n")
                else:
                    type.type("The shark bumps you - testing, curious. You feel its rough skin scrape against your side. You thrash for shore, panic overwhelming caution.")
                    print("\n")
                    self.hurt(random.randint(15, 30))
                    type.type("You make it out, but your side is scraped raw. Could have been so much worse.")
                    print("\n")
        elif random_chance == 3:
            type.type("You find a coral formation, alive with color and movement. Fish dart in and out of the crevices. An octopus watches you from its den, changing colors nervously.")
            print("\n")
            type.type("You float there, watching the reef ecosystem, until your lungs force you to surface. For a moment, you weren't a gambler living in a wagon. You were just... part of the ocean.")
            print("\n")
            self.heal(random.randint(10, 20))
            type.type("You feel connected to something bigger than yourself.")
            self.add_status("Ocean-Blessed")
            print("\n")
        else:
            type.type("You dive and explore for a while, finding nothing but shells and the occasional startled fish. A moray eel gives you the stink-eye from its hole.")
            print("\n")
            type.type("Eventually you surface and swim back to shore, tired but content. The underwater world is peaceful, alien, beautiful.")
            print("\n")

    def city_streets(self):
        self.meet("City Streets Event")
        type.type("You wander the city's labyrinth of neon and shadow, where every alley whispers a different story. The air is thick with exhaust, food cart smoke, and the promise of trouble. A pigeon watches you from a fire escape like it knows something you don't.")
        print("\n")
        event = random.choice(["drug_dealer", "stray_cat", "rent_bike", "food_cart", "busker", "none"])
        if event == "drug_dealer":
            type.type("A gaunt figure in a hoodie steps from a flickering doorway, eyes darting like a nervous bird. " + quote("Looking for a little edge?") + " he asks, holding out a small bag. The city seems to hold its breath.")
            print("\n")
            type.type("Do you accept, decline politely, or tell him to get lost?")
            choice = input("(accept/decline/scram): ").strip().lower()
            if choice == "accept":
                outcome = random.choice(["buff", "bad_trip", "police", "fake"])
                if outcome == "buff":
                    type.type("You slip the contents under your tongue. The world sharpens - colors brighter, sounds clearer. For a while, you feel invincible, your luck uncanny.")
                    self.add_status("Energized")
                elif outcome == "bad_trip":
                    type.type("Your heart races, the world tilts, and you stagger into the street. You lose track of time - and some money. When you come to, your pockets are lighter and your head aches.")
                    self.hurt(random.randint(15, 30))
                    self.change_balance(-random.randint(200, 800))
                elif outcome == "police":
                    type.type("Suddenly, blue lights flash. " + quote("Police! Hands up!") + " You drop the bag and run, barely escaping. You lose some money in the chaos.")
                    self.change_balance(-random.randint(100, 400))
                else:
                    type.type("It's oregano. He sold you cooking herbs. You feel like an idiot, but at least you're not high.")
                print("\n")
            elif choice == "scram":
                type.type("You tell him where he can shove his product. He looks hurt, actually hurt, then slinks back into the shadows.")
                print("\n")
                type.type(quote("Man, you don't gotta be like that..."))
                print("\n")
            else:
                type.type("You shake your head and move on. The dealer shrugs and lights a cigarette, already looking for his next mark.")
                print("\n")
        elif event == "stray_cat":
            type.type("A scruffy, one-eyed cat weaves between your legs, meowing with a raspy voice like it's been smoking since kittenhood. Its fur is matted, but its gaze is sharp and knowing.")
            print("\n")
            type.type("Do you pet it, feed it (if you have food), or ignore it?")
            choice = input("(pet/feed/ignore): ").strip().lower()
            if choice == "pet":
                fate = random.choice(["lucky", "scratch", "ally", "fleas"])
                if fate == "lucky":
                    type.type("The cat purrs like a tiny motor, rubbing its head against your hand. It leaves a whisker in your palm. You feel luckier, as if the city itself is watching over you.")
                    self.add_status("Street Lucky")
                elif fate == "scratch":
                    type.type("The cat hisses and claws your hand before darting away. You wince, blood trickling from the scratch. Typical.")
                    self.hurt(random.randint(3, 10))
                elif fate == "ally":
                    type.type("The cat follows you for blocks, scaring off a would-be pickpocket with a ferocious hiss. You gain a furry guardian for the night.")
                    self.add_item("Street Cat Ally")
                else:
                    type.type("The cat nuzzles you... and you immediately start itching. Fleas. Of course. You spend the next hour scratching.")
                    self.hurt(random.randint(2, 5))
                print("\n")
            elif choice == "feed":
                if self.has_item("Can of Tuna"):
                    type.type("You crack open your can of tuna. The cat goes WILD, purring and rubbing against you, then devouring the fish.")
                    self.use_item("Can of Tuna")
                    print("\n")
                    type.type("Other cats start appearing from everywhere - alleys, dumpsters, fire escapes. Soon you're surrounded by a dozen grateful felines. You feel blessed by the street cat gods.")
                    self.add_status("Cat Whisperer")
                else:
                    type.type("You don't have any food. The cat gives you a disappointed look and walks away, tail high.")
                print("\n")
            else:
                type.type("You ignore the cat. It stares at your back as you walk away, judging you silently.")
                print("\n")
        elif event == "rent_bike":
            type.type("You spot a row of rental bikes, some more battered than others. The city traffic is a snarl of taxis and delivery trucks, but on two wheels, you could fly.")
            print("\n")
            type.type("Do you rent a nice one ($50), a cheap one ($20), or skip it?")
            choice = input("(nice/cheap/skip): ").strip().lower()
            if choice == "nice":
                if self.get_balance() >= 50:
                    self.change_balance(-50)
                    type.type("You pick the sleekest bike in the row. It rides like a dream, weaving through traffic like water through rocks.")
                    print("\n")
                    self.add_status("Refreshed")
                    type.type("You arrive at your destination exhilarated, wind-blown, and feeling alive.")
                else:
                    type.type("You don't have enough cash. The bike attendant shrugs sympathetically.")
                print("\n")
            elif choice == "cheap":
                if self.get_balance() >= 20:
                    self.change_balance(-20)
                    outcome = random.choice(["fine", "crash", "stolen"])
                    if outcome == "fine":
                        type.type("The bike squeaks and wobbles, but it gets you where you're going. Not elegant, but effective.")
                    elif outcome == "crash":
                        type.type("The brakes fail. You crash into a hot dog cart, sending wieners flying. You escape with bruises and mustard stains.")
                        self.hurt(random.randint(8, 18))
                    else:
                        type.type("You stop to rest, and when you turn around, some kid is pedaling away on YOUR bike. You don't even bother chasing.")
                else:
                    type.type("Even the cheap bike is too rich for your blood right now.")
                print("\n")
            else:
                type.type("You decide to walk. The city's rhythm sets your pace. Sometimes slow is safe.")
                print("\n")
        elif event == "food_cart":
            type.type("The smell hits you first - garlic, grease, something spicy. A food cart, wedged between a dumpster and a parked car, manned by a guy who looks like he hasn't slept in days.")
            print("\n")
            type.type(quote("Best gyro in the city. Five bucks. You want or no?"))
            print("\n")
            buy = ask.yes_or_no("Buy the gyro?")
            if buy == "yes":
                if self.get_balance() >= 5:
                    self.change_balance(-5)
                    outcome = random.randrange(3)
                    if outcome == 0:
                        type.type("It IS the best gyro in the city. Holy crap. The tzatziki sauce alone is life-changing. You feel restored.")
                        self.heal(random.randint(15, 30))
                    elif outcome == 1:
                        type.type("It's... fine. Food is food. You eat it standing on the curb, watching the city go by.")
                        self.heal(random.randint(5, 10))
                    else:
                        type.type("Something was NOT right with that lamb. You spend the next hour in a public bathroom, questioning your life choices.")
                        self.hurt(random.randint(10, 20))
                else:
                    type.type(quote("No money, no gyro. Come back when you got five bucks."))
            else:
                type.type(quote("Your loss, my friend. Your loss."))
            print("\n")
        elif event == "busker":
            type.type("A street musician plays saxophone under a flickering streetlight, the notes winding through the night air like smoke. A few people have stopped to listen. His case is open, a handful of coins inside.")
            print("\n")
            type.type("Do you stop to listen, tip him, or keep walking?")
            choice = input("(listen/tip/walk): ").strip().lower()
            if choice == "listen":
                type.type("You lean against a wall and let the music wash over you. It's jazz, slow and melancholy, the kind of song that makes you think about everyone you've ever lost.")
                print("\n")
                type.type("When it ends, you feel... lighter. Like you let something go.")
                self.heal(random.randint(5, 15))
                print("\n")
            elif choice == "tip":
                tip = random.randint(5, 20)
                if self.get_balance() >= tip:
                    self.change_balance(-tip)
                    type.type("You drop " + str(tip) + " bucks in his case. He nods at you, a silent thanks, and launches into an upbeat number just for you.")
                    print("\n")
                    type.type("You walk away feeling generous. It's a good feeling.")
                    self.add_status("Generous")
                else:
                    type.type("You pat your pockets apologetically. He winks and keeps playing anyway.")
                print("\n")
            else:
                type.type("You keep walking. The music fades behind you, replaced by car horns and distant sirens.")
                print("\n")
        else:
            type.type("Tonight, the city is just a city. Neon reflections in puddles. Distant laughter. The hum of a thousand lives you'll never know.")
            print("\n")
            type.type("You wander, lost in thought, until you find yourself back at your wagon, unsure how you got there.")
            print("\n")

    # SUZY STORYLINE - RICH NIGHT
    def whats_my_favorite_animal(self):
        # Only triggers if favorite color is set but favorite animal is not
        if self.get_favorite_color() == None or self.get_favorite_animal() != None:
            self.night_event()
            return
        
        type.type("The city lights are starting to dim as people head home for the night. But through the fading glow, you hear a sound that's become strangely comforting-sneakers on concrete, a jump rope slapping the ground.")
        print("\n")
        type.type(quote(self.__name + "! There you are! I've been looking EVERYWHERE for you!"))
        print("\n")
        type.type("Suzy bounces over, somehow still full of energy despite the late hour.")
        print("\n")
        type.type(quote("Okay okay okay, I have another question. This one's even MORE important than the color one."))
        print("\n")
        type.type("She stops jump roping for the first time you've ever seen, looking at you with complete seriousness.")
        print("\n")
        type.type(quote("What's your favorite animal?"))
        print("\n")
        
        animal = str(input("Your favorite animal: "))
        self.set_favorite_animal(animal)
        
        type.type(quote("A " + animal + "?! NO WAY! That's MY favorite animal too!"))
        print("\n")
        type.type("Suzy starts jumping up and down excitedly.")
        print("\n")
        type.type(quote("We're like... BEST FRIENDS now! " + animal + " buddies forever!"))
        print("\n")
        type.type(quote("Oh! I almost forgot! I made you something. But it's not done yet. I'll give it to you when I see you again, okay? PROMISE you'll be around?"))
        print("\n")
        answer = ask.yes_or_no("Do you promise?")
        if answer == "yes":
            type.type(quote("YAY! Okay! Pinky promise! Don't break it or you'll have bad luck FOREVER!"))
        else:
            type.type(quote("Hmm... well, I'll find you anyway. I'm REALLY good at finding people!"))
        print("\n")
        type.type("Suzy resumes jump roping and bounces off into the night, humming a tune you can't quite place.")
        print("\n")

    # RABBIT CHASE CHAIN - RICH NIGHT
    def chase_the_fourth_rabbit(self):
        # Fourth rabbit chase - another chance to catch
        if self.get_rabbit_chase() != 3 or self.has_met("Caught Rabbit"):
            self.night_event()
            return
        
        type.type("It's become a ritual at this point. You see the flash of white fur in your peripheral vision, and your legs start moving before your brain catches up.")
        print("\n")
        type.type("The rabbit leads you through the city streets this time, darting under parked cars and around corners. People stare at you chasing what they probably think is nothing.")
        print("\n")
        type.type("Finally, you corner it in an alley. There's nowhere for it to go.")
        print("\n")
        type.type(quote("Got you now, you little..."))
        print("\n")
        
        catch_chance = random.randrange(5)  # 20% chance
        if catch_chance == 0:
            type.type("You lunge, and miraculously, your hands close around the rabbit's soft fur!")
            print("\n")
            type.type(green(bright("FINALLY!")))
            print("\n")
            type.type("The rabbit squeaks, poops out a shower of coins, and vanishes in a burst of sparkles. You're left sitting in an alley, covered in money, laughing like a maniac.")
            print("\n")
            coins = random.randint(2000, 5000)
            type.type("You collect " + green(bright("$" + str(coins))) + " from the ground.")
            self.change_balance(coins)
            self.meet("Caught Rabbit")
        else:
            type.type("The rabbit looks at you, twitches its nose, and then... walks straight through the wall. Just phases right through solid brick.")
            print("\n")
            type.type(quote("...What."))
            print("\n")
            type.type(yellow("That rabbit is definitely not a normal rabbit. The hunt continues."))
        
        self.advance_rabbit_chase()
        print("\n")
        
    # Doughman Nights (500,000 - 900,000)
    def city_stroll(self):
        self.meet("City Stroll Event")
        type.type("You wander the city streets at dusk, neon signs buzzing to life as the sky turns purple. The sidewalks are crowded with people heading home, heading out, heading somewhere. You're just... heading. Trees planted in sidewalk grates rustle their leaves, the only nature brave enough to survive here.")
        print("\n")
        event = random.choice(["bank_robbery", "dog_walker", "mugging", "street_performer", "lost_tourist", "none"])
        if event == "bank_robbery":
            type.type("BANG. Glass shatters. Alarms scream. Three people in masks burst out of the bank across the street, bags in hand. Cops aren't here yet.")
            print("\n")
            type.type("What do you do?")
            action = input("(help/run/sneak/film): ").strip().lower()
            if action == "help":
                type.type("You sprint toward them like an idiot hero. One robber turns - ")
                if random.random() < 0.3:
                    type.type("and you clothesline him into the pavement. His bag splits open. You grab a handful of cash before the cops arrive.")
                    print("\n")
                    type.type("They question you for an hour but eventually let you go with thanks and a reward.")
                    self.change_balance(random.randint(1000, 3000))
                else:
                    type.type("and clocks you in the jaw with a pistol. You go down HARD. When you wake up, cops are everywhere and your head is ringing.")
                    self.hurt(random.randint(20, 40))
                    self.lose_sanity(random.choice([2, 3, 4]))  # Sudden violence
                print("\n")
            elif action == "sneak":
                type.type("You circle around the chaos, moving low. A bag dropped in the confusion...")
                if random.random() < 0.4:
                    type.type("You snag it and walk away like nothing happened. Inside: " + green(bright("$" + str(random.randint(500, 2000)))) + ".")
                    self.change_balance(random.randint(500, 2000))
                else:
                    type.type("A cop spots you with the bag. You spend the night in a cell explaining yourself. Costs you lawyer fees.")
                    self.change_balance(-random.randint(500, 1500))
                print("\n")
            elif action == "film":
                type.type("You pull out your phone and start recording. The video goes viral. Local news pays you for the footage.")
                self.change_balance(random.randint(200, 800))
                print("\n")
            else:
                type.type("You run like a sensible person. The chaos fades behind you. You hear sirens, then nothing.")
                print("\n")
        elif event == "dog_walker":
            type.type("A dog walker rounds the corner, pulled along by SIX dogs of various sizes. A Great Dane, a corgi, a poodle, a mutt, a husky, and something that might be a small bear.")
            print("\n")
            type.type("They see you and SURGE forward, tails wagging. The walker loses her grip on two leashes.")
            print("\n")
            type.type("Do you help catch them, let them tackle you with love, or dodge?")
            action = input("(help/love/dodge): ").strip().lower()
            if action == "love":
                type.type("You drop to your knees and let the dogs swarm you. Tongues everywhere. So much fur. Pure joy.")
                print("\n")
                self.heal(random.randint(15, 30))
                type.type("The walker apologizes profusely while you laugh, covered in dog hair and feeling better than you have in weeks.")
                self.add_status("Dog Blessed")
                self.restore_sanity(random.choice([2, 3, 4]))  # Restores sanity
            elif action == "help":
                type.type("You snag the trailing leashes and help wrangle the pack. The walker is VERY grateful.")
                print("\n")
                type.type(quote("Oh my god, thank you! Here, let me give you something for your trouble."))
                self.change_balance(random.randint(50, 150))
            else:
                type.type("You sidestep like a matador. The dogs rocket past you. The walker chases after them, screaming names. You feel like you missed out on something special.")
            print("\n")
        elif event == "mugging":
            # Check for Bodyguard Bruno - complete protection
            if self.has_item("Bodyguard Bruno"):
                type.type("A figure emerges from an alley. Then another. Then a third. They fan out, blocking your path.")
                print("\n")
                type.type("Before they can speak, Bruno steps out of the shadows behind them.")
                print("\n")
                type.type(quote("Evening, gentlemen. My friend here is under my protection."))
                print("\n")
                type.type("The muggers exchange nervous glances. One by one, they back away and disappear into the night.")
                type.type(" Bruno nods at you. " + quote("Stay safe out there."))
                print("\n")
            else:
                type.type("A figure emerges from an alley. Then another. Then a third. They fan out, blocking your path. One has a knife.")
                print("\n")
                type.type(quote("Wallet. Phone. Now. Don't make this difficult."))
                print("\n")
                type.type("What's your move?")
                action = input("(fight/talk/comply/run): ").strip().lower()
                
                if action == "fight":
                    # Pocket Knife gives you a real edge (consumed)
                    if self.has_item("Pocket Knife"):
                        self.use_item("Pocket Knife")
                        type.type("You pull out your pocket knife. The blade catches the streetlight.")
                        print("\n")
                        type.type("The muggers hesitate. That moment of doubt is all you need - you slash at the closest one, and they scatter.")
                        print("\n")
                        type.type("You're left standing in the alley, breathing hard. The knife is bent - useless now - but you're alive.")
                        print("\n")
                    else:
                        type.type("You've had enough of this city taking from you. You throw the first punch - ")
                        if random.randrange(100) < 30:  # 30% base chance
                            type.type("and it connects beautifully. In the chaos, they scatter like roaches when the lights come on. You stand alone, fists shaking, alive.")
                        else:
                            type.type("but they're three and you're one. You go down swinging, but you go down.")
                            self.hurt(random.randint(25, 45))
                            self.change_balance(-random.randint(500, 1500))
                            self.lose_sanity(random.choice([3, 4, 5]))
                        print("\n")
                elif action == "talk":
                    type.type("You start talking, fast, making stuff up. You're a cop. Your brother is in the mob. You have a disease that spreads by touch.")
                    if random.randrange(100) < 40:  # 40% base chance
                        type.type(" Something works. They exchange glances, suddenly unsure. They back off.")
                    else:
                        type.type(" The one with the knife laughs. " + quote("Nice try.") + " They take your stuff anyway.")
                        self.change_balance(-random.randint(300, 800))
                    print("\n")
                elif action == "run":
                    type.type("You BOLT. Pure animal instinct. Behind you, footsteps - ")
                    if random.randrange(100) < 55:  # 55% base chance to escape
                        type.type("that fade as you outrun them. You don't stop until you're ten blocks away, gasping, but free.")
                    else:
                        type.type("and a hand grabs your collar. You hit the ground. They take what they want and leave you there.")
                        self.hurt(random.randint(10, 25))
                        self.change_balance(-random.randint(200, 600))
                        self.lose_sanity(random.choice([2, 3]))
                    print("\n")
                else:
                    type.type("You hand over your wallet. Not worth dying over. They grab it and disappear into the city.")
                    self.change_balance(-random.randint(100, 400))
                    print("\n")
        elif event == "street_performer":
            type.type("A street performer has gathered a crowd - a man painted entirely silver, standing motionless on a crate. He hasn't moved in the ten minutes you've been watching. Is he even breathing?")
            print("\n")
            type.type("A kid throws a coin. The man LUNGES forward, making robot sounds. The crowd laughs.")
            print("\n")
            type.type("Do you tip him, try to make him flinch, or just watch?")
            action = input("(tip/flinch/watch): ").strip().lower()
            if action == "tip":
                self.change_balance(-random.randint(1, 5))
                type.type("You drop some cash in his bucket. He salutes you in slow motion, then freezes again. Worth every penny.")
                self.add_status("Amused")
            elif action == "flinch":
                type.type("You wave your hand in front of his face. Make sudden movements. Nothing. This guy is a PROFESSIONAL.")
                print("\n")
                type.type("Finally, you give up. As you walk away, you hear him whisper: " + quote("Better luck next time."))
            else:
                type.type("You watch the crowd tip him, try to mess with him, take photos. The whole city walks past this moment of weird magic. Eventually you move on, but you're smiling.")
            print("\n")
        elif event == "lost_tourist":
            type.type("A family of tourists blocks the sidewalk, spinning in circles, staring at their phones, looking increasingly panicked. Mom, Dad, two kids, all wearing matching 'I HEART THE CITY' shirts.")
            print("\n")
            type.type(quote("Excuse me? Do you know where the... um...") + " the dad holds up his phone, showing an address that's literally two blocks away.")
            print("\n")
            type.type("Do you help them, ignore them, or intentionally send them the wrong way?")
            action = input("(help/ignore/trick): ").strip().lower()
            if action == "help":
                type.type("You walk them there yourself. Takes five minutes. The mom tries to give you money but you wave it off. The kids wave goodbye.")
                print("\n")
                type.type("You feel... good? Like, genuinely good. Weird.")
                self.heal(random.randint(5, 15))
                self.add_status("Good Samaritan")
            elif action == "trick":
                type.type("You give them completely wrong directions with a smile. They thank you profusely and head off into a part of the city they should NOT be in.")
                print("\n")
                type.type("You feel like a jerk. Because you are one.")
            else:
                type.type("You pretend to be on your phone and brush past them. Someone else will help. Probably.")
            print("\n")
        else:
            type.type("Tonight, the city is just background noise. You walk and walk, past closed shops and flickering signs, past sleeping homeless and busy taxis, until your legs are tired and your mind is empty.")
            print("\n")
            type.type("A raccoon waddles across your path, looks at you like you're the intruder here, and disappears into a storm drain. Fair enough.")
            print("\n")

    def city_park(self):
        self.meet("City Park Event")
        type.type("You step into the city park, an oasis of green amidst concrete and steel. Ancient oak trees stretch overhead, their leaves whispering secrets. Fireflies blink in the bushes. Somewhere, an owl hoots. It's like the forest never left - it just learned to hide.")
        print("\n")
        event = random.choice(["pigeons", "hobo_joe", "free_pizza", "pond", "chess_hustler", "midnight_gardener", "none"])
        
        if event == "pigeons":
            type.type("You sit on a bench. Immediately, pigeons materialize. Dozens of them. They strut toward you like a feathered army, heads bobbing, eyes hungry.")
            print("\n")
            type.type("One lands on your shoulder. Another on your head. This is getting out of hand.")
            print("\n")
            type.type("Do you feed them, flee, or assert dominance?")
            choice = input("(feed/flee/dominance): ").strip().lower()
            if choice == "feed":
                type.type("You tear up some bread from your pocket (you always have bread, don't question it). The pigeons go INSANE with joy. More come. The ground becomes a sea of cooing feathers.")
                print("\n")
                if random.random() < 0.7:
                    type.type("An old man watches from another bench, smiling. " + quote("They like you. That's good luck."))
                    self.add_status("Pigeon Blessed")
                else:
                    type.type("One of them poops on your shoe. Still worth it.")
                print("\n")
            elif choice == "dominance":
                type.type("You stand up, spread your arms, and make direct eye contact with the alpha pigeon. You hold your ground.")
                print("\n")
                type.type("The pigeons... back off. They respect your energy. One bows its head. You have established yourself in the pecking order.")
                self.add_status("Pigeon King")
                print("\n")
            else:
                type.type("You sprint. They follow for half a block before giving up. You look ridiculous. Several people recorded you.")
                print("\n")
        
        elif event == "hobo_joe":
            type.type("A figure waves from a bench beneath a willow tree. It's Hobo Joe, a man you've seen around - scraggly beard, army jacket, kind eyes, a harmonica that's seen better days.")
            print("\n")
            type.type(quote("Hey friend. Got time for an old man?"))
            print("\n")
            type.type("Do you sit with him, give him money, or keep walking?")
            choice = input("(sit/money/walk): ").strip().lower()
            if choice == "sit":
                type.type("You sit. Joe plays a tune on his harmonica - slow, sad, beautiful. When he finishes, he tells you a story.")
                print("\n")
                story = random.choice(["war", "love", "treasure"])
                if story == "war":
                    type.type(quote("I was in the war. Saw things no man should see. But you know what got me through? Kindness. Random kindness from strangers. That's the only magic that's real."))
                    self.add_status("Wise")
                elif story == "love":
                    type.type(quote("Had a wife once. Beautiful woman. Lost her to cancer twenty years ago. Still talk to her every night, right here under this tree. She answers sometimes, in the wind."))
                    self.heal(random.randint(10, 20))
                else:
                    type.type(quote("You know there's money buried in this park? From the old days. Bank robbers. I've been looking for years. Maybe you'll have better luck."))
                    self.add_item("Joe's Treasure Map")
                print("\n")
            elif choice == "money":
                give = random.randint(10, 50)
                if self.get_balance() >= give:
                    self.change_balance(-give)
                    type.type("You hand him some cash. He looks at you, really looks, and nods.")
                    print("\n")
                    type.type(quote("Bless you. Here, take this. Found it in the fountain. Probably worth more than what you gave me."))
                    self.add_item("Lucky Coin")
                else:
                    type.type("You don't have much to give, but you give what you can. Joe understands.")
                print("\n")
            else:
                type.type("You walk past. Joe doesn't take it personally. He starts playing another tune, for no one and everyone.")
                print("\n")
        
        elif event == "free_pizza":
            type.type("A food truck is parked by the fountain with a sign: 'FREE PIZZA - GRAND OPENING!' There's already a line, but it's moving fast.")
            print("\n")
            type.type("Do you get in line, cut the line, or resist the siren call of free cheese?")
            choice = input("(line/cut/resist): ").strip().lower()
            if choice == "line":
                type.type("You wait your turn like a civilized person. Twenty minutes later, you're holding a slice of the best pizza you've ever tasted.")
                self.heal(random.randint(15, 30))
                print("\n")
            elif choice == "cut":
                type.type("You slip to the front. A guy in a gym shirt grabs your arm.")
                print("\n")
                type.type(quote("Hey! Back of the line, pal!"))
                print("\n")
                if random.random() < 0.5:
                    type.type("You talk your way out of it - emergency, low blood sugar, etc. You get your pizza, but you feel like a jerk.")
                    self.heal(random.randint(10, 20))
                else:
                    type.type("He shoves you. You shove back. Security shows up. No pizza for you.")
                    self.hurt(random.randint(5, 10))
                print("\n")
            else:
                type.type("You walk past. The pizza smells amazing. You tell yourself it probably has too many carbs anyway. You don't believe yourself.")
                print("\n")
        
        elif event == "pond":
            type.type("You find yourself at the park's pond, a mirror of black water reflecting the city lights. Ducks sleep along the edge. Koi fish circle lazily in the shallows. A turtle watches you from a rock.")
            print("\n")
            type.type("Do you feed the ducks, skip stones, or just... sit and breathe?")
            choice = input("(feed/skip/sit): ").strip().lower()
            if choice == "feed":
                type.type("You toss some crumbs into the water. The ducks wake up, quacking excitedly. The koi surge to the surface. The turtle doesn't move - too dignified.")
                print("\n")
                type.type("For a moment, you're the center of this little ecosystem. It feels nice to be needed.")
                self.heal(random.randint(5, 15))
                print("\n")
            elif choice == "skip":
                type.type("You find a flat stone and send it skipping across the pond. Three skips. Four. Five!")
                print("\n")
                type.type("A kid watching nearby claps. You feel unreasonably proud.")
                self.add_status("Simple Joy")
                print("\n")
            else:
                type.type("You sit on the bank and just... exist. No gambling. No wagon. No past or future. Just you, the water, and the sound of the city breathing around you.")
                print("\n")
                self.heal(random.randint(15, 30))
                self.add_status("Centered")
                print("\n")
        
        elif event == "chess_hustler":
            type.type("A man sits at a stone table with a chess board, pieces mid-game. He sees you looking.")
            print("\n")
            type.type(quote("Twenty bucks says you can't beat me. Fifty if you can."))
            print("\n")
            type.type("Do you play, watch someone else play, or decline?")
            choice = input("(play/watch/decline): ").strip().lower()
            if choice == "play":
                if self.get_balance() >= 20:
                    self.change_balance(-20)
                    type.type("You sit down. The game is intense. He's good. Really good.")
                    if random.random() < 0.3:
                        type.type("But you're better. Somehow, you see the winning move. Checkmate.")
                        print("\n")
                        type.type(quote("Well damn.") + " He hands you fifty bucks, grinning. " + quote("Come back anytime."))
                        self.change_balance(50)
                    else:
                        type.type("He destroys you in twelve moves. You didn't even see it coming.")
                        print("\n")
                        type.type(quote("Good game. Want to go again?") + " You decline.")
                else:
                    type.type("You don't have twenty bucks to spare. He shrugs and waits for the next sucker.")
                print("\n")
            elif choice == "watch":
                type.type("You watch him demolish three different challengers. The man is a shark. You learn something about patience and sacrifice.")
                self.add_status("Strategic")
                print("\n")
            else:
                type.type(quote("Scared money don't make money,") + " he calls after you. You don't look back.")
                print("\n")
        
        elif event == "midnight_gardener":
            type.type("In a far corner of the park, you spot someone tending to the flower beds. At midnight. With a headlamp on.")
            print("\n")
            type.type("It's an old woman, kneeling in the dirt, whispering to the roses.")
            print("\n")
            type.type("Do you approach her, watch from a distance, or leave her alone?")
            choice = input("(approach/watch/leave): ").strip().lower()
            if choice == "approach":
                type.type("She looks up as you approach, not startled at all. Her eyes are sharp despite her age.")
                print("\n")
                type.type(quote("The flowers grow best when no one's watching. Like people, really."))
                print("\n")
                type.type("She hands you a small cutting - a rose, dark red, still fresh.")
                print("\n")
                type.type(quote("Plant this somewhere. Keep something alive."))
                self.add_item("Midnight Rose")
                print("\n")
            elif choice == "watch":
                type.type("You watch her work for a while. There's something meditative about it - the careful attention, the gentle hands. You feel calmer just watching.")
                self.heal(random.randint(5, 10))
                print("\n")
            else:
                type.type("You leave her to her work. Some people and their magic are best left undisturbed.")
                print("\n")
        
        else:
            type.type("The park is quiet tonight. You find a bench beneath an ancient elm and sit, watching the fireflies blink their slow morse code.")
            print("\n")
            type.type("A squirrel watches you from a branch. A bat flutters overhead. The city rumbles on, but here, in this bubble of green, you can almost forget where you are.")
            print("\n")
            self.heal(random.randint(5, 10))

    # RABBIT CHASE CHAIN - DOUGHMAN NIGHT
    def chase_the_fifth_rabbit(self):
        # Fifth rabbit chase - getting desperate
        if self.get_rabbit_chase() != 4 or self.has_met("Caught Rabbit"):
            self.night_event()
            return
        
        type.type("You've lost count of how many times you've chased this rabbit. It's become personal. An obsession, some might say.")
        print("\n")
        type.type("Tonight, you spot it in the park, sitting on a bench like it owns the place. It's almost like it's waiting for you.")
        print("\n")
        type.type("You approach slowly this time. No running. No chasing. Maybe that's been your mistake all along.")
        print("\n")
        type.type("The rabbit watches you, those dark eyes gleaming with something that might be intelligence. You're within arm's reach...")
        print("\n")
        
        catch_chance = random.randrange(4)  # 25% chance
        if catch_chance == 0:
            type.type("You move like lightning, and for once, the rabbit doesn't react in time!")
            print("\n")
            type.type(green(bright("VICTORY!")))
            print("\n")
            type.type("The rabbit squeaks once, poops out an absolute fortune in coins, and explodes into a cloud of glitter. You're showered in money and sparkles.")
            print("\n")
            coins = random.randint(5000, 15000)
            type.type("When the sparkles settle, you've collected " + green(bright("$" + str(coins))) + "!")
            self.change_balance(coins)
            self.meet("Caught Rabbit")
        else:
            type.type("The rabbit lets out what can only be described as a sigh, then simply... blinks out of existence. One second it's there, the next it's gone.")
            print("\n")
            type.type(yellow("You sit on the bench for a long time, questioning reality. Is any of this real? Is the rabbit real? Are YOU real?"))
            print("\n")
            type.type(yellow("The hunt must continue. You're too deep now to quit."))
        
        self.advance_rabbit_chase()
        print("\n")

    # Nearly There Nights (900,000+)
    def woodlands_adventure(self):
        self.meet("Woodlands Adventure Event")
        type.type("The forest is different tonight. Older. Deeper. The trees seem to lean in, listening. An owl hoots three times - an omen, the old folks say.")
        print("\n")
        type.type("You sense this night will be... significant.")
        print("\n")
        type.type(yellow(bright("=== WOODLANDS ADVENTURE ===")))
        print("\n")
        event = random.choice([
            "hunting_competition", "gigantic_bear", "fountain_of_youth", "hermit_cabin", "casual_day"
        ])
        
        if event == "hunting_competition":
            type.type("Torchlight flickers through the trees. You follow it to a clearing where a dozen hunters have gathered, their faces hard and weathered. A man with a scar across his eye addresses the crowd.")
            print("\n")
            type.type(quote("The Midnight Hunt begins. Last one standing with a trophy wins the pot. Entry fee is $5,000. Rules are simple: no killing other hunters. Everything else is fair game."))
            print("\n")
            type.type("The pot looks huge. Do you enter the competition, bet on a hunter, or just observe?")
            print("\n")
            action = input("(enter/bet/observe): ").strip().lower()
            
            if action == "enter":
                if self.get_balance() >= 5000:
                    self.change_balance(-5000)
                    type.type("You pay the entry fee and receive a hunting knife. The other hunters size you up - most of them dismiss you immediately. Their mistake.")
                    print("\n")
                    type.type(yellow("=== ROUND 1: THE STALKING ==="))
                    print("\n")
                    type.type("You split off into the darkness. The forest is alive with sounds - animals, or other hunters pretending to be animals. You spot movement ahead.")
                    print("\n")
                    type.type("Do you track it, set a trap, or climb a tree for a better view?")
                    r1 = input("(track/trap/climb): ").strip().lower()
                    
                    hunter_score = 0
                    
                    if r1 == "track":
                        if random.random() < 0.5:
                            type.type("You move silently through the underbrush, following the trail. It's a deer - a big one. You mark its position.")
                            hunter_score += 1
                        else:
                            type.type("You follow the movement right into another hunter's trap. You escape, but you've wasted valuable time.")
                    elif r1 == "trap":
                        if random.random() < 0.4:
                            type.type("You rig a snare using vines and your knife. Within an hour, you've caught a rabbit. Small, but it counts.")
                            hunter_score += 1
                        else:
                            type.type("Your trap fails. You're losing time.")
                    else:
                        if random.random() < 0.6:
                            type.type("From the tree, you spot a wild boar rooting in a clearing. You mark the location and climb down.")
                            hunter_score += 2
                        else:
                            type.type("You climb, but the branches are rotten. You fall and make a ton of noise. Every animal in a mile radius knows where you are.")
                    
                    print("\n")
                    type.type(yellow("=== ROUND 2: THE KILL ==="))
                    print("\n")
                    type.type("Dawn approaches. You need to make your move. You've tracked your prey to a clearing. Other hunters are closing in - you can hear them.")
                    print("\n")
                    type.type("Do you rush in now, wait for the perfect moment, or try to sabotage another hunter?")
                    r2 = input("(rush/wait/sabotage): ").strip().lower()
                    
                    if r2 == "rush":
                        if random.random() < 0.4:
                            type.type("You burst into the clearing, knife raised. The animal bolts - but you're faster. You bring it down with a single strike.")
                            hunter_score += 2
                        else:
                            type.type("You rush in and spook everything. The animals scatter. Empty-handed.")
                    elif r2 == "wait":
                        if random.random() < 0.6:
                            type.type("Patience pays off. Another hunter rushes in, spooks the prey, and it runs directly into your path. Easy kill.")
                            hunter_score += 2
                        else:
                            type.type("You wait too long. Someone else makes the kill.")
                    else:
                        if random.random() < 0.5:
                            type.type("You throw a rock, mimicking an animal call. Another hunter takes the bait, chasing a phantom while you snag the real prize.")
                            hunter_score += 2
                        else:
                            type.type("The hunter you tried to trick isn't stupid. He catches on and now you've made an enemy.")
                            self.hurt(random.randint(10, 20))
                    
                    print("\n")
                    type.type(yellow("=== FINAL JUDGMENT ==="))
                    print("\n")
                    
                    if hunter_score >= 3:
                        type.type("The hunters gather as dawn breaks. You present your trophies. The scarred man nods, impressed.")
                        print("\n")
                        type.type(quote("We have a winner."))
                        print("\n")
                        winnings = random.randint(15000, 40000)
                        type.type("You collect " + green(bright("$" + str(winnings))) + " and the respect of the hunting community.")
                        self.change_balance(winnings)
                        self.add_item("Hunter's Mark")
                    elif hunter_score >= 1:
                        type.type("You didn't win, but you didn't embarrass yourself either. You place third and receive a consolation prize.")
                        winnings = random.randint(3000, 8000)
                        self.change_balance(winnings)
                    else:
                        type.type("You return empty-handed. The other hunters laugh. The scarred man shakes his head.")
                        print("\n")
                        type.type(quote("Stick to the city, friend."))
                    print("\n")
                else:
                    type.type("You don't have the entry fee. The scarred man waves you off dismissively.")
                    print("\n")
            
            elif action == "bet":
                type.type("You study the hunters - their gear, their posture, their eyes. One looks particularly dangerous.")
                print("\n")
                type.type("How much do you bet? ($1000 minimum)")
                try:
                    bet = int(input("Bet amount: $"))
                    if bet >= 1000 and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        type.type("You place your bet and watch the hunt from the treeline...")
                        print("\n")
                        if random.random() < 0.45:
                            winnings = bet * 3
                            type.type("Your hunter wins! You collect " + green(bright("$" + str(winnings))) + "!")
                            self.change_balance(winnings)
                        else:
                            type.type("Your hunter comes up empty. There goes your money.")
                    else:
                        type.type("You can't afford that bet, or it's below the minimum.")
                except:
                    type.type("The betting window closes. You missed your chance.")
                print("\n")
            
            else:
                type.type("You watch from the shadows. The hunt is brutal, elegant, primal. You learn things about tracking you never knew.")
                self.add_status("Tracker's Eye")
                print("\n")
        
        elif event == "gigantic_bear":
            type.type("You hear it before you see it. Branches snapping. The ground shaking. Then it emerges from the darkness - a bear the size of a truck, its eyes glowing amber in the moonlight. This isn't a normal bear. This is something OLD.")
            print("\n")
            type.type(yellow("=== CONFRONTATION: THE BEAST ==="))
            print("\n")
            type.type("The bear rises on its hind legs. It must be twelve feet tall. It sniffs the air, then looks directly at you.")
            print("\n")
            type.type("What's your move?")
            print("\n")
            action = input("(fight/flee/offer/submit): ").strip().lower()
            
            if action == "fight":
                type.type("You've lost your mind. But here goes nothing.")
                print("\n")
                type.type(yellow("=== BATTLE ==="))
                type.type("The bear charges. You have one chance.")
                print("\n")
                type.type("Do you go for the eyes, dodge and strike, or play dead at the last second?")
                attack = input("(eyes/dodge/dead): ").strip().lower()
                
                if attack == "eyes":
                    if random.random() < 0.15:
                        type.type("You lunge forward, jamming your fingers into its eyes. The bear ROARS and swipes blindly. You roll clear. Somehow, impossibly, you've hurt it.")
                        print("\n")
                        type.type("The bear backs off, shaking its massive head. It gives you one last look - respect? fear? - and disappears into the trees.")
                        print("\n")
                        type.type("You've earned the right to call yourself a monster slayer.")
                        self.add_item("Bear King's Respect")
                        self.add_status("Legend")
                    else:
                        type.type("You miss. The bear does not. Its claws tear through you like paper.")
                        self.hurt(random.randint(60, 90))
                        type.type("You wake up hours later, alive but BARELY. The bear is gone. Why didn't it finish you?")
                elif attack == "dodge":
                    if random.random() < 0.3:
                        type.type("You sidestep like a matador and slash at its flank as it passes. The bear roars in surprise. You've drawn blood from a god.")
                        print("\n")
                        type.type("The bear retreats, wounded in more than body - its pride is hurt. It leaves you a gift: a tooth, knocked loose in the scuffle.")
                        self.add_item("Giant Bear Tooth")
                        self.change_balance(random.randint(5000, 15000))
                    else:
                        type.type("You're not fast enough. The bear clips you, sending you spinning into a tree. Stars explode behind your eyes.")
                        self.hurt(random.randint(40, 70))
                else:
                    if random.random() < 0.5:
                        type.type("You drop and go limp. The bear sniffs you, its hot breath washing over your face. Don't move. Don't breathe.")
                        print("\n")
                        type.type("After an eternity, it loses interest and wanders off. You lie there until dawn, shaking, but alive.")
                    else:
                        type.type("The bear isn't fooled. It bats you around like a cat toy before getting bored and leaving. You're alive, but barely.")
                        self.hurt(random.randint(50, 80))
                print("\n")
            
            elif action == "flee":
                type.type("You RUN. Branches whip your face. Roots grab your ankles. Behind you, the thunder of the bear's pursuit.")
                print("\n")
                type.type("You see a river ahead. A cliff to your left. A thick bramble patch to your right.")
                flee = input("(river/cliff/brambles): ").strip().lower()
                
                if flee == "river":
                    if random.random() < 0.6:
                        type.type("You dive in. The current is strong but you're a good swimmer. The bear stops at the bank, unwilling to follow. You wash up downstream, exhausted but alive.")
                    else:
                        type.type("The bear follows you into the water. You fight the current AND the beast. You barely make it out, waterlogged and bleeding.")
                        self.hurt(random.randint(30, 50))
                elif flee == "cliff":
                    if random.random() < 0.4:
                        type.type("You scramble down the cliff face. The bear is too heavy to follow. You escape, but your hands are torn to ribbons from the rocks.")
                        self.hurt(random.randint(15, 25))
                    else:
                        type.type("You slip. The fall is short but brutal. The bear watches from above as you limp away, broken but breathing.")
                        self.hurt(random.randint(40, 60))
                else:
                    if random.random() < 0.7:
                        type.type("You dive into the thorns. It hurts like hell, but the bear won't follow. You crawl through, bleeding from a hundred tiny cuts, and emerge victorious.")
                        self.hurt(random.randint(10, 20))
                    else:
                        type.type("The bear crashes through the brambles like they're nothing. You're trapped. But it just looks at you, snorts, and leaves. Like you're not worth the effort.")
                print("\n")
            
            elif action == "offer":
                type.type("You slowly reach for whatever food you have. A sandwich. Some jerky. You hold it out with a trembling hand.")
                print("\n")
                type.type(quote("Here. Take it. I don't want trouble."))
                print("\n")
                if random.random() < 0.5:
                    type.type("The bear approaches slowly, sniffs your offering, and... eats it. Delicately. Almost politely. Then it sits down next to you.")
                    print("\n")
                    type.type("You spend the next hour sitting with a bear. It's the most surreal experience of your life. When it finally leaves, it drops something at your feet - a gold coin, old and worn. Where did a bear get a gold coin?")
                    self.add_item("Bear's Gold Coin")
                    self.change_balance(random.randint(3000, 8000))
                else:
                    type.type("The bear sniffs your offering... and knocks it aside. It wants something else. You run while it's distracted, and don't look back.")
                print("\n")
            
            else:  # submit
                type.type("You drop to your knees and lower your head. Total submission. You acknowledge the bear as your superior in every way.")
                print("\n")
                if random.random() < 0.6:
                    type.type("The bear studies you for a long moment. Then it does something impossible - it nods. Like it understands. Like it respects you.")
                    print("\n")
                    type.type("It turns and walks away, disappearing into the forest. You feel like you've passed some kind of test.")
                    self.add_status("Forest Blessed")
                    self.heal(random.randint(20, 40))
                else:
                    type.type("The bear isn't interested in your submission. It cuffs you once, hard, sending you flying. Then it leaves.")
                    self.hurt(random.randint(20, 35))
                print("\n")
        
        elif event == "fountain_of_youth":
            type.type("Deep in the woods, where no trail leads, you find something impossible. A spring, bubbling up from between ancient stones, its waters glowing with soft golden light. The air around it is warm despite the cold night. Flowers bloom along its banks - flowers that shouldn't exist in this season.")
            print("\n")
            type.type(yellow("=== THE FOUNTAIN ==="))
            print("\n")
            type.type("You kneel at the water's edge. Your reflection looks... younger. Healthier. Is it a trick of the light?")
            print("\n")
            type.type("What do you do?")
            print("\n")
            action = input("(drink/wash/bottle/leave): ").strip().lower()
            
            if action == "drink":
                type.type("You cup the water in your hands and drink deeply. It's cold and sweet, like nothing you've ever tasted.")
                print("\n")
                type.type("Warmth spreads through your body. Old aches disappear. Scars fade. You feel... ALIVE.")
                self.heal(100)
                print("\n")
                side_effect = random.choice(["good", "bad", "neutral"])
                if side_effect == "good":
                    type.type("The effect lingers. You feel younger, stronger, luckier. Like the world has decided to give you a second chance.")
                    self.add_status("Youthful")
                    self.add_status("Blessed")
                elif side_effect == "bad":
                    type.type("But something else happens too. Your hair starts to gray. Your hands shake. The fountain gives... but it also takes. You've traded years of your future for this moment of healing.")
                    self.add_status("Time-Touched")
                else:
                    type.type("The effect is temporary, you can feel it. But for now, you feel incredible.")
                print("\n")
            elif action == "wash":
                type.type("You wash your face and hands in the water. Every cut, every bruise, every mark of your hard life washes away.")
                self.heal(random.randint(50, 75))
                print("\n")
                type.type("You don't look younger exactly, but you look... refreshed. Like you just woke up from the best sleep of your life.")
                print("\n")
            elif action == "bottle":
                type.type("You fill your canteen with the glowing water. As you seal it, the glow fades slightly, but the water still shimmers.")
                self.add_item("Fountain Water")
                print("\n")
                type.type("You have no idea what this will do when you drink it later. But you have a feeling it'll be worth something.")
                print("\n")
            else:
                type.type("You step back from the fountain. Something about it feels wrong. Too good. Nothing is free in this world.")
                print("\n")
                type.type("As you leave, you swear you hear laughter from the water. Did you make the right choice? You'll never know.")
                print("\n")
        
        elif event == "hermit_cabin":
            type.type("Smoke rises from a chimney you didn't expect. A cabin, hidden among the trees, so well-camouflaged you almost walked into the door.")
            print("\n")
            type.type("A sign hangs crooked: 'KNOCK OR DON'T. EITHER WAY, I KNOW YOU'RE THERE.'")
            print("\n")
            type.type("Do you knock, peek in the window, or leave?")
            action = input("(knock/peek/leave): ").strip().lower()
            
            if action == "knock":
                type.type("The door opens before your knuckles touch wood. An old woman stands there, wrapped in furs, eyes like chips of ice.")
                print("\n")
                type.type(quote("Took you long enough. Come in. I've been waiting."))
                print("\n")
                type.type("Inside, the cabin is filled with herbs, bones, books, and things you can't identify. She gestures to a chair.")
                print("\n")
                type.type(quote("I know why you're here. The gambling. The debt. The endless road. You want out, don't you?"))
                print("\n")
                answer = ask.yes_or_no("Tell her the truth?")
                if answer == "yes":
                    type.type("She nods slowly. " + quote("Honesty. Good. I can help you, but it'll cost you. Not money. Something else."))
                    print("\n")
                    type.type("She offers three options: your luckiest memory, a year of your life, or a favor to be named later.")
                    cost = input("(memory/year/favor): ").strip().lower()
                    if cost == "memory":
                        type.type("She reaches toward your forehead. A flash of light. You can't remember... something. Something that used to make you happy. But in exchange, you feel LUCKY. Deeply, impossibly lucky.")
                        self.add_status("Witch Lucky")
                        self.change_balance(random.randint(10000, 25000))
                    elif cost == "year":
                        type.type("She takes your hand. You feel a jolt, and suddenly you're... older. Just slightly. But in return, she gives you something - a bag that clinks with gold.")
                        self.change_balance(random.randint(15000, 35000))
                        self.add_status("Aged")
                    else:
                        type.type("She grins. " + quote("Smart. Or stupid. We'll see.") + " She gives you a coin - old, worn, glowing faintly. " + quote("When you need help, flip this. I'll know."))
                        self.add_item("Witch's Favor")
                else:
                    type.type("She laughs. " + quote("A liar. I can work with that.") + " She hands you a vial of something dark. " + quote("Drink this. It won't kill you. Probably."))
                    self.add_item("Mystery Potion")
                print("\n")
            elif action == "peek":
                type.type("You creep to the window and peer inside. The old woman is sitting at a table, staring directly at you.")
                print("\n")
                type.type(quote("I can see you, fool."))
                print("\n")
                type.type("The door flies open. She doesn't look happy.")
                print("\n")
                type.type(quote("Peepers get what peepers deserve."))
                print("\n")
                if random.random() < 0.5:
                    type.type("She throws something in your face. Your vision goes dark. When it clears, you're a mile away with no memory of how you got there. But there's money in your pocket that wasn't there before. Witch logic.")
                    self.change_balance(random.randint(2000, 8000))
                else:
                    type.type("She curses you. You feel it settle into your bones like cold water.")
                    self.add_status("Witch Cursed")
                    self.hurt(random.randint(15, 30))
                print("\n")
            else:
                type.type("You back away from the cabin. Some doors are better left unknocked.")
                print("\n")
                type.type("As you leave, you hear her voice on the wind: " + quote("We'll meet again."))
                print("\n")
        
        else:
            type.type("The forest is quiet tonight. No adventures find you - or perhaps you weren't ready for them.")
            print("\n")
            type.type("You rest beneath an ancient oak, listening to the wind in the leaves. Sometimes the greatest adventure is simply being still.")
            self.heal(random.randint(15, 30))
            print("\n")



    def swamp_adventure(self):
        self.meet("Swamp Adventure Event")
        type.type("The swamp stretches before you, endless and alive. Cypress trees draped in moss rise from black water like the fingers of drowned giants. Strange lights flicker in the distance. The air smells of decay and growth, death and life tangled together.")
        print("\n")
        type.type(yellow(bright("=== SWAMP ADVENTURE ===")))
        print("\n")
        event = random.choice([
            "tortoise_racing", "ogre", "fairy_bottle", "disgusting_mermaid", "gator_wrestling", "casual_day"
        ])
        
        if event == "tortoise_racing":
            type.type("You hear cheering ahead - actual cheering, deep in the swamp. Following the sound, you emerge into a torchlit clearing where a crowd of swamp folk has gathered around a muddy track.")
            print("\n")
            type.type("They're racing TORTOISES. And betting HEAVILY.")
            print("\n")
            type.type(yellow("=== TORTOISE GRAND PRIX ==="))
            print("\n")
            type.type("A grizzled man with no teeth approaches you. " + quote("Stranger! You want action? Entry fee's $2,000 to race. Or you can bet on any turtle you like."))
            print("\n")
            type.type("The tortoises are lined up: Ol' Mossy (the favorite), Lightning Lou (young and fast), Shellshock Sally (unpredictable), and Mud Monster (the underdog).")
            print("\n")
            action = input("(race/bet/watch): ").strip().lower()
            
            if action == "race":
                if self.get_balance() >= 2000:
                    self.change_balance(-2000)
                    type.type("You're handed a tortoise named 'City Slicker' - apparently what they call any newcomer's turtle. It blinks at you slowly.")
                    print("\n")
                    type.type(yellow("=== RACE START ==="))
                    type.type("The tortoises are released! City Slicker immediately starts heading the wrong direction.")
                    print("\n")
                    type.type("Quick! How do you motivate your tortoise?")
                    r1 = input("(lettuce/yelling/poking): ").strip().lower()
                    
                    race_score = random.randint(0, 3)  # Base randomness
                    
                    if r1 == "lettuce":
                        if self.has_item("Lettuce") or random.random() < 0.3:
                            type.type("You wave lettuce in front of City Slicker's face. It SNAPS to attention and starts moving!")
                            race_score += 2
                        else:
                            type.type("You don't have lettuce! City Slicker continues his existential wandering.")
                    elif r1 == "yelling":
                        if random.random() < 0.4:
                            type.type("Your screaming seems to startle City Slicker into moving faster. Who knew tortoises responded to psychological warfare?")
                            race_score += 1
                        else:
                            type.type("City Slicker is unimpressed by your volume. He withdraws into his shell for a nap.")
                    else:
                        if random.random() < 0.5:
                            type.type("You poke City Slicker's rear. He gives you a look of pure betrayal but does start moving.")
                            race_score += 1
                        else:
                            type.type("City Slicker bites your finger. You deserve this.")
                            self.hurt(random.randint(1, 5))
                    
                    print("\n")
                    type.type("The race enters the final stretch! City Slicker is neck-and-neck with Shellshock Sally!")
                    print("\n")
                    type.type("Do you cheer, pray, or throw something to distract the other tortoises?")
                    r2 = input("(cheer/pray/throw): ").strip().lower()
                    
                    if r2 == "throw":
                        if random.random() < 0.5:
                            type.type("You throw a pebble near Sally. She veers off course! The crowd boos but you don't care!")
                            race_score += 2
                        else:
                            type.type("A swamp man catches your throw. " + quote("CHEATER!") + " They disqualify City Slicker.")
                            race_score = 0
                    elif r2 == "pray":
                        type.type("You close your eyes and pray to whatever swamp gods might be listening.")
                        if random.random() < 0.3:
                            type.type("The swamp gods answer. A gust of wind pushes City Slicker forward!")
                            race_score += 2
                        else:
                            type.type("The swamp gods are busy. Or don't exist. Probably both.")
                    else:
                        type.type("You cheer like a maniac. City Slicker seems to appreciate the support.")
                        race_score += 1
                    
                    print("\n")
                    type.type(yellow("=== FINISH LINE ==="))
                    print("\n")
                    
                    if race_score >= 5:
                        type.type("CITY SLICKER WINS! The crowd goes WILD. The toothless man looks stunned.")
                        print("\n")
                        type.type(quote("First time anyone ever won with that turtle..."))
                        print("\n")
                        winnings = random.randint(12000, 25000)
                        type.type("You collect " + green(bright("$" + str(winnings))) + " and the title of Tortoise Champion.")
                        self.change_balance(winnings)
                        self.add_item("Tortoise Trophy")
                    elif race_score >= 3:
                        type.type("City Slicker places second! Not bad for a newcomer.")
                        winnings = random.randint(4000, 8000)
                        type.type("You win " + green(bright("$" + str(winnings))) + ".")
                        self.change_balance(winnings)
                    else:
                        type.type("City Slicker finishes dead last. He seems proud of himself anyway.")
                        type.type("You leave with nothing but a newfound respect for tortoises.")
                    print("\n")
                else:
                    type.type("You can't afford the entry fee. The toothless man shrugs sympathetically.")
                    print("\n")
            
            elif action == "bet":
                type.type("Which tortoise do you bet on?")
                type.type("1. Ol' Mossy (2:1 odds)")
                type.type("2. Lightning Lou (3:1 odds)")
                type.type("3. Shellshock Sally (5:1 odds)")
                type.type("4. Mud Monster (10:1 odds)")
                turtle = input("Pick a number (1-4): ").strip()
                
                type.type("How much do you bet?")
                try:
                    bet = int(input("Bet: $"))
                    if bet > 0 and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        winner = random.choice(["mossy", "mossy", "lou", "lou", "sally", "monster"])
                        
                        if turtle == "1" and winner == "mossy":
                            type.type("Ol' Mossy wins! You collect " + green(bright("$" + str(bet * 2))) + "!")
                            self.change_balance(bet * 2)
                        elif turtle == "2" and winner == "lou":
                            type.type("Lightning Lou blazes to victory! You win " + green(bright("$" + str(bet * 3))) + "!")
                            self.change_balance(bet * 3)
                        elif turtle == "3" and winner == "sally":
                            type.type("Shellshock Sally shocks everyone! You win " + green(bright("$" + str(bet * 5))) + "!")
                            self.change_balance(bet * 5)
                        elif turtle == "4" and winner == "monster":
                            type.type("MUD MONSTER WINS! THE UNDERDOG! You win " + green(bright("$" + str(bet * 10))) + "!!!")
                            self.change_balance(bet * 10)
                            self.add_status("Lucky Gambler")
                        else:
                            type.type("Your tortoise lost. Better luck next time.")
                    else:
                        type.type("You can't bet what you don't have.")
                except:
                    type.type("Betting closed. You missed your chance.")
                print("\n")
            
            else:
                type.type("You watch the race from the sidelines. Ol' Mossy wins. The crowd exchanges money. You learn something about patience and betting.")
                self.add_status("Swamp Wise")
                print("\n")
        
        elif event == "ogre":
            type.type("The ground shakes. Trees topple. And then you see it - an OGRE, three times your height, covered in moss and mud, carrying a club made from an entire tree trunk.")
            print("\n")
            type.type(yellow("=== BOSS ENCOUNTER: THE SWAMP OGRE ==="))
            print("\n")
            type.type("It sees you. Its tiny eyes narrow. Its massive mouth opens, revealing teeth like tombstones.")
            print("\n")
            type.type(quote("LITTLE THING IN OGRE'S SWAMP. OGRE NOT LIKE."))
            print("\n")
            action = input("(fight/bribe/riddle/run): ").strip().lower()
            
            if action == "fight":
                type.type(yellow("=== BATTLE: YOU VS. OGRE ==="))
                type.type("This is either very brave or very stupid. The ogre swings its club.")
                print("\n")
                type.type("How do you attack?")
                attack = input("(kneecaps/climb/distract): ").strip().lower()
                
                if attack == "kneecaps":
                    type.type("You go low, slashing at its knees. The ogre HOWLS.")
                    if random.random() < 0.3:
                        type.type("It crumples! You've crippled a monster three times your size!")
                        print("\n")
                        type.type("The ogre crawls away, whimpering. In its nest, you find its hoard - gold, gems, and bones. You take the valuables and leave the bones.")
                        self.change_balance(random.randint(15000, 35000))
                        self.add_item("Ogre's Gemstone")
                    else:
                        type.type("But it doesn't go down. The backhand sends you flying into the swamp.")
                        self.hurt(random.randint(40, 70))
                elif attack == "climb":
                    type.type("You run up its leg like climbing a hairy tree. It swats at you but you're too fast.")
                    if random.random() < 0.25:
                        type.type("You reach its head and jam your knife into its ear! The ogre SCREAMS and throws you off, but it's hurt BAD.")
                        print("\n")
                        type.type("It stumbles away into the swamp, leaving behind a trail of blood and treasure it dropped.")
                        self.change_balance(random.randint(8000, 20000))
                    else:
                        type.type("It grabs you mid-climb and squeezes. You hear ribs cracking.")
                        self.hurt(random.randint(50, 80))
                else:
                    type.type("You throw mud in its eyes! " + quote("ARGH! OGRE NO SEE!"))
                    if random.random() < 0.5:
                        type.type("While it's blinded, you escape with some gold from its belt pouch.")
                        self.change_balance(random.randint(3000, 8000))
                    else:
                        type.type("It swings wildly - and connects. Blind luck, literally.")
                        self.hurt(random.randint(35, 60))
                print("\n")
            
            elif action == "bribe":
                type.type(quote("Wait! I have gold! You like gold, right?"))
                print("\n")
                type.type("The ogre pauses. Its tiny brain processes this information.")
                print("\n")
                type.type(quote("OGRE... LIKE SHINY THINGS."))
                print("\n")
                type.type("How much do you offer? ($3000 minimum)")
                try:
                    bribe = int(input("Offer: $"))
                    if bribe >= 3000 and self.get_balance() >= bribe:
                        self.change_balance(-bribe)
                        if bribe >= 8000:
                            type.type("The ogre's eyes go wide. " + quote("MUCH SHINY! OGRE HAPPY!") + " It lets you pass AND gives you a 'gift' - a crusty but valuable gem from its pocket.")
                            self.add_item("Ogre's Gift")
                        else:
                            type.type("The ogre snatches the gold and counts it on its fingers. It lets you pass, but watches you until you're out of sight.")
                    else:
                        type.type("The ogre isn't impressed. " + quote("LITTLE THING TRY TRICK OGRE!") + " It swings its club.")
                        self.hurt(random.randint(30, 50))
                except:
                    type.type("The ogre grows impatient with your fumbling.")
                    self.hurt(random.randint(20, 40))
                print("\n")
            
            elif action == "riddle":
                type.type(quote("Wait! I challenge you to a battle of wits!"))
                print("\n")
                type.type("The ogre stops. Scratches its head.")
                print("\n")
                type.type(quote("OGRE... LIKE RIDDLES?"))
                print("\n")
                type.type("You pose a riddle: 'What walks on four legs in the morning, two at noon, and three in the evening?'")
                print("\n")
                type.type("The ogre thinks. Steam seems to come from its ears. Finally:")
                print("\n")
                type.type(quote("OGRE KNOW! IS... IS..."))
                if random.random() < 0.3:
                    type.type(quote("...HUMAN THING!"))
                    print("\n")
                    type.type("The ogre solved the riddle. It grins proudly. " + quote("NOW OGRE EAT YOU ANYWAY."))
                    self.hurt(random.randint(40, 60))
                else:
                    type.type(quote("...OGRE NO KNOW. OGRE HEAD HURT."))
                    print("\n")
                    type.type("The ogre sits down, defeated, holding its head. You slip past while it's having an existential crisis. On the way, you snag some gold from its belt.")
                    self.change_balance(random.randint(5000, 12000))
                print("\n")
            
            else:
                type.type("You RUN. The ogre gives chase, but you're faster and you know how to use the terrain.")
                if random.random() < 0.6:
                    type.type("You dive into water too deep for the ogre to follow. It roars in frustration as you swim away.")
                else:
                    type.type("It catches you by the ankle. The throw is spectacular - you land in a mud pit fifty feet away.")
                    self.hurt(random.randint(25, 45))
                print("\n")
        
        elif event == "fairy_bottle":
            type.type("Something glows in the hollow of a dead tree. You approach carefully - could be a trap, could be treasure, could be both.")
            print("\n")
            type.type("It's a bottle. Inside the bottle is a fairy, no bigger than your thumb, wings pressed against the glass. She looks FURIOUS.")
            print("\n")
            type.type(yellow("=== THE TRAPPED FAIRY ==="))
            print("\n")
            type.type("She pounds on the glass. Her tiny voice is muffled but you can make out: " + quote("LET ME OUT, YOU GIANT OAF!"))
            print("\n")
            action = input("(free/keep/negotiate/ignore): ").strip().lower()
            
            if action == "free":
                type.type("You uncork the bottle. The fairy shoots out like a tiny, angry bullet, circling your head.")
                print("\n")
                type.type(quote("Finally! I've been trapped in there for DECADES by that stupid witch!"))
                print("\n")
                type.type("She lands on your shoulder, catching her breath.")
                print("\n")
                type.type(quote("You freed me, so I owe you. THREE wishes. And before you ask - no immortality, no resurrection, no time travel. I'm a swamp fairy, not a god."))
                print("\n")
                for i in range(3):
                    type.type(f"Wish {i+1} of 3:")
                    wish = input("(money/luck/health/item/info): ").strip().lower()
                    if wish == "money":
                        amount = random.randint(5000, 15000)
                        type.type("The fairy waves her hand. Your pockets suddenly feel heavier. " + green(bright("$" + str(amount))) + " appears.")
                        self.change_balance(amount)
                    elif wish == "luck":
                        type.type("The fairy sprinkles dust on you. " + quote("You'll be lucky for a while. Don't waste it."))
                        self.add_status("Fairy Lucky")
                    elif wish == "health":
                        type.type("The fairy touches your forehead. Warmth spreads through you, healing old wounds.")
                        self.heal(random.randint(40, 60))
                    elif wish == "item":
                        type.type("The fairy conjures something from thin air - a glowing acorn.")
                        type.type(quote("Plant this somewhere and come back in a year. You'll like what grows."))
                        self.add_item("Magic Acorn")
                    else:
                        type.type("The fairy whispers a secret in your ear - the location of something valuable, hidden nearby.")
                        self.add_item("Fairy's Secret Map")
                    print("\n")
                
                type.type("The fairy stretches her wings. " + quote("We're square now. Don't let any witches catch you - they're vindictive."))
                print("\n")
                type.type("She disappears into the swamp, trailing sparkles.")
                self.add_status("Fairy Friend")
                print("\n")
            
            elif action == "keep":
                type.type("You pocket the bottle. The fairy goes BALLISTIC, screaming tiny curses at you.")
                print("\n")
                type.type(quote("YOU'LL REGRET THIS! MY SISTERS WILL FIND YOU!"))
                print("\n")
                type.type("But she's trapped. And fairies are worth a LOT to the right buyer.")
                self.add_item("Captured Fairy")
                self.add_status("Fairy Cursed")
                print("\n")
            
            elif action == "negotiate":
                type.type(quote("What's in it for me if I let you out?"))
                print("\n")
                type.type("The fairy stops pounding. She considers.")
                print("\n")
                type.type(quote("Freedom first. Then we talk. I'm not making promises from inside a bottle."))
                print("\n")
                type.type("Do you trust her?")
                trust = ask.yes_or_no()
                if trust == "yes":
                    type.type("You open the bottle. The fairy stretches her wings and sighs with relief.")
                    print("\n")
                    type.type(quote("Okay, fine. One wish. That's the deal."))
                    wish = input("(money/luck/health): ").strip().lower()
                    if wish == "money":
                        self.change_balance(random.randint(8000, 18000))
                        type.type("Gold appears from nowhere. " + quote("Happy now, greedy giant?"))
                    elif wish == "luck":
                        self.add_status("Negotiator's Luck")
                        type.type("She sighs and sprinkles dust on you.")
                    else:
                        self.heal(random.randint(50, 80))
                        type.type("She touches your heart. Pain fades away.")
                    print("\n")
                else:
                    type.type("You walk away, leaving her in the bottle. Her screams follow you for a long time.")
                print("\n")
            
            else:
                type.type("You leave the fairy where she is. Not your problem.")
                print("\n")
                type.type("As you walk away, you hear her sobbing. It almost makes you feel bad. Almost.")
                print("\n")
        
        elif event == "disgusting_mermaid":
            type.type("You see her sitting on a log in the middle of the swamp - a mermaid. But not the beautiful kind from stories.")
            print("\n")
            type.type("This mermaid is HIDEOUS. Covered in algae, barnacles growing on her scales, breath like rotting fish. She grins at you with teeth like broken bottles.")
            print("\n")
            type.type(yellow("=== THE SWAMP MERMAID ==="))
            print("\n")
            type.type(quote("Hello, handsome,") + " she rasps. " + quote("It's been sooooo long since I had company. How about a kiss?"))
            print("\n")
            action = input("(kiss/talk/run/insult): ").strip().lower()
            
            if action == "kiss":
                type.type("You close your eyes, hold your breath, and lean in. The kiss is... wet. Very wet. And cold. And it tastes like a fish market in summer.")
                print("\n")
                outcome = random.choice(["good", "bad", "weird"])
                if outcome == "good":
                    type.type("When you pull back, the mermaid is... beautiful? Was she always beautiful? You can't remember.")
                    print("\n")
                    type.type(quote("A brave soul! Take this gift, and remember: true beauty is seeing past the surface."))
                    print("\n")
                    self.add_item("Mermaid's Pearl")
                    self.change_balance(random.randint(10000, 25000))
                    self.add_status("Mermaid Kissed")
                elif outcome == "bad":
                    type.type("The mermaid's grip tightens. She tries to drag you into the water!")
                    print("\n")
                    type.type("You fight her off, barely escaping with your life and a collection of bruises.")
                    self.hurt(random.randint(25, 45))
                else:
                    type.type("The mermaid giggles and releases you. " + quote("That was nice. Here, have a fish."))
                    print("\n")
                    type.type("She hands you a literal fish. It's alive and flopping. Why did you kiss a swamp mermaid?")
                    self.add_item("Live Fish")
                print("\n")
            
            elif action == "talk":
                type.type(quote("So... how did you end up here?"))
                print("\n")
                type.type("The mermaid sighs, a sound like a drain unclogging.")
                print("\n")
                type.type(quote("I used to be beautiful, you know. Queen of the coral palace. Then I made fun of a sea witch's nose. One curse later, here I am. Eternal ugliness, stuck in a swamp."))
                print("\n")
                type.type("She looks genuinely sad. Do you try to comfort her?")
                comfort = ask.yes_or_no()
                if comfort == "yes":
                    type.type(quote("Beauty fades anyway. At least you're still you."))
                    print("\n")
                    type.type("The mermaid stares at you. A tear rolls down her barnacled cheek.")
                    print("\n")
                    type.type(quote("That's... the nicest thing anyone's said to me in three hundred years."))
                    print("\n")
                    type.type("She gives you a handful of pearls from her hair. They're grimy, but real.")
                    self.change_balance(random.randint(5000, 12000))
                    self.add_status("Mermaid Friend")
                else:
                    type.type("The mermaid shrugs. " + quote("Yeah, I wouldn't comfort me either."))
                print("\n")
            
            elif action == "insult":
                type.type(quote("Wow, you're really ugly."))
                print("\n")
                type.type("The mermaid's face twists with rage.")
                print("\n")
                type.type(quote("HOW DARE YOU!"))
                print("\n")
                type.type("She lunges. You run. She can't follow on land, but she throws things - rocks, fish, profanities.")
                self.hurt(random.randint(10, 25))
                print("\n")
            
            else:
                type.type("You start backing away slowly. The mermaid's face falls.")
                print("\n")
                type.type(quote("Everyone always runs..."))
                print("\n")
                type.type("You feel a little bad, but not bad enough to stay.")
                print("\n")
        
        elif event == "gator_wrestling":
            type.type("A crowd of swamp folk stands around a muddy pit. Inside, a man is wrestling an ALLIGATOR. And winning.")
            print("\n")
            type.type("He pins the gator, and the crowd erupts. Money changes hands. A man with a megaphone spots you.")
            print("\n")
            type.type(quote("YOU THERE! Stranger! You look strong! Wanna try your luck against SALLY? Only $1,000 entry, winner takes the pot!"))
            print("\n")
            type.type(yellow("=== GATOR WRESTLING ==="))
            print("\n")
            action = input("(wrestle/bet/watch/nope): ").strip().lower()
            
            if action == "wrestle":
                if self.get_balance() >= 1000:
                    self.change_balance(-1000)
                    type.type("You climb into the pit. Sally the gator eyes you hungrily. She's twelve feet long and NOT happy.")
                    print("\n")
                    type.type(yellow("=== ROUND 1: THE STAREDOWN ==="))
                    type.type("Sally hisses. The crowd goes quiet. What's your opening move?")
                    r1 = input("(circle/charge/taunt): ").strip().lower()
                    
                    gator_score = 0
                    
                    if r1 == "circle":
                        type.type("You circle slowly, keeping Sally's eyes on you. She turns, watching, waiting.")
                        if random.random() < 0.6:
                            type.type("She lunges left - you dodge right. Good read!")
                            gator_score += 1
                        else:
                            type.type("She fakes left and catches your leg. You pull free, but you're bleeding.")
                            self.hurt(random.randint(10, 20))
                    elif r1 == "charge":
                        type.type("You CHARGE like a maniac, diving at Sally before she can react!")
                        if random.random() < 0.4:
                            type.type("You land on her back! The crowd ROARS!")
                            gator_score += 2
                        else:
                            type.type("She rolls. You miss. She doesn't. Her tail whips your legs out.")
                            self.hurt(random.randint(15, 25))
                    else:
                        type.type("You pound your chest and scream at the gator. Sally looks... confused? Insulted?")
                        if random.random() < 0.5:
                            type.type("The confusion gives you an opening!")
                            gator_score += 1
                        else:
                            type.type("Sally charges in pure anger. You barely dodge.")
                    
                    print("\n")
                    type.type(yellow("=== ROUND 2: THE GRAPPLE ==="))
                    type.type("Sally and you are tangled up in the mud. Her jaws are inches from your arm!")
                    r2 = input("(jaw_clamp/roll/escape): ").strip().lower()
                    
                    if r2 == "jaw_clamp":
                        type.type("You grab her jaws and HOLD THEM SHUT. Gators have weak jaw-opening muscles!")
                        if random.random() < 0.6:
                            type.type("IT WORKS! Sally struggles but can't open her mouth!")
                            gator_score += 2
                        else:
                            type.type("She's too strong. She snaps free and you only barely get your hands away.")
                    elif r2 == "roll":
                        type.type("You roll WITH her death roll, using momentum!")
                        if random.random() < 0.5:
                            type.type("Genius move! You end up on top!")
                            gator_score += 2
                        else:
                            type.type("You get disoriented and she lands on top of you. The crowd gasps.")
                            self.hurt(random.randint(15, 25))
                    else:
                        type.type("You slip free and create distance. Smart but not impressive.")
                        gator_score += 1
                    
                    print("\n")
                    type.type(yellow("=== FINAL: THE PIN ==="))
                    
                    if gator_score >= 4:
                        type.type("You've got Sally pinned! Her legs churn the mud but she can't escape! The referee counts to three - YOU WIN!")
                        winnings = random.randint(8000, 20000)
                        type.type("You collect " + green(bright("$" + str(winnings))) + " and the title of GATOR CHAMPION!")
                        self.change_balance(winnings)
                        self.add_item("Gator Tooth Necklace")
                    elif gator_score >= 2:
                        type.type("Neither you nor Sally can get the advantage. The referee calls it a draw!")
                        type.type("You get your entry fee back, plus a little extra for the entertainment.")
                        self.change_balance(2000)
                    else:
                        type.type("Sally pins YOU. Her jaws open wide - but the handlers pull her off. You lost, but you survived. That's something.")
                        self.lose_sanity(random.choice([3, 4, 5]))  # Near-death by gator
                    print("\n")
                else:
                    type.type("You can't afford the entry fee. The announcer looks disappointed.")
                    print("\n")
            
            elif action == "bet":
                type.type("Who do you bet on? The current champion is Big Earl. The challenger is a tourist from Florida.")
                bet = random.randint(500, 2000)
                if self.get_balance() >= bet:
                    self.change_balance(-bet)
                    if random.random() < 0.5:
                        type.type("Big Earl wins! You collect " + green(bright("$" + str(bet * 2))) + "!")
                        self.change_balance(bet * 2)
                    else:
                        type.type("The tourist wins! Upset of the century! There goes your money.")
                else:
                    type.type("You don't have enough to bet.")
                print("\n")
            
            elif action == "watch":
                type.type("You watch match after match. People get bit, thrown, and occasionally victorious. It's the best worst entertainment you've ever seen.")
                self.add_status("Entertained")
                print("\n")
            
            else:
                type.type(quote("NOPE.") + " You walk away. Some experiences aren't worth having.")
                print("\n")
        
        else:
            type.type("Tonight, the swamp is quiet. You rest beneath the moss-draped trees, listening to the bullfrogs and the distant splash of gators. The dreams that come are strange and wild, but not unpleasant.")
            self.heal(random.randint(15, 30))
            print("\n")



    def beach_adventure(self):
        self.meet("Beach Adventure Event")
        type.type("The moon hangs low over the endless sand. The beach is alive with laughter, music, and the crash of waves. Tiki torches line the shore. Tonight, anything could happen.")
        print("\n")
        type.type(yellow(bright("=== BEACH ADVENTURE ===")))
        print("\n")
        event = random.choice([
            "volleyball_tournament", "bonfire_ritual", "message_in_bottle", "crab_racing", "sandcastle_contest", "casual_day"
        ])
        
        if event == "volleyball_tournament":
            type.type("A crowd gathers around lit courts - the MIDNIGHT VOLLEYBALL CHAMPIONSHIP is happening!")
            print("\n")
            type.type(yellow("=== MIDNIGHT VOLLEYBALL TOURNAMENT ==="))
            print("\n")
            type.type("A buff guy with a clipboard approaches. " + quote("We need a fourth! Entry is $3,000, winner's pot is $50,000. You in?"))
            print("\n")
            action = input("(join/bet/watch/nope): ").strip().lower()
            
            if action == "join":
                if self.get_balance() >= 3000:
                    self.change_balance(-3000)
                    type.type("You're placed on Team Sunset - two surfer bros and a surprisingly athletic grandma.")
                    print("\n")
                    
                    # Match 1
                    type.type(yellow("=== ROUND 1: vs. THE BEACH BUMS ==="))
                    type.type("They look drunk. This should be easy.")
                    type.type("The serve comes your way! What do you do?")
                    m1 = input("(bump/spike/dive): ").strip().lower()
                    
                    team_score = random.randint(0, 2)
                    
                    if m1 == "spike":
                        if random.random() < 0.4:
                            type.type("You SLAM it down! The drunk guys don't even react in time!")
                            team_score += 2
                        else:
                            type.type("You swing and miss. The grandma sighs heavily.")
                    elif m1 == "bump":
                        if random.random() < 0.6:
                            type.type("Clean bump! Grandma sets it, surfer bro spikes it. POINT!")
                            team_score += 1
                        else:
                            type.type("You bump it into the net. Whoops.")
                    else:
                        if random.random() < 0.5:
                            type.type("Epic dive! You save an impossible shot! The crowd goes wild!")
                            team_score += 2
                        else:
                            type.type("You dive face-first into sand. You eat a lot of sand.")
                            self.hurt(random.randint(5, 10))
                    
                    print("\n")
                    
                    # Match 2
                    type.type(yellow("=== ROUND 2: vs. THE PROS ==="))
                    type.type("These guys are SERIOUS. Matching uniforms. Headbands. Game faces.")
                    type.type("It's match point. The pressure is ON. The ball's coming fast!")
                    m2 = input("(block/set/cheer): ").strip().lower()
                    
                    if m2 == "block":
                        if random.random() < 0.3:
                            type.type("You time it PERFECTLY. The spike bounces off your hands and down!")
                            team_score += 3
                        else:
                            type.type("Too slow. It rockets past you.")
                    elif m2 == "set":
                        if random.random() < 0.5:
                            type.type("Beautiful set! Grandma, where did she learn to spike like that?!")
                            team_score += 2
                        else:
                            type.type("Your set goes wild. The surfer bros look disappointed.")
                    else:
                        type.type("You cheer instead of playing. Your team loses the point, but appreciates the morale support.")
                        team_score += 1
                    
                    print("\n")
                    
                    # Finals
                    type.type(yellow("=== FINALS: vs. THE CHAMPIONS ==="))
                    type.type("The defending champions. They've won five years running. The grandma cracks her knuckles.")
                    type.type("Final play. Everything comes down to this!")
                    m3 = input("(trust_grandma/go_hero/teamwork): ").strip().lower()
                    
                    if m3 == "trust_grandma":
                        type.type("You set up the grandma. She leaps - higher than any grandma should - and DESTROYS the ball!")
                        team_score += 3
                    elif m3 == "go_hero":
                        if random.random() < 0.3:
                            type.type("You take the shot yourself. Time slows. The ball sails over the net... and IN!")
                            team_score += 4
                        else:
                            type.type("You go for glory and miss. The surfer bros shake their heads.")
                    else:
                        type.type("Perfect teamwork! Bump, set, spike chain. The champions look SHOCKED!")
                        team_score += 2
                    
                    print("\n")
                    type.type(yellow("=== TOURNAMENT RESULTS ==="))
                    
                    if team_score >= 9:
                        type.type("TEAM SUNSET WINS THE CHAMPIONSHIP! The crowd ERUPTS!")
                        print("\n")
                        type.type("Grandma high-fives you hard enough to leave a bruise.")
                        winnings = random.randint(15000, 35000)
                        type.type("You collect your share: " + green(bright("$" + str(winnings))) + "!")
                        self.change_balance(winnings)
                        self.add_item("Championship Medal")
                    elif team_score >= 6:
                        type.type("Second place! Not bad for a pickup team!")
                        winnings = random.randint(6000, 12000)
                        type.type("You win " + green(bright("$" + str(winnings))) + ".")
                        self.change_balance(winnings)
                    else:
                        type.type("You're eliminated early, but the grandma gives you her number. 'For training,' she says.")
                        self.add_item("Grandma's Number")
                    print("\n")
                else:
                    type.type("You can't afford the entry fee. Better luck next time.")
                    print("\n")
            
            elif action == "bet":
                type.type("Which team do you bet on?")
                type.type("1. The Champions (2:1)")
                type.type("2. Team Sunset (5:1)")
                type.type("3. The Pros (3:1)")
                type.type("4. The Beach Bums (15:1)")
                pick = input("Pick a number (1-4): ").strip()
                
                type.type("How much do you bet?")
                try:
                    bet = int(input("Bet: $"))
                    if bet > 0 and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        winner = random.choice(["champs", "champs", "sunset", "pros", "pros", "bums"])
                        
                        if pick == "1" and winner == "champs":
                            type.type("The Champions win, as expected. You collect " + green(bright("$" + str(bet * 2))) + ".")
                            self.change_balance(bet * 2)
                        elif pick == "2" and winner == "sunset":
                            type.type("The pickup team wins! " + green(bright("$" + str(bet * 5))) + "!")
                            self.change_balance(bet * 5)
                        elif pick == "3" and winner == "pros":
                            type.type("The Pros take it! " + green(bright("$" + str(bet * 3))) + "!")
                            self.change_balance(bet * 3)
                        elif pick == "4" and winner == "bums":
                            type.type("THE DRUNK GUYS WON?! IMPOSSIBLE! " + green(bright("$" + str(bet * 15))) + "!!!")
                            self.change_balance(bet * 15)
                            self.add_status("Chaos Gambler")
                        else:
                            type.type("Your team lost. The sand claims your money.")
                    else:
                        type.type("You don't have that kind of money.")
                except:
                    type.type("The betting window closes before you can decide.")
                print("\n")
            
            elif action == "watch":
                type.type("You watch the tournament unfold. The underdog team with the athletic grandma actually wins! You feel inspired by their story.")
                self.add_status("Inspired")
                print("\n")
            
            else:
                type.type("You decline and walk away. Volleyball isn't for everyone.")
                print("\n")
        
        elif event == "bonfire_ritual":
            type.type("A circle of strangers in flowing robes beckons you toward a massive bonfire. Sparks spiral into the stars. They're chanting something ancient.")
            print("\n")
            type.type(yellow("=== THE BONFIRE RITUAL ==="))
            print("\n")
            type.type("A woman with ocean eyes approaches. " + quote("Traveler, the flames call to you. Will you join our ceremony tonight?"))
            print("\n")
            action = input("(join/observe/sabotage/leave): ").strip().lower()
            
            if action == "join":
                type.type("You step into the circle. The warmth of the fire is immediate, almost alive. They give you herbs to hold.")
                print("\n")
                type.type("The chanting intensifies. What do you focus on?")
                focus = input("(wealth/love/power/peace): ").strip().lower()
                
                type.type("You throw your herbs into the flames. They burn green, then blue, then white.")
                print("\n")
                
                outcome = random.choice(["blessed", "cursed", "vision", "nothing"])
                
                if outcome == "blessed":
                    if focus == "wealth":
                        type.type("Gold light washes over you. You feel richer - and when you check your pockets, you ARE richer.")
                        self.change_balance(random.randint(8000, 20000))
                    elif focus == "love":
                        type.type("Pink light surrounds you. Someone across the fire catches your eye and smiles.")
                        self.add_status("Love Blessed")
                        self.add_item("Beach Romance Number")
                    elif focus == "power":
                        type.type("Red light pulses through you. You feel STRONG. Invincible.")
                        self.add_status("Fire Empowered")
                        self.heal(random.randint(30, 50))
                    else:
                        type.type("White light fills your mind. Every worry, every stress - gone.")
                        self.add_status("Enlightened")
                        self.heal(random.randint(20, 40))
                    print("\n")
                elif outcome == "cursed":
                    type.type("The flames turn black. The chanters go silent. Something went wrong.")
                    print("\n")
                    type.type("The woman with ocean eyes looks worried. " + quote("The spirits are displeased..."))
                    self.add_status("Fire Cursed")
                    self.hurt(random.randint(15, 30))
                elif outcome == "vision":
                    type.type("The world tilts. You see... things. The future? The past? Another reality?")
                    print("\n")
                    vision = random.choice(["treasure", "warning", "weird"])
                    if vision == "treasure":
                        type.type("You see a location - a place where something valuable is hidden. When you wake, you remember it clearly.")
                        self.add_item("Vision Map")
                    elif vision == "warning":
                        type.type("You see danger ahead. Something to avoid. You'll know it when you see it.")
                        self.add_status("Forewarned")
                    else:
                        type.type("You see a talking crab give a speech about tax law. You're not sure what it means but you feel changed.")
                        self.add_status("Confused but Wiser")
                else:
                    type.type("The ritual ends. You feel... the same? Maybe rituals aren't your thing.")
                    print("\n")
            
            elif action == "observe":
                type.type("You watch from outside the circle. The ritual is beautiful - fire, dance, and ancient words.")
                print("\n")
                type.type("When it ends, a robed figure approaches and hands you a small token.")
                print("\n")
                type.type(quote("For the respectful observer."))
                self.add_item("Ritual Token")
                print("\n")
            
            elif action == "sabotage":
                type.type("You wait for the right moment... then kick sand into the fire!")
                print("\n")
                if random.random() < 0.3:
                    type.type("CHAOS! The fire explodes with sparks. The chanters scatter. In the confusion, you grab some of their offerings.")
                    self.change_balance(random.randint(3000, 8000))
                else:
                    type.type("They're faster than they look. Several tackle you and drag you away.")
                    print("\n")
                    type.type(quote("You dare desecrate our fire?! YOU WILL PAY!"))
                    self.hurt(random.randint(25, 45))
                    self.add_status("Cultist Enemy")
                print("\n")
            
            else:
                type.type("You walk away, leaving the ritual to its mysteries. Some things are better left unknown.")
                print("\n")
        
        elif event == "message_in_bottle":
            type.type("Something glints in the moonlight - a bottle, half-buried in the sand, a rolled paper inside.")
            print("\n")
            type.type(yellow("=== THE MESSAGE IN A BOTTLE ==="))
            print("\n")
            action = input("(open/shake/throw_back/sell): ").strip().lower()
            
            if action == "open":
                type.type("You pop the cork and unroll the message. The paper is old, the ink faded...")
                print("\n")
                message = random.choice(["map", "love_letter", "warning", "code", "help"])
                
                if message == "map":
                    type.type("IT'S A TREASURE MAP! X marks a spot on this very beach!")
                    print("\n")
                    type.type("Do you follow it immediately?")
                    follow = ask.yes_or_no()
                    if follow == "yes":
                        type.type("You pace off the steps... 30 north... 15 east... you start digging.")
                        print("\n")
                        if random.random() < 0.6:
                            type.type("YOUR SHOVEL HITS SOMETHING! A chest! Inside: gold doubloons!")
                            self.change_balance(random.randint(10000, 30000))
                            self.add_item("Treasure Chest")
                        else:
                            type.type("You dig... and dig... and dig. Nothing. Either someone got here first, or it was a prank.")
                    else:
                        type.type("You save the map for later.")
                        self.add_item("Treasure Map")
                
                elif message == "love_letter":
                    type.type("It's a love letter, written decades ago. Passionate, desperate, beautiful.")
                    print("\n")
                    type.type("There's a name and address. Still legible.")
                    type.type("Do you try to find the recipient?")
                    find = ask.yes_or_no()
                    if find == "yes":
                        type.type("You track down the address - an elderly woman answers. She reads the letter with tears in her eyes.")
                        print("\n")
                        type.type(quote("He did love me... I thought he abandoned me. Thank you, stranger."))
                        print("\n")
                        type.type("She presses something into your hand - an antique ring.")
                        self.add_item("Antique Ring")
                        self.add_status("Good Karma")
                    else:
                        type.type("Some stories are better left unfinished.")
                
                elif message == "warning":
                    type.type("'BEWARE THE TWELFTH TIDE. THE SLEEPER WAKES. DO NOT BE ON THE BEACH WHEN THE MOON IS FULL.'")
                    print("\n")
                    type.type("You glance at the moon. It's... almost full. Almost.")
                    self.add_status("Paranoid")
                
                elif message == "code":
                    type.type("Numbers. Coordinates? A code? Gibberish?")
                    print("\n")
                    type.type("'13-15-14-5-25 2-21-18-9-5-4 21-14-4-5-18 16-9-5-18'")
                    type.type("Do you try to decode it?")
                    decode = ask.yes_or_no()
                    if decode == "yes":
                        type.type("You work it out... A=1, B=2... 'MONEY BURIED UNDER PIER'")
                        print("\n")
                        type.type("You rush to the pier and dig. There's a metal box!")
                        self.change_balance(random.randint(8000, 18000))
                    else:
                        type.type("You keep the code for later.")
                        self.add_item("Mysterious Code")
                
                else:
                    type.type("'HELP ME. STRANDED ON ISLAND. 1847.'")
                    print("\n")
                    type.type("...This message is over 150 years old. You hope they got rescued.")
                print("\n")
            
            elif action == "shake":
                type.type("You shake the bottle. Something rattles inside besides paper...")
                print("\n")
                type.type("You break the bottle open. A small key falls out!")
                self.add_item("Mysterious Key")
                type.type("The paper just says: 'For the vault.'")
                print("\n")
            
            elif action == "throw_back":
                type.type("You throw the bottle back into the sea. Let fate decide its next owner.")
                print("\n")
                if random.random() < 0.2:
                    type.type("A wave immediately throws it back at your feet. Okay, FINE.")
                    self.add_item("Persistent Bottle")
                print("\n")
            
            else:
                type.type("You find a collector on the beach who offers $500 for it, unopened.")
                self.change_balance(500)
                print("\n")
        
        elif event == "crab_racing":
            type.type("A crowd has gathered around a sandy track lit by tiki torches. They're racing CRABS. Big ones. Fast ones. Angry ones.")
            print("\n")
            type.type(yellow("=== CRAB RACING CHAMPIONSHIP ==="))
            print("\n")
            type.type("A sun-weathered man holds up a bucket. " + quote("$500 to race! Pick your crab! Winner takes the pot - $5,000!"))
            print("\n")
            action = input("(race/bet/catch_own/watch): ").strip().lower()
            
            if action == "race":
                if self.get_balance() >= 500:
                    self.change_balance(-500)
                    type.type("You reach into the bucket and pull out a crab. It's purple and VERY angry. The man nods approvingly.")
                    print("\n")
                    type.type(quote("That's Deathclaw. Good luck."))
                    print("\n")
                    type.type("The race starts! Crabs scatter in every direction except forward!")
                    print("\n")
                    type.type("How do you motivate Deathclaw?")
                    motivate = input("(yelling/food/poking/singing): ").strip().lower()
                    
                    if motivate == "food":
                        if self.has_item("Fish") or self.has_item("Live Fish"):
                            type.type("You dangle fish in front of Deathclaw. He ROCKETS forward!")
                            result = random.choice(["1st", "2nd", "1st", "1st"])
                        else:
                            type.type("You mime having food. Deathclaw is unimpressed.")
                            result = random.choice(["3rd", "4th", "2nd", "3rd"])
                    elif motivate == "singing":
                        type.type("You sing... a sea shanty? Deathclaw pauses. Then starts scuttling... rhythmically?")
                        result = random.choice(["1st", "2nd", "3rd", "2nd"])
                    elif motivate == "poking":
                        type.type("You poke Deathclaw. He turns and PINCHES you.")
                        self.hurt(random.randint(5, 10))
                        result = random.choice(["3rd", "4th", "4th", "3rd"])
                    else:
                        type.type("You scream at the crab. Several spectators look concerned for your sanity.")
                        result = random.choice(["2nd", "3rd", "4th", "2nd"])
                    
                    print("\n")
                    type.type(yellow("=== RACE RESULTS ==="))
                    
                    if result == "1st":
                        type.type("DEATHCLAW WINS! The crowd goes wild! You've never been prouder of a crustacean!")
                        self.change_balance(5000)
                        self.add_item("Crab Racing Trophy")
                    elif result == "2nd":
                        type.type("Second place. Deathclaw takes losing personally.")
                        self.change_balance(1500)
                    else:
                        type.type("Deathclaw gets distracted and wanders off. You lose.")
                    print("\n")
                else:
                    type.type("You can't afford the entry fee.")
                    print("\n")
            
            elif action == "bet":
                type.type("Which crab?")
                type.type("1. Pinchy Pete (2:1)")
                type.type("2. Lightning Larry (3:1)")
                type.type("3. Deathclaw (5:1)")
                type.type("4. Mr. Sideways (10:1)")
                pick = input("Pick (1-4): ").strip()
                
                type.type("How much do you bet?")
                try:
                    bet = int(input("Bet: $"))
                    if bet > 0 and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        winner = random.choice(["pete", "pete", "larry", "larry", "death", "sideways"])
                        
                        if pick == "1" and winner == "pete":
                            self.change_balance(bet * 2)
                            type.type("Pinchy Pete wins! " + green(bright("$" + str(bet * 2))) + "!")
                        elif pick == "2" and winner == "larry":
                            self.change_balance(bet * 3)
                            type.type("Lightning Larry lives up to his name! " + green(bright("$" + str(bet * 3))) + "!")
                        elif pick == "3" and winner == "death":
                            self.change_balance(bet * 5)
                            type.type("DEATHCLAW! " + green(bright("$" + str(bet * 5))) + "!")
                        elif pick == "4" and winner == "sideways":
                            self.change_balance(bet * 10)
                            type.type("MR. SIDEWAYS WINS! NOBODY SAW THAT COMING! " + green(bright("$" + str(bet * 10))) + "!")
                        else:
                            type.type("Your crab lost. Back to the ocean with your dreams.")
                    else:
                        type.type("You don't have that kind of money.")
                except:
                    type.type("Betting closed.")
                print("\n")
            
            elif action == "catch_own":
                type.type("You run to the water's edge and try to catch your own crab!")
                print("\n")
                if random.random() < 0.3:
                    type.type("You catch a MASSIVE crab! The regulars look intimidated!")
                    print("\n")
                    type.type("The man waives your entry fee. " + quote("Let's see what that monster can do."))
                    if random.random() < 0.5:
                        type.type("Your wild crab DOMINATES! You win the pot!")
                        self.change_balance(5000)
                    else:
                        type.type("Your crab immediately runs back into the ocean. Freedom > victory, apparently.")
                else:
                    type.type("You get pinched multiple times and catch nothing.")
                    self.hurt(random.randint(5, 15))
                print("\n")
            
            else:
                type.type("You watch the races. A crab named Mr. Sideways pulls off an upset. Good times.")
                print("\n")
        
        elif event == "sandcastle_contest":
            type.type("A sandcastle competition is underway! Elaborate fortresses dot the beach, each more impressive than the last.")
            print("\n")
            type.type(yellow("=== SANDCASTLE CHAMPIONSHIP ==="))
            print("\n")
            type.type("A judge approaches. " + quote("$200 entry. Grand prize is $8,000 and the Golden Shovel trophy!"))
            print("\n")
            action = input("(enter/judge/sabotage/watch): ").strip().lower()
            
            if action == "enter":
                if self.get_balance() >= 200:
                    self.change_balance(-200)
                    type.type("You're given a plot of sand and two hours. Go!")
                    print("\n")
                    type.type("What style do you build?")
                    style = input("(classic_castle/modern/weird/huge): ").strip().lower()
                    
                    score = random.randint(0, 3)
                    
                    if style == "classic_castle":
                        type.type("Towers, walls, a moat - you go traditional. The judges nod approvingly.")
                        score += 2
                    elif style == "modern":
                        type.type("You build a sand sculpture of... a car? A spaceship? It's avant-garde.")
                        if random.random() < 0.5:
                            type.type("The judges are impressed by your creativity!")
                            score += 3
                        else:
                            type.type("The judges are confused.")
                    elif style == "weird":
                        type.type("You build a giant sand crab. It's horrifying. People gather to stare.")
                        score += random.randint(1, 4)
                    else:
                        type.type("You go BIG. The biggest castle this beach has ever seen!")
                        if random.random() < 0.4:
                            type.type("It holds! It's MAGNIFICENT!")
                            score += 4
                        else:
                            type.type("It collapses halfway through. The crowd gasps.")
                            score = 0
                    
                    print("\n")
                    type.type(yellow("=== JUDGING ==="))
                    
                    if score >= 6:
                        type.type("FIRST PLACE! You win the Golden Shovel and " + green(bright("$8,000")) + "!")
                        self.change_balance(8000)
                        self.add_item("Golden Shovel")
                    elif score >= 4:
                        type.type("Second place! " + green(bright("$2,000")) + " and a Silver Bucket!")
                        self.change_balance(2000)
                    elif score >= 2:
                        type.type("Third place. You get a participation ribbon and your money back.")
                        self.change_balance(200)
                    else:
                        type.type("Disqualified for structural failure. Better luck next time.")
                    print("\n")
                else:
                    type.type("You can't afford the entry fee.")
                    print("\n")
            
            elif action == "judge":
                type.type("The head judge is sick! They ask you to fill in!")
                print("\n")
                type.type("You walk around judging castles. One builder slips you $500 to vote for them.")
                type.type("Do you take the bribe?")
                bribe = ask.yes_or_no()
                if bribe == "yes":
                    type.type("You pocket the cash and vote for their... mediocre castle. You feel slightly dirty.")
                    self.change_balance(500)
                    self.add_status("Corrupt Judge")
                else:
                    type.type("You judge fairly. A child wins with an adorable turtle sculpture. Heartwarming.")
                    self.add_status("Fair Judge")
                print("\n")
            
            elif action == "sabotage":
                type.type("You wait until no one's looking... then kick over the leading castle!")
                print("\n")
                if random.random() < 0.4:
                    type.type("Success! The builder screams. The crowd gasps. You slip away into the night.")
                    self.add_status("Sandcastle Villain")
                else:
                    type.type("A child sees you and screams " + quote("THAT PERSON KICKED THE CASTLE!"))
                    print("\n")
                    type.type("The crowd turns on you. You run. Someone throws a bucket. It hurts.")
                    self.hurt(random.randint(10, 20))
                print("\n")
            
            else:
                type.type("You watch the competition. Art takes many forms. Some of them are sand.")
                print("\n")
        
        else:
            type.type("Tonight, the beach is peaceful. You lie on the warm sand, watching shooting stars streak across the sky. The waves sing you to sleep.")
            self.heal(random.randint(20, 35))
            self.add_status("Beach Relaxed")
            print("\n")

    def underwater_adventure(self):
        self.meet("Underwater Adventure Event")
        type.type("You don your gear and slip beneath the waves. The world above fades to silence. Down here, in the blue abyss, ancient secrets wait to be discovered.")
        print("\n")
        type.type(yellow(bright("=== UNDERWATER ADVENTURE ===")))
        print("\n")
        event = random.choice([
            "hunting_competition", "sunken_shipwreck", "giant_octopus", "mermaid_kingdom", "treasure_dive"
        ])
        
        if event == "hunting_competition":
            type.type("You find a gathering of underwater hunters - professional spearfishers preparing for the DEEP SEA HUNT.")
            print("\n")
            type.type(yellow("=== THE DEEP SEA HUNTING CHAMPIONSHIP ==="))
            print("\n")
            type.type("A grizzled hunter with a harpoon gun approaches. " + quote("Entry's $5,000. First prize is $50,000 and the Golden Trident. You in?"))
            print("\n")
            action = input("(compete/bet/sabotage/watch): ").strip().lower()
            
            if action == "compete":
                if self.get_balance() >= 5000:
                    self.change_balance(-5000)
                    type.type("You're given a spear and assigned to Zone 3 - shark territory. The timer starts.")
                    print("\n")
                    
                    # Round 1: Target Selection
                    type.type(yellow("=== ROUND 1: THE HUNT ==="))
                    type.type("You descend into the darkness. Three potential targets:")
                    type.type("- A massive GROUPER hiding in coral (easy, small points)")
                    type.type("- A fast TUNA swimming past (medium, medium points)")
                    type.type("- A legendary MARLIN in the distance (hard, huge points)")
                    print("\n")
                    target = input("(grouper/tuna/marlin): ").strip().lower()
                    
                    hunt_score = random.randint(0, 2)
                    
                    if target == "grouper":
                        type.type("You approach the grouper slowly... it doesn't see you coming...")
                        if random.random() < 0.8:
                            type.type("PERFECT SHOT! The grouper is yours!")
                            hunt_score += 2
                        else:
                            type.type("It spots you at the last second and vanishes into the coral!")
                    elif target == "tuna":
                        type.type("You chase the tuna, matching its speed...")
                        if random.random() < 0.5:
                            type.type("You lead the shot perfectly! The tuna is caught!")
                            hunt_score += 4
                        else:
                            type.type("Too fast! Your spear misses by inches!")
                    else:
                        type.type("You go for glory - the marlin. It's HUGE.")
                        if random.random() < 0.25:
                            type.type("THE SHOT OF A LIFETIME! YOU HIT THE MARLIN!")
                            hunt_score += 8
                        else:
                            type.type("The marlin is too fast, too far. You miss completely.")
                    
                    print("\n")
                    
                    # Round 2: Danger
                    type.type(yellow("=== ROUND 2: DANGER ==="))
                    type.type("A SHARK appears! It smells blood in the water!")
                    print("\n")
                    type.type("How do you handle this?")
                    shark = input("(fight/hide/bait/flee): ").strip().lower()
                    
                    if shark == "fight":
                        type.type("You turn and face the shark, spear ready...")
                        if random.random() < 0.3:
                            type.type("You SPEAR THE SHARK! Bonus points AND you're alive!")
                            hunt_score += 5
                        else:
                            type.type("The shark is faster. It bites your leg before you drive it off.")
                            self.hurt(random.randint(25, 45))
                    elif shark == "hide":
                        type.type("You duck into a crevice. The shark circles... circles...")
                        if random.random() < 0.6:
                            type.type("It loses interest and swims away. Safe!")
                        else:
                            type.type("It finds you! You escape but lose your catch!")
                            hunt_score = max(0, hunt_score - 2)
                    elif shark == "bait":
                        if hunt_score > 0:
                            type.type("You sacrifice your catch! The shark takes the bait!")
                            hunt_score = 0
                            type.type("You're alive but starting over.")
                        else:
                            type.type("You have nothing to bait with! The shark CHARGES!")
                            self.hurt(random.randint(20, 35))
                    else:
                        type.type("You swim for the surface as fast as you can!")
                        if random.random() < 0.5:
                            type.type("You escape! But you lose valuable hunting time.")
                            hunt_score = max(0, hunt_score - 1)
                        else:
                            type.type("The shark catches you before you can escape!")
                            self.hurt(random.randint(30, 50))
                    
                    print("\n")
                    
                    # Round 3: Final Push
                    type.type(yellow("=== ROUND 3: FINAL HUNT ==="))
                    type.type("Time is running out! One last chance to catch something!")
                    final = input("(deep_dive/surface_hunt/ambush): ").strip().lower()
                    
                    if final == "deep_dive":
                        type.type("You dive DEEP, into the darkness where monsters lurk...")
                        if random.random() < 0.3:
                            type.type("You find a GIANT SEA BASS! It's massive! You spear it!")
                            hunt_score += 6
                        else:
                            type.type("Too dark. You catch nothing and barely make it back up.")
                    elif final == "surface_hunt":
                        type.type("You stay shallow where the fish are plentiful...")
                        type.type("You catch several smaller fish!")
                        hunt_score += random.randint(2, 4)
                    else:
                        type.type("You set up an ambush near a reef...")
                        if random.random() < 0.5:
                            type.type("A beautiful reef fish swims right into your trap!")
                            hunt_score += 4
                        else:
                            type.type("Nothing takes the bait. The reef is empty today.")
                    
                    print("\n")
                    type.type(yellow("=== RESULTS ==="))
                    
                    if hunt_score >= 15:
                        type.type("YOU WIN THE CHAMPIONSHIP! Your catches are LEGENDARY!")
                        print("\n")
                        type.type("The Golden Trident is yours, along with " + green(bright("$50,000")) + "!")
                        self.change_balance(50000)
                        self.add_item("Golden Trident")
                    elif hunt_score >= 10:
                        type.type("Second place! Impressive hunting!")
                        self.change_balance(random.randint(12000, 20000))
                    elif hunt_score >= 5:
                        type.type("Third place. Not bad for the deep sea.")
                        self.change_balance(random.randint(6000, 10000))
                    else:
                        type.type("You didn't place. The ocean bested you today.")
                    print("\n")
                else:
                    type.type("You can't afford the entry fee. Maybe next time.")
                    print("\n")
            
            elif action == "bet":
                type.type("Who do you bet on?")
                type.type("1. The Champion - Harpoon Harry (2:1)")
                type.type("2. The Newcomer - Sally Spear (4:1)")
                type.type("3. The Veteran - Old Man Sea (3:1)")
                type.type("4. The Wildcard - Crazy Ivan (8:1)")
                pick = input("Pick (1-4): ").strip()
                
                type.type("How much do you bet?")
                try:
                    bet = int(input("Bet: $"))
                    if bet > 0 and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        winner = random.choice(["harry", "harry", "sally", "sea", "sea", "ivan"])
                        
                        if pick == "1" and winner == "harry":
                            self.change_balance(bet * 2)
                            type.type("Harpoon Harry wins! " + green(bright("$" + str(bet * 2))) + "!")
                        elif pick == "2" and winner == "sally":
                            self.change_balance(bet * 4)
                            type.type("The newcomer shocks everyone! " + green(bright("$" + str(bet * 4))) + "!")
                        elif pick == "3" and winner == "sea":
                            self.change_balance(bet * 3)
                            type.type("Old Man Sea proves experience matters! " + green(bright("$" + str(bet * 3))) + "!")
                        elif pick == "4" and winner == "ivan":
                            self.change_balance(bet * 8)
                            type.type("CRAZY IVAN WINS! NOBODY SAW THAT COMING! " + green(bright("$" + str(bet * 8))) + "!")
                        else:
                            type.type("Your pick lost. Better luck next time.")
                    else:
                        type.type("You can't bet that much.")
                except:
                    type.type("Betting closed.")
                print("\n")
            
            elif action == "sabotage":
                type.type("You sneak around, looking for opportunities to cheat...")
                print("\n")
                type.type("You could cut someone's air hose, steal their catch, or release a shark near them.")
                sabotage = input("(airhose/steal/shark): ").strip().lower()
                
                if sabotage == "airhose":
                    if random.random() < 0.3:
                        type.type("You cut the champion's air hose! He has to surface early! Disqualified!")
                        type.type("The odds shift dramatically - you bet on the second favorite and WIN!")
                        self.change_balance(random.randint(8000, 15000))
                    else:
                        type.type("You're CAUGHT! The hunters don't take kindly to attempted murder!")
                        self.hurt(random.randint(40, 60))
                        self.add_status("Underwater Criminal")
                elif sabotage == "steal":
                    if random.random() < 0.5:
                        type.type("You grab a prize marlin from another hunter's line!")
                        self.add_item("Stolen Marlin")
                        self.change_balance(random.randint(5000, 10000))
                    else:
                        type.type("The hunter notices and attacks you with a spear!")
                        self.hurt(random.randint(25, 40))
                else:
                    type.type("You release chum to attract sharks near the other hunters...")
                    if random.random() < 0.4:
                        type.type("CHAOS! Sharks everywhere! The competition is called off!")
                        type.type("In the confusion, you grab abandoned catches.")
                        self.change_balance(random.randint(6000, 12000))
                    else:
                        type.type("The sharks find YOU first. Bad plan. Very bad plan.")
                        self.hurt(random.randint(35, 55))
                print("\n")
            
            else:
                type.type("You watch from a safe distance. Harpoon Harry wins again. The guy is legendary.")
                self.add_status("Oceanwise")
                print("\n")
        
        elif event == "sunken_shipwreck":
            type.type("Your light catches something massive on the ocean floor - the remains of an ancient ship, half-buried in sand.")
            print("\n")
            type.type(yellow("=== THE SUNKEN WRECK ==="))
            print("\n")
            type.type("The ship looks centuries old. Its cargo hold is partially exposed. Sharks circle lazily above.")
            print("\n")
            action = input("(explore/quick_loot/photograph/leave): ").strip().lower()
            
            if action == "explore":
                type.type("You descend carefully toward the wreck. The wood creaks even underwater.")
                print("\n")
                type.type("Where do you explore first?")
                area = input("(captains_quarters/cargo_hold/deck/hull): ").strip().lower()
                
                if area == "captains_quarters":
                    type.type("You squeeze through a broken window into the captain's quarters...")
                    print("\n")
                    type.type("A skeleton in a captain's uniform sits at a desk, a chest beside it.")
                    type.type("Do you open the chest?")
                    open_it = ask.yes_or_no()
                    if open_it == "yes":
                        if random.random() < 0.6:
                            type.type("GOLD COINS! The captain's personal fortune!")
                            self.change_balance(random.randint(15000, 35000))
                            self.add_item("Captain's Compass")
                        else:
                            type.type("A trap! The chest releases ink, blinding you! You barely escape!")
                            self.hurt(random.randint(15, 30))
                    else:
                        type.type("You leave the captain to his eternal rest.")
                
                elif area == "cargo_hold":
                    type.type("You swim into the cargo hold. Crates everywhere, most rotted away.")
                    print("\n")
                    if random.random() < 0.5:
                        type.type("You find crates of preserved spices - still valuable to collectors!")
                        self.change_balance(random.randint(8000, 15000))
                    else:
                        type.type("The floor gives way! You fall into a lower deck and get trapped!")
                        print("\n")
                        type.type("Your air is running low! How do you escape?")
                        escape = input("(break_hull/signal/calm): ").strip().lower()
                        if escape == "break_hull":
                            type.type("You smash through rotted wood and swim free!")
                            self.hurt(random.randint(10, 20))
                        elif escape == "signal":
                            if random.random() < 0.5:
                                type.type("Other divers see your signal! They pull you free!")
                            else:
                                type.type("No one sees. You have to break your way out anyway.")
                                self.hurt(random.randint(15, 25))
                        else:
                            type.type("You stay calm, conserve air, find a gap in the wood, and squeeze through.")
                
                elif area == "deck":
                    type.type("You explore the main deck. A cannon still points toward the enemy that sank this ship.")
                    print("\n")
                    type.type("You find cannonballs nearby - solid iron, valuable as antiques.")
                    self.change_balance(random.randint(5000, 10000))
                    if random.random() < 0.3:
                        type.type("Wait - there's something stuck in the cannon! A gem! Someone hid it there!")
                        self.add_item("Cannon Gem")
                
                else:
                    type.type("You explore the hull breach that sank this ship. Inside, you find skeletons of sailors.")
                    print("\n")
                    type.type("One still clutches a lockbox. Do you take it?")
                    take = ask.yes_or_no()
                    if take == "yes":
                        type.type("You pry it from skeletal fingers. The lock is rusted shut.")
                        self.add_item("Sailor's Lockbox")
                    else:
                        type.type("You leave the dead in peace.")
                print("\n")
            
            elif action == "quick_loot":
                type.type("You grab what you can see quickly - no time for deep exploration.")
                if random.random() < 0.7:
                    type.type("You snag some coins and a silver chalice before a shark notices you.")
                    self.change_balance(random.randint(5000, 12000))
                else:
                    type.type("A shark charges! You drop everything and swim for your life!")
                    self.hurt(random.randint(15, 30))
                print("\n")
            
            elif action == "photograph":
                type.type("You photograph the wreck instead of looting it. This could be an archaeological find!")
                print("\n")
                type.type("Do you sell the photos to a museum or a treasure hunter?")
                sell = input("(museum/hunter): ").strip().lower()
                if sell == "museum":
                    type.type("The museum pays you a finder's fee.")
                    self.change_balance(random.randint(8000, 15000))
                    self.add_status("Archaeological Hero")
                else:
                    type.type("The treasure hunter pays WELL for the location.")
                    self.change_balance(random.randint(15000, 25000))
                    self.add_status("Morally Flexible")
                print("\n")
            
            else:
                type.type("You leave the wreck undisturbed. Some things are better left buried.")
                print("\n")
        
        elif event == "giant_octopus":
            type.type("The water grows dark. Something MASSIVE moves in the depths. Eight tentacles, each thicker than your body, unfurl from the abyss.")
            print("\n")
            type.type(yellow("=== BOSS ENCOUNTER: THE KRAKEN ==="))
            print("\n")
            type.type("A giant octopus - ancient, intelligent, and HUNGRY. Its eye, the size of a dinner plate, focuses on YOU.")
            print("\n")
            action = input("(fight/communicate/flee/offer): ").strip().lower()
            
            if action == "fight":
                type.type(yellow("=== BATTLE: YOU VS. THE KRAKEN ==="))
                print("\n")
                type.type("You raise your spear. This is insane. This is suicide. This is... HAPPENING.")
                print("\n")
                type.type("The kraken attacks! A tentacle sweeps toward you!")
                attack1 = input("(dodge/cut/grab): ").strip().lower()
                
                kraken_damage = 0
                
                if attack1 == "dodge":
                    if random.random() < 0.6:
                        type.type("You twist away! The tentacle misses!")
                    else:
                        type.type("Too slow! It catches your leg!")
                        self.hurt(random.randint(20, 35))
                        kraken_damage -= 1
                elif attack1 == "cut":
                    if random.random() < 0.4:
                        type.type("Your blade bites deep! Ink clouds the water!")
                        kraken_damage += 2
                    else:
                        type.type("Your blade bounces off its rubbery skin!")
                else:
                    type.type("You GRAB the tentacle?! Bold move!")
                    if random.random() < 0.3:
                        type.type("You use its own momentum against it!")
                        kraken_damage += 1
                    else:
                        type.type("It wraps around you and SQUEEZES!")
                        self.hurt(random.randint(25, 40))
                
                print("\n")
                type.type("The kraken's beak snaps at you! Those jaws could crush a boat!")
                attack2 = input("(eyes/throat/retreat): ").strip().lower()
                
                if attack2 == "eyes":
                    if random.random() < 0.35:
                        type.type("You JAB at its eye! The kraken SCREAMS underwater! It releases you!")
                        kraken_damage += 3
                    else:
                        type.type("It blinks! Your attack deflects off its eyelid!")
                elif attack2 == "throat":
                    type.type("You dive for its beak, aiming for the soft throat...")
                    if random.random() < 0.25:
                        type.type("CRITICAL HIT! The kraken recoils in pain!")
                        kraken_damage += 4
                    else:
                        type.type("Its beak snaps shut, nearly taking your arm!")
                        self.hurt(random.randint(30, 45))
                else:
                    type.type("You create distance. The kraken pauses, considering you.")
                
                print("\n")
                
                if kraken_damage >= 5:
                    type.type("The kraken has had ENOUGH. It retreats into the depths, leaving behind... a PEARL.")
                    print("\n")
                    type.type("Not just any pearl - a KRAKEN PEARL. Priceless. Legendary.")
                    self.add_item("Kraken Pearl")
                    self.change_balance(random.randint(30000, 60000))
                elif kraken_damage >= 2:
                    type.type("The kraken considers you not worth the effort. It sinks away, leaving you alive.")
                else:
                    type.type("The kraken wraps you in tentacles and drags you deeper before you escape.")
                    self.hurt(random.randint(35, 55))
                print("\n")
            
            elif action == "communicate":
                type.type("You extend your arms in a non-threatening gesture. The kraken pauses.")
                print("\n")
                type.type("Its massive eye studies you. Intelligence sparkles within.")
                print("\n")
                if random.random() < 0.4:
                    type.type("It... understands? A tentacle gently touches your head. Images flood your mind.")
                    print("\n")
                    type.type("The location of treasure. Ancient secrets. The kraken shares its knowledge.")
                    self.add_item("Kraken's Memory")
                    self.add_status("Kraken Friend")
                    self.change_balance(random.randint(10000, 25000))
                else:
                    type.type("The kraken is not interested in communication. It simply... leaves.")
                    type.type("You're alive. That's more than most can say.")
                print("\n")
            
            elif action == "offer":
                type.type("You remember you have some fish. You offer them to the kraken.")
                print("\n")
                if self.has_item("Fish") or self.has_item("Live Fish") or self.has_item("Stolen Marlin"):
                    type.type("The kraken accepts your offering! It seems... grateful?")
                    print("\n")
                    type.type("It gently places something in your hands - a glowing stone from the deep.")
                    self.add_item("Deep Stone")
                    self.add_status("Kraken Respect")
                else:
                    type.type("You mime offering food. The kraken is unimpressed by your empty hands.")
                    type.type("It lets you go, but barely.")
                print("\n")
            
            else:
                type.type("You SWIM. Faster than you've ever swum. The kraken's tentacles reach for you...")
                print("\n")
                if random.random() < 0.5:
                    type.type("You reach your boat just in time! The tentacles slap the hull but you're SAFE!")
                else:
                    type.type("It catches your leg! You kick free but not without damage!")
                    self.hurt(random.randint(20, 40))
                print("\n")
        
        elif event == "mermaid_kingdom":
            type.type("You spot something impossible - lights in the deep. Buildings. A CITY beneath the waves.")
            print("\n")
            type.type(yellow("=== THE MERMAID KINGDOM ==="))
            print("\n")
            type.type("Mermaids swim through coral towers, going about their daily lives. One spots you and approaches.")
            print("\n")
            type.type("She's beautiful - iridescent scales, flowing hair, a voice like music even underwater.")
            print("\n")
            type.type(quote("A surface dweller! We haven't had a visitor in centuries! Will you join us for a feast?"))
            print("\n")
            action = input("(accept/decline/ask_questions/steal): ").strip().lower()
            
            if action == "accept":
                type.type("You follow the mermaid into the city. The architecture is breathtaking - made of coral and pearl.")
                print("\n")
                type.type("The feast is incredible - foods you've never seen, drinks that let you breathe underwater longer.")
                print("\n")
                type.type("After the feast, the Mermaid Queen approaches.")
                print("\n")
                type.type(quote("You've shown respect. Take this gift from our kingdom."))
                self.add_item("Mermaid Crown")
                self.change_balance(random.randint(15000, 30000))
                self.heal(random.randint(30, 50))
                print("\n")
            
            elif action == "ask_questions":
                type.type(quote("What is this place? How do you live down here?"))
                print("\n")
                type.type("The mermaid explains - they've lived here for millennia, hidden from the surface world.")
                print("\n")
                type.type(quote("We have treasures from every shipwreck. Knowledge from ages past. Would you like to see our library?"))
                library = ask.yes_or_no()
                if library == "yes":
                    type.type("The library holds ancient maps and secrets. One map shows treasure locations on land!")
                    self.add_item("Ancient Sea Map")
                    self.change_balance(random.randint(10000, 20000))
                else:
                    type.type("You decline politely. The mermaid looks disappointed but gives you a pearl for your respect.")
                    self.add_item("Mermaid Pearl")
                print("\n")
            
            elif action == "steal":
                type.type("You pretend interest while looking for valuables to grab...")
                print("\n")
                if random.random() < 0.3:
                    type.type("You snag a golden artifact and swim for the surface!")
                    self.change_balance(random.randint(12000, 22000))
                    self.add_status("Mermaid Enemy")
                else:
                    type.type("They catch you immediately. Mermaids are FAST.")
                    print("\n")
                    type.type("They don't kill you - they curse you instead.")
                    self.add_status("Sea Cursed")
                    self.hurt(random.randint(20, 35))
                print("\n")
            
            else:
                type.type("You politely decline and swim away. The mermaid looks sad but waves goodbye.")
                type.type("Some mysteries are better left unexplored.")
                print("\n")
        
        else:  # treasure_dive
            type.type("You found it - the coordinates from an old treasure map. X marks the spot, and you're directly above it.")
            print("\n")
            type.type(yellow("=== THE TREASURE DIVE ==="))
            print("\n")
            type.type("The dive will be deep - dangerous. But the treasure could be life-changing.")
            print("\n")
            action = input("(dive/hire_help/sell_map/abandon): ").strip().lower()
            
            if action == "dive":
                type.type("You take a deep breath and descend into the abyss...")
                print("\n")
                type.type("Deeper... darker... your flashlight barely cuts through the murk...")
                print("\n")
                type.type("There! A chest! But also... danger. A moray eel guards the spot.")
                eel = input("(fight_eel/distract/sneak): ").strip().lower()
                
                if eel == "fight_eel":
                    if random.random() < 0.5:
                        type.type("You spear the eel! The treasure is yours!")
                        self.change_balance(random.randint(25000, 50000))
                        self.add_item("Pirate Treasure")
                    else:
                        type.type("The eel bites you HARD. You grab some treasure and escape.")
                        self.hurt(random.randint(25, 40))
                        self.change_balance(random.randint(10000, 20000))
                elif eel == "distract":
                    type.type("You throw some bait away from the chest. The eel investigates...")
                    if random.random() < 0.7:
                        type.type("You grab the chest and SWIM! The treasure is yours!")
                        self.change_balance(random.randint(20000, 40000))
                    else:
                        type.type("The eel catches on and attacks! You escape with only a few coins.")
                        self.change_balance(random.randint(3000, 8000))
                        self.hurt(random.randint(15, 25))
                else:
                    type.type("You move slowly, silently, reaching for the chest...")
                    if random.random() < 0.4:
                        type.type("The eel never notices. You take the treasure and leave.")
                        self.change_balance(random.randint(25000, 45000))
                    else:
                        type.type("You bump the chest! The eel attacks!")
                        self.hurt(random.randint(20, 35))
                        self.change_balance(random.randint(5000, 12000))
                print("\n")
            
            elif action == "hire_help":
                type.type("You hire professional divers to help. Cost: $5,000.")
                if self.get_balance() >= 5000:
                    self.change_balance(-5000)
                    type.type("The team descends with you. Strength in numbers!")
                    print("\n")
                    type.type("They handle the eel, you grab the treasure. A clean operation.")
                    loot = random.randint(20000, 35000)
                    type.type("Total haul: " + green(bright("$" + str(loot))) + " after splitting with the crew.")
                    self.change_balance(loot)
                else:
                    type.type("You can't afford the help. You'll have to go alone or not at all.")
                print("\n")
            
            elif action == "sell_map":
                type.type("You sell the map's location to a collector.")
                self.change_balance(random.randint(8000, 15000))
                type.type("Easy money. No risk. But you'll always wonder what was really down there.")
                print("\n")
            
            else:
                type.type("Too dangerous. You keep the coordinates for another day.")
                self.add_item("Treasure Coordinates")
                print("\n")
        print("\n")

    def city_adventure(self):
        self.meet("City Adventure Event")
        type.type("The city at night is two worlds stacked on top of each other. Penthouses gleaming above, gutters rotting below. The rich don't look down. The poor can't look up.")
        print("\n")
        type.type(yellow(bright("=== CITY AFTER DARK ===")))
        print("\n")
        event = random.choice([
            "underground_den", "overdose_witness", "loan_shark", "homeless_camp",
            "crack_alley", "penthouse_party", "desperate_gambler", "bank_heist", "casual_night"
        ])
        
        if event == "underground_den":
            type.type("Down a stairwell that smells like piss and broken dreams, you find it. An underground gambling den. No windows. No exits except the one you came in.")
            print("\n")
            type.type("The air is thick with cigarette smoke and desperation. Men hunched over tables, eyes hollow, feeding bills into games they can't win.")
            print("\n")
            type.type("A woman in the corner is crying. Nobody looks at her. A man next to her bets his wedding ring.")
            print("\n")
            type.type(yellow("=== THE UNDERGROUND DEN ==="))
            print("\n")
            type.type("A bouncer with no neck approaches. " + quote("You play or you leave. House takes forty percent."))
            print("\n")
            action = input("(play/watch/help_woman/leave): ").strip().lower()
            
            if action == "play":
                type.type("You sit at a table. The game is rigged - you can tell immediately. The dealer's hands move too fast, the cards feel wrong.")
                print("\n")
                type.type("But you play anyway. Because that's what you do. That's what you are.")
                print("\n")
                type.type("How much do you put in?")
                try:
                    bet = int(input("Bet: $"))
                    if bet > 0 and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        if random.random() < 0.25:  # House is rigged
                            winnings = int(bet * 1.5)
                            type.type("You win. " + green(bright("$" + str(winnings))) + ". The bouncer watches you closer now.")
                            self.change_balance(winnings)
                        else:
                            type.type("You lose. Of course you lose. The house always wins in places like this.")
                            type.type("The crying woman looks at you. Recognition in her eyes. She's been you. You're becoming her.")
                    else:
                        type.type("You don't have enough. The bouncer's hand is on your shoulder before you can explain.")
                        self.hurt(random.randint(10, 20))
                except:
                    type.type("The bouncer doesn't like hesitation. You're escorted out. Roughly.")
                    self.hurt(random.randint(5, 15))
                print("\n")
            
            elif action == "help_woman":
                type.type("You approach the crying woman. Up close, you can see track marks on her arms. She's young - too young for eyes that dead.")
                print("\n")
                type.type(quote("Please,") + " she whispers. " + quote("I just need enough to get home. He took everything. My phone, my shoes, everything."))
                print("\n")
                give = ask.yes_or_no("Give her money?")
                if give == "yes":
                    type.type("You press $200 into her hand. She doesn't say thank you. Just stares at the money like she's forgotten what it's for.")
                    self.change_balance(-200)
                    print("\n")
                    type.type("Then she walks to the table and bets it all.")
                    print("\n")
                    type.type("She loses.")
                    print("\n")
                    type.type("The crying starts again. You leave before you can watch anymore.")
                else:
                    type.type("You can't save everyone. You can barely save yourself.")
                    type.type("Her sobs follow you up the stairs and into the night.")
                print("\n")
            
            elif action == "watch":
                type.type("You stand in the corner and watch. This is what addiction looks like when the pretty wrapping comes off.")
                print("\n")
                type.type("A man wins $500 and immediately bets $600. A woman loses her third straight hand and asks for a 'loan' from a man in a pinstripe suit.")
                print("\n")
                type.type("You see the loan shark's eyes light up. Fresh meat.")
                print("\n")
                type.type("Nobody leaves this place richer. Not really. The money just moves around until the house takes it all.")
                print("\n")
                type.type("You learn something about yourself watching them. Something you didn't want to know.")
                self.add_status("Self-Aware")
                print("\n")
            
            else:
                type.type("You turn and leave. The bouncer calls after you: " + quote("You'll be back. They always come back."))
                print("\n")
                type.type("You tell yourself he's wrong.")
                print("\n")
                type.type("You're not sure you believe it.")
                print("\n")
        
        elif event == "overdose_witness":
            type.type("An alley. A body. At first you think they're dead.")
            print("\n")
            type.type("Then you see the chest move. Barely.")
            print("\n")
            type.type("A young man, maybe nineteen, foam at the corners of his mouth. A needle still in his arm. His lips are blue. His eyes are rolled back.")
            print("\n")
            type.type(yellow("=== THE OVERDOSE ==="))
            print("\n")
            type.type("You could call 911. You could try to help. You could walk away like everyone else.")
            print("\n")
            action = input("(call_911/help/narcan/leave): ").strip().lower()
            
            if action == "call_911":
                type.type("You dial. Your hands are shaking. The operator asks questions you don't know the answers to.")
                print("\n")
                type.type("Paramedics arrive. They push you aside, professional and tired. They've done this before. They'll do it again.")
                print("\n")
                if random.random() < 0.7:
                    type.type("He lives. Barely. They load him into the ambulance. One paramedic looks at you.")
                    print("\n")
                    type.type(quote("Most people just walk by. Thanks for not being most people."))
                    self.add_status("Decent Human")
                else:
                    type.type("They try. They really try. But he's been down too long.")
                    print("\n")
                    type.type("The paramedic shakes her head. " + quote("We'll take it from here."))
                    print("\n")
                    type.type("You walk away with death on your hands. Or maybe you just walk away.")
                print("\n")
            
            elif action == "help":
                type.type("You kneel beside him. You don't know what you're doing but you try - chest compressions, mouth to mouth, something you half-remember from a movie.")
                print("\n")
                type.type("His skin is cold. His heart is barely beating.")
                print("\n")
                if random.random() < 0.4:
                    type.type("He gasps. Coughs. Eyes flutter open. He looks at you like you're a stranger - because you are.")
                    print("\n")
                    type.type(quote("Don't call anyone,") + " he whispers. " + quote("Please. They'll lock me up again."))
                    print("\n")
                    type.type("You help him to his feet. He limps away into the darkness. You'll never know if he made it.")
                else:
                    type.type("Nothing works. You try until someone pulls you away - a woman in scrubs, running home from her night shift.")
                    print("\n")
                    type.type(quote("It's too late, honey. It was probably too late before you got here."))
                    print("\n")
                    type.type("You sit on the curb for a long time after they take the body away.")
                    self.hurt(random.randint(5, 10))  # Emotional damage
                print("\n")
            
            elif action == "narcan":
                if self.has_met("Dealer Narcan"):
                    type.type("You have Narcan. Why do you have Narcan? You don't ask yourself that question.")
                    print("\n")
                    type.type("You administer it. His eyes snap open. He gasps, panics, swings at you.")
                    print("\n")
                    type.type(quote("What the fuck? What the FUCK?"))
                    print("\n")
                    type.type("He doesn't thank you. He's angry. You just killed his high.")
                    print("\n")
                    type.type("He stumbles away. You'll see him again, in another alley, with another needle. Or you won't.")
                else:
                    type.type("You don't have Narcan. But you know where to get it - the woman at the convenience store keeps it behind the counter.")
                    print("\n")
                    type.type("By the time you get back, the alley is empty. Someone else found him. Or didn't.")
                print("\n")
            
            else:
                type.type("You keep walking. Like everyone else. Like you've always done.")
                print("\n")
                type.type("Someone else's problem. Someone else's son.")
                print("\n")
                type.type("The city swallows him. The city swallows everything.")
                print("\n")
        
        elif event == "loan_shark":
            type.type("He finds you. They always find you. A man in a nice suit with a smile that doesn't reach his eyes.")
            print("\n")
            type.type(quote("You look like someone who could use a little... liquidity."))
            print("\n")
            type.type(yellow("=== THE LOAN SHARK ==="))
            print("\n")
            type.type(quote("I'm Mr. Vincent. I help people like you. People who need money right now, no questions asked."))
            print("\n")
            type.type("His terms: any amount up to $50,000. Twenty percent interest. Per week.")
            print("\n")
            action = input("(borrow/refuse/threaten/ask_about_him): ").strip().lower()
            
            if action == "borrow":
                type.type("How much do you need?")
                try:
                    amount = int(input("Amount: $"))
                    if amount > 0 and amount <= 50000:
                        self.change_balance(amount)
                        type.type("He counts the money out. Slow. Deliberate. Making sure you see every bill.")
                        print("\n")
                        type.type(quote("You've got one week. After that, I add twenty percent. After two weeks, I send my associates."))
                        print("\n")
                        type.type("He hands you a card with just a phone number.")
                        print("\n")
                        type.type(quote("Don't make me come find you."))
                        self.add_status("Loan Shark Debt")
                        # Store the debt amount somewhere
                    else:
                        type.type(quote("Cute. Come back when you're serious."))
                except:
                    type.type(quote("Not in the mood for games. Find me when you grow up."))
                print("\n")
            
            elif action == "threaten":
                type.type(quote("I know people who eat loan sharks for breakfast."))
                print("\n")
                type.type("Vincent laughs. It's not a nice laugh.")
                print("\n")
                type.type(quote("Kid, I AM the people who eat people for breakfast."))
                print("\n")
                type.type("Two men materialize from the shadows. You didn't see them before. That's concerning.")
                print("\n")
                type.type(quote("Consider this a free lesson in manners."))
                self.hurt(random.randint(20, 40))
                self.change_balance(-random.randint(1000, 5000))
                print("\n")
            
            elif action == "ask_about_him":
                type.type(quote("What's your story, Vincent?"))
                print("\n")
                type.type("He seems surprised by the question. Nobody asks him questions.")
                print("\n")
                type.type(quote("I grew up in places like this.") + " He gestures at the street. " + quote("Watched my father gamble away everything. My mother worked three jobs until it killed her. I swore I'd never be poor again."))
                print("\n")
                type.type("He adjusts his cufflinks. Gold. Expensive.")
                print("\n")
                type.type(quote("Now I help people make the same mistakes my father made. Circle of life."))
                print("\n")
                type.type("He walks away without offering you money. You might have seen something human in him. Or maybe you imagined it.")
                print("\n")
            
            else:
                type.type(quote("I'm good."))
                print("\n")
                type.type(quote("Nobody's ever good,") + " he says. " + quote("But suit yourself. I'll be around when you change your mind."))
                print("\n")
        
        elif event == "homeless_camp":
            type.type("Under the overpass, a city within the city. Tents made of tarps. Shopping carts full of everything someone owns. A fire in a barrel.")
            print("\n")
            type.type("These are the people the penthouses don't see. The ones the city pretends don't exist.")
            print("\n")
            type.type(yellow("=== THE ENCAMPMENT ==="))
            print("\n")
            type.type("An old man waves you over. His beard is gray and matted. His eyes are surprisingly clear.")
            print("\n")
            type.type(quote("You lost?") + " he asks. " + quote("Or you one of us now?"))
            print("\n")
            action = input("(sit/give_money/share_food/ask_advice/leave): ").strip().lower()
            
            if action == "sit":
                type.type("You sit by the fire. Nobody asks questions. Nobody judges. For a while, you're just another body trying to stay warm.")
                print("\n")
                type.type("The old man tells stories. He used to be a banker. Lost it all to gambling - then the drinking started, then the divorce, then the street.")
                print("\n")
                type.type(quote("Funny thing is, I'm happier now than I ever was in that corner office. Got nothing left to lose."))
                print("\n")
                type.type("You don't know if that's wisdom or delusion. Maybe there's no difference.")
                self.heal(random.randint(10, 20))
                self.add_status("Humbled")
                print("\n")
            
            elif action == "give_money":
                amount = random.randint(100, 500)
                type.type("You hand over " + str(amount) + " dollars. The old man looks at it, then at you.")
                self.change_balance(-amount)
                print("\n")
                type.type(quote("You sure? Money like this won't fix nothing for us. It'll be gone by morning - booze, food, gone."))
                print("\n")
                type.type("He takes it anyway. Passes it around the camp. For one night, they eat well.")
                print("\n")
                type.type(quote("Thanks, stranger. Hope you find what you're looking for."))
                print("\n")
            
            elif action == "share_food":
                if self.has_item("Food"):
                    type.type("You share what you have. It's not much, but their gratitude is real.")
                    self.use_item("Food")
                else:
                    type.type("You don't have any food. But you sit with them while they eat what they have.")
                print("\n")
                type.type("A woman shows you a picture - a daughter somewhere, a life that used to be.")
                print("\n")
                type.type(quote("We're not that different, you and me. Just a few bad breaks apart."))
                print("\n")
            
            elif action == "ask_advice":
                type.type(quote("You look like you know things. What's the secret to surviving out here?"))
                print("\n")
                type.type("The old man laughs.")
                print("\n")
                type.type(quote("Secret? There ain't no secret. You just don't die. And some days that's harder than others."))
                print("\n")
                type.type("He points at your clothes, your shoes, the way you carry yourself.")
                print("\n")
                type.type(quote("You got a gambling problem. I can smell it on you. Here's my advice: stop. Just stop. Before you end up here."))
                print("\n")
                type.type(quote("But you won't. Nobody ever does. We just keep playing until we lose everything."))
                self.add_status("Warned")
                print("\n")
            
            else:
                type.type("You leave. The firelight fades behind you. Tomorrow, you'll forget they exist.")
                print("\n")
                type.type("That's how the city works. Out of sight, out of mind.")
                print("\n")
        
        elif event == "crack_alley":
            type.type("You took a wrong turn. Or maybe the right one, depending on what you're looking for.")
            print("\n")
            type.type("The alley is alive with shadows and whispers. The smell of burnt chemicals. Eyes watching from doorways.")
            print("\n")
            type.type(yellow("=== CRACK ALLEY ==="))
            print("\n")
            type.type("A man approaches. His teeth are rotted. His hands shake. But his eyes are calculating.")
            print("\n")
            type.type(quote("You buying, selling, or lost?"))
            print("\n")
            action = input("(lost/curious/buy/run): ").strip().lower()
            
            if action == "lost":
                type.type(quote("Just lost. Wrong turn."))
                print("\n")
                type.type("He stares at you. Decides you're telling the truth.")
                print("\n")
                type.type(quote("Straight down, two rights, you're back on the main road. Don't come back here unless you mean to."))
                print("\n")
                type.type("You follow his directions. You feel his eyes on your back the whole way.")
                print("\n")
            
            elif action == "curious":
                type.type(quote("What goes on here?"))
                print("\n")
                type.type("He laughs. It turns into a cough.")
                print("\n")
                type.type(quote("What DOESN'T go on here? This is where the city sends everything it doesn't want to see. Us. The junkies, the dealers, the runaways. We got our own economy down here."))
                print("\n")
                type.type("He gestures at the alley - the huddled forms, the quick transactions, the desperate faces.")
                print("\n")
                type.type(quote("You want something? Pills, powder, rock, whatever? Or maybe something else?") + " His eyes narrow. " + quote("Information?"))
                print("\n")
                if random.random() < 0.5:
                    type.type("He tells you about a high-stakes game three blocks over. Entry: $5,000. Pot: Whatever you can win.")
                    self.add_status("Underground Intel")
                else:
                    type.type("He tells you about a man who's been asking around about gamblers. A man with a glass eye.")
                    type.type("You don't know what to make of that.")
                print("\n")
            
            elif action == "buy":
                type.type("You don't know why you said that. Maybe you do.")
                print("\n")
                type.type("He names a price. You pay it before you can think.")
                self.change_balance(-random.randint(100, 500))
                print("\n")
                type.type("The high is immediate. Overwhelming. Everything feels possible.")
                print("\n")
                type.type("Then it fades. And you feel worse than before. Emptier.")
                self.add_status("Shame")
                self.heal(random.randint(5, 15))  # Temporary
                self.hurt(random.randint(10, 20))  # Comedown
                print("\n")
            
            else:
                type.type("You run. Someone shouts behind you but you don't look back.")
                print("\n")
                type.type("You run until your lungs burn. Until the alley is far behind you.")
                print("\n")
                type.type("You tell yourself you'll never go back there.")
                print("\n")
                type.type("You're probably lying.")
                print("\n")
        
        elif event == "penthouse_party":
            type.type("The elevator goes up. And up. And up. You're not sure how you got the invitation, but here you are.")
            print("\n")
            type.type("The penthouse is everything the street below isn't. Crystal chandeliers. Champagne that costs more than your car. People who've never worried about money in their lives.")
            print("\n")
            type.type(yellow("=== THE PENTHOUSE ==="))
            print("\n")
            type.type("They look at you like you're entertainment. The gambling addict from the casino. The man who lives in his car. A curiosity.")
            print("\n")
            type.type("A woman in diamonds approaches. " + quote("You're the one who won big at Mortimer's place, aren't you? I've heard SO much about you."))
            print("\n")
            action = input("(play_along/be_honest/steal/leave): ").strip().lower()
            
            if action == "play_along":
                type.type("You play the part. The high roller. The winner. The man who's got it figured out.")
                print("\n")
                type.type("They eat it up. Pour you drinks. Introduce you to people with last names that appear on buildings.")
                print("\n")
                type.type("For one night, you're one of them. Or at least they let you pretend.")
                print("\n")
                if random.random() < 0.5:
                    type.type("A man slips you a card. " + quote("Private game. Tomorrow night. Big stakes. You interested?"))
                    self.add_status("VIP Connection")
                    self.change_balance(random.randint(1000, 5000))  # Someone "tips" you
                else:
                    type.type("By midnight, they've moved on to the next curiosity. You're escorted out gently but firmly.")
                print("\n")
            
            elif action == "be_honest":
                type.type(quote("I'm nobody. I live in my car and gamble because I can't stop."))
                print("\n")
                type.type("Silence. Then laughter. They think you're joking.")
                print("\n")
                type.type("When they realize you're not, the laughter dies. The diamond woman's smile freezes.")
                print("\n")
                type.type(quote("Security? Please escort our... guest... out."))
                print("\n")
                type.type("On the elevator down, you see the city lights. All those penthouses, all those people who'll never understand.")
                print("\n")
                type.type("Maybe that's for the best.")
                print("\n")
            
            elif action == "steal":
                type.type("So much money. So much excess. They wouldn't even notice if something went missing.")
                print("\n")
                type.type("You pocket what you can. A gold lighter. Cash from a purse. A watch from the bathroom counter.")
                print("\n")
                if random.random() < 0.4:
                    self.change_balance(random.randint(5000, 15000))
                    type.type("You slip out before anyone notices. Tomorrow, someone will wonder where their Rolex went.")
                    type.type("They'll buy another one without thinking twice.")
                else:
                    type.type("A hand on your shoulder. Security. " + quote("Empty your pockets. Now."))
                    print("\n")
                    type.type("They take back what you stole and throw you onto the street. Literally.")
                    self.hurt(random.randint(15, 25))
                    self.add_status("Blacklisted")
                print("\n")
            
            else:
                type.type("You don't belong here. You never did.")
                print("\n")
                type.type("The elevator down is quiet. Through the glass walls, you watch the city get smaller, then bigger.")
                print("\n")
                type.type("Back on the street, you breathe easier. This is where you belong. For better or worse.")
                print("\n")
        
        elif event == "desperate_gambler":
            type.type("You recognize him. Or maybe you recognize yourself in him.")
            print("\n")
            type.type("A man, your age, standing outside an ATM. His card has been declined. He's holding a picture - family, kids, a life that used to be.")
            print("\n")
            type.type(yellow("=== THE DESPERATE GAMBLER ==="))
            print("\n")
            type.type(quote("I just need one more game,") + " he says to no one. " + quote("One more hand. I can win it all back."))
            print("\n")
            type.type("He looks at you. Eyes desperate. " + quote("You got any cash? I swear I'll pay you back. I've got a system."))
            print("\n")
            action = input("(give_money/give_advice/take_picture/ignore): ").strip().lower()
            
            if action == "give_money":
                type.type("How much?")
                try:
                    amount = int(input("Amount: $"))
                    if amount > 0 and self.get_balance() >= amount:
                        self.change_balance(-amount)
                        type.type("He takes the money with shaking hands. " + quote("Thank you. Thank you. I'll pay you back, I swear."))
                        print("\n")
                        type.type("He walks toward the casino district. You know you'll never see that money again.")
                        print("\n")
                        type.type("You know, because you've been him. You are him.")
                    else:
                        type.type("You can't spare it. He nods, understanding. Fellow gamblers know the truth.")
                except:
                    type.type("You hesitate. He walks away. " + quote("Never mind. Forget it."))
                print("\n")
            
            elif action == "give_advice":
                type.type(quote("There is no system. There's no winning it back. I've been where you are."))
                print("\n")
                type.type("He laughs bitterly.")
                print("\n")
                type.type(quote("You think I don't know that? You think I don't know I'm destroying my life?"))
                print("\n")
                type.type("He holds up the picture. " + quote("My wife left. My kids won't talk to me. I've lost everything. All I have left is the hope that one more game will fix it."))
                print("\n")
                type.type(quote("Without that hope, I've got nothing."))
                print("\n")
                type.type("You don't have a response to that. Neither does he.")
                self.add_status("Haunted")
                self.lose_sanity(random.choice([1, 2, 3]))  # Seeing yourself in a broken man
                print("\n")
            
            elif action == "take_picture":
                type.type(quote("Can I see that?"))
                print("\n")
                type.type("He hands it over. A woman. Two kids. A backyard. Normalcy.")
                print("\n")
                type.type(quote("They're beautiful,") + " you say. " + quote("Is that why you gamble? To give them better?"))
                print("\n")
                type.type(quote("I told myself that at first. Now I gamble because I don't know how to stop."))
                print("\n")
                type.type("You hand the picture back. " + quote("Call them. Tonight. Before you play again."))
                print("\n")
                type.type("He looks at the picture for a long time. Then at you.")
                print("\n")
                type.type(quote("Maybe. Maybe I will."))
                print("\n")
                type.type("You both know he won't. But the lie feels nice.")
                print("\n")
            
            else:
                type.type("You walk past him. Like everyone else.")
                print("\n")
                type.type("His eyes follow you. Understanding. No judgment. Just recognition.")
                print("\n")
                type.type("One gambler recognizing another. Both of you pretending you're different.")
                print("\n")
        
        elif event == "bank_heist":
            type.type("You're walking past First National when you see them. Three figures in dark clothes, cutting through a side door. Professional. Silent.")
            print("\n")
            type.type("One of them spots you. For a moment, time freezes. Then she walks toward you - calm, deliberate. A woman with cold eyes and a colder smile.")
            print("\n")
            type.type(yellow("=== THE BANK HEIST ==="))
            print("\n")
            type.type(quote("Wrong place, wrong time, friend. But maybe right place, right time for you."))
            print("\n")
            type.type("She explains quickly: they're hitting the vault. Insider job. Security's paid off. They need a lookout - someone who doesn't look like a criminal.")
            print("\n")
            type.type(quote("You stand on the corner, smoke a cigarette, text us if cops show up. Easy money. Or...") + " She lets the alternative hang in the air.")
            print("\n")
            type.type("You could join them inside. You could call the cops. You could try to blackmail your way into a bigger cut. Or you could just watch from the shadows and see what falls off the truck.")
            print("\n")
            action = input("(join/report/blackmail/fight/watch): ").strip().lower()
            
            if action == "join":
                type.type("You're handed a mask and a bag. " + quote("Don't be stupid, don't be a hero. Just grab and go."))
                print("\n")
                type.type(yellow("=== THE HEIST ==="))
                type.type("You're inside the vault! Gold everywhere! How much do you take?")
                grab = input("(reasonable/greedy/pocket_stuff): ").strip().lower()
                
                if grab == "greedy":
                    type.type("You load up HEAVY. Your bag weighs a ton.")
                    if random.random() < 0.4:
                        type.type("You escape with the crew! Your cut is MASSIVE!")
                        self.change_balance(random.randint(40000, 80000))
                        self.add_status("Wanted Felon")
                    else:
                        type.type("Too slow! The cops arrive! You drop half the gold escaping!")
                        self.change_balance(random.randint(15000, 30000))
                        self.add_status("Wanted")
                elif grab == "pocket_stuff":
                    type.type("You pretend to fill your bag while pocketing small but VALUABLE gems.")
                    self.change_balance(random.randint(8000, 18000))
                    type.type("The crew doesn't notice. Smart. Safe.")
                else:
                    type.type("You take a reasonable amount and escape with the crew.")
                    self.change_balance(random.randint(20000, 40000))
                    self.add_status("Wanted")
                print("\n")
            
            elif action == "report":
                type.type("You back away slowly and call 911. The cops arrive in FORCE.")
                print("\n")
                if random.random() < 0.6:
                    type.type("The crew is caught! The city rewards you handsomely!")
                    self.change_balance(random.randint(10000, 25000))
                    self.add_item("Key to the City")
                else:
                    type.type("One robber escapes and sees your face. You're a target now.")
                    self.add_status("Marked")
                print("\n")
            
            elif action == "blackmail":
                type.type(quote("How about you cut me in, or I make a very loud phone call?"))
                print("\n")
                if random.random() < 0.5:
                    type.type("The masked figure considers, then tosses you a bag of gold.")
                    type.type(quote("Smart. But remember - we know your face too now."))
                    self.change_balance(random.randint(15000, 30000))
                    self.add_status("Criminal Contacts")
                else:
                    type.type("The masked figure pulls a gun. " + quote("Bad choice."))
                    self.hurt(random.randint(30, 50))
                print("\n")
            
            elif action == "fight":
                type.type("You attack the robber before they can react!")
                print("\n")
                if random.random() < 0.3:
                    type.type("You knock them out! The others flee! You're a HERO!")
                    self.change_balance(random.randint(15000, 30000))
                    self.add_item("Hero Medal")
                else:
                    type.type("The robber's friends don't appreciate that. They beat you severely.")
                    self.hurt(random.randint(40, 65))
                print("\n")
            
            else:
                type.type("You watch from the shadows as the heist unfolds.")
                print("\n")
                if random.random() < 0.3:
                    type.type("A bag falls off the van as they speed away. You grab it.")
                    self.change_balance(random.randint(5000, 15000))
                else:
                    type.type("The heist goes smoothly. You've witnessed history.")
                    self.add_status("Witness")
                print("\n")
        
        elif event == "free_ice_cream":
            type.type("A brightly colored truck plays cheerful music. 'FREE ICE CREAM!' the sign says. Too good to be true?")
            print("\n")
            type.type(yellow("=== THE ICE CREAM TRUCK ==="))
            print("\n")
            action = input("(get_ice_cream/suspicious/follow_truck/ignore): ").strip().lower()
            
            if action == "get_ice_cream":
                type.type("You approach the window. A jolly man hands you a cone.")
                print("\n")
                type.type(quote("Chocolate, vanilla, or mystery flavor?"))
                flavor = input("(chocolate/vanilla/mystery): ").strip().lower()
                
                if flavor == "mystery":
                    type.type("The mystery flavor is... actually incredible? Like nothing you've ever tasted.")
                    self.heal(random.randint(30, 50))
                    self.add_status("Mysteriously Refreshed")
                elif flavor == "chocolate":
                    type.type("Rich, creamy chocolate. You feel restored.")
                    self.heal(random.randint(20, 35))
                else:
                    type.type("Classic vanilla. Can't go wrong.")
                    self.heal(random.randint(15, 25))
                
                if random.random() < 0.2:
                    type.type("The ice cream man winks and slips you a $20 bill.")
                    type.type(quote("You look like you needed that."))
                    self.change_balance(20)
                print("\n")
            
            elif action == "suspicious":
                type.type("You investigate the truck. Something's off...")
                print("\n")
                if random.random() < 0.3:
                    type.type("It's a FRONT! The truck is actually selling weapons out the back!")
                    type.type("Do you report it or buy something?")
                    choice = input("(report/buy): ").strip().lower()
                    if choice == "buy":
                        type.type("You buy a suspicious item. Might come in handy.")
                        self.change_balance(-500)
                        self.add_item("Suspicious Package")
                    else:
                        type.type("You report it. The cops arrive and you get a reward.")
                        self.change_balance(random.randint(2000, 5000))
                else:
                    type.type("It's just... free ice cream. A local business doing charity. You feel paranoid.")
                    self.add_status("Paranoid")
                print("\n")
            
            elif action == "follow_truck":
                type.type("You follow the truck... it drives to a MANSION and parks.")
                print("\n")
                type.type("A wealthy-looking person gets out and goes inside. This is their PERSONAL ice cream truck.")
                if random.random() < 0.4:
                    type.type("They notice you following and invite you in for ice cream. You make a rich friend.")
                    self.add_item("Rich Friend's Number")
                    self.change_balance(random.randint(1000, 5000))
                else:
                    type.type("Security spots you. They're not happy.")
                    self.add_status("Trespasser")
                print("\n")
            
            else:
                type.type("Nothing is free in this city. You walk past.")
                type.type("A child happily eating ice cream waves at you. You feel a twinge of regret.")
                print("\n")
        
        elif event == "fighting_ring":
            type.type("Down a grimy stairwell, you hear the roar of a crowd. An underground FIGHTING RING.")
            print("\n")
            type.type(yellow("=== THE UNDERGROUND FIGHT CLUB ==="))
            print("\n")
            type.type("A bouncer blocks the door. " + quote("$500 entry. Or $2,000 to fight. Prize pot is $20,000."))
            print("\n")
            action = input("(fight/bet/watch/organize): ").strip().lower()
            
            if action == "fight":
                if self.get_balance() >= 2000:
                    self.change_balance(-2000)
                    type.type("You step into the ring. Your opponent is HUGE.")
                    print("\n")
                    type.type(yellow("=== ROUND 1 ==="))
                    type.type("He swings at your head! What do you do?")
                    r1 = input("(duck/block/counter): ").strip().lower()
                    
                    fight_score = random.randint(0, 2)
                    
                    if r1 == "duck":
                        if random.random() < 0.6:
                            type.type("You duck under and land a body shot!")
                            fight_score += 2
                        else:
                            type.type("You duck into his knee. Stars explode in your vision.")
                            self.hurt(random.randint(10, 20))
                    elif r1 == "block":
                        if random.random() < 0.7:
                            type.type("You block and push him back! Solid defense!")
                            fight_score += 1
                        else:
                            type.type("The force nearly breaks your arm!")
                            self.hurt(random.randint(15, 25))
                    else:
                        if random.random() < 0.4:
                            type.type("You counter with a DEVASTATING right hook!")
                            fight_score += 3
                        else:
                            type.type("He sees it coming and rocks you instead!")
                            self.hurt(random.randint(20, 30))
                    
                    print("\n")
                    type.type(yellow("=== ROUND 2 ==="))
                    type.type("You're in a clinch! He's trying to throw you!")
                    r2 = input("(knee/headbutt/trip): ").strip().lower()
                    
                    if r2 == "knee":
                        if random.random() < 0.5:
                            type.type("Knee to the ribs! He doubles over!")
                            fight_score += 2
                        else:
                            type.type("He catches your leg and slams you down!")
                            self.hurt(random.randint(15, 25))
                    elif r2 == "headbutt":
                        type.type("CRACK! You both see stars!")
                        self.hurt(random.randint(10, 15))
                        fight_score += 2
                    else:
                        if random.random() < 0.5:
                            type.type("You trip him! He goes DOWN!")
                            fight_score += 3
                        else:
                            type.type("He's too heavy! He uses your momentum against you!")
                            self.hurt(random.randint(15, 20))
                    
                    print("\n")
                    type.type(yellow("=== FINAL ROUND ==="))
                    type.type("Both of you are exhausted. One more exchange decides it!")
                    r3 = input("(all_in/defensive/taunt): ").strip().lower()
                    
                    if r3 == "all_in":
                        if random.random() < 0.4:
                            type.type("You throw EVERYTHING into one punch! HE GOES DOWN!")
                            fight_score += 4
                        else:
                            type.type("He catches you with a hook as you charge! You hit the mat!")
                            fight_score -= 2
                            self.hurt(random.randint(20, 30))
                    elif r3 == "defensive":
                        type.type("You survive to the bell! Decision time!")
                        fight_score += 1
                    else:
                        type.type("You taunt him! He charges blindly!")
                        if random.random() < 0.5:
                            type.type("You sidestep and counter! He's OUT!")
                            fight_score += 3
                        else:
                            type.type("His rage makes him STRONGER! Uh oh.")
                            self.hurt(random.randint(25, 35))
                    
                    print("\n")
                    type.type(yellow("=== DECISION ==="))
                    
                    if fight_score >= 8:
                        type.type("KNOCKOUT! YOU WIN! The crowd goes INSANE!")
                        type.type("You collect " + green(bright("$20,000")) + " and the respect of everyone here!")
                        self.change_balance(20000)
                        self.add_item("Fight Champion Belt")
                    elif fight_score >= 5:
                        type.type("Split decision - you win by points!")
                        self.change_balance(random.randint(10000, 15000))
                    elif fight_score >= 3:
                        type.type("Draw! You get your entry back.")
                        self.change_balance(2000)
                    else:
                        type.type("You lose. Badly. But you'll fight another day.")
                    print("\n")
                else:
                    type.type("You can't afford the entry fee. Maybe next time.")
                    print("\n")
            
            elif action == "bet":
                type.type("Who do you bet on?")
                type.type("1. The Champion - Iron Mike (2:1)")
                type.type("2. The Underdog - Scrappy Pete (5:1)")
                type.type("3. The Wildcard - Mama Bear (8:1)")
                type.type("4. The Newcomer - Some Kid (10:1)")
                pick = input("Pick (1-4): ").strip()
                
                type.type("How much do you bet?")
                try:
                    bet = int(input("Bet: $"))
                    if bet > 0 and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        winner = random.choice(["mike", "mike", "mike", "pete", "mama", "kid"])
                        
                        if pick == "1" and winner == "mike":
                            self.change_balance(bet * 2)
                            type.type("Iron Mike destroys! " + green(bright("$" + str(bet * 2))) + "!")
                        elif pick == "2" and winner == "pete":
                            self.change_balance(bet * 5)
                            type.type("THE UNDERDOG WINS! " + green(bright("$" + str(bet * 5))) + "!")
                        elif pick == "3" and winner == "mama":
                            self.change_balance(bet * 8)
                            type.type("MAMA BEAR IS TERRIFYING! " + green(bright("$" + str(bet * 8))) + "!")
                        elif pick == "4" and winner == "kid":
                            self.change_balance(bet * 10)
                            type.type("THE KID KNOCKED OUT THE CHAMPION?! " + green(bright("$" + str(bet * 10))) + "!!!")
                        else:
                            type.type("Your fighter lost. The pit takes your money.")
                    else:
                        type.type("You can't bet that much.")
                except:
                    type.type("Betting closed.")
                print("\n")
            
            elif action == "organize":
                type.type("You approach the organizer. " + quote("I want to set up a fight. Big stakes."))
                print("\n")
                if self.get_balance() >= 10000:
                    type.type("The organizer grins. " + quote("You want to be a promoter? $10,000 investment, you keep 30% of the winnings."))
                    invest = ask.yes_or_no()
                    if invest == "yes":
                        self.change_balance(-10000)
                        if random.random() < 0.6:
                            earnings = random.randint(15000, 35000)
                            type.type("The fight is LEGENDARY! You earn " + green(bright("$" + str(earnings))) + "!")
                            self.change_balance(earnings)
                            self.add_status("Fight Promoter")
                        else:
                            type.type("The cops raid the place! You lose your investment!")
                            self.add_status("Raid Survivor")
                    else:
                        type.type("Smart. This business isn't for everyone.")
                else:
                    type.type("You don't have enough to be a promoter.")
                print("\n")
            
            else:
                if self.get_balance() >= 500:
                    self.change_balance(-500)
                    type.type("You watch the fights. Blood, sweat, glory. You feel tougher just being here.")
                    self.add_status("Fight Veteran")
                else:
                    type.type("You can't afford the entry. The bouncer doesn't let you in for free.")
                print("\n")
        
        elif event == "intense_mugging":
            type.type("An alley. Wrong turn. Three figures block the exit. Chains. Knives. Bad news.")
            print("\n")
            type.type(yellow("=== THE MUGGING ==="))
            print("\n")
            type.type("The leader steps forward. " + quote("Everything. Wallet, watch, whatever else you got."))
            print("\n")
            action = input("(fight/negotiate/surrender/distraction/run): ").strip().lower()
            
            if action == "fight":
                type.type("You're not going down without a fight!")
                print("\n")
                type.type("How do you attack?")
                attack = input("(leader/closest/wild_swing): ").strip().lower()
                
                if attack == "leader":
                    if random.random() < 0.3:
                        type.type("You drop the leader with one punch! The others hesitate!")
                        print("\n")
                        type.type("They run! You keep everything AND take the leader's wallet!")
                        self.change_balance(random.randint(500, 2000))
                    else:
                        type.type("The leader was ready. They beat you badly.")
                        self.hurt(random.randint(35, 55))
                        self.change_balance(-random.randint(5000, 15000))
                elif attack == "closest":
                    type.type("You swing at the nearest thug!")
                    if random.random() < 0.4:
                        type.type("He goes down! You escape in the chaos!")
                    else:
                        type.type("The others grab you. It's not a fair fight.")
                        self.hurt(random.randint(30, 45))
                        self.change_balance(-random.randint(3000, 10000))
                else:
                    type.type("You swing WILDLY in all directions!")
                    self.hurt(random.randint(20, 35))  # You get hit too
                    if random.random() < 0.35:
                        type.type("Chaotic, but it works! You escape!")
                    else:
                        type.type("They take you down eventually.")
                        self.change_balance(-random.randint(5000, 12000))
                print("\n")
            
            elif action == "negotiate":
                type.type(quote("Look, I've only got a few hundred. Take it, no trouble."))
                print("\n")
                if random.random() < 0.5:
                    type.type("The leader considers. " + quote("Fine. Dump your pockets."))
                    self.change_balance(-random.randint(500, 2000))
                    type.type("They take a small amount and let you go.")
                else:
                    type.type(quote("Liar.") + " They search you anyway and take more.")
                    self.change_balance(-random.randint(3000, 8000))
                print("\n")
            
            elif action == "surrender":
                type.type("You put your hands up. " + quote("Take it. All of it. Just don't hurt me."))
                print("\n")
                loss = min(self.get_balance(), random.randint(5000, 15000))
                self.change_balance(-loss)
                type.type("They take " + str(loss) + " dollars and disappear.")
                if random.random() < 0.3:
                    type.type("One of them drops something as they run. A gold watch!")
                    self.add_item("Stolen Watch")
                print("\n")
            
            elif action == "distraction":
                type.type(quote("COPS! BEHIND YOU!"))
                print("\n")
                if random.random() < 0.4:
                    type.type("They turn! You RUN! It works!")
                else:
                    type.type(quote("Nice try.") + " They beat you for the insult.")
                    self.hurt(random.randint(25, 40))
                    self.change_balance(-random.randint(5000, 12000))
                print("\n")
            
            else:
                type.type("You turn and SPRINT!")
                print("\n")
                if random.random() < 0.5:
                    type.type("You're faster! You escape!")
                else:
                    type.type("They catch you. Runners get extra punishment.")
                    self.hurt(random.randint(30, 50))
                    self.change_balance(-random.randint(5000, 15000))
                print("\n")
        
        elif event == "casino_heist":
            type.type("A woman in a red dress approaches you. " + quote("You look like someone who wants to get rich quick."))
            print("\n")
            type.type(yellow("=== THE CASINO HEIST ==="))
            print("\n")
            type.type("She explains: there's a high-stakes casino downtown. Security is tight, but she has a plan.")
            print("\n")
            type.type(quote("In and out. Forty thousand split. You in?"))
            print("\n")
            action = input("(join/refuse/betray/negotiate): ").strip().lower()
            
            if action == "join":
                type.type("You're in. She gives you a fake ID and a earpiece.")
                print("\n")
                type.type("Inside the casino, your job is to create a distraction. How?")
                distraction = input("(fight/fire_alarm/drunk_act/spill): ").strip().lower()
                
                if distraction == "fire_alarm":
                    type.type("You pull the alarm! Chaos erupts!")
                    if random.random() < 0.6:
                        type.type("The heist goes perfectly! She meets you outside with YOUR CUT!")
                        self.change_balance(random.randint(20000, 40000))
                    else:
                        type.type("Security catches HER. You barely escape. No money.")
                elif distraction == "drunk_act":
                    type.type("You pretend to be wasted and start a scene!")
                    if random.random() < 0.5:
                        type.type("Perfect! They're so focused on you, she empties the vault!")
                        self.change_balance(random.randint(15000, 30000))
                    else:
                        type.type("They just... escort you out. The heist fails.")
                elif distraction == "fight":
                    type.type("You start a fistfight with a random guy!")
                    self.hurt(random.randint(10, 20))
                    if random.random() < 0.5:
                        type.type("Maximum chaos! The heist succeeds!")
                        self.change_balance(random.randint(18000, 35000))
                    else:
                        type.type("You get detained. She escapes without you. No cut.")
                else:
                    type.type("You 'accidentally' spill a drink on a high roller!")
                    if random.random() < 0.4:
                        type.type("The argument draws security! Heist successful!")
                        self.change_balance(random.randint(15000, 30000))
                    else:
                        type.type("The high roller is too calm. Security stays alert. Heist fails.")
                print("\n")
            
            elif action == "betray":
                type.type("You agree... then call the cops.")
                print("\n")
                type.type("The heist is foiled! You get a reward!")
                self.change_balance(random.randint(5000, 12000))
                self.add_status("Informant")
                print("\n")
            
            elif action == "negotiate":
                type.type(quote("Sixty-forty. My way, or I walk."))
                print("\n")
                if random.random() < 0.5:
                    type.type("She smirks. " + quote("I like you. Deal."))
                    type.type("The heist succeeds! You get the bigger cut!")
                    self.change_balance(random.randint(25000, 45000))
                else:
                    type.type("She walks. You watch her disappear into the crowd.")
                print("\n")
            
            else:
                type.type(quote("I don't do crime."))
                print("\n")
                type.type("She shrugs. " + quote("Your loss.") + " She disappears into the night.")
                print("\n")
        
        else:
            type.type("Tonight, the city is quiet. The neon still flickers, the sirens still wail, but nothing touches you.")
            print("\n")
            type.type("You walk alone through streets that don't care if you live or die. Past people who don't see you. Past windows that glow with lives you'll never know.")
            print("\n")
            type.type("Some nights, the city is just a city. Empty. Indifferent. Waiting.")
            print("\n")
            type.type("You find a bench and sit. Watch the cars go by. Wonder what it would be like to just... stop.")
            print("\n")
            type.type("Stop gambling. Stop running. Stop pretending any of this means something.")
            print("\n")
            type.type("But morning will come, and you'll play again. Because that's who you are.")
            self.heal(random.randint(5, 15))
            print("\n")

    # RABBIT CHASE CHAIN - NEARLY THERE NIGHT (FINALE)
    def chase_the_last_rabbit(self):
        # Final rabbit chase - the cave, chance for great reward or death
        if self.get_rabbit_chase() != 5 or self.has_met("Caught Rabbit"):
            self.night_event()
            return
        
        type.type("You've finally cornered it. After all this time, all these chases across every corner of this town, the rabbit has led you here-to the mouth of a dark cave at the edge of the wilderness.")
        print("\n")
        type.type("The rabbit sits at the entrance, almost glowing in the moonlight. It looks at you one last time, then hops into the darkness.")
        print("\n")
        type.type("This is it. The final chase. But something about that cave fills you with dread.")
        print("\n")
        follow = ask.yes_or_no("Do you follow the rabbit into the cave?")
        
        if follow == "yes":
            type.type("You take a deep breath and step into the darkness. The cave swallows all light. You can hear the rabbit's footsteps echoing ahead.")
            print("\n")
            type.type("You stumble deeper and deeper, guided only by sound. The air grows cold. The walls seem to close in.")
            print("\n")
            
            outcome = random.randrange(10)
            
            if outcome < 3:  # 30% - Great reward
                type.type("Then, suddenly-light! The cave opens into an enormous cavern, filled with glittering treasures. Gold coins, gems, artifacts from ages past.")
                print("\n")
                type.type("And there, sitting atop a mountain of wealth, is the rabbit. It looks at you and nods, as if to say " + quote("You earned this."))
                print("\n")
                type.type("Then, in a final burst of sparkles, it vanishes forever.")
                print("\n")
                type.type(green(bright("You've found the rabbit's treasure trove!")))
                coins = random.randint(50000, 100000)
                type.type("You stuff your pockets with " + green(bright("$" + str(coins))) + " worth of valuables.")
                self.change_balance(coins)
                self.add_item("Rabbit's Blessing")
                self.meet("Caught Rabbit")
            elif outcome < 7:  # 40% - Nothing, rabbit escapes
                type.type("You chase the sound of footsteps, but they lead nowhere. The cave twists and turns, and eventually...")
                print("\n")
                type.type("You find yourself back at the entrance. The rabbit is gone. Vanished, like it was never there at all.")
                print("\n")
                type.type(yellow("Maybe some things aren't meant to be caught. The hunt is over. You walk back to your wagon, somehow at peace."))
                self.meet("Caught Rabbit")  # Ends the chain
            else:  # 30% - Rabbit suicide / player death
                type.type("You follow the footsteps until they suddenly stop. Then you hear it-a rumble, deep within the earth.")
                print("\n")
                type.type("The ground beneath you gives way.")
                print("\n")
                type.type("You fall, and fall, and fall into the endless dark. The last thing you see is the rabbit, standing at the edge of the chasm above you, watching you plummet.")
                print("\n")
                type.slow(red(bright("Some mysteries are better left unsolved. The rabbit claimed its final victim. You should have let it go.")))
                print("\n")
                self.kill()
        else:
            type.type("You stand at the mouth of the cave for a long time. The rabbit doesn't come back out.")
            print("\n")
            type.type("Eventually, you turn around and walk away. Some chases have to end, even without a catch.")
            print("\n")
            type.type(yellow("You never see the rabbit again. But sometimes, late at night, you swear you can hear footsteps outside your wagon, and a soft, rhythmic thumping."))
            self.meet("Caught Rabbit")  # Ends the chain peacefully
            print("\n")

    def empty_event(self):
        type.type("This day's events are empty. Therefore, this played. Thank you.")
        print("\n")

    # Story Events
    def trusty_tom(self):
        self.meet("Tom Event")
        type.type("You wake up to a blaring engine, roaring down the road towards you. ")
        type.type("As you scratch your eyes awake, you read \'Tom's Trusty Trucks and Tires\' painted on the hood of a bright gold truck. ")
        type.type("Waving the vehicle down, the truck slows, then halts, and an old, jolly man jumps out. ")
        print("\n")
        type.type("\"Well, howdy! The name's Tom. It appears you've gotten yourself in a bit of a pickle, ya think?\" ")
        type.type("Tom pulls a big red wrench out of his pocket, and walks to the hood of your beaten down wagon. ")
        repair_price = random.choice([150, 200, 250, 300, 350])
        type.type("\"Yep, this thing's busted alright! Tell ya what, for, I don't know, " + green(bright(str(repair_price) + " bucks")) + ", I'll get this thing replaced for ya, good as new! Whaddya say?\" ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if(yes_or_no == "n") or (yes_or_no == "no"):
                type.type("\"Really? No dice, huh. Yunno, I think you're makin' a mistake, but I ain't one to judge. You have a nice day now.\" ")
                type.type("Tom has a sad look in his eye. It's clear that he wanted to help you. ")
                type.type("You watch as his big golden truck stutters, starts, then drives away.")
                print("\n")
                return
            elif((yes_or_no == "y") or (yes_or_no == "yes")):
                if self.__balance >= repair_price:
                    self.meet("Tom")
                    type.type("\"Really? Awesome! I'll be the best dang mechanic this ol' automobile has ever seen!\" ")
                    type.type("You watch in awe, as Tom, a man who has clearly perfected his craft, fixes up your wagon in no time. Sweet. ")
                    self.change_balance(-repair_price)
                    self.add_item("Car")
                    type.type(magenta(bright("Your car has been fixed! You can now drive around!")))
                    print("\n")
                    type.type("\"Well, gee, this has been fun. Be seein' you around, ya know?\" ")
                    type.type("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                    print("\n")
                    return
                else:
                    type.type("\"Aww man, sorry to tell you, but you just don't got enough funds for this, yunno?\" ")
                    random_chance = random.randrange(2)
                    # Broke, and Tom offers discount
                    if random_chance == 0:
                        print("\n")
                        type.type("\"You know what? I'm feelin' generous, and the shop's been doing well lately. ")
                        type.type("Tell ya what, I can take the offer down " + green(bright(str(50) + " dollars")) + " just for you. ")
                        type.type("Could ya do " + green(bright(str(repair_price-50) + " bucks")) + "?\" ")
                        while True:
                            yes_or_no_2 = input("").lower()
                            print()
                            # Declining Tom's second offer
                            if(yes_or_no_2 == "n") or (yes_or_no_2=="no"):
                                print()
                                type.type("\"Really? No dice, huh. Even with the discount? Yunno, I think you're makin' a mistake, but I ain't one to judge. You have a nice day now.\" ")
                                type.type("Tom has a dissapointed look in his eye. It's clear that he wanted to help you. ")
                                type.type("You watch as his big golden truck stutters, starts, then drives away.")
                                print("\n")
                                return
                            elif((yes_or_no_2 == "y") or (yes_or_no_2 == "yes")):
                                if self.__balance >= (repair_price-50):
                                    self.meet("Tom")
                                    type.type("\"Really? Awesome! I'll be the best dang mechanic this ol' automobile has ever seen!\" ")
                                    type.type("You watch in awe, as Tom, a man who has clearly perfected his craft, fixes up your wagon in no time. Sweet. ")
                                    self.change_balance(-(repair_price-50))
                                    self.add_item("Car")
                                    type.type(magenta(bright("Your car has been fixed! You can now drive around!")))
                                    print("\n")
                                    type.type("\"Well, gee, this has been fun. Be seein' you around, ya know?\" ")
                                    type.type("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                                    print("\n")
                                    return
                                else:
                                    type.type("\"Still can't afford it? That's a real shame. I really wish there was something I could do. Best of luck my friend. Be seeing ya around, ya know?\" ")
                                    type.type("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                                    print("\n")
                                return
                            else:
                                type.type("\"Whaddya say?\" ")

                    # Broke, and Tom can't offer discount
                    elif random_chance == 1:
                        print("\n")
                        type.type("\"I really wish there was something I could do. Best of luck my friend. Be seeing ya around, ya know?\" ")
                        type.type("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                        print("\n")
                        return
            else:
                type.type("\"Whaddya say?\" ")



    def filthy_frank(self):
        self.meet("Frank Event")
        type.type("You wake up to a roaring engine, blasting into your eardrums. ")
        type.type("As you jump up out of the front seat, you read \'Filthy Frank's Flawless Fixtures\' painted on the hood of a...well...a beater. ")
        type.type("Waving the vehicle down, the beater slows, then appears to break down, and an old man with tattoo sleeves and long black hair steps out. He kicks his car, and the engine starts blaring once more. ")
        print("\n")
        type.type("\"Hello, the name's Frank. Now I've got a baseball game to catch, but it looks like you could use some help.\" ")
        type.type("Frank pulls a shiny silver hammer out of his pocket, and walks to the hood of your beaten down wagon. ")
        repair_price = random.choice([50, 75, 100])
        type.type("\"My god. This is just awful. Tell you what, I can fix this up for like " + green(bright(str(repair_price) + " bucks")) + ", and your engine will be runnin' just as good as mine. You game?\" ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if(yes_or_no == "n") or (yes_or_no == "no"):
                type.type("\"What?! How could you not accept my service? I'm the cheapest damn autoshop worker on this here planet! But NOOOO, NOT FRANK! Never Frank. He Voted For Trump! Let's all ridicule frank for his political party. You god damn liberals.\" ")
                type.type("Frank spits in your face, and get back in his truck. ")
                print("\n")
                type.type("You watch as he revs his engine, gets out of his truck, kicks his beater, gets back in, revs his engine, and speeds off into the horizon. ")
                print("\n")
                return
            elif((yes_or_no == "y") or (yes_or_no == "yes")):
                if self.__balance >= repair_price:
                    type.type("\"Darn tootin! Lemme just do my thing.\" ")
                    type.type("You watch in terror as Frank takes the hammer, and begins to beat the living daylight out of your wagon's engine. Each swing causes you to wince more and more. ")
                    self.change_balance(-repair_price)
                    random_chance = random.randrange(5)
                    if random_chance < 2:
                        self.meet("Frank")
                        self.add_item("Car")
                        type.type(magenta(bright("Your car has been fixed! You can now drive around!")))
                        print("\n")
                        type.type("\"Ah, I love fixin people's cars. You sure do drive a shitty vehicle, but I'm just glad I can help get you back up and going to your job every day. Gotta do something to help in this economy, you know?\" ")
                        print("\n")
                        type.type("And with that, you watch as he revs his engine, gets out of his truck, kicks his beater, gets back in, revs his engine, and speeds off into the horizon.")
                        print("\n")
                        return
                    else: 
                        type.type("You notice Frank beginning to sweat while trying to fix your car. Each swing of his hammer is getting louder and louder, and Frank is clearly beginning to panic. Frank turns towards you, with tears streaming down his face. Or maybe it's just sweat.")
                        print("\n")
                        type.type("\"Oh man, listen, I'm so sorry about this, you know? I really thought if I just gave it the old hammer whirl that would do the trick. Hold on, maybe I have something in my truck. Stay right here!\"")
                        print("\n")
                        type.type("You watch Frank runs over to his truck, kicks the side of it, gets in, revs his engine, and speeds off into the horizon. God Dammit.")
                        print("\n")
                        return
                else:
                    self.add_danger("Frank")
                    type.type("\"Are you tryna rip me off? Clearly you don't have enough money to afford my services, which is honestly pathetic, since I have the cheapest services around! I don't get what it is with you young folk and not working, just staying home and smoking weed. It's miserable. You're miserable. Dontchu know I know people on the inside! I'll remember this one.\"")
                    print("\n")
                    type.type("You watch as he revs his engine, gets out of his truck, kicks his beater, gets back in, revs his engine, and speeds off into the horizon.")
                    print("\n")
                    return
            else:
                type.type("\"Speak up! You're mumbling. \" ")



    def optimal_oswald(self):
        self.meet("Oswald Event")
        type.type("You wake up to the sight of a glossy black limousine, quietly approaching your wagon. ")
        type.type("As you sit up from your slumber, you read \'Oswald's Optimal Outoparts\' cursively engraved in gold letters on the side of the limo. ")
        type.type("Waving the vehicle down, the limo slows, then stops before you. The door opens vertically, and a large red carpet is rolled out onto the street. You watch in awe as a man, with a combover and a tuxedo, walks out before you. He coughs, then speaks.")
        print("\n")
        type.type("\"Why hello there! The name's Oswald, as you can see by my nametag. Do you like my bowtie? Well of course you do! It appears your limousine has broken down.\" ")
        type.type("Oswald pulls a gold whistle out of his pocket, and blows into it deeply. ")
        type.type("\"Oh Stuart!\" You watch as a bald man in a tailcoat suit, no taller than 4 feet, hobbles over to Oswald's side.")
        print("\n")
        type.type("\"This is Stuart! He will fix your limousine up for a fair price. Let's say, I don't know, I suppose a fair price is " + green(bright("500,000 dollars")) + ". ")
        repair_price = random.choice([800, 850, 900])
        type.type("Okay, the look on your face says that I'm making a big mistake. Let's try " + green(bright("$" + str(repair_price))) + ", and Stuart here will get you back on the road! Do you accept?\" ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if(yes_or_no == "n") or (yes_or_no == "no"):
                type.type("\"Really? You don't want my services? I'm so sorry Stuart, But it appears they don't want our services.\" ")
                type.type("Stuart begins to break down into tears, and he runs quickly back into the limo. ")
                type.type("\"Shame on you! Shame on you! I hope to never see the likes of you again.\"")
                print("\n")
                type.type("You watch as Oswald rolls up the red carpet, gets back in the limo, and drives off into the distance.")
                print("\n")
                return
            elif((yes_or_no == "y") or (yes_or_no == "yes")):
                if self.__balance >= repair_price:
                    self.meet("Oswald")
                    type.type("\"Jolly good! Stuart!\" ")
                    type.type("You watch as the little man walks to the front of your wagon, opens the hood, and jumps in. You can't really see what's going on, but after a couple of minutes, Stuart jumps back out, covered in oil.")
                    self.change_balance(-repair_price)
                    self.add_item("Car")
                    type.type(magenta(bright("Your car has been fixed! You can now drive around!")))
                    print("\n")
                    type.type("\"Oh my Stuart! Someone got a little too excited, didn't you? Yep, you're getting a bath as soon as we get back to the shop. Thanks again, stranger, it's been a pleasure doing business with you. I recall it's good custom to tip after events like this, yes? Here, take this.\" ")
                    tip = random.choice([50, 100])
                    type.type("Oswald hands you a bright green bill, worth " + green(bright("$" + str(tip))) + ".")
                    self.change_balance(tip)
                    type.type("And with that, you watch as Stuart rolls up the red carpet. Oswald and Stuart get back in the limo, and drive off into the distance.")
                    print("\n")
                    return
                else:
                    type.type("\"Why, it appears you're far too poor to attain my services. I'm truly sorry about this. Tell you what, here's a little something to get you back on your feet.\" ")
                    tip = random.choice([50, 100])
                    type.type("Oswald hands you a bright green bill, worth " + green(bright("$" + str(tip))) + ".")
                    self.change_balance(tip)
                    type.type("And with that, you watch as Stuart rolls up the red carpet. Oswald and Stuart get back in the limo, and drive off into the distance. ")
                    if self.__balance > repair_price:
                        type.type("Looking down, you see that after Oswald's tip, you had enough money to pay for the repair service after all, but it was too late. Oh well.")
                    print("\n")
                    return
            else:
                type.type("\"Come again?\" ")


    def update_story_event_prereqs(self):
        if(self.__balance>=200):
            self.__prereqs[0] = True
        if self.has_item("Car"):
            self.__prereqs_done[0] = True

    def start_day(self):
        type.typeover("Press a key to continue:", bright(yellow("~ ~ ~ Morning, Day " + str(self.__day) + " ~ ~ ~ ")), True)

        # ============================================
        # DAILY ITEM EFFECTS (Passive triggers)
        # ============================================
        
        # Suzy's Gift - Slow sanity restoration from her kindness
        if self.apply_suzys_gift_effects():
            pass  # Silent effect - player doesn't know
        
        # Necronomicon - Corrupts the soul
        if self.apply_necronomicon_effects():
            if random.randrange(3) == 0:  # Sometimes show a hint
                type.slow(red("You wake with whispers echoing in your skull. The book pulses in your bag."))
                print("\n")
        
        # Cursed Coin - Random misfortune
        if self.apply_cursed_coin_effects():
            cursed_effect = random.choice([
                "You stub your toe getting out of the car. Hard. The coin in your pocket feels warm.",
                "A bird poops directly on your windshield. Then another. Then five more. The coin jingles.",
                "You feel a strange sense of dread wash over you. The cursed coin seems to glow faintly.",
                "Your coffee was somehow already cold. You didn't even have coffee. Where did this cold coffee come from?"
            ])
            type.type(cursed_effect)
            print("\n")
            if random.randrange(5) == 0:
                small_loss = random.randint(5, 25)
                type.type("You realize you've lost " + red(bright("${:,}".format(small_loss))) + " somewhere. Weird.")
                self.change_balance(-small_loss)
        
        # Broken state effects at start of day
        if self.__is_broken:
            print()
            self.sanity_indicator()
            if random.randrange(3) == 0:
                effect = self.get_broken_effect()
                type.slow(red(effect))
                print("\n")
        # Display sanity status at start of day
        elif self.__sanity <= 75:
            print()
            self.sanity_indicator()
        
        self.update_rank()
        self.update_story_event_prereqs()
        ranStoryEvent = False

        # MILLIONAIRE MORNING - Special visitor when you've hit $1M and still have it
        if self.is_millionaire() and self.__balance >= 1000000 and not self.was_millionaire_visited():
            self.millionaire_morning_visitor()
            self.set_millionaire_visited()
            return  # Skip normal day events - this is your final day

        if((self.__prereqs[0]) and not (self.__prereqs_done[0])):
            random_chance = random.randrange(3)
            if random_chance == 0:
                while((not self.has_met("Tom Event")) or (not self.has_met("Frank Event")) or (not self.has_met("Oswald Event"))):
                    random_chance = random.randrange(3)
                    if (random_chance == 0) and (not self.has_met("Tom Event")):
                        self.trusty_tom()
                        ranStoryEvent = True
                        break
                    elif (random_chance == 1) and (not self.has_met("Frank Event")):
                        self.filthy_frank()
                        ranStoryEvent = True
                        break
                    elif (random_chance == 2) and (not self.has_met("Oswald Event")):
                        self.optimal_oswald()
                        ranStoryEvent = True
                        break

        if ranStoryEvent == False:
            self.day_event()

        self.update_rank()


    def has_pests(self):
        if self.has_danger("Spider") or self.has_danger("Cockroach") or self.has_danger("Rat") or self.has_danger("Termite"):
            return True
        else:
            return False

    def kill_pests(self):
        self.use_item("Pest Control")
        if self.has_danger("Spider"):
            self.lose_danger("Spider")
        if self.has_danger("Cockroach"):
            self.lose_danger("Cockroach")
        if self.has_danger("Rat"):
            self.lose_danger("Rat")
        if self.has_danger("Termite"):
            self.lose_danger("Termite")

    def get_mark_index(self, mark):
        match mark:
            case "Spider Bite":
                return 0
            case "Hepatitis":
                return 1
            case "Squirrel Bite":
                return 2
            case "Squirrely Fed":
                return 3
            case "Rabies":
                return 4
            case "Rat Bite":
                return 5
            case "Snake Bite":
                return 6
            case "Sore Throat":
                return 7
            case "Cold":
                return 8
            case "Mechanic":
                return 9

    def mark_day(self, mark, time="day"):
        i = self.get_mark_index(mark)
        if time == "day":
            self.__counting_days[i] = self.__day
        if time == "night":
            self.__counting_days[i] = self.__day-1

    def get_days_elapsed(self, mark):
        i = self.get_mark_index(mark)
        return self.__day - self.__counting_days[i]
    
    
    def update_silver_value(self):
        if self.has_item("Enchanting Silver Bar"):
            return 1000

    def update_status(self):
        damage = 0
        if self.__clear_all_status == True:
            type.type("Whatever the Witch Doctor gave you yesterday, it worked wonders on you. You feel amazing, as though your body had been completely cleansed.")
            print("\n")
            self.__status_effects = set()
            self.__injuries = set()
            self.__is_sick = False
            self.__is_injured = False
            self.__clear_all_status = False

        # Physical Threats
        # Spider Bite
        if self.has_status("Spider Bite"):
            days_elapsed = self.get_days_elapsed("Spider Bite")
            if(self.__clear_status):
                self.remove_status("Spider Bite")
                type.type("Your spider bite is starting to heal. ")
            elif days_elapsed == 0:
                damage += random.choice([1, 2])
                type.type("The fangmarks of your spider bite are faint but visible. ")
            elif days_elapsed == 1:
                damage += random.choice([3, 4, 5, 6])
                type.type("Your spider bite is sore and swolen. ")
            elif days_elapsed == 2:
                damage += random.choice([4, 5, 6, 7, 8, 9])
                type.type("Your spider bite is really painful. You don't feel good. ")
            elif days_elapsed >= 3:
                random_chance = random.randrange(4)
                if (random_chance == 0):
                    self.remove_status("Spider Bite")
                    type.type("Your spider bite is starting to heal. ")
                else:
                    damage += random.choice([7, 9, 11, 13, 15])
                    type.type("Your spider bite is purple and pussing. A trip to the doctors might be a good idea. ")
            print("\n")

            if damage >= self.__health:
                self.hurt(damage)

        # Snake Bite
        if self.has_status("Snake Bite"):
            days_elapsed = self.get_days_elapsed("Snake Bite")
            if(self.__clear_status):
                self.remove_status("Snake Bite")
                type.type("Your snake bite is starting to heal. ")
            elif days_elapsed == 0:
                damage += random.choice([2, 4])
                type.type("The fangmarks of your snake bite are faint but visible. There's some swelling. ")
            elif days_elapsed == 1:
                damage += random.choice([6, 8, 10, 12])
                type.type("Your snake bite is swolen, and very painful. ")
            elif days_elapsed == 2:
                damage += random.choice([8, 10, 12, 14, 16, 18])
                type.type("Your snake bite is really painful. You feel really nauseous. ")
            elif days_elapsed >= 3:
                damage += random.choice([7, 14, 18, 22, 26, 30])
                type.type("Your snake bite is turning black. A trip to the doctors is probably the right choice. ")
            print("\n")

            if damage >= self.__health:
                self.hurt(damage)

        # Squirrel Bite
        if self.has_status("Squirrel Bite"):
            days_elapsed = self.get_days_elapsed("Squirrel Bite")
            if(self.__clear_status):
                self.remove_status("Squirrel Bite")
                type.type("Your squirrel bite is starting to heal. ")
            elif days_elapsed == 0:
                type.type("You look at the bite mark the squirrel left on your leg, but it's hard to tell if it's infected. A trip to the doctor's would solve all your worries.")
            elif ((days_elapsed >= 1) and self.has_status("Rabies")) or (days_elapsed < 5):
                type.type("Your squirrel bite looks the same as it did yesterday.")
            elif (days_elapsed == 5):
                self.remove_status("Squirrel Bite")
                type.type("Your squirrel bite is starting to heal. ")
            print("\n")

        # Rat Bite
        if self.has_status("Rat Bite"):
            days_elapsed = self.get_days_elapsed("Rat Bite")
            if(self.__clear_status):
                self.remove_status("Rat Bite")
                type.type("Your rat bite is starting to heal. ")
            elif days_elapsed == 0:
                type.type("You look at the bite mark the rat left on your ankle. It hurts like a motherfucker, but it's hard to tell if the bite infected. A trip to the doctor's is what a smart person would do.")
            elif ((days_elapsed >= 1) and self.has_status("Rabies")) or (days_elapsed < 5):
                type.type("Your rat bite looks the same as it did yesterday. It might hurt worse, but it's hard to tell.")
            elif (days_elapsed == 5):
                self.remove_status("Rat Bite")
                type.type("Your rat bite is starting to heal. ")
            print("\n")

        # Rabies
        if self.has_status("Rabies"):
            days_elapsed = self.get_days_elapsed("Rabies")
            if(self.__clear_status) and (days_elapsed<=3):
                self.remove_status("Rabies")
            elif days_elapsed==3:
                type.type(red("Your mouth has begun to foam. It seems you've contracted rabies. Death is inevitable, and it's hurdling towards you."))
                damage += random.choice([10, 30, 50, 70])
                self.lose_sanity(random.choice([5, 6, 7]))  # Rabies symptoms severely drain sanity
                print("\n")
            elif days_elapsed==4:
                type.type(red("The foaming has gotten worse, to the point where you begin to choke on it. You have a seizure in your car. Life is coming to an end."))
                damage += random.choice([50, 70, 90])
                self.lose_sanity(random.choice([8, 10, 12]))  # Advanced rabies destroys your mind
                print("\n")
            elif days_elapsed==5:
                type.slow(red(bright("Your mind has gone completely insane. You start tearing at your face, ripping away chunks of skin. The foam in your mouth turns red, and you feel yourself begin to fade from existance. You pull your eyes from their sockets, and scream in agony, as you die a painful death.")))
                self.kill()

            if damage >= self.__health:
                self.hurt(damage)


        # Sicknesses
        # Cold
        if self.has_status("Cold"):
            self.__is_sick = True
            days_elapsed = self.get_days_elapsed("Cold")
            if(self.__clear_status):
                self.remove_status("Cold")
            elif days_elapsed == 0:
                damage += random.choice([2, 3, 6])
            elif days_elapsed == 1:
                damage += random.choice([2, 5, 7])
            elif days_elapsed > 3:
                random_chance = random.randrange(2)
                if random_chance == 0:
                    self.remove_status("Cold")
                else:
                    damage += random.choice([3, 4, 5, 6, 7, 8, 9])

        # Sore Throat
        if self.has_status("Sore Throat"):
            self.__is_sick = True
            days_elapsed = self.get_days_elapsed("Sore Throat")
            if(self.__clear_status):
                self.remove_status("Sore Throat")
            elif self.has_item("Cough Drops"):
                type.type("With your " + bright(magenta("Cough Drops")) + " in hand, you begin to suck each drop, one by one, until the box is empty, and your throat feels nice and cool.")
            elif days_elapsed == 0:
                damage += random.choice([1, 3, 5])
            elif days_elapsed == 1:
                damage += random.choice([2, 4, 5])
            elif days_elapsed > 3:
                random_chance = random.randrange(2)
                if random_chance == 0:
                    self.remove_status("Sore Throat")
                else:
                    damage += random.choice([5, 6])

        # Hepatitis
        if self.has_status("Hepatitis"):
            self.__is_sick = True
            days_elapsed = self.get_days_elapsed("Hepatitis")
            if(self.__clear_status):
                self.remove_status("Hepatitis")
            elif days_elapsed == 0:
                damage += random.choice([1, 3, 5])
            elif days_elapsed == 1:
                damage += random.choice([5, 6, 7])
            elif days_elapsed == 2:
                damage += random.choice([2, 7, 10, 12])
            elif days_elapsed == 3:
                damage += random.choice([2, 8, 15, 17, 20])
            elif days_elapsed == 4:
                damage += random.choice([3, 9, 18, 20, 25])
            elif days_elapsed > 4:
                random_chance = random.randrange(4)
                if random_chance == 0:
                    self.remove_status("Hepatitis")
                else:
                    damage += random.choice([5, 10, 15, 20, 25, 30])


        # Sets is_sick to False if you don't have any sicknesses, an prints a health update
        if (self.__is_sick) and not (self.has_status("Hepatitis") and not self.has_status("Sore Throat") or self.has_status("Cold")):
            if self.has_status("Rabies"):
                type.type("With rabies in your system, you're lucky to be alive.")
            elif self.has_status("Snake Bite") or self.has_status("Spider Bite"):
                type.type("You may not be 100%, but at least you don't feel under the weather anymore.")
            else:
                type.type("You feel much less sick than you did yesterday, which is always good.")
            self.__is_sick = False
            print("\n")

        # if player is sick, prints a sickness update
        if self.__is_sick:
            type.type(self.__lists.get_sickness_update())
            print("\n")

        # If sickness kills the player, this does it.
        if damage >= self.__health:
                type.slow(bright(red(self.__lists.get_sickness_death())))
                self.kill()

        # Sets is_injured to True if you have 1 or more injuries
        if len(self.__injuries)>0:
            self.__is_injured = True

        # Sets is_injured to False if you have 0 injuries, and prints a healed update
        if (self.__is_injured) and len(self.__injuries)==0:
            type.type("The injuries on your body are doing much better.")
            print("\n")
            self.__is_injured = False
        
        # If you're injured, prints an injury update, and adds damage
        if self.__is_injured:
            damage += len(self.__injuries)
            type.type(self.__lists.get_injury_update())
            print("\n")

        # If you took damage, this does it.
        if damage > 0:
            self.hurt(damage)

        self.__clear_status = False

        # Sprays your car with Pest Control if you have a pest
        if self.has_pests() and self.has_item("Pest Control") and (not self.has_travel_restriction("Rain")) and (not self.has_travel_restriction("Wind")):
            type.type("Believing that there may be an unwanted pest somewhere in your car, you spray your " + magenta(bright("Pest Control")) + " throughout the vehicle, hoping that it'll solve your pest issues. ")
            self.kill_pests()
            type.type("After giving the wagon a minute to air out, you get back inside.")
            print("\n")

        # Feeds Squirrely if you have Acorns
        if self.has_item("Bag of Acorns") and self.has_item("Squirrely"):
            type.type("You give Squirrely your " + magenta(bright("Bag of Acorns")) + ", and he goes to town, munching down all of them. What a good squirrel.")
            print("\n")

        # Gives Squirrely Status Update
        if self.has_item("Squirrely"):
            days_elapsed = self.get_days_elapsed("Squirrely Fed")
            if self.has_travel_restriction("rain") or self.has_travel_restriction("Wind"):
                type.type(self.__lists.get_worried_squirrely_update())
            if days_elapsed == 0:
                type.type("Squirrely is well-fed, and happy as can be.")
            elif days_elapsed <= 4:
                type.type(self.__lists.get_fed_squirrely_update())
            elif days_elapsed < 6:
                type.type(self.__lists.get_hungry_squirrely_update())
            elif days_elapsed >= 6:
                random_chance = random.randrange(5)
                if random_chance == 0:
                    type.type("Looking around, you can't find Squirrely anywhere. No, seriously, you can't find him anywhere. Beginning to panic, you start to tear the car apart, hoping that you'll find him somewhere. You call out his name, 'Squirrely', 'Squirrely', but you get no response. Tears start falling from your eyes. Is this really it? Is this really goodbye? Poor Squrrely, all alone. You may never see your little Squirrely ever again.")
                    self.use_item("Squirrely")
                    self.meet("Squirrely")
                    self.lose_sanity(random.choice([3, 4, 5]))  # Losing Squirrely is devastating
                elif random_chance == 1:
                    type.type("Looking around, you can't find Squirrely anywhere. No, seriously, you can't find him anywhere. And that smell, it reeks! You begin to fear for the worst. Tearing the car apart, you find him, laying lifeless under the passenger seat. Poor Squirrely.")
                    print("\n")
                    type.type("Using an old shirt, you pick Squirrely off the floor of the wagon. Carrying him into the woods, you set him down, and dig a hole. You place Squirrely inside, cover him up with dirt, and place a flower over the grave. Goodbye, Squirrely. I loved you.")
                    self.use_item("Squirrely")
                    self.meet("Dead Squirrely")
                    self.lose_sanity(random.choice([5, 6, 7]))  # Finding Squirrely dead is traumatic
                else:
                    type.type(self.__lists.get_hungry_squirrely_update())
            print("\n")


    def get_unlocked_adventure_areas(self):
        """Returns a list of adventure areas the player can walk to.
        
        Unlock requirements:
        - Woodlands: All 3 woodlands events (path, river, field) OR woodlands_adventure. Rank 3+ to walk.
        - Swamp: All 3 swamp events (stroll, wade, swim) OR swamp_adventure. Rank 4+ to walk.
        - Beach: All 3 beach events (stroll, swim, dive) OR beach_adventure. Rank 4+ to walk.
        - City: All 3 city events (streets, stroll, park) OR city_adventure. Rank 5 to walk.
        - Underwater: beach_adventure OR underwater_adventure. Rank 5 to walk.
        
        At rank 5, all adventures are available even if not yet visited."""
        areas = []
        rank = self.get_rank()
        
        # Check if player has completed all 3 events for each area
        all_woodlands_events = (self.has_met("Woodlands Path Event") and 
                                 self.has_met("Woodlands River Event") and 
                                 self.has_met("Woodlands Field Event"))
        
        all_swamp_events = (self.has_met("Swamp Stroll Event") and
                            self.has_met("Swamp Wade Event") and
                            self.has_met("Swamp Swim Event"))
        
        all_beach_events = (self.has_met("Beach Stroll Event") and
                            self.has_met("Beach Swim Event") and
                            self.has_met("Beach Dive Event"))
        
        all_city_events = (self.has_met("City Streets Event") and
                           self.has_met("City Stroll Event") and
                           self.has_met("City Park Event"))
        
        # Woodlands - rank 3+ to walk, must have done all 3 woodlands events OR woodlands_adventure
        if rank >= 3:
            if all_woodlands_events or self.has_met("Woodlands Adventure Event"):
                areas.append(("The Woodlands", "woodlands_adventure"))
        
        # Swamp - rank 4+ to walk, must have done all 3 swamp events OR swamp_adventure
        if rank >= 4:
            if all_swamp_events or self.has_met("Swamp Adventure Event"):
                areas.append(("The Swamp", "swamp_adventure"))
        
        # Beach - rank 4+ to walk, must have done all 3 beach events OR beach_adventure
        if rank >= 4:
            if all_beach_events or self.has_met("Beach Adventure Event"):
                areas.append(("The Beach", "beach_adventure"))
        
        # At rank 5, all adventures are available even if not visited yet
        if rank >= 5:
            # Add any not already in the list
            if ("The Woodlands", "woodlands_adventure") not in areas:
                areas.append(("The Woodlands", "woodlands_adventure"))
            if ("The Swamp", "swamp_adventure") not in areas:
                areas.append(("The Swamp", "swamp_adventure"))
            if ("The Beach", "beach_adventure") not in areas:
                areas.append(("The Beach", "beach_adventure"))
            # City - rank 5 to walk, must have done all 3 city events OR city_adventure
            if all_city_events or self.has_met("City Adventure Event"):
                areas.append(("The City", "city_adventure"))
            # Underwater - rank 5 to walk, unlocked by beach_adventure OR underwater_adventure
            if self.has_met("Beach Adventure Event") or self.has_met("Underwater Adventure Event"):
                areas.append(("The Ocean Depths", "underwater_adventure"))
        
        return areas

    def afternoon(self):
        self.update_status()
        self.update_rank()
        self.update_convenience_store_inventory()

        # Wind Restriction (1,000-10,000)
        if self.has_travel_restriction("Wind"):
            random_chance = random.randrange(3)
            if random_chance == 0:
                type.type("You watch the wind pull twigs and branches from the trees all afternoon.")
            elif random_chance == 1:
                type.type("One branch falls, and lands on the hood of your wagon. Had it been any bigger, that could've been bad.")
            elif random_chance == 2:
                type.type("You hear a loud crash in the distance. A tree must've fallen nearby.")
            else:
                type.type("The wind pushes the light gray clouds across the sky, and you watch them all afternoon.")
            
            print("\n")
            
            type.type("As the sun begins to fall, you collect your money, and leave the warmth of your wagon. You barrel out into the wind, trudging your way to the casino.")

            print("\n")
            random_chance = random.randrange(3)
            if random_chance == 1:
                type.slow(red("It's a windy one today. Now, let us gamble."))
            elif random_chance == 2:
                type.slow(red("Suprised you made it here in one piece, given the weather. It's time to bet."))
            elif random_chance == 3:
                type.slow(red("It's nice to see you tonight. Shows commitment. You ready?"))
            else:
                type.slow(red("Wind didn't blow any of your money away, did it? Anyways, let's play."))
            print("\n")

        # Rain Restriction (500,000-900,000)
        elif self.has_travel_restriction("Rain"):
            type.type("You watch, as the rain pours, and pours, and pours. By nightfall, the rain hasn't let up, and the flooding in the streets has only gotten worse. Unfortunately, you're gonna have to skip out on Blackjack for the night.")
            print("\n")
            type.type("You get cozy in your car, and begin to doze off. That's all for " + bright(yellow("Day " + str(self.__day))) + ".")
            print("\n")
            type.type("As you sleep, you dream and dream about the sand beneath your feet, the waterfall above you raining water down, splashing in the river, leading out to the ocean and the horizon before you. The sun looks so bright in the fading orange sky, and the hot sand began to cool below you. Before you get the chance to say goodbye, you wake up, having slept through all of " + bright(yellow("Day " + str(self.__day + 1))) + " and " + bright(yellow("Day " + str(self.__day + 2))) + "." )
            random_chance = random.randrange(2)
            if random_chance == 0:
                self.__day += 3
            else:
                type.type(" And even " + bright(yellow("Day " + str(self.__day + 3))))
                self.__day += 4
            print("\n")
            type.type("As you awake on " + bright(yellow("Day " + str(self.__day))) + ", you notice the raindrops begin to slow down, clouds begin to clear, and a golden ray of sunshine fills your soaked wagon. Looking in the seat next to you, your pile of green bills brings a sparkle to your eyes. You hear the money call to you. It's time. Let's go win some hands.")

            print("\n")

            type.type("As the sun begins to fall, you collect your money, and leave the safety of your wagon. You barrel out into the damp air, up the muddy dirt road, and into the casino.")

            print("\n")
            random_chance = random.randrange(3)
            if random_chance == 1:
                type.slow(red("Wipe those shoes. It's difficult to wash these carpets."))
            elif random_chance == 2:
                type.slow(red("Long time no see, yeah? Let's get back to it."))
            elif random_chance == 3:
                type.slow(red("You broke the streak you had going. Wanna make up for it in bets?"))
            else:
                type.slow(red("Glad the rain didn't permanently wash you away. That would have been a shame."))
            print("\n")

        elif self.has_travel_restriction("Battery"):
            pass

        elif self.has_travel_restriction("Engine"):
            pass
        
        # MILLIONAIRE AFTERNOON - Special choices after the visitor
        elif self.was_millionaire_visited() and self.__balance >= 1000000:
            self.millionaire_afternoon()
            
        elif self.has_item("Car"):
            choice = None
            shops = self.__lists.make_shop_list()
            adventure_areas = self.get_unlocked_adventure_areas()
            
            type.type("Would you like to spend your day driving somewhere? ")
            print()
            
            # List shops
            for i in range(len(shops)):
                type.type(str(i+1) + ". " + shops[i])
                time.sleep(0.5)
                print()
            
            # List unlocked adventure areas
            adventure_start = len(shops)
            if len(adventure_areas) > 0:
                print()
                type.type(yellow("--- Night Destinations ---"))
                print()
                for i, (area_name, _) in enumerate(adventure_areas):
                    type.type(str(adventure_start + i + 1) + ". Drive to " + area_name)
                    time.sleep(0.5)
                    print()
            
            # Stay Home option
            stay_home_num = len(shops) + len(adventure_areas) + 1
            type.type(str(stay_home_num) + ". Stay Home")
            time.sleep(0.5)
            print()
            
            type.type("Choose a number: ")
            total_choices = len(shops) + len(adventure_areas) + 1
            
            while True:
                while choice is None:
                    try:
                        choice = int(input())
                    except ValueError:
                        type.type("Choose a number: ")
                if 1 <= choice <= len(shops):
                    shop = shops[choice-1]
                    break
                elif len(shops) < choice <= len(shops) + len(adventure_areas):
                    # Player chose an adventure area
                    area_index = choice - len(shops) - 1
                    area_name, area_func = adventure_areas[area_index]
                    type.type("You fire up the wagon and head for " + area_name + ".")
                    print("\n")
                    adventure = getattr(self, area_func)
                    adventure()
                    self.update_rank()
                    self.start_night()
                    return
                elif choice == stay_home_num:
                    shop = "Home"
                    break
                else:
                    choice = None
                    type.type("That number's not a choice!")
                    print()
                    type.type("Choose a number: ")
            print()

            if shop == "Doctor's Office": self.visit_doctor()
            elif shop == "Witch Doctor's Tower": self.visit_witch_doctor()
            elif shop == "Trusty Tom's Trucks and Tires": self.visit_tom()
            elif shop == "Filthy Frank's Flawless Fixtures": self.visit_frank()
            elif shop == "Oswald's Optimal Outoparts": self.visit_oswald()
            elif shop == "Convenience Store": self.visit_convenience_store()
            elif shop == "Marvin's Mystical Merchandise": self.visit_marvin()
            elif shop == "Grimy Gus's Pawn Emporium": self.visit_pawn_shop()
            elif shop == "Airport": self.visit_airport()
            elif shop == "Make a Phone Call": self.visit_phone_call()
            else: self.night_event()
            
        else:
            self.night_event()

    #Doctor's Office Interaction    
    def visit_doctor(self):
        type.type("You get in your car and drive to the Doctor's Office. ")
        if not self.has_met("Doctor's Office"):
            self.meet("Doctor's Office")
            type.type("As you pull up closer to the bright blue building, you notice that the parking lot is concerningly empty. You park your wagon right up front next to the entrance, and step out towards the doors. ")
            print("\n")
            type.type("When you enter into the lobby, you're immediately hit with the strong smell of hand sanitizer in the air. The carpets are dull and brown, the light above you is flickering, and the walls are filled with posters telling you to 'Floss More Often!' and 'Wash Your Hands Before You Eat!' ")
            type.type("If you didn't know any better, you would have guessed you were on a movie set.")
            print("\n")
            type.type("Walking towards the front desk, you see a cheery old lady, who looks up from her computer to smile at you. Her gray hair covers her glasses, and her hand trembles as she hands you a pen and a clipboard with some paperwork. Of course it's paperwork.")
            print("\n")
            type.type("After filling out your information, you walk back to the front desk, and hand the lady the clipboard. She smiles, and begins to speak to you.")
        print("\n")
        type.type("I see you're here for a checkup. The Doctor will see you now.")
        print("\n")
        type.type("Hey there champ! How are you? Doing all right? Let's check you out and make sure you're all up to snuff.")
        print()
        if (self.len_status() == 0) and (self.__health == 100):
            type.type("Why, you look just as healthy as the day I met you, fresh from your mother's womb! Let me just give you this lollipop and you'll be free to go.")
        elif (self.len_status() == 0):
            type.type("Why, you don't seem to really need my help. You appear a little worse for wear, but this medicine should do the trick.")
            print("\n")
        else:
            self.__clear_status = True
            if self.has_status("Spider Bite"):
                type.type("I see you have a nasty spider bite. That thing looks gross. Let me get that cleaned up for you.")
                print()
            print()
            type.type("Well, that seems to be everything. You still appear a little worse for wear, but this medicine should do the trick.")
        print("\n")
        self.heal(100)
        self.restore_sanity(random.choice([1, 2, 3]))  # Restores sanity
        type.type("You walk back to the front desk to checkout.")
        print("\n")
        cost = int((random.randint(65, 90)/100)*self.__balance)
        type.type("That will be " + bright(green("${:,}".format(cost))))
        if self.has_item("Faulty Insurance"):
            print("\n")
            type.type("You show off your " + bright(magenta("Faulty Insurance")) + " to the lady, and put a convincing smile on your face. ")
            random_chance = random.randrange(10)
            if random_chance < 2:
                self.add_danger("Doctor Ban")
                print("\n")
                self.use_item("Faulty Insurance")
                type.type("Is this supposed to fool me? A fake insurance card? That's it, I'm calling the cops!")
                print("\n")
                type.type("Without hesitation, you turn, and run far, far away from the hospital, knowing that your face can't be seen there again.")
                print("\n")
                self.start_night()
                return
            else:
                print("\n")
                type.type("I see, you have insurance. Well, that should give you quite the discount.")
                print()
                cost = int((random.randint(10, 35)/100)*self.__balance)
                type.type("That will be " + bright(green("${:,}".format(cost))))
                self.change_balance(-cost)
                self.update_faulty_insurance_durability()
                self.start_night()
                return
        else:
            self.change_balance(-cost)
            self.start_night()
            return


    # Witch Doctor's shop and interactions
    def visit_witch_doctor(self):
        potions = self.__lists.make_witch_inventory()
        type.type("You get in your car and drive to the Witch Doctor's Tower. ")
        print("\n")
        type.type("Muahahahahaha, hahahahahaha, HAHAHAHAHA!")
        print()
        type.type("Would you like me to HEAL you, HUMAN? ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if((yes_or_no == "y") or (yes_or_no == "yes")):
                type.type("Now THATS what I LIKE to hear!")
                print("\n")
                type.type("You watch as the Witch goes from shelf to shelf, grabbing frog legs and horse hairs and bee carcasses, throwing them all into the black boiling pot. It begins to glow green, and the Witch looks pleased. ")
                print("\n")
                type.type("HAHAHAHAHA! DRINK this, my DEAR!")
                print("\n")
                type.type("You drink the strange concoction, and it burns in your stomach. Hopefully, it makes you feel better.")
                
                print("\n")

                random_chance = random.randrange(10)
                if random_chance < 5:
                    self.__clear_status = True
                elif random_chance == 5:
                    self.__clear_all_status = True

                random_chance = random.randrange(3)
                if random_chance == 0:
                    self.heal(100)
                
                cost = int((random.randint(5, 25)/100)*self.__balance)
                type.type("YOU owe ME some of your green BILLS! I THINK that " + bright(green("${:,}".format(cost))) + " would SUFFICE!")
                self.change_balance(-cost)
                if len(potions)==0:
                    type.type("SORRY FOR YOU, but I'm simply out of FLASKS. No FLASKS means no POTIONS. Maybe try COMING BACK another DAY!")
                    print("\n")
                    self.start_night()
                    return
                else:
                    type.type("NOW, while I have YOU here, care to PURCHASE any of my POWERFUL POTIONS?")
                break
            elif((yes_or_no == "n") or (yes_or_no == "no")):
                type.type("HAHAH-oh what? You don't want MY help? That's QUITE UNFORTUNATE!")
                print("\n")
                if len(potions)==0:
                    type.type("SORRY FOR YOU, but I'm simply out of FLASKS. No FLASKS means no POTIONS. Maybe try COMING BACK another DAY!")
                    print("\n")
                    self.start_night()
                    return
                else:
                    type.type("WELL, are YOU in the MOOD to spend some MONEY on my MAGIC POTIONS?")
                    break
            else:
                type.type("WHAT did you SAY? ")

        print()

        no_bust_price = 0
        imminent_blackjack_price = 0
        dealers_whispers_price = 0
        bonus_fortune_price = 0
        antivenom_price = 0
        antivirus_price = 0
        fortunate_day_price = 0
        fortunate_night_price = 0
        second_chance_price = 0
        split_serum_price = 0
        dealers_hesitation_price = 0
        pocket_aces_price = 0
        while(True):
            for i in range(len(potions)+1):
                if(i<len(potions)):
                    type.type(str(i+1) + ". Flask of " + potions[i])
                    time.sleep(0.5)
                    print()
                else:
                    type.type(str(i+1) + ". I'm not buying anything")
                    time.sleep(0.5)
                    print()

            if(self.len_flasks()==1):
                type.type("NOW, I'm not ONE to JUDGE, but MIXING potions can be RISKY BUSINESS. Don't BLAME ME if you feel SICK.")
                print()
            elif(self.len_flasks()==2):
                type.type("SO, you're TEETERING on DANGEROUS levels of potion in your BLOOD. Proceed with CAUTON.")
                print()
            elif(self.len_flasks()>=3):
                type.type("ANY additional POTIONS in YOUR SYSTEM is ENTIRELY YOUR DECISION, and A BAD ONE AT THAT BUT I'M NOT YOU. Just please don't DIE on my CARPETS.")
                print()
            type.type("CHOOSE a number: ")
            while True:
                choice = None
                while choice is None:
                    try:
                        choice = int(input())
                    except ValueError:
                        type.type("Choose A number: ")
                if(1<=choice<=len(potions)):
                    potion = potions[choice-1]
                    break
                elif choice==len(potions)+1:
                    potion = "Home"
                    break
                else:
                    choice = None
                    type.type("I DONT have that NUMBER!")
                    print()
                    type.type("Choose a NUMBER: ")

            print()

            if potion == "No Bust":
                type.type("AHHH, so YOU WANT the Flask of No Bust?")
                if no_bust_price == 0:
                    no_bust_price = random.choice([25000, 27000, 30000])
                price = no_bust_price
            elif potion == "Imminent Blackjack":
                type.type("I SEE, so YOU WANT the Flask of Imminent Blackjack?")
                if imminent_blackjack_price == 0:
                    imminent_blackjack_price = random.choice([40000, 45000, 50000])
            elif potion == "Dealer's Whispers":
                type.type("HAHAHA, so YOU WANT the Flask of Dealer's Whispers?")
                if dealers_whispers_price == 0:
                    dealers_whispers_price = random.choice([23000, 27000, 32000])
                price = dealers_whispers_price
            elif potion == "Bonus Fortune":
                type.type("OOOOOOOOHHH, so YOU WANT the Flask of Bonus Fortune?")
                if bonus_fortune_price == 0:
                    bonus_fortune_price = random.choice([35000, 42000, 45000])
                price = bonus_fortune_price
            elif potion == "Anti-Venom":
                type.type("OF COURSEEEE, YOU WANT the Flask of Anti-Venom?")
                if antivenom_price == 0:
                    antivenom_price = random.choice([25000, 26000, 27000])
                price = antivenom_price
            elif potion == "Anti-Virus":
                type.type("AH-HA, YOU WANT the Flask of Anti-Virus?")
                if antivirus_price == 0:
                    antivirus_price = random.choice([26000, 27000, 28000])
                price = antivirus_price
            elif potion == "Fortunate Day":
                type.type("HEHEHAHAIHEHIA, so YOU WANT the Flask of Fortunate Day?")
                if fortunate_day_price == 0:
                    fortunate_day_price = random.choice([12000, 13000, 18000])
                price = fortunate_day_price
            elif potion == "Fortunate Night":
                type.type("MUAHAHAHAHA, so YOU WANT the Flask of Fortunate Night?")
                if fortunate_night_price == 0:
                    fortunate_night_price = random.choice([12000, 15000, 20000])
                price = fortunate_night_price
            elif potion == "Second Chance":
                type.type("OHOHOHOHO, so YOU WANT the Flask of Second Chance?")
                if second_chance_price == 0:
                    second_chance_price = random.choice([28000, 32000, 36000])
                price = second_chance_price
            elif potion == "Split Serum":
                type.type("YESYESYES, so YOU WANT the Flask of Split Serum?")
                if split_serum_price == 0:
                    split_serum_price = random.choice([30000, 35000, 40000])
                price = split_serum_price
            elif potion == "Dealer's Hesitation":
                type.type("MUEHEHEHE, so YOU WANT the Flask of Dealer's Hesitation?")
                if dealers_hesitation_price == 0:
                    dealers_hesitation_price = random.choice([20000, 24000, 28000])
                price = dealers_hesitation_price
            elif potion == "Pocket Aces":
                type.type("OOOOOH LALA, so YOU WANT the Flask of Pocket Aces?")
                if pocket_aces_price == 0:
                    pocket_aces_price = random.choice([45000, 50000, 55000])
                price = pocket_aces_price
            else: 
                type.type("Then OUR BUSINESS has been SETTLED. Be GONE. GOODBYE! COME AGAIN!")
                print("\n")
                self.start_night()
                return

            print()

            type.type("I SUPPOSE I can PART WAYS with THIS for " + green(bright("${:,}".format(price))) + ". What do YOU think? ")
            
            while True:
                yes_or_no = input("").lower()
                if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self.__balance<price):
                    print()
                    type.type("YOUR WALLETS are far too SMALL for this TRANSACTION.")
                    print("\n")
                    type.type("PERHAPS one of the OTHER potions?")
                    break
                elif (yes_or_no == "y") or (yes_or_no == "yes"):
                    print()
                    type.type("HAHAHAHAHAHAHAHAHA! YES! YES!")
                    self.change_balance(-price)
                    self.add_flask(potion)
                    potions.pop(choice-1)
                    type.type("You got the " + magenta(bright("Flask of " + potion)) + "!")
                    print()
                    type.type("Description: " + self.get_item_desc(potion))
                    print("\n")
                    if(self.len_flasks()==1):
                        type.type("You chug the potion, and begin to feel warm inside.")
                        print("\n")
                    elif(self.len_flasks()==2):
                        type.type("You chug the potion, and feel a bit dizzy. Maybe no more potions.")
                        print("\n")
                    elif(self.len_flasks()>=3):
                        type.type("You chug the potion, and feel really, really awful.")
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            self.__flask_effects = set()
                            print("\n")
                            type.type("You stumble back and forth, on the verge of fainting. You puke all over the floor.")
                            print("\n")
                            type.type("NOOOO, NOT ON THE CARPETS! WHAT did I SAY! NO MORE. NO MORE. YOU are DONE for TODAY. OUT, NOW.")
                            print("\n")
                            type.type("As you walk out, you feel your body begin to weaken. After all that, it seems the potions you had injested are now laying in a puddle on the floor of the Witch Doctor's tower. ")
                            print("\n")
                            self.start_night()
                            return
                        
                        damage = random.choice([10, 12, 15, 20, 30, 40])
                        if damage >= self.__health:
                            print("\n")
                            type.slow(red("Your vision starts turning red, then green, then purple. "))
                            type.slow(red("Panicking, you run around the room, desperate to find an antidote. "))
                            type.slow(red("You begin drinking potion, after potion, to no avail. "))
                            type.slow(red("You can hear the Witch cackling in the background of your ringing ears, and slowly, you fall to the ground. "))
                            type.slow(red("Your face rests on the soft carpet. It's so cozy. Too cosy. "))
                            type.slow(red("Is that God? Yes, I think I can hear him! God! God! "))
                            type.slow(red("My goodness, he's real! God begins to decend from the roof hundreds of feet above you, and as he slowly glides down the tower, "))
                            type.slow(red("you get a closer look at his figure. A golden ring surrounds his body, and his white cloak is long and elegant. "))
                            print("\n")
                            type.slow(red(bright("As God decends, he looks you in the eyes, and you watch his face melt in front of you, his skin dripping onto your skin. ")))
                            type.slow(red(bright("It burns, and all you can do is sit with the pain and agony as your body slowly shuts down.")))
                            self.kill()
                        else:
                            print("\n")
                            self.hurt(damage)
                            self.lose_sanity(random.choice([4, 5, 6]))  # Potion-induced hallucinations drain sanity

                    if len(potions)==0:
                        type.type("YOU bought EVERYTHING! How EXCITING! I suppose we're DONE exchanging GOODS! GOODBYE NOW!")
                        print("\n")
                        self.start_night()
                        return
                    else:
                        type.type("OOOOH YES! Capitalism is FUN! I WANT MORE! MORE!")
                        print()
                    break
                elif (yes_or_no == "n") or (yes_or_no == "no"):
                    print()
                    type.type("OK OK I see how IT IS! ")
                    print("\n")
                    type.type("PERHAPS a DIFFERENT potion?")
                    print()
                    break
                else:
                    print()
                    type.type("GIVE me an ANSWER! ")


    # Tom's shop and interactions
    def tom_dialogue(self):
        if self.__mechanic_visits == 0:
            type.type(quote("Well howdy there, stranger! Name's Tom. Welcome to Tom's Trusty Trucks and Tires!"))
            print("\n")
            type.type("The old mechanic wipes his hands on a rag that's seen better days. His eyes are kind, but tired. The kind of tired that comes from years of hard work and harder choices.")
            print("\n")
            type.type(quote("You got the look of a man runnin' from somethin'. I seen it before. Hell, I been there myself."))
            print("\n")
            type.type("He gestures to a faded photograph on the wall. A younger Tom, standing with a woman and two small children.")
            print("\n")
            type.type(quote("Family's a funny thing, yunno? You don't realize what you got 'til it's gone. Spent years chasin' money, chasin' dreams. Almost lost everything that mattered."))
            print("\n")
            type.type("He taps the photo frame with a calloused finger.")
            print("\n")
            type.type(quote("But it ain't never too late to go back. That's what I learned. It ain't never too late to pick up the phone and say sorry."))
            print("\n")
            type.type("He looks at you with something like recognition.")
            print("\n")
            type.type(quote("Anyway. What can I do for ya today?"))
        elif self.__mechanic_visits == 1:
            type.type(quote("Hey there! Good to see ya again. You stayin' outta trouble?"))
            print("\n")
            type.type("Tom chuckles, but there's concern in his eyes.")
            print("\n")
            type.type(quote("You know, I been meanin' to ask... you got anyone waitin' for ya back home? Someone who might be worryin'?"))
        elif self.__mechanic_visits == 2:
            type.type(quote("There he is! My favorite customer!"))
            print("\n")
            type.type("Tom's smile fades slightly as he looks at you.")
            print("\n")
            type.type(quote("You look tired, friend. Real tired. You been sleepin' alright? Eatin'?"))
            print("\n")
            type.type("He shakes his head.")
            print("\n")
            type.type(quote("I worry about you, yunno. Reminds me of myself, back when I was lost. Just... don't forget what's important, alright?"))
        elif self.__mechanic_visits >= 3:
            type.type(quote("Welcome back, friend."))
            print("\n")
            type.type("Tom's voice is softer now. More serious.")
            print("\n")
            type.type(quote("Listen... I found somethin' the other day. A phone. Fell outta your car when you was here last. Someone's been callin' it. A lot."))
            print("\n")
            type.type("He looks at you with those tired, kind eyes.")
            print("\n")
            type.type(quote("I ain't one to pry, but... whoever's callin', they sound real worried. Real sad. Maybe you should think about pickin' up."))

    def visit_tom(self):
        days_elapsed = self.get_days_elapsed("Mechanic")
        self.mark_day("Mechanic")
        type.type("You get in your car and drive to Tom's Trusty Trucks and Tires. ")
        print("\n")
        self.tom_dialogue()
        print("\n")
        repairing_items_len = len(self.__repairing_inventory)
        if(repairing_items_len>0):
            if days_elapsed == 3:
                type.type("You've been gone a while. Honestly, I forgot about ya stuff. Just come back soon, and I'll get to it.")
                print("\n")
            else:
                type.type("You left me some items to fix up since I last saw you. Here's the rundown:")
                print("\n")
                repairing_items = self.__lists.make_repairing_items_list()
                for item in repairing_items:
                    if item == "Delight Indicator":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I managed to get this Delight Indicator up and running for ya. Just took a few new wires.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Health Indicator":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I somehow managed to get this Health Indicator workin'. Just took a few new screws.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Dirty Old Hat":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("This Dirty Old Hat has never looked cleaner! If that's what you want, at least.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Golden Watch":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I put new gears in your Golden Watch. Should tell the time now.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Faulty Insurance":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("Against my better judgement, I touched up your Faulty Insurance card. If it'll work, well, my guess is as good as yours.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Sneaky Peeky Shades":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I replaced the frame in your Sneaky Peeky Shades, so now you can see out of them.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                    elif item == "Quiet Sneakers":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I relaced these Quiet Sneakers, so you can run again.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                    elif item == "Lucky Coin":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("Gave this Lucky Coin a good polish. She's shining bright again!")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Worn Gloves":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I patched up these Worn Gloves with some spare leather I had lyin' around.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                    elif item == "Tattered Cloak":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("My wife sewed up all the holes in your Tattered Cloak. Good as new, yunno!")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Rusty Compass":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I oiled up this Rusty Compass and replaced the glass. Points north again!")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Pocket Watch":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I tinkered with your Pocket Watch and got all the gears turnin' again.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")

                if len(self.__repairing_inventory) == repairing_items_len:
                    type.type("Yesterday was a long one, and I retired to home early to see my wife and the girlies. Didn't get much progress on your things, but I assure you, they'll be fixed before you know it.")
                elif len(self.__repairing_inventory) > 1:
                    type.type("I've still got " + str(len(self.__repairing_inventory)) + " items of yours that I'm still looking at. Just swing by tomorrow, and hopefully I'll have them done.")
                elif len(self.__repairing_inventory) == 1:
                    type.type("I've still got " + str(len(self.__repairing_inventory)) + " item of yours that I'm still looking at. Just swing by tomorrow, and hopefully I'll have it done.")
                elif len(self.__repairing_inventory) == 0:
                    type.type("That should be everything you left with me. Hopefully everything's up to snuff and good as new, ya know!")
                print("\n")

        if(len(self.__broken_inventory)>0):
            broken_items = self.__lists.make_broken_items_list()
            delight_indicator_price = 0
            health_indicator_price = 0
            dirty_old_hat_price = 0
            golden_watch_price = 0
            faulty_insurance_price = 0
            sneaky_peeky_glasses_price = 0
            quiet_sneakers_price = 0
            lucky_coin_price = 0
            worn_gloves_price = 0
            tattered_cloak_price = 0
            rusty_compass_price = 0
            pocket_watch_price = 0
            type.type("I see you came in here with some broken valuables. Mind if I take a look at em?")
            print()
            while(True):
                for i in range(len(broken_items)+1):
                    if(i<len(broken_items)):
                        type.type(str(i+1) + ". " + broken_items[i])
                        time.sleep(0.5)
                        print()
                    else:
                        type.type(str(i+1) + ". I'm all set")
                        time.sleep(0.5)
                        print()
                type.type("Choose a number: ")
                while True:
                    choice = None
                    while choice is None:
                        try:
                            choice = int(input())
                        except ValueError:
                            type.type("Choose a number: ")
                    if(1<=choice<=len(broken_items)):
                        item = broken_items[choice-1]
                        break
                    elif choice==len(broken_items)+1:
                        item = "Home"
                        break
                    else:
                        choice = None
                        type.type("You don't have an item with that number!")
                        print()
                        type.type("Choose a number: ")

                print()

                if item == "Delight Indicator":
                    type.type("You want me to fix that Delight Indicator of yours?")
                    if delight_indicator_price == 0:
                        delight_indicator_price = random.choice([4500, 5500, 6000])
                    price = delight_indicator_price
                elif item == "Health Indicator":
                    type.type("You want me to fix that Health Indicator for ya?")
                    if health_indicator_price == 0:
                        health_indicator_price = random.choice([4000, 4500, 5500])
                    price = health_indicator_price
                elif item == "Dirty Old Hat":
                    type.type("You want me to fix that Dirty Old Hat you got there?")
                    if dirty_old_hat_price == 0:
                        dirty_old_hat_price = random.choice([12500, 14000, 15000])
                    price = dirty_old_hat_price
                elif item == "Golden Watch":
                    type.type("You want me to fix that Golden Watch you're wearin'?")
                    if golden_watch_price == 0:
                        golden_watch_price = random.choice([15000, 16000, 17500])
                    price = golden_watch_price
                elif item == "Faulty Insurance":
                    type.type("Uhm, you want me to fix your Faulty Insurance card?")
                    if faulty_insurance_price == 0:
                        faulty_insurance_price = random.choice([5000, 5500, 6000])
                    price = faulty_insurance_price
                elif item == "Sneaky Peeky Shades":
                    type.type("You want me to fix those Sneaky Peeky Shades on your head?")
                    if sneaky_peeky_glasses_price == 0:
                        sneaky_peeky_glasses_price = random.choice([17000, 18000, 20000])
                    price = sneaky_peeky_glasses_price
                elif item == "Quiet Sneakers":
                    type.type("You want me to fix them there Quiet Sneakers you're rockin'?")
                    if quiet_sneakers_price == 0:
                       quiet_sneakers_price = random.choice([7500, 9000, 10000])
                    price = quiet_sneakers_price
                elif item == "Lucky Coin":
                    type.type("You want me to fix that Lucky Coin of yours?")
                    if lucky_coin_price == 0:
                        lucky_coin_price = random.choice([6000, 7000, 8000])
                    price = lucky_coin_price
                elif item == "Worn Gloves":
                    type.type("You want me to fix them Worn Gloves you got?")
                    if worn_gloves_price == 0:
                        worn_gloves_price = random.choice([9000, 10000, 11000])
                    price = worn_gloves_price
                elif item == "Tattered Cloak":
                    type.type("You want me to fix that Tattered Cloak of yours?")
                    if tattered_cloak_price == 0:
                        tattered_cloak_price = random.choice([11000, 12500, 14000])
                    price = tattered_cloak_price
                elif item == "Rusty Compass":
                    type.type("You want me to fix that Rusty Compass you're carryin'?")
                    if rusty_compass_price == 0:
                        rusty_compass_price = random.choice([4000, 5000, 6000])
                    price = rusty_compass_price
                elif item == "Pocket Watch":
                    type.type("You want me to fix that Pocket Watch of yours?")
                    if pocket_watch_price == 0:
                        pocket_watch_price = random.choice([10000, 11500, 13000])
                    price = pocket_watch_price
                else: 
                    type.type("Well then, I hope you have a great rest of your night. Stay safe now.")
                    print("\n")
                    self.start_night()
                    return

                print()

                type.type("It'll take me a couple days, but I can do that for ya for " + green(bright("${:,}".format(price))) + ". Whaddya say? ")
                
                while True:
                    yes_or_no = input("").lower()
                    if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self.__balance<price):
                        print()
                        type.type("Aww man, sorry to tell you, but you just don't got enough funds for this, yunno?")
                        print("\n")
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("Ugh, man, I just hate seein' people in need of help and not gettin' it, ya hear? ")
                            type.type("Tell ya what, limited time offer, I'm giving out a special discount, just for you. ")
                            discount = random.choice([20, 25, 30, 35])
                            price = int(price - (price*(discount/100)))
                            type.type("Say yes right now, and I'll take " + str(discount) + "%" + " off your order.")
                            print("\n")
                            type.type("That means you're only payin' " + green(bright("${:,}".format(price))) + ". Could ya do that? ")

                            while True:
                                yes_or_no_2 = input("").lower()
                                if ((yes_or_no_2 == "y") or (yes_or_no_2 == "yes")) and (self.__balance<price):
                                    print()
                                    type.type("Still can't afford it? That's tough luck, man. I really wish there was more I could do, ya know?")
                                    print("\n")
                                    type.type("Maybe you can fix up something else.")
                                    print()
                                    break
                                elif (yes_or_no == "y") or (yes_or_no == "yes"):
                                    print()
                                    type.type("Really? Awesome. Just leave this here with me, and let me wrench that baby back to life for ya.")
                                    self.change_balance(-price)
                                    self.repair_item(item)
                                    broken_items.pop(choice-1)
                                    type.type("Your " + magenta(bright(item)) + " is safe with Tom. Come back later to see if it's fixed!")
                                    print("\n")
                                    if len(broken_items)==0:
                                        type.type("Well, that appears to be everything, doesn't it? Thanks for letting me help ya out. Have a nice day, now.")
                                        print("\n")
                                        self.start_night()
                                        return
                                    else:
                                        type.type("Got anything else for me?")
                                        print()
                                        break
                                elif (yes_or_no_2 == "n") or (yes_or_no_2 == "no"):
                                    type.type("Really? Even with the discount? You do you, I suppose.")
                                    print("\n")
                                    type.type("Is there anything else I can fix for ya?")
                                    print()
                                    break
                                else:
                                    print()
                                    type.type("Couldn't hear ya. Whaddya say? ")
                            break
                        else:
                            broken_items.pop(choice-1)
                            type.type("Maybe you can afford to fix up somethin' else?")
                            print()
                        break
                    elif (yes_or_no == "y") or (yes_or_no == "yes"):
                        print()
                        type.type("Really? Awesome. Just leave this here with me, and let me wrench that baby back to life for ya.")
                        self.change_balance(-price)
                        self.repair_item(item)
                        broken_items.pop(choice-1)
                        type.type("Your " + magenta(bright(item)) + " is safe with Tom. Come back later to see if it's fixed!")
                        print("\n")
                        if len(broken_items)==0:
                            type.type("Well, that appears to be everything, doesn't it? Thanks for letting me help ya out. Have a nice day, now.")
                            print("\n")
                            self.start_night()
                            return
                        else:
                            type.type("Got anything else for me?")
                            print()
                        break
                    elif (yes_or_no == "n") or (yes_or_no == "no"):
                        print()
                        type.type("No dice? ")
                        random_chance = random.randrange(10)
                        if random_chance == 0:
                            type.type("You don't say. I mean, my prices are unbeatable. You know what, I'll prove it!")
                            print("\n")
                            type.type("Tell ya what, limited time offer, I'm giving out a special discount, just for you. ")
                            discount = random.choice([15, 20, 25])
                            price = int(price - (price*(discount/100)))
                            type.type("Say yes right now, and I'll take " + str(discount) + "%" + " off your order.")
                            print("\n")
                            type.type("That means you're only payin' " + green(bright("${:,}".format(price))) + ". You interested? ")
                            while True:
                                yes_or_no_2 = input("").lower()
                                if ((yes_or_no_2 == "y") or (yes_or_no_2 == "yes")) and (self.__balance<price):
                                    print()
                                    type.type("You can't afford it? Really? That's tough luck, man. I really wish there was more I could do, ya know?")
                                    print("\n")
                                    type.type("Maybe you can fix up something else.")
                                    print()
                                    break
                                elif (yes_or_no_2 == "y") or (yes_or_no_2 == "yes"):
                                    print()
                                    type.type("Really? Awesome. Just leave this here with me, and let me wrench that baby back to life for ya.")
                                    self.change_balance(-price)
                                    self.repair_item(item)
                                    broken_items.pop(choice-1)
                                    type.type("Your " + magenta(bright(item)) + " is safe with Tom. Come back later to see if it's fixed!")
                                    print("\n")
                                    if len(broken_items)==0:
                                        type.type("Well, that appears to be everything, doesn't it? Thanks for letting me help ya out. Have a nice day, now.")
                                        print("\n")
                                        self.start_night()
                                        return
                                    else:
                                        type.type("Got anything else for me?")
                                        print()
                                        break
                                elif (yes_or_no_2 == "n") or (yes_or_no_2 == "no"):
                                    type.type("Really? No interest, whatsoever? Even with the discount? You do you, I suppose.")
                                    print("\n")
                                    type.type("Want me to fix anything else?")
                                    print()
                                    break
                                else:
                                    print()
                                    type.type("Couldn't hear ya. Whaddya say? ")
                            break
                        else:
                            type.type("That's alright, now.")
                            print("\n")
                            type.type("What about your other wares?")
                            print()
                            break
                    else:
                        print()
                        type.type("Couldn't hear ya. Whaddya say? ")

        self.start_night()
        return



    # Frank's shop and interactions
    def frank_dialogue(self):
        if self.__mechanic_visits == 0:
            type.type(quote("The hell you want?"))
            print("\n")
            type.type("The man behind the counter doesn't look up from his newspaper. He's got tattoos crawling up his arms - some faded, some fresh. You catch a glimpse of something that looks like lightning bolts before he shifts his sleeve.")
            print("\n")
            type.type(quote("Name's Frank. This is my shop. My rules. You want somethin' fixed, I'll fix it. You want conversation, go find a therapist."))
            print("\n")
            type.type("He finally looks at you. His eyes are cold. Calculating.")
            print("\n")
            type.type(quote("You ain't from around here, are ya? Nah, I can tell. Got that look. The 'I'm just passin' through' look."))
            print("\n")
            type.type("He spits into a cup on the counter.")
            print("\n")
            type.type(quote("Well, long as you're passin' through MY town, you follow MY rules. We got a way of doin' things here. A way of keepin' things... pure. Clean. You understand what I'm sayin'?"))
            print("\n")
            type.type("He doesn't wait for an answer.")
            print("\n")
            type.type(quote("That casino up on the hill. You been there, right? 'Course you have. Everyone goes there eventually. That glass-eyed freak runnin' the place... he ain't one of us. Never will be. Came here from God knows where, settin' up shop like he owns the place."))
            print("\n")
            type.type("Frank's jaw tightens.")
            print("\n")
            type.type(quote("One of these days, someone's gonna do somethin' about him. Someone's gonna remind him that this is OUR town."))
            print("\n")
            type.type("He waves his hand dismissively.")
            print("\n")
            type.type(quote("Anyway. What do you need?"))
        elif self.__mechanic_visits == 1:
            type.type(quote("Oh, it's you again."))
            print("\n")
            type.type("Frank barely acknowledges you. In the back of the shop, you hear voices. Laughter. The rumble of motorcycle engines.")
            print("\n")
            type.type(quote("Got some friends over. Business associates, you might say. We're plannin' somethin' big."))
            print("\n")
            type.type("He grins. It's not a nice grin.")
            print("\n")
            type.type(quote("You keep comin' around, maybe I'll introduce you. Could always use another pair of hands. Another... believer."))
        elif self.__mechanic_visits == 2:
            type.type(quote("Back again, huh? You're persistent, I'll give you that."))
            print("\n")
            type.type("Frank's watching you more carefully now. Like he's sizing you up.")
            print("\n")
            type.type(quote("You know, I been thinkin'. You and me, we ain't so different. We both know what it's like to be overlooked. To be treated like shit by people who think they're better than us."))
            print("\n")
            type.type("He leans in closer. His breath smells like cigarettes and something sour.")
            print("\n")
            type.type(quote("The Dealer. He looks at you like you're nothin'. Like you're just another mark, another sucker to bleed dry. Don't that make you angry? Don't that make you want to DO somethin' about it?"))
        elif self.__mechanic_visits >= 3:
            type.type(quote("Well, well, well. Look who keeps crawlin' back."))
            print("\n")
            type.type("Frank's demeanor has changed. He's more confident. More dangerous.")
            print("\n")
            type.type(quote("You know, I been watchin' you. Talkin' to the boys about you. We think you got potential."))
            print("\n")
            type.type("He pulls out a worn leather jacket from under the counter. You can see patches on it. Symbols that make your stomach turn.")
            print("\n")
            type.type(quote("When you're ready to stop bein' a victim and start bein' a winner, you come find me. We'll take care of that Dealer problem once and for all."))
            print("\n")
            type.type("He tosses the jacket back under the counter.")
            print("\n")
            type.type(quote("Think about it."))

    def visit_frank(self):
        days_elapsed = self.get_days_elapsed("Mechanic")
        self.mark_day("Mechanic")
        type.type("You get in your car and drive to Filthy Frank's Flawless Fixtures. ")
        print("\n")
        self.frank_dialogue()
        print("\n")
        repairing_items_len = len(self.__repairing_inventory)
        if(repairing_items_len>0):
            if days_elapsed == 2:
                type.type("You didn't show up yesterday. That means I haven't looked at your stuff. Come back soon, and maybe I will have made some progress, yeah?")
                print("\n")
            else:
                type.type("You left me some of your trinkets. This is what I've got for you:")
                print("\n")
                repairing_items = self.__lists.make_repairing_items_list()
                for item in repairing_items:
                    if item == "Delight Indicator":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("With a couple new wires I got your Delight Indicator working.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("Honestly, after one look at this Delight Indicator thingy, I gave up entirely. Take it back. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Health Indicator":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("Tighted some screws and the Health Indicator started up again. Seems good? Just take it.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("Get that the fuck out my face with that fancy wizard crap. This Health Indicator thing is too complicated. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Dirty Old Hat":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("I gave this Dirty Old Hat to my wife, and after enough convincing, she sewed it back up.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("You gave me a Dirty Old Hat and asked me to fix it. What did you expect? No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Golden Watch":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("All I had to do was tap the watch face with my finger and it started ticking again, so I'd say that's a job well done.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I looked at the watch, spun all the gears and clicked all the buttons, but nothing worked. Sorry dude. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Faulty Insurance":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("My guy was around last night, and he looked at your Faulty Insurance card. Should work again.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I've been calling my guy, but he won't answer. I can't fix your Faulty Insurance card. Take it back. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Sneaky Peeky Shades":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("A little mouth water vapor and my shirt was more than enough to polish up the Sneaky Peeky Shades you gave me.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I ain't no opotometigist. These Sneaky Peeky Shades, well, they are glasses. I fix cars. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(("Your broken " + red(bright(item)) + " have been returned."))
                            print("\n")
                    elif item == "Quiet Sneakers":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("I gave your Quiet Sneakers to my son Kyle, and ran around the yard all day yesterday. Should've broken them in for ya.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("These Quiet Sneakers reek like hell. Please take them. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " have been returned."))
                            print("\n")
                    elif item == "Lucky Coin":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("I let Kyle use your Lucky Coin for his piggy bank for a bit. He cried when I took it back. You're welcome.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I tried flipping this Lucky Coin and it landed in a storm drain. Fished it out but now it smells like sewer. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Worn Gloves":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("I been using these Worn Gloves to change oil all week. They're real broken in now. Might smell a little funky.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I ain't no seamstress. These Worn Gloves got fingers falling off. That's a wife problem. She said no. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " have been returned."))
                            print("\n")
                    elif item == "Tattered Cloak":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("Kyle's been using your Tattered Cloak as a superhero cape. Duct taped the holes shut. Kid knows what he's doing.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("My dog got ahold of this Tattered Cloak and made it worse. Way worse. I'm not apologizing. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Rusty Compass":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("I dunked this Rusty Compass in a bucket of Coca-Cola overnight. Don't ask why it works, it just does.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("This Rusty Compass keeps pointing at my fridge. I think it's haunted. Get it outta here. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Pocket Watch":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("I smacked your Pocket Watch against the counter real hard and it started ticking again. That'll be full price.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I opened up this Pocket Watch and a bunch of tiny gears flew everywhere. Kyle vacuumed 'em up. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")

                if len(self.__repairing_inventory) == repairing_items_len:
                    type.type("I didn't fix a damn thing of yours, and I ain't afraid to show it. Look at this box. It has all the stuff you gave me. It hasn't moved since you gave me it. Now scram, hard work takes time.")
                elif len(self.__repairing_inventory) > 1:
                    type.type("That leaves " + str(len(self.__repairing_inventory)) + " items of yours still in my posession. Just swing by tomorrow, and I'll do my best to finish them up.")
                elif len(self.__repairing_inventory) == 1:
                    type.type("That leaves " + str(len(self.__repairing_inventory)) + " item of yours still in my posession. Just swing by tomorrow, and I'll do my best to finish it up.")
                elif len(self.__repairing_inventory) == 0:
                    type.type("That's all your junk, fixed better than the best. Enjoy it while it lasts.")
                print("\n")

        if(len(self.__broken_inventory)>0):
            broken_items = self.__lists.make_broken_items_list()
            delight_indicator_price = 0
            health_indicator_price = 0
            dirty_old_hat_price = 0
            golden_watch_price = 0
            faulty_insurance_price = 0
            sneaky_peeky_glasses_price = 0
            quiet_sneakers_price = 0
            lucky_coin_price = 0
            worn_gloves_price = 0
            tattered_cloak_price = 0
            rusty_compass_price = 0
            pocket_watch_price = 0
            type.type("You have some broken things for me. Come on, don't be shy. Let me take a whack at them.")
            print()
            while(True):
                for i in range(len(broken_items)+1):
                    if(i<len(broken_items)):
                        type.type(str(i+1) + ". " + broken_items[i])
                        time.sleep(0.5)
                        print()
                    else:
                        type.type(str(i+1) + ". I'm all set")
                        time.sleep(0.5)
                        print()
                type.type("Choose a number: ")
                while True:
                    choice = None
                    while choice is None:
                        try:
                            choice = int(input())
                        except ValueError:
                            type.type("Choose a number: ")
                    if(1<=choice<=len(broken_items)):
                        item = broken_items[choice-1]
                        break
                    elif choice==len(broken_items)+1:
                        item = "Home"
                        break
                    else:
                        choice = None
                        type.type("Did I stutter?")
                        print()
                        type.type("Choose a number: ")

                print()

                if item == "Delight Indicator":
                    type.type("You need me to repair your Delight Indicator?")
                    if delight_indicator_price == 0:
                        delight_indicator_price = random.choice([4000, 4250, 4500, 5500, 6000, 9000])
                    price = delight_indicator_price
                elif item == "Health Indicator":
                    type.type("You need me to repair that Health Indicator?")
                    if health_indicator_price == 0:
                        health_indicator_price = random.choice([3000, 3200, 4000, 4500, 5500, 7000])
                    price = health_indicator_price
                elif item == "Dirty Old Hat":
                    type.type("You need me to repair the Dirty Old Hat you have?")
                    if dirty_old_hat_price == 0:
                        dirty_old_hat_price = random.choice([10000, 10500, 12500, 14000, 15000, 17000])
                    price = dirty_old_hat_price
                elif item == "Golden Watch":
                    type.type("You need me to repair that Golden Watch on your wrist?")
                    if golden_watch_price == 0:
                        golden_watch_price = random.choice([13000, 14000, 15000, 16000, 17500, 19500])
                    price = golden_watch_price
                elif item == "Faulty Insurance":
                    type.type("You need me to touch up your Faulty Insurance card?")
                    if faulty_insurance_price == 0:
                        faulty_insurance_price = random.choice([3500, 4000, 5000, 5500, 6000, 7000])
                    price = faulty_insurance_price
                elif item == "Sneaky Peeky Shades":
                    type.type("You need me to repair those Sneaky Peeky Shades over your eyes?")
                    if sneaky_peeky_glasses_price == 0:
                        sneaky_peeky_glasses_price = random.choice([15500, 16500, 17000, 18000, 20000, 25000])
                    price = sneaky_peeky_glasses_price
                elif item == "Quiet Sneakers":
                    type.type("You need me to repair those Quiet Sneakers you're wearing?")
                    if quiet_sneakers_price == 0:
                       quiet_sneakers_price = random.choice([6000, 6500, 7500, 9000, 10000, 12000])
                    price = quiet_sneakers_price
                elif item == "Lucky Coin":
                    type.type("You need me to buff out that Lucky Coin?")
                    if lucky_coin_price == 0:
                        lucky_coin_price = random.choice([5000, 5500, 6000, 7000, 8000, 10000])
                    price = lucky_coin_price
                elif item == "Worn Gloves":
                    type.type("You need me to patch up those Worn Gloves?")
                    if worn_gloves_price == 0:
                        worn_gloves_price = random.choice([7500, 8000, 9000, 10000, 11000, 13000])
                    price = worn_gloves_price
                elif item == "Tattered Cloak":
                    type.type("You need me to stitch up that Tattered Cloak?")
                    if tattered_cloak_price == 0:
                        tattered_cloak_price = random.choice([9000, 10000, 11000, 12500, 14000, 16000])
                    price = tattered_cloak_price
                elif item == "Rusty Compass":
                    type.type("You need me to oil up that Rusty Compass?")
                    if rusty_compass_price == 0:
                        rusty_compass_price = random.choice([3000, 3500, 4000, 5000, 6000, 7500])
                    price = rusty_compass_price
                elif item == "Pocket Watch":
                    type.type("You need me to tinker with that Pocket Watch?")
                    if pocket_watch_price == 0:
                        pocket_watch_price = random.choice([8500, 9000, 10000, 11500, 13000, 15000])
                    price = pocket_watch_price
                else: 
                    type.type("Well then I've done all I can do. Stay out of trouble, now.")
                    print("\n")
                    self.start_night()
                    return
                
                print()

                type.type("I can fix this up for like " + green(bright("${:,}".format(price))) + ". You game? ")
                
                while True:
                    yes_or_no = input("").lower()
                    if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self.__balance<price):
                        print()
                        type.type("Are you tryna rip me off? Nah man, I'm just kidding. But seriously, don't mess with me like that.")
                        print("\n")
                        broken_items.pop(choice-1)
                        type.type("Am I repairing something for you or what?")
                        break
                    elif (yes_or_no == "y") or (yes_or_no == "yes"):
                        print()
                        type.type("Darn tootin! Lemme just take this from you, and sooner or later I'll wield my hammer and do my thing.")
                        self.change_balance(-price)
                        self.repair_item(item)
                        broken_items.pop(choice-1)
                        type.type("Your " + magenta(bright(item)) + " is in Frank's possession. Come back tomorrow to see if it's fixed!")
                        print("\n")
                        if len(broken_items)==0:
                            type.type("Well I'd say that's all you've got that I could fix. Just check in tomorrow and hopefully it'll be to your liking.")
                            print("\n")
                            self.start_night()
                            return
                        else:
                            type.type("Got anything else I can repair?")
                            print()
                        break
                    elif (yes_or_no == "n") or (yes_or_no == "no"):
                        print()
                        type.type("What?! Why'd you ask, then. God, that's just annoying. You bug me sometimes, man.")
                        print("\n")
                        type.type("Anything you actually want me to repair?")
                        print()
                        break
                    else:
                        print()
                        type.type("Speak up! You're mumbling. ")
        self.start_night()
        return



    # Oswald's shop and interactions
    def oswald_dialogue(self):
        if self.__mechanic_visits == 0:
            type.type(quote("Oh my! A customer! A real, live, breathing customer!"))
            print("\n")
            type.type("A man in an impeccably clean suit practically bounces toward you. His smile is so wide it looks painful. Behind him, a hulking figure in overalls works silently on a car engine.")
            print("\n")
            type.type(quote("Welcome, welcome, welcome to Oswald's Optimal Outoparts! I'm Oswald, and that magnificent specimen of mechanical mastery is Stuart. Say hello, Stuart!"))
            print("\n")
            type.type("Stuart grunts without looking up.")
            print("\n")
            type.type(quote("Isn't he wonderful? Best mechanic this side of anywhere! Of course, he wouldn't be where he is today without my business acumen. My entrepreneurial spirit! My VISION!"))
            print("\n")
            type.type("Oswald gestures grandly around the shop.")
            print("\n")
            type.type(quote("You see, I'm not just a mechanic. I'm a businessman! An investor! I see opportunity where others see obstacles. Why, just last week I was thinking about expanding into the entertainment industry. Casinos! Gambling! There's SO much money to be made!"))
            print("\n")
            type.type("His eyes glitter with something between excitement and obsession.")
            print("\n")
            type.type(quote("But enough about my brilliant plans! What can we do for you today, my new friend?"))
        elif self.__mechanic_visits == 1:
            type.type(quote("AH! You've returned! Splendid, simply splendid!"))
            print("\n")
            type.type("Oswald rushes over, practically vibrating with energy.")
            print("\n")
            type.type(quote("I've been doing some research since we last spoke. This gambling thing - it's FASCINATING. The mathematics! The psychology! The sheer volume of money changing hands!"))
            print("\n")
            type.type("He pulls out a notebook filled with calculations.")
            print("\n")
            type.type(quote("Did you know that casinos have an average profit margin of 15-25%? That's REMARKABLE! And it's all legal! All you need is the right location, the right equipment, and the right... person."))
            print("\n")
            type.type("He looks at you with unsettling intensity.")
            print("\n")
            type.type(quote("Someone who UNDERSTANDS the game. Someone with EXPERIENCE."))
        elif self.__mechanic_visits == 2:
            type.type(quote("My favorite gambler! How goes the card-slapping?"))
            print("\n")
            type.type("Oswald's smile is even wider today. Almost manic.")
            print("\n")
            type.type(quote("I've been making some calls. Talking to some investors. The casino idea is really taking shape! Stuart's been helping me with the technical aspects. Show them the blueprints, Stuart!"))
            print("\n")
            type.type("Stuart silently holds up a crude drawing of a building. It's covered in Oswald's handwriting - profit projections, seating arrangements, something about 'automatic shufflers'.")
            print("\n")
            type.type(quote("Magnificent, isn't it? Of course, we'll need someone to run it. Someone with your... expertise. Your PASSION for the game!"))
            print("\n")
            type.type("He winks at you.")
            print("\n")
            type.type(quote("Think about it, won't you? We could make beautiful music together. Beautiful, PROFITABLE music."))
        elif self.__mechanic_visits >= 3:
            type.type(quote("YOU! Perfect timing!"))
            print("\n")
            type.type("Oswald grabs your arm with surprising strength.")
            print("\n")
            type.type(quote("The plans are nearly complete. Stuart's been working day and night on some... special modifications. Upgrades, you might say. Technology that will give us an EDGE."))
            print("\n")
            type.type("He leans in close. His eyes have a strange gleam.")
            print("\n")
            type.type(quote("What if I told you we could transcend the limitations of mere flesh? What if we could become MORE than human? Faster, stronger, smarter? The perfect gambling machine!"))
            print("\n")
            type.type("He laughs, but it doesn't quite reach his eyes.")
            print("\n")
            type.type(quote("Just kidding, of course! Ha ha! Unless... no, no, we'll talk about that later. When you're ready. When we're BOTH ready."))
            print("\n")
            type.type("Stuart looks up from his work. For just a moment, you could swear you see something mechanical glinting beneath his sleeve.")

    def visit_oswald(self):
        type.type("You get in your car and drive to Oswald's Optimal Outoparts. ")
        print("\n")
        self.oswald_dialogue()
        print("\n")

        if(len(self.__broken_inventory)>0):
            broken_items = self.__lists.make_broken_items_list()
            tips = 0
            free_money = 0
            delight_indicator_price = 0
            health_indicator_price = 0
            dirty_old_hat_price = 0
            golden_watch_price = 0
            faulty_insurance_price = 0
            sneaky_peeky_glasses_price = 0
            quiet_sneakers_price = 0
            lucky_coin_price = 0
            worn_gloves_price = 0
            tattered_cloak_price = 0
            rusty_compass_price = 0
            pocket_watch_price = 0
            type.type("It appears that you possess some valuables in need of attention. Oh Stuart!")
            print("\n")
            type.type("Is there anything you would like Stuart to fix?")
            print()
            while(True):
                for i in range(len(broken_items)+1):
                    if(i<len(broken_items)):
                        type.type(str(i+1) + ". " + broken_items[i])
                        time.sleep(0.5)
                        print()
                    else:
                        type.type(str(i+1) + ". I'm all set")
                        time.sleep(0.5)
                        print()
                type.type("Choose a number: ")
                while True:
                    choice = None
                    while choice is None:
                        try:
                            choice = int(input())
                        except ValueError:
                            type.type("Choose a number: ")
                    if(1<=choice<=len(broken_items)):
                        item = broken_items[choice-1]
                        break
                    elif choice==len(broken_items)+1:
                        item = "Home"
                        break
                    else:
                        choice = None
                        type.type("Did you comprehend that?")
                        print()
                        type.type("Choose a number: ")

                print()

                if item == "Delight Indicator":
                    type.type("You'd like Stuart to repair your Delight Indicator?")
                    if delight_indicator_price == 0:
                        delight_indicator_price = random.choice([5500, 6000, 9000, 10000])
                    price = delight_indicator_price
                elif item == "Health Indicator":
                    type.type("You'd like Stuart to repair your Health Indicator?")
                    if health_indicator_price == 0:
                        health_indicator_price = random.choice([4500, 5500, 7000, 9000, 11000])
                    price = health_indicator_price
                elif item == "Dirty Old Hat":
                    type.type("You'd like Stuart to repair the cloth on your Dirty Old Hat?")
                    if dirty_old_hat_price == 0:
                        dirty_old_hat_price = random.choice([14000, 15000, 17000, 20000])
                    price = dirty_old_hat_price
                elif item == "Golden Watch":
                    type.type("You'd like Stuart to repair that Golden Watch you possess?")
                    if golden_watch_price == 0:
                        golden_watch_price = random.choice([16000, 17500, 18000, 20000, 30000])
                    price = golden_watch_price
                elif item == "Faulty Insurance":
                    type.type("You'd like Stuart to restore your Faulty Insurance card?")
                    if faulty_insurance_price == 0:
                        faulty_insurance_price = random.choice([5500, 6000, 7000, 9000, 10000])
                    price = faulty_insurance_price
                elif item == "Sneaky Peeky Shades":
                    type.type("You'd like Stuart to fix up those Sneaky Peeky Shades on top of your eyelids?")
                    if sneaky_peeky_glasses_price == 0:
                        sneaky_peeky_glasses_price = random.choice([18000, 20000, 25000, 30000])
                    price = sneaky_peeky_glasses_price
                elif item == "Quiet Sneakers":
                    type.type("You'd like Stuart to sew up those Quiet Sneakers on your feet?")
                    if quiet_sneakers_price == 0:
                       quiet_sneakers_price = random.choice([9000, 10000, 12000])
                    price = quiet_sneakers_price
                elif item == "Lucky Coin":
                    type.type("You'd like Stuart to polish that Lucky Coin of yours?")
                    if lucky_coin_price == 0:
                        lucky_coin_price = random.choice([7000, 8000, 10000])
                    price = lucky_coin_price
                elif item == "Worn Gloves":
                    type.type("You'd like Stuart to mend those Worn Gloves you carry?")
                    if worn_gloves_price == 0:
                        worn_gloves_price = random.choice([10000, 11000, 13000])
                    price = worn_gloves_price
                elif item == "Tattered Cloak":
                    type.type("You'd like Stuart to weave together that Tattered Cloak?")
                    if tattered_cloak_price == 0:
                        tattered_cloak_price = random.choice([12500, 14000, 16000])
                    price = tattered_cloak_price
                elif item == "Rusty Compass":
                    type.type("You'd like Stuart to restore that Rusty Compass?")
                    if rusty_compass_price == 0:
                        rusty_compass_price = random.choice([5000, 6000, 7500])
                    price = rusty_compass_price
                elif item == "Pocket Watch":
                    type.type("You'd like Stuart to recalibrate that Pocket Watch?")
                    if pocket_watch_price == 0:
                        pocket_watch_price = random.choice([11500, 13000, 15000])
                    price = pocket_watch_price
                else: 
                    type.type("Welp, then I've done all I can possibly do. Good day, my friend.")
                    print("\n")
                    self.start_night()
                    return
                
                print()

                type.type("Stuart will be able to fix this, for say, " + green(bright("${:,}".format(price))) + ". Do you accept? ")
                
                while True:
                    yes_or_no = input("").lower()
                    if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self.__balance<price):
                        print()
                        type.type("Oh dear! I'm afraid you can't afford this purchase.")
                        if tips <= 2:
                            random_chance = random.randrange(2)
                            print("\n")
                            if random_chance <= 1:
                                type.type("Here, take this as a pick me up, hopefully it helps. Try again?")
                                self.change_balance(random.choice([50, 100, 200, 300, 400, 500]))
                                tips += 1
                            else:
                                broken_items.pop(choice-1)
                                type.type("Maybe give me something else to fix.")
                        else:
                            broken_items.pop(choice-1)  
                            print("\n")
                            type.type("Shall Stuart repair something else?")
                        break
                    elif (yes_or_no == "y") or (yes_or_no == "yes"):
                        print()
                        type.type("Jolly good! Stuart!")
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            print("\n")
                            type.type("Yes! Yes! Work your magic, you little man.")
                            self.change_balance(-price)
                            self.fix_item(item)
                            broken_items.pop(choice-1)
                            if item=="Sneaky Peeky Shades" or item=="Quiet Sneakers":
                                type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            else:
                                type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        else:
                            print("\n")
                            type.type("Okay, Stuart. What are you doing? It appears that Stuart has gotten stuck whilst trying to fix your thingy. No matter! Stuart, will you please stop? Here, friend, I am giving you your item back. I won't even charge you.")
                            print("\n")
                            broken_items.pop(choice-1)
                            if free_money < 2:
                                random_chance = random.randrange(2)
                                if random_chance == 0:
                                    type.type("In fact, here, just take it, this is yours now.")
                                    self.change_balance(random.choice([50, 100, 200, 500, 1000]))
                                    free_money += 1
                                else:
                                    type.type("I'm so sorry that Stuart was unable to help. My deepest condolences.")
                                    print("\n")
                            else:
                                type.type("Honestly, Stuart is trying his best, and you shouldn't get mad at him.")
                                print("\n")

                            
                        if len(broken_items)==0:
                            type.type("My my, that's everything! Please come again soon, and we can continue performing business!")
                            print("\n")
                            self.start_night()
                            return
                        else:
                            type.type("Is there anything else Stuart can help you with?")
                            print()
                        break
                    elif (yes_or_no == "n") or (yes_or_no == "no"):
                        print()
                        type.type("Really? Nevermind Stuart, you aren't going to fix this. I apologise, but they simply don't want you to. Blame them.")
                        print("\n")
                        type.type("Are you done teasing Stuart? Have anything else for him?")
                        print()
                        break
                    else:
                        print()
                        type.type("Come again? ")
        
        # Oswald's Upgrade Shop
        self.oswald_upgrade_shop()
        return

    def oswald_upgrade_shop(self):
        # Get list of base items that can be upgraded
        upgradeable_items = []
        base_items = ["Delight Indicator", "Health Indicator", "Dirty Old Hat", 
                     "Golden Watch", "Sneaky Peeky Shades", "Quiet Sneakers",
                     "Faulty Insurance", "Lucky Coin", "Worn Gloves",
                     "Tattered Cloak", "Rusty Compass", "Pocket Watch"]
        
        for item in base_items:
            if self.can_upgrade(item):
                upgradeable_items.append(item)
        
        if len(upgradeable_items) == 0:
            if self.all_items_upgraded():
                type.type("My my, look at you! Every single item you possess has been upgraded!")
                print("\n")
                type.type("Stuart is practically in tears. He's so proud of his work. Isn't that right, Stuart?")
                print("\n")
                type.type("You hear a deep voice from behind a shelf: " + quote("Yeah, that's tight, yo."))
                print("\n")
                self.meet("Oswald Upgrades Complete")
            else:
                type.type("It appears you have nothing that Stuart can upgrade at this time. Do come back when you have more items!")
                print("\n")
            self.start_night()
            return
        
        print("\n")
        type.type("Now then! Stuart has been developing quite the skillset lately. He can now " + cyan(bright("UPGRADE")) + " your items to make them even more powerful!")
        print("\n")
        type.type("Of course, such enhancements don't come cheap. But you look like someone who appreciates quality, yes?")
        print("\n")
        
        while len(upgradeable_items) > 0:
            type.type("Which item would you like Stuart to upgrade?")
            print()
            
            # Display upgradeable items with their upgraded versions
            for i in range(len(upgradeable_items) + 1):
                if i < len(upgradeable_items):
                    item = upgradeable_items[i]
                    upgraded = self.get_upgraded_version(item)
                    type.type(str(i+1) + ". " + item + " → " + cyan(upgraded))
                    time.sleep(0.3)
                    print()
                else:
                    type.type(str(i+1) + ". I'm finished")
                    time.sleep(0.3)
                    print()
            
            type.type("Choose a number: ")
            while True:
                choice = None
                while choice is None:
                    try:
                        choice = int(input())
                    except ValueError:
                        type.type("Choose a number: ")
                if 1 <= choice <= len(upgradeable_items):
                    item = upgradeable_items[choice-1]
                    break
                elif choice == len(upgradeable_items) + 1:
                    type.type("Very well! Do come again when you desire further enhancements!")
                    print("\n")
                    self.start_night()
                    return
                else:
                    choice = None
                    type.type("I beg your pardon?")
                    print()
                    type.type("Choose a number: ")
            
            print()
            
            # Upgrade prices
            prices = {
                "Delight Indicator": 150000, "Health Indicator": 150000, "Dirty Old Hat": 200000,
                "Golden Watch": 300000, "Sneaky Peeky Shades": 400000, "Quiet Sneakers": 250000,
                "Faulty Insurance": 120000, "Lucky Coin": 200000, "Worn Gloves": 250000,
                "Tattered Cloak": 300000, "Rusty Compass": 160000, "Pocket Watch": 350000
            }
            price = prices.get(item, 200000)
            upgraded = self.get_upgraded_version(item)
            
            type.type("Ah, the " + magenta(bright(item)) + "! A fine choice.")
            print("\n")
            type.type("Stuart can transform this into the " + cyan(bright(upgraded)) + " for " + green(bright("${:,}".format(price))) + ".")
            print("\n")
            
            type.type("Do you accept this offer?")
            print()
            
            while True:
                yes_or_no = input("").lower()
                if (yes_or_no == "y" or yes_or_no == "yes") and self.__balance < price:
                    print()
                    type.type("Oh dear! It appears your funds are insufficient for this particular enhancement.")
                    print("\n")
                    type.type("Perhaps save up a bit more and return? Stuart will be waiting!")
                    print()
                    break
                elif yes_or_no == "y" or yes_or_no == "yes":
                    print()
                    type.type("Splendid! Stuart, work your magic!")
                    print("\n")
                    self.change_balance(-price)
                    new_item = self.perform_upgrade(item)
                    type.type("Stuart's tiny hands move with incredible precision. Sparks fly, gears turn, and...")
                    print("\n")
                    type.type("Your " + magenta(bright(item)) + " has become the " + cyan(bright(new_item)) + "!")
                    print("\n")
                    upgradeable_items.remove(item)
                    
                    if len(upgradeable_items) > 0:
                        type.type("Would you like Stuart to upgrade anything else?")
                        print()
                    break
                elif yes_or_no == "n" or yes_or_no == "no":
                    print()
                    type.type("No? Well, perhaps another time then. Stuart doesn't judge.")
                    print("\n")
                    type.type("Anything else catch your eye?")
                    print()
                    break
                else:
                    print()
                    type.type("I'm terribly sorry, I didn't quite catch that. ")
        
        if len(upgradeable_items) == 0:
            if self.all_items_upgraded():
                print("\n")
                type.type(cyan(bright("INCREDIBLE!")))
                print("\n")
                type.type("Every single item in your possession has been fully upgraded!")
                print("\n")
                type.type("Stuart emerges from behind the counter. For the first time, he speaks directly to you.")
                print("\n")
                type.type(quote("Yo. That's tight. You're like... a god now or whatever."))
                print("\n")
                type.type("Oswald beams with pride. " + quote("Indeed! You are now operating at PEAK efficiency! The world is your oyster, my friend!"))
                print("\n")
                self.meet("Oswald Upgrades Complete")
            else:
                type.type("That's all Stuart can upgrade for now. Do return when you have more items!")
                print("\n")
        
        self.start_night()
        return
    # Convenience Store
    def update_convenience_store_inventory(self):
        if self.__day == 2: self.__convenience_store_inventory = self.__lists.make_convenience_store_inventory()
        if (self.__day % 7) == 0:
            self.__convenience_store_inventory = self.__lists.make_convenience_store_inventory()

    def visit_convenience_store(self):
        type.type("You get in your car and drive to the Convenience Store. ")
        if not self.has_met("Convenience Store"):
            self.meet("Convenience Store")
            type.type("When pulling into the parking lot, you have to grip the wheel tightly to keep control of the wagon, as the concrete beneath you is littered with potholes. As you drive closer to bright red brick building, you begin to read the sign 'Convenience Store' written in bold. ")
            type.type("Really? This place really called 'Convenience Store'? They couldn't have come up with anything more creative? You park nearby, and get out, being sure not to trip on the loose chunks of road. ")
            print("\n")
            type.type("Walking closer to the store, you notice there's a poster with a smiling dude on it, holding his thumbs up, with the caption 'We Love our Customers! That's why we're limiting each customer to one item per visit. That means there's more for everyone! Sharing is caring!' ")
            type.type("Looking through the window, the store is barren, with only a few items on the shelf. If not for someone standing at the register, you would have thought the place to be abandoned.")
            print("\n")
            type.type("When you open the glass door, you notice a bell above you ring. There's a teenager on his phone, sitting with his feet up on the counter. His face is covered with pimples, and he's in the middle of blowing a bubble with the gum in his mouth.")
            print("\n")
            type.type("You get closer to the boy, and he finally notices you, and puts his phone down.")
        print("\n")
        if(len(self.__convenience_store_inventory)==0):
            type.type("As you walk up to the store, you see a white sign hanging on the front door. They're closed. Bummer.")
            print("\n")
            self.start_night()
            return
        type.type("Sup. Name's Kyle. Got a one-item limit. Managers orders. I don't make the rules. ")
        print("\n")
        items_bought = 0
        while True:
            choice = None
            items = self.__convenience_store_inventory
            if items_bought == 0:
                type.type("What do you want?")
            else:
                type.type("What else you want?")
            print()
            for i in range(len(items)+1):
                if(i<len(items)):
                    type.type(str(i+1) + ". " + items[i][0] + " - " + green(bright("${:,}".format(items[i][1]))))
                    print()
                else:
                    type.type(str(i+1) + ". I'm not buying anything")
                    time.sleep(0.5)
                    print()
            type.type("Choose a number: ")
            while True:
                while choice is None:
                    try:
                        choice = int(input())
                    except ValueError:
                        type.type("C'mon I don't have all day just pick something: ")
                if(1<=choice<=len(items)):
                    item = items[choice-1][0]
                    price = items[choice-1][1]
                    if(price<=self.__balance):
                        break
                    else:
                        type.type("Dude, you obviously can't afford that. Try again, buddy: ")
                elif choice==len(items)+1:
                    item = "Home"
                    break
                else:
                    choice = None
                    type.type("We clearly don't have that in right now.")
                    print()
                    type.type("It's not hard, just choose a number: ")
            print()

            if choice!=len(items)+1:
                items.pop(choice-1)

            # === FOOD ITEMS (Consumable - heal and/or restore sanity) ===
            if item == "Candy Bar":
                type.type("You got a " + bright(magenta("Candy Bar!")))
                print()
                type.type("You chomp down the candy bar. Its sweet chocolate and caramel fill your stomach, and you feel a little better.")
                self.heal(5)
                self.restore_sanity(1)  # Hidden sanity restore
            elif item == "Bag of Chips":
                type.type("You got a " + bright(magenta("Bag of Chips!")))
                print()
                type.type("You chomp down the bag of chips. Its salty potato goodness fills your stomach, and you feel better.")
                self.heal(8)
            elif item == "Turkey Sandwich":
                type.type("You got a " + bright(magenta("Turkey Sandwich!")))
                print()
                type.type("You chomp down the turkey sandwich. Its savory turkey and provolone fill your stomach, and you feel much better.")
                self.heal(15)
                self.restore_sanity(2)  # Hidden sanity restore
            elif item == "Energy Drink":
                type.type("You got an " + bright(magenta("Energy Drink!")))
                print()
                type.type("You crack it open and chug. The caffeine hits you like a truck. You feel wired.")
                self.heal(3)
                # Energy drink effect could be tracked for bonus actions
            elif item == "Beef Jerky":
                type.type("You got some " + bright(magenta("Beef Jerky!")))
                print()
                type.type("Tough, chewy, and delicious. Pure protein. You feel stronger.")
                self.heal(12)
            elif item == "Cup Noodles":
                type.type("You got " + bright(magenta("Cup Noodles!")))
                print()
                type.type("You ask Kyle for hot water. He sighs but obliges. Warm, salty, comforting.")
                self.heal(10)
                self.restore_sanity(2)  # Comfort food restores sanity
            elif item == "Granola Bar":
                type.type("You got a " + bright(magenta("Granola Bar!")))
                print()
                type.type("Healthy and crunchy. You feel responsible for once.")
                self.heal(7)
            elif item == "Hot Dog":
                type.type("You got a " + bright(magenta("Hot Dog!")))
                print()
                type.type("It's been spinning on that roller for god knows how long, but it tastes fine.")
                self.heal(8)
                if random.randrange(10) == 0:
                    type.type(" Actually, your stomach gurgles ominously...")
                    self.hurt(3)
            elif item == "Microwave Burrito":
                type.type("You got a " + bright(magenta("Microwave Burrito!")))
                print()
                type.type("Kyle nukes it for exactly 90 seconds. It's scalding on the outside, frozen in the middle. Classic.")
                self.heal(9)
            
            # === COMMON UTILITY ITEMS ===
            elif item == "Deck of Cards":
                type.type(bright(magenta("You got a Deck of Cards!")))
                print()
                type.type("Maybe you can practice your shuffling.")
                self.add_item("Deck of Cards")
            elif item == "Pest Control":
                type.type(bright(magenta("You got Pest Control!")))
                print()
                type.type("This should help with any unwanted critters in your car.")
                self.add_item("Pest Control")
            elif item == "Cough Drops":
                type.type(bright(magenta("You got Cough Drops!")))
                print()
                type.type("Mentholyptus flavor. Your throat thanks you in advance.")
                self.add_item("Cough Drops")
            elif item == "Dog Treat":
                type.type(bright(magenta("You got a Dog Treat!")))
                print()
                type.type("Bacon flavored. For dogs. Probably.")
                self.add_item("Dog Treat")
            elif item == "Spare Tire":
                type.type(bright(magenta("You got a Spare Tire!")))
                print()
                type.type("It's small and a bit worn, but it'll do in a pinch.")
                self.add_item("Spare Tire")
            elif item == "Flashlight":
                type.type(bright(magenta("You got a Flashlight!")))
                print()
                type.type("Batteries included. Surprisingly.")
                self.add_item("Flashlight")
            elif item == "First Aid Kit":
                type.type(bright(magenta("You got a First Aid Kit!")))
                print()
                type.type("Band-aids, antiseptic, the works. Could save your life someday.")
                self.add_item("First Aid Kit")
            elif item == "Umbrella":
                type.type(bright(magenta("You got an Umbrella!")))
                print()
                type.type("Compact and flimsy, but it'll keep you dry.")
                self.add_item("Umbrella")
            elif item == "Sunglasses":
                type.type(bright(magenta("You got Sunglasses!")))
                print()
                type.type("Cheap knockoffs, but they look cool enough.")
                self.add_item("Sunglasses")
            elif item == "Lighter":
                type.type(bright(magenta("You got a Lighter!")))
                print()
                type.type("A simple Bic lighter. Fire is useful.")
                self.add_item("Lighter")
            elif item == "Duct Tape":
                type.type(bright(magenta("You got Duct Tape!")))
                print()
                type.type("If you can't fix it with duct tape, you're not using enough duct tape.")
                self.add_item("Duct Tape")
            elif item == "Pocket Knife":
                type.type(bright(magenta("You got a Pocket Knife!")))
                print()
                type.type("A small Swiss Army style knife. Has a tiny scissor and everything.")
                self.add_item("Pocket Knife")
            elif item == "Bag of Acorns":
                type.type("You got a " + bright(magenta("Bag of Acorns!")))
                print()
                type.type("Perfect for feeding squirrels. Or throwing at people, I guess.")
                self.add_item("Bag of Acorns")
            elif item == "Can of Tuna":
                type.type("You got a " + bright(magenta("Can of Tuna!")))
                print()
                type.type("Chunk light in water. Cats love this stuff.")
                self.add_item("Can of Tuna")
            elif item == "Lettuce":
                type.type("You got some " + bright(magenta("Lettuce!")))
                print()
                type.type("A sad, wilted head of iceberg lettuce. Kyle looks at you weird.")
                self.add_item("Lettuce")
            elif item == "Binoculars":
                type.type(bright(magenta("You got Binoculars!")))
                print()
                type.type("See things far away. Very far away. Creepily far away.")
                self.add_item("Binoculars")
            
            # === SPECIAL ITEMS ===
            elif item == "LifeAlert":
                type.type(bright(magenta("You got LifeAlert!")))
                print()
                type.type("'Help, I've fallen and I can't get up!' Now you're prepared for the worst.")
                self.add_item("LifeAlert")
            elif item == "Lottery Ticket":
                type.type(bright(magenta("You got a Lottery Ticket!")))
                print()
                lottery_result = random.randrange(100)
                if lottery_result == 0:
                    winnings = random.randint(1000, 5000)
                    type.type("Holy crap! You scratch it right there and... " + green(bright("YOU WON ${:,}!".format(winnings))))
                    self.change_balance(winnings)
                elif lottery_result < 10:
                    winnings = random.randint(10, 50)
                    type.type("You scratch it and win " + green(bright("${:,}".format(winnings))) + ". Not bad!")
                    self.change_balance(winnings)
                else:
                    type.type("You scratch it eagerly... nothing. As expected.")
            elif item == "Lucky Penny":
                type.type(bright(magenta("You got a Lucky Penny!")))
                print()
                type.type("Heads up! That's good luck, right?")
                self.add_item("Lucky Penny")
            elif item == "Lucky Rabbit Foot":
                type.type(bright(magenta("You got a Lucky Rabbit Foot!")))
                print()
                type.type("Dyed purple and attached to a little chain. Wasn't so lucky for the rabbit.")
                self.add_item("Lucky Rabbit Foot")
            
            # === PREMIUM ITEMS ===
            elif item == "Expensive Cologne":
                type.type(bright(magenta("You got Expensive Cologne!")))
                print()
                type.type("Smells like money and bad decisions. Perfect for the casino.")
                self.add_item("Expensive Cologne")
            elif item == "Fancy Cigars":
                type.type(bright(magenta("You got Fancy Cigars!")))
                print()
                type.type("Cuban, apparently. Kyle says he 'knows a guy.'")
                self.add_item("Fancy Cigars")
            elif item == "Gold Chain":
                type.type(bright(magenta("You got a Gold Chain!")))
                print()
                type.type("Thick and gaudy. You look like a rapper from 2005.")
                self.add_item("Gold Chain")
            elif item == "Vintage Wine":
                type.type(bright(magenta("You got Vintage Wine!")))
                print()
                type.type("1987. A good year, apparently. You wouldn't know.")
                self.add_item("Vintage Wine")
            
            # === TRAP/CURSED ITEMS ===
            elif item == "Necronomicon":
                type.type(bright(magenta("You got a ") + red("Necronomicon!")))
                print()
                type.type("Kyle looks genuinely disturbed that you bought this. " + quote("Dude, that thing gives me the creeps. Take it and go."))
                self.add_item("Necronomicon")
                self.lose_sanity(5)  # Immediate sanity hit
            elif item == "Cursed Coin":
                type.type(bright(magenta("You got a ") + red("Cursed Coin!")))
                print()
                type.type("It's cold to the touch. Unnaturally cold. The face on it seems to be... frowning?")
                self.add_item("Cursed Coin")
                # Cursed coin has bad effects later
            
            # === RARE MYSTERY ITEMS ===
            elif item == "Mysterious Envelope":
                type.type(bright(magenta("You got a Mysterious Envelope!")))
                print()
                type.type("Sealed with red wax. Kyle says it's been in the lost and found for years.")
                self.add_item("Mysterious Envelope")
            elif item == "Old Photograph":
                type.type(bright(magenta("You got an Old Photograph!")))
                print()
                type.type("Black and white. Shows a family standing in front of... wait, is that the casino?")
                self.add_item("Old Photograph")
            elif item == "Broken Compass":
                type.type(bright(magenta("You got a Broken Compass!")))
                print()
                type.type("The needle spins wildly, never settling. Useless for directions, but... interesting.")
                self.add_item("Broken Compass")
            
            # === RANK 0 ITEMS ===
            elif item == "Cheap Sunscreen":
                type.type(bright(magenta("You got Cheap Sunscreen!")))
                print()
                type.type("SPF 15. Better than nothing, probably.")
                self.add_item("Cheap Sunscreen")
            elif item == "Plastic Poncho":
                type.type(bright(magenta("You got a Plastic Poncho!")))
                print()
                type.type("Clear plastic, one size fits most. Crinkles when you walk.")
                self.add_item("Plastic Poncho")
            elif item == "Breath Mints":
                type.type(bright(magenta("You got Breath Mints!")))
                print()
                type.type("Extra strong. Your breath could use some help after living in a car.")
                self.add_item("Breath Mints")
            elif item == "Rubber Bands":
                type.type(bright(magenta("You got Rubber Bands!")))
                print()
                type.type("A ball of various rubber bands. You never know when you'll need one.")
                self.add_item("Rubber Bands")
            
            # === RANK 1 ITEMS ===
            elif item == "Bug Spray":
                type.type(bright(magenta("You got Bug Spray!")))
                print()
                type.type("Industrial strength. Mosquitoes fear you now.")
                self.add_item("Bug Spray")
            elif item == "Disposable Camera":
                type.type(bright(magenta("You got a Disposable Camera!")))
                print()
                type.type("27 exposures. Capture some memories... or evidence.")
                self.add_item("Disposable Camera")
            elif item == "Road Flares":
                type.type(bright(magenta("You got Road Flares!")))
                print()
                type.type("For emergencies. Or starting fires. No judgment here.")
                self.add_item("Road Flares")
            elif item == "Air Freshener":
                type.type(bright(magenta("You got an Air Freshener!")))
                print()
                type.type("Pine scent. Your car desperately needs this.")
                self.add_item("Air Freshener")
            
            # === RANK 2 ITEMS ===
            elif item == "Padlock":
                type.type(bright(magenta("You got a Padlock!")))
                print()
                type.type("Combination lock. 4 digits. You set it to something you'll remember... hopefully.")
                self.add_item("Padlock")
            elif item == "Fishing Line":
                type.type(bright(magenta("You got Fishing Line!")))
                print()
                type.type("50 yards of monofilament. Strong enough to catch a big one.")
                self.add_item("Fishing Line")
            elif item == "Super Glue":
                type.type(bright(magenta("You got Super Glue!")))
                print()
                type.type("Bonds in seconds. Kyle warns you not to glue your fingers together. Voice of experience.")
                self.add_item("Super Glue")
            elif item == "Hand Warmers":
                type.type(bright(magenta("You got Hand Warmers!")))
                print()
                type.type("Just snap 'em and they heat up. Good for cold nights.")
                self.add_item("Hand Warmers")
            
            # === RANK 3 ITEMS ===
            elif item == "Leather Gloves":
                type.type(bright(magenta("You got Leather Gloves!")))
                print()
                type.type("Soft Italian leather. Makes you feel like a professional at... something.")
                self.add_item("Leather Gloves")
            elif item == "Silver Flask":
                type.type(bright(magenta("You got a Silver Flask!")))
                print()
                type.type("Engraved with initials. Not yours, but that's fine.")
                self.add_item("Silver Flask")
            elif item == "Fancy Pen":
                type.type(bright(magenta("You got a Fancy Pen!")))
                print()
                type.type("A Mont Blanc knockoff. Still writes nicely though.")
                self.add_item("Fancy Pen")
            
            # === RANK 4+ ITEMS ===
            elif item == "Silk Handkerchief":
                type.type(bright(magenta("You got a Silk Handkerchief!")))
                print()
                type.type("Embroidered edges. Very classy. You stuff it in your pocket.")
                self.add_item("Silk Handkerchief")
            elif item == "Monogrammed Lighter":
                type.type(bright(magenta("You got a Monogrammed Lighter!")))
                print()
                type.type("Gold-plated Zippo. Has someone else's initials, but fire is fire.")
                self.add_item("Monogrammed Lighter")
            elif item == "Antique Pocket Watch":
                type.type(bright(magenta("You got an Antique Pocket Watch!")))
                print()
                type.type("Victorian era, supposedly. Ticks with a satisfying rhythm.")
                self.add_item("Antique Pocket Watch")
            
            elif item == "Home":
                type.type("Suit yourself.")
                print("\n")
                self.start_night()
                return
            
            items_bought+=1
            print("\n")

            if items_bought == 1:
                random_chance = random.randrange(5)
                if random_chance < 2:
                    type.type("You know what? Rules are made to be broken. I mean, screw em! I hate my manager anyways. ")
                    type.type("You can have one more item, just don't tell anyone I let you do this.")
                    print("\n")
                else:
                    type.type("Welp. There you go. That's your item. Weird thing to buy, if you ask me. Now get lost, I'm going on break.")
                    print("\n")
                    self.start_night()
                    return
            else:
                type.type("Welp. There you go. Two whole items. Wow. Now get lost. I've got a girl to text. She's super hot.")
                print("\n")
                self.start_night()
                return


    # Marvin's Shop and interactions
    def visit_marvin(self):
        type.type("You get in your car and drive to Marvin's Mystical Merchandise. ")
        print("\n")
        inventory = self.__lists.make_marvin_inventory()
        if len(inventory) == 0:
            type.type("Sorry man, I've got no product for you tonight. Maybe try coming back another day. ")
            return
        else:
            type.type("Welcome, welcome. I've got some very valuable stuff in stock, just for a fine gambler like you.")
            print("\n")
            type.type("While I won't get bogged down in the details of how I got my hands on it, I think you'll wanna check these out:")
            print("\n")

        for item_number in range(len(inventory)):
            item = inventory[item_number]
            if (item_number==0) and (len(inventory)==1):
                type.type("The only item I've got right now is the " + self.__lists.get_marvin_adjective() + " " + magenta(bright(item)))
            elif (item_number==0):
                type.type("The first item I've got is the " + self.__lists.get_marvin_adjective() + " " + magenta(bright(item)))
            elif item_number==len(inventory)-1:
                type.type("The last item I've got is the " + self.__lists.get_marvin_adjective() + " " + magenta(bright(item)))
            else:
                type.type("The next item I've got is the " + self.__lists.get_marvin_adjective() + " " + magenta(bright(item)))

            print()

            if item == "Delight Indicator":
                type.type("With this little device, you can read how happy anyone is, just by pointing it at them! Could get you out of a lot of trouble.")
                price = random.choice([8500, 9500, 10000])
            elif item == "Health Indicator":
                type.type("This gadget lets you see how healthy you are at any given moment. It's great for knowing how imminent a trip to the ER is.")
                price = random.choice([8000, 8500, 9500])
            elif item == "Dirty Old Hat":
                type.type("By wearing this, you're telling the whole world \"I'm poor and I'm not afraid to show it!\" It's a foolproof way for people to take pity on you.")
                price = random.choice([25000, 28000, 30000])
            elif item == "Golden Watch":
                type.type("This watch was my grandfathers at one point. It's a beauty. If you're a gambling man, anyone in their right mind would wanna see you betting on their table.")
                price = random.choice([29000, 32000, 35000])
            elif item == "Faulty Insurance":
                type.type("I got this thing forged by a buddy of mine. It's a fake insurance card. I've used it to get out of so many hospital bills, and you could too!")
                price = random.choice([10000, 11000, 12000])
            elif item == "Enchanting Silver Bar":
                type.type("Listen, I know this silver bar looks a bit useless, but I swear, it's awesome. Look at the stock market, this thing is only gonna get more and more expensive. And if I sell it to you, you can sell it off later and make some money.")
                price = 10000
            elif item == "Sneaky Peeky Shades":
                type.type("These aren't your ordinary pair of glasses. Put them on, and you'll catch glimpses that others can't see. But use them wisely; you only get one peek per night.")
                price = random.choice([35000, 38000, 40000])
            elif item == "Quiet Sneakers":
                type.type("Sometimes, the best move is to walk away. Use this when you feel trouble brewing, and avoid the day's misfortunes.")
                price = random.choice([15000, 18000, 20000])
            elif item == "Lucky Coin":
                type.type("This here's an old coin with a four-leaf clover on it. My grandma used to say it could turn bad luck into no luck at all. Lost a hand? Flip this, and maybe you'll get your bet back.")
                price = random.choice([12000, 14000, 16000])
            elif item == "Worn Gloves":
                type.type("These gloves are pretty beat up, but trust me, they've got some magic left in 'em. Wear these when you play, and you'll feel the cards better. Might just get luckier draws.")
                price = random.choice([18000, 20000, 22000])
            elif item == "Tattered Cloak":
                type.type("Don't let the moth holes fool ya. This cloak's got some sneaky enchantment. Dealers sometimes just... forget to collect when you lose. Weird, right?")
                price = random.choice([22000, 25000, 28000])
            elif item == "Rusty Compass":
                type.type("The glass is cracked and it's missing a few screws, but this compass still points to opportunity. Carry it around, and you might stumble upon something unexpected.")
                price = random.choice([8000, 10000, 12000])
            elif item == "Pocket Watch":
                type.type("This brass beauty is always running a bit slow, but hey, that works in your favor. Flash it at the table, and you might squeeze in an extra round.")
                price = random.choice([20000, 23000, 26000])

            print()

            type.type("For " + green(bright("${:,}".format(price))) + ", it can be all yours. You buying? ")
            while True:
                yes_or_no = input("").lower()
                if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self.__balance<price):
                    print()
                    type.type("Cmon man, you can't afford this.")
                    print("\n")
                    break
                if (yes_or_no == "y") or (yes_or_no == "yes"):
                    print()
                    type.type("Great! It's all yours.")
                    self.change_balance(-price)
                    self.add_item(item)
                    type.type("You got the " + magenta(bright(item)) + "!")
                    print()
                    type.type("Description: " + self.get_item_desc(item))
                    print("\n")
                    break
                elif (yes_or_no == "n") or (yes_or_no == "no"):
                    print()
                    type.type("Not your thing, huh? Well that's ok. ")
                    break
                else:
                    print()
                    type.type("What was that? ")

        type.type("That's all I've got to sell you tonight. Maybe try coming back another day. ")
        self.start_night()

    # Pawn Shop Interaction
    def visit_pawn_shop(self):
        type.type("You get in your car and drive down a winding backstreet to Grimy Gus's Pawn Emporium. ")
        print("\n")
        if not self.has_met("Pawn Shop"):
            self.meet("Pawn Shop")
            type.type("The shop is tucked between a boarded-up laundromat and a place that just says 'MEAT' in flickering neon. The windows are blacked out, and the door looks like it hasn't been painted since the Cold War.")
            print("\n")
            type.type("You push inside. The smell hits you first-mothballs, old leather, and something vaguely chemical. Every surface is covered in dusty trinkets, tarnished jewelry, and items that probably have stories you don't want to hear.")
            print("\n")
            type.type("In the corner, you notice a strange contraption-rusted pipes, grinding gears, and a funnel on top. A sign reads: " + cyan(bright("\"THE GARBLE MACHINE\"")))
            print("\n")
            type.type("Grimy Gus sits behind a counter made of stacked milk crates, reading a newspaper from three weeks ago. He looks up and grins, revealing those yellow teeth.")
            print("\n")
            type.type(quote("Ah, you came! I knew you would. People like us... we understand each other."))
            print("\n")
        else:
            type.type(quote("Back again, eh? Let's see what treasures you've dug up this time."))
            print("\n")
        
        # Get collectible prices
        collectible_prices = self.get_collectible_prices()
        all_collectibles = self.get_all_collectibles_list()
        total_collectibles = len(all_collectibles)
        items_sold = self.get_gus_items_sold()
        
        # Gus's hints about collecting everything
        if items_sold >= 5 and items_sold < total_collectibles - 10:
            type.type("Gus scratches his chin thoughtfully.")
            print("\n")
            type.type(quote("You know... I'm working on something. Something special. If you keep bringing me treasures, ALL the treasures... I might just share my most precious grime with you."))
            print("\n")
        elif items_sold >= total_collectibles - 10 and items_sold < total_collectibles - 5:
            remaining = total_collectibles - items_sold
            type.type("Gus's eyes gleam with anticipation.")
            print("\n")
            type.type(quote("You're getting close, friend. Real close. Only about ") + yellow(bright(str(remaining))) + quote(" more unique items and you'll see something nobody else has ever seen."))
            print("\n")
        elif items_sold >= total_collectibles - 5 and items_sold < total_collectibles:
            remaining = total_collectibles - items_sold
            type.type("Gus is practically vibrating with excitement.")
            print("\n")
            type.type(quote("Just ") + yellow(bright(str(remaining))) + quote(" more! Just ") + yellow(bright(str(remaining))) + quote(" more unique treasures and the GRIME will be yours!"))
            print("\n")
        
        # Find what player can sell
        sellable_items = []
        for item, price in collectible_prices.items():
            if self.has_item(item):
                sellable_items.append((item, price))
        
        # Menu options
        type.type("What would you like to do?")
        print()
        type.type("1. See what I can sell")
        print()
        type.type("2. Start selling")
        print()
        type.type("3. Leave")
        print()
        
        choice = input("Choose: ").strip()
        
        if choice == "1":
            # List what player has
            print("\n")
            if len(sellable_items) == 0:
                type.type(quote("You got nothing I want right now. Come back when you've found some treasures out in the world."))
                print("\n")
            else:
                type.type(quote("Let me see here... you've got some interesting stuff:"))
                print("\n")
                for item, price in sellable_items:
                    already_sold = " " + yellow("(already sold one)") if self.has_sold_to_gus(item) else ""
                    type.type("  • " + cyan(bright(item)) + " - " + green("${:,}".format(price)) + already_sold)
                    print()
                print()
                type.type(quote("That's ") + yellow(bright(str(len(sellable_items)))) + quote(" items I'd be willing to take off your hands."))
                print("\n")
                type.type(quote("I've bought ") + yellow(bright(str(items_sold))) + quote(" unique collectibles from you so far. Out of... well, let's just say there's a LOT more out there."))
                print("\n")
            
            # Recurse back to menu
            self.visit_pawn_shop_menu(sellable_items, collectible_prices)
            return
        
        elif choice == "2":
            if len(sellable_items) == 0:
                type.type(quote("You got nothing I want. Come back when you've got something interesting."))
                print("\n")
                self.start_night()
                return
            self.visit_pawn_shop_sell(sellable_items, collectible_prices)
            return
        
        else:
            type.type(quote("Come back when you've got the goods."))
            print("\n")
            self.start_night()
            return
    
    def visit_pawn_shop_menu(self, sellable_items, collectible_prices):
        """Return to pawn shop menu after viewing inventory"""
        type.type("What would you like to do?")
        print()
        type.type("1. Start selling")
        print()
        type.type("2. Leave")
        print()
        
        choice = input("Choose: ").strip()
        
        if choice == "1":
            if len(sellable_items) == 0:
                type.type(quote("You got nothing I want. Come back when you've got something interesting."))
                print("\n")
                self.start_night()
                return
            self.visit_pawn_shop_sell(sellable_items, collectible_prices)
        else:
            type.type(quote("Come back when you've got the goods."))
            print("\n")
            self.start_night()
    
    def visit_pawn_shop_sell(self, sellable_items, collectible_prices):
        """Handle the selling process at Gus's shop"""
        type.type(quote("Let me take a look at what you've got..."))
        print("\n")
        
        sold_something = False
        total_collectibles = self.get_gus_total_collectibles()
        
        # Gus's unique descriptions for items
        gus_descriptions = {
            # Underwater Legendary
            "Golden Trident": "Sweet mother of Neptune! A GOLDEN TRIDENT! The kind of thing kings kill for. The kind of thing that makes men mad.",
            "Kraken Pearl": "This... this came from a KRAKEN? Do you have ANY idea how many sailors are at the bottom of the ocean because of these things?",
            "Mermaid Crown": "Royalty of the deep. The fish-ladies don't just GIVE these away. Someone's gonna be looking for this.",
            "Kraken's Memory": "I can feel it... pulsing. Like it's remembering something terrible. I LOVE it.",
            "Ancient Sea Map": "Maps to places that ain't supposed to exist anymore. Or places that never should've existed at all.",
            "Deep Stone": "Heavy. Too heavy for its size. Like it's got the whole ocean compressed into it.",
            "Pirate Treasure": "YARR! Just kidding. But seriously, this is the real deal. Probably has a curse on it.",
            "Treasure Coordinates": "Numbers that lead to riches. Or death. Usually both.",
            "Captain's Compass": "Points somewhere, but not north. Somewhere more... interesting.",
            "Cannon Gem": "Pulled from a sunken warship? These absorb the violence of their history.",
            "Sailor's Lockbox": "Sailors kept their deepest secrets in these. Their real names. Their real sins.",
            "Mermaid's Pearl": "From a mermaid's own collection. They say these grant wishes. They also say wishes have prices.",
            "Mermaid Pearl": "Pretty thing. Probably worth more than my whole shop. Probably cursed too.",
            "Matched Pearls": "A matching pair! The ocean hates giving up pairs. You must've impressed someone down there.",
            "Pink Pearl": "Pink for love, they say. Or pink for blood diluted in seawater. Depends who you ask.",
            "Giant Oyster": "Still sealed? Bold. Could be a pearl in there. Could be a tiny angry crab.",
            # Beach Events
            "Golden Shovel": "Solid gold? For DIGGING? Someone had more money than sense. My kind of customer.",
            "Underwater Camera": "Full of someone else's memories. I'll sell 'em to the highest bidder.",
            "Crab Racing Trophy": "First place in CRAB RACING? This is a thing? I love this world.",
            "Championship Medal": "You won something! Or you stole this. Either way, I'm buying.",
            "Antique Ring": "Engagement ring, by the looks of it. Sad story here. I can sell sad stories.",
            "Treasure Chest": "The whole chest? With actual treasure? Christmas came early.",
            "Midnight Rose": "A rose that blooms at midnight? Either magic or very confused. Both valuable.",
            # Woodlands
            "Hunter's Mark": "The hunters gave you this? You must've killed something impressive. Or stupid.",
            "Bear King's Respect": "THE Bear King? As in the giant nightmare bear? And you have its RESPECT?",
            "Giant Bear Tooth": "This tooth is bigger than my hand. The bear it came from must be the size of a truck.",
            "Bear's Gold Coin": "Bears don't use currency. Which means this came from someone the bear ATE.",
            "Witch's Favor": "A favor from a witch. Dangerous to keep. Dangerous to sell. I'll take that risk.",
            "Magic Acorn": "Plant this and who knows what grows? A money tree? A murder tree? Only one way to find out.",
            "Fairy's Secret Map": "Fairies guard their secrets jealously. This map is probably booby-trapped.",
            "Captured Fairy": "A LIVE FAIRY? In a jar? This is either very valuable or very illegal. Probably both.",
            # Swamp
            "Gator Tooth Necklace": "Gator teeth. Strung together by someone who lived in the swamp too long.",
            "Tortoise Trophy": "First place in TORTOISE RACING? These swamp folks are wild.",
            "Ogre's Gemstone": "From an actual ogre? These things are worth a fortune. The ogre probably wasn't happy.",
            "Ogre's Gift": "The ogre GAVE you this? What did you do, compliment its cooking?",
            "Swamp Gold": "Gold from the swamp. Probably pulled off a corpse. I don't judge.",
            "Witch's Riddle": "A riddle from a witch. Answer it wrong and bad things happen. Not my problem anymore.",
            "Witch's Ward": "Protection magic. Good stuff. Someone out there is now unprotected.",
            "Voodoo Doll": "Ooh, careful with this one. Stick a pin in the wrong place and someone has a VERY bad day.",
            "Lucky Lure": "Lucky for fishing. Unlucky for fish. The circle of life.",
            "Earl's Lucky Lure": "Earl's personal lure? Earl must be either dead or very generous.",
            "Granny's Swamp Nectar": "Swamp granny moonshine. This stuff could strip paint. Or cure diseases. Same thing.",
            # City
            "Key to the City": "They gave you a KEY TO THE CITY? You're either a hero or a really good liar.",
            "Hero Medal": "For heroism? In THIS economy? You must've done something actually good.",
            "Fight Champion Belt": "Underground fighting? You've got more guts than brains. I respect that.",
            "Stolen Watch": "I'm not gonna ask where this came from. That's not how Gus does business.",
            "Suspicious Package": "I'm DEFINITELY not gonna ask about this one. Just give it here.",
            # Rabbit
            "Lucky Penny": "A penny for luck. Five bucks for your penny. That's the Gus markup.",
            "Lucky Rabbit Foot": "Wasn't lucky for the rabbit. But it might be lucky for me.",
            "Carrot": "A... carrot. You're bringing me a carrot. Fine. FINE. I'll take the stupid carrot.",
            "Rabbit's Blessing": "The rabbit BLESSED you? That's not a normal rabbit. This blessing might actually be worth something.",
            # Misc
            "Mysterious Lockbox": "Locked box, no key. The mystery is half the value.",
            "Mysterious Key": "A key with no lock. Someone out there is very frustrated.",
            "Mysterious Code": "Numbers and symbols that mean something to someone. Not me. But someone.",
            "Fountain Water": "From the Fountain of Youth? Either this is priceless or you got scammed.",
            "Treasure Map": "X marks the spot. Or X marks the trap. One way to find out.",
            "Joe's Treasure Map": "Joe's map specifically? Joe's dead, isn't he? Don't answer that.",
            # Secret
            "Dealer's Joker": "This... this came from HIM? The Dealer? I've heard stories. This card shouldn't exist.",
            "Ace of Spades": "The death card. The money card. The Gus-wants-it card.",
        }
        
        for item, price in sellable_items:
            type.type("Gus picks up your " + cyan(bright(item)) + " and examines it closely, turning it over in his grimy fingers.")
            print("\n")
            
            # Get Gus's description
            if item in gus_descriptions:
                type.type(quote(gus_descriptions[item]))
            else:
                type.type(quote("Interesting piece you've got here. Very interesting indeed."))
            
            print("\n")
            type.type(quote("I'll give you ") + green(bright("${:,}".format(price))) + quote(" for it. Cash in hand. Right now. What do you say?"))
            print("\n")
            
            answer = ask.yes_or_no("Sell the " + item + "? ")
            if answer == "yes":
                self.lose_item(item)
                self.change_balance(price)
                sold_something = True
                
                # Track if this is a new unique item sold
                is_new_collectible = not self.has_sold_to_gus(item)
                if is_new_collectible:
                    self.sell_item_to_gus(item)
                
                # THE GARBLE MACHINE RITUAL
                type.type("Gus snatches the " + cyan(bright(item)) + " and scurries over to the Garble Machine.")
                print("\n")
                type.type("He drops it into the funnel on top. The machine groans to life.")
                print("\n")
                time.sleep(0.5)
                type.type(cyan("*GRRRRRIND*"))
                print()
                time.sleep(0.5)
                type.type(cyan("*GARBLE GARBLE GARBLE*"))
                print()
                time.sleep(0.5)
                type.type("The " + cyan(bright(item)) + " is garbled till it's " + yellow("guck") + " and it's " + yellow("goo") + "...")
                print()
                time.sleep(0.5)
                type.type("Then the " + yellow("gunk") + " is turned to " + magenta(bright("GRIME")) + ".")
                print("\n")
                type.type("A tiny bit of dark, shimmering grime drips into a jar behind the counter. Gus watches it with reverent eyes.")
                print("\n")
                type.type(quote("Beautiful. Just beautiful."))
                print("\n")
                
                # Check if all collectibles have been sold
                items_sold_now = self.get_gus_items_sold()
                if items_sold_now == total_collectibles:
                    self.gus_complete_collection()
                    return
                
            else:
                type.type("Gus shrugs and hands it back to you.")
                print("\n")
                type.type(quote("Your loss. Or maybe your gain. The grime will wait."))
                print("\n")
        
        if sold_something:
            items_sold_now = self.get_gus_items_sold()
            type.type("Gus counts out your money with practiced fingers, then slides it across the counter.")
            print("\n")
            type.type(quote("Pleasure doing business. That's ") + yellow(bright(str(items_sold_now))) + quote(" unique treasures you've brought me now. Keep 'em coming."))
        else:
            type.type(quote("Changed your mind on everything, huh? That's fine. The grime can wait."))
        
        print("\n")
        self.start_night()
    
    def gus_complete_collection(self):
        """Called when player has sold every unique collectible to Gus"""
        print("\n")
        type.type(yellow(bright("=== THE COLLECTION IS COMPLETE ===")))
        print("\n")
        type.type("Gus freezes. His whole body trembles. Tears stream down his grimy face.")
        print("\n")
        type.type(quote("You... you did it. You actually did it. Every treasure. Every trinket. Every... everything."))
        print("\n")
        type.type("He reaches under the counter with shaking hands and pulls out a small, ornate jar. Inside, something dark and shimmering swirls like a living shadow.")
        print("\n")
        type.type(quote("My most precious grime. Years of garbling. YEARS. Every item I ever bought, ground down, reduced, purified into this."))
        print("\n")
        type.type("He holds it out to you, his yellow teeth visible in the widest smile you've ever seen.")
        print("\n")
        type.type(quote("It's yours. You've earned it. The ") + magenta(bright("GUS'S PRECIOUS GRIME")) + quote(". Cherish it. CHERISH IT."))
        print("\n")
        type.type("You take the jar. It's warm. It pulses faintly. You have absolutely no idea what to do with it.")
        print("\n")
        self.add_item("Gus's Precious Grime")
        type.type(yellow(bright("You got Gus's Precious Grime!")))
        print("\n")
        type.type("Gus wipes his tears on his stained trench coat.")
        print("\n")
        type.type(quote("Now get out of my shop. I need to be alone with my feelings."))
        print("\n")
        self.start_night()

    def update_no_bust_durability(self, invincible=False):
        if (self.has_flask_effect("No Bust")):
            if invincible:
                self.__flask_durability[0] = -1
                
            if (self.__flask_durability[0] > 0):
                self.__flask_durability[0] -= random.choice([1, 2])
                if self.__flask_durability[0] <= 0:
                    self.__flask_durability[0] = 0
                    self.remove_flask_effect("No Bust")
                    print("\n")
                    type.slow(red(bright("Your Flask of No Bust effect ran out!")))

            # Sets durability when you get the item, or if the item is fixed
            if (self.__flask_durability[0] == 0):
                self.__flask_durability[0] = 4

    def update_delight_indicator_durability(self, invincible=False):
        if self.has_item("Delight Indicator"):
            if invincible:
                self.__item_durability[0] = -1
                
            if (self.__item_durability[0] > 0):
                self.__item_durability[0] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[0] <= 0:
                    self.__item_durability[0] = 0
                    self.break_item("Delight Indicator")
                    print("\n")
                    type.slow(red(bright("Your Delight Indicator broke!")))

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[0] == 0):
                self.__item_durability[0] = 45


    def update_health_indicator_durability(self, invincible=False):
        if self.has_item("Health Indicator"):
            if invincible:
                self.__item_durability[1] = -1
                
            if (self.__item_durability[1] > 0):
                self.__item_durability[1] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[1] <= 0:
                    self.__item_durability[1] = 0
                    self.break_item("Health Indicator")
                    type.slow(red(bright("Your Health Indicator broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[1] == 0):
                self.__item_durability[1] = 30


    def update_dirty_old_hat_durability(self, invincible=False):
        if self.has_item("Dirty Old Hat"):
            if invincible:
                self.__item_durability[2] = -1
                
            if (self.__item_durability[2] > 0):
                self.__item_durability[2] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[2] <= 0:
                    self.__item_durability[2] = 0
                    self.break_item("Dirty Old Hat")
                    type.slow(red(bright("Your Dirty Old Hat broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[2] == 0):
                self.__item_durability[2] = 25


    def update_golden_watch_durability(self, invincible=False):
        if self.has_item("Golden Watch"):
            if invincible:
                self.__item_durability[3] = -1
                
            if (self.__item_durability[3] > 0):
                self.__item_durability[3] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[3] <= 0:
                    self.__item_durability[3] = 0
                    self.break_item("Golden Watch")
                    type.slow(red(bright("Your Golden Watch broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[3] == 0):
                self.__item_durability[3] = 20


    def update_sneaky_peeky_glasses_durability(self, invincible=False):
        if self.has_item("Sneaky Peeky Shades"):
            if invincible:
                self.__item_durability[5] = -1

            if (self.__item_durability[5] > 0):
                self.__item_durability[5] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[5] <= 0:
                    self.__item_durability[5] = 0
                    self.break_item("Sneaky Peeky Shades")
                    type.slow(red(bright("Your Sneaky Peeky Shades broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[5] == 0):
                self.__item_durability[5] = 15


    def update_quiet_sneakers_durability(self, invincible=False):
        if self.has_item("Quiet Sneakers"):
            if invincible:
                self.__item_durability[6] = -1

            if (self.__item_durability[6] > 0):
                self.__item_durability[6] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[6] <= 0:
                    self.__item_durability[6] = 0
                    self.break_item("Quiet Sneakers")
                    type.slow(red(bright("Your Quiet Sneakers broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[6] == 0):
                self.__item_durability[6] = 15


    def update_faulty_insurance_durability(self, invincible=False):
        if self.has_item("Faulty Insurance"):
            if invincible:
                self.__item_durability[7] = -1
                
            if (self.__item_durability[7] > 0):
                self.__item_durability[7] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[7] <= 0:
                    self.__item_durability[7] = 0
                    self.break_item("Faulty Insurance")
                    type.slow(red(bright("Your Faulty Insurance broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[7] == 0):
                self.__item_durability[7] = 15


    def update_lucky_coin_durability(self, invincible=False):
        if self.has_item("Lucky Coin"):
            if invincible:
                self.__item_durability[8] = -1
                
            if (self.__item_durability[8] > 0):
                self.__item_durability[8] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[8] <= 0:
                    self.__item_durability[8] = 0
                    self.break_item("Lucky Coin")
                    type.slow(red(bright("Your Lucky Coin broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[8] == 0):
                self.__item_durability[8] = 20


    def update_worn_gloves_durability(self, invincible=False):
        if self.has_item("Worn Gloves"):
            if invincible:
                self.__item_durability[9] = -1
                
            if (self.__item_durability[9] > 0):
                self.__item_durability[9] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[9] <= 0:
                    self.__item_durability[9] = 0
                    self.break_item("Worn Gloves")
                    type.slow(red(bright("Your Worn Gloves broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[9] == 0):
                self.__item_durability[9] = 25


    def update_tattered_cloak_durability(self, invincible=False):
        if self.has_item("Tattered Cloak"):
            if invincible:
                self.__item_durability[10] = -1
                
            if (self.__item_durability[10] > 0):
                self.__item_durability[10] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[10] <= 0:
                    self.__item_durability[10] = 0
                    self.break_item("Tattered Cloak")
                    type.slow(red(bright("Your Tattered Cloak broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[10] == 0):
                self.__item_durability[10] = 18


    def update_rusty_compass_durability(self, invincible=False):
        if self.has_item("Rusty Compass"):
            if invincible:
                self.__item_durability[11] = -1
                
            if (self.__item_durability[11] > 0):
                self.__item_durability[11] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[11] <= 0:
                    self.__item_durability[11] = 0
                    self.break_item("Rusty Compass")
                    type.slow(red(bright("Your Rusty Compass broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[11] == 0):
                self.__item_durability[11] = 22


    def update_pocket_watch_durability(self, invincible=False):
        if self.has_item("Pocket Watch"):
            if invincible:
                self.__item_durability[12] = -1
                
            if (self.__item_durability[12] > 0):
                self.__item_durability[12] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[12] <= 0:
                    self.__item_durability[12] = 0
                    self.break_item("Pocket Watch")
                    type.slow(red(bright("Your Pocket Watch broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[12] == 0):
                self.__item_durability[12] = 15


    def update_second_chance_durability(self, invincible=False):
        if (self.has_flask_effect("Second Chance")):
            if invincible:
                self.__flask_durability[8] = -1
                
            if (self.__flask_durability[8] > 0):
                self.__flask_durability[8] -= random.choice([1, 2])
                if self.__flask_durability[8] <= 0:
                    self.__flask_durability[8] = 0
                    self.remove_flask_effect("Second Chance")
                    print("\n")
                    type.slow(red(bright("Your Flask of Second Chance effect ran out!")))

            # Sets durability when you get the item
            if (self.__flask_durability[8] == 0):
                self.__flask_durability[8] = 4


    def update_split_serum_durability(self, invincible=False):
        if (self.has_flask_effect("Split Serum")):
            if invincible:
                self.__flask_durability[9] = -1
                
            if (self.__flask_durability[9] > 0):
                self.__flask_durability[9] -= random.choice([1, 2])
                if self.__flask_durability[9] <= 0:
                    self.__flask_durability[9] = 0
                    self.remove_flask_effect("Split Serum")
                    print("\n")
                    type.slow(red(bright("Your Flask of Split Serum effect ran out!")))

            # Sets durability when you get the item
            if (self.__flask_durability[9] == 0):
                self.__flask_durability[9] = 4


    def update_dealers_hesitation_durability(self, invincible=False):
        if (self.has_flask_effect("Dealer's Hesitation")):
            if invincible:
                self.__flask_durability[10] = -1
                
            if (self.__flask_durability[10] > 0):
                self.__flask_durability[10] -= random.choice([1, 2])
                if self.__flask_durability[10] <= 0:
                    self.__flask_durability[10] = 0
                    self.remove_flask_effect("Dealer's Hesitation")
                    print("\n")
                    type.slow(red(bright("Your Flask of Dealer's Hesitation effect ran out!")))

            # Sets durability when you get the item
            if (self.__flask_durability[10] == 0):
                self.__flask_durability[10] = 4
        

    def get_item_desc(self, item):
        if item == "Delight Indicator": return "A small gadget, with wires tangled around it, and a small meter that displays the Dealer's happiness before every round of Blackjack."
        elif item == "Health Indicator": return "A small gadget, with wires construed around it, and a small gauge that displays changes in your health. Your current health is " + bright(magenta(str(self.__health) + "%")) + "."
        elif item == "Dirty Old Hat": return "A dark brown leather hat, covered in dirt and tears. It makes you look poor, and lowers the Dealer's minimum bet."
        elif item == "Golden Watch": return "A bright gold watch that glistens in any light. It makes you look rich, and increases the number of Blackjack rounds the Dealer lets you play."
        elif item == "Enchanting Silver Bar": return "A silver bar that slowly increases in worth every day. Sell this after 3 days to make a profit."
        elif item == "Sneaky Peeky Shades": return "A pair of glasses that allow you to sneak a peek at the next card in the deck once per night."
        elif item == "Quiet Sneakers": return "A pair of shoes that allows you to skip an unfavorable event during the day."
        elif item == "Faulty Insurance": return "A plastic card, with the company \'Super Real Insurance\' written on it. This card can be brought to the doctor's office for a chance of lowering bill fees."
        elif item == "Lucky Coin": return "A tarnished copper coin with a four-leaf clover etched on one side. Flip it before a hand to occasionally turn a loss into a push."
        elif item == "Worn Gloves": return "A pair of threadbare leather gloves that help you feel the cards better. Slightly increases your chances of getting a favorable card when hitting."
        elif item == "Tattered Cloak": return "A moth-eaten cloak that helps you blend into the shadows. The Dealer sometimes forgets to collect your bet when you lose."
        elif item == "Rusty Compass": return "An old compass with a cracked glass face. It points towards nearby opportunities, occasionally revealing a hidden shop or event."
        elif item == "Pocket Watch": return "A small brass pocket watch that's always a few minutes slow. It sometimes gives you an extra round at the Blackjack table."

        elif item == "Delight Manipulator": return "A small gadget, embedded in your right arm, with wires sticking into your veins. Attached is a small antenna that elicits complete and absolute happiness in anyone around you."
        elif item == "Health Manipulator": return "A small gadget, embedded in your left arm, with wires construed throughout your veins and into your heart. The device pumps artificial blood with a syntetic heartbeat throught your body, ensuring that you're always perfectly healthy."
        elif item == "Unwashed Hair": return "An implant into your scalp, giving you a fake hairdo covered in grime and grease. It makes you look abysmally poor, and sets the Dealer's minimum bet to one measly dollar"
        elif item == "Sapphire Watch": return "A sparkling sapphire watch that lights up any room. It makes you look richer than everyone else in the room, and greatly increases the number of Blackjack rounds the Dealer lets you play."
        elif item == "Enchanting Gold Bar": return "A gold bar that quickly increases in worth every day. Sell this after 3 days to make a profit."
        elif item == "Sneaky Peeky Goggles": return "A pair of goggles that allow you to sneak a peek at the next card in the deck once per round."
        elif item == "Quiet Bunny Slippers": return "A pair of slippers that allows you to skip all unfavorable events during the day."
        elif item == "Real Insurance": return "A plastic card, with the company \'Super Duper Real Insurance\' written on it. This card can be brought to the doctor's office to cover all bill fees."
        elif item == "Lucky Medallion": return "A gleaming gold medallion with a shooting star carved into its center. Flip it before a hand to always turn a loss into a push."
        elif item == "Velvet Gloves": return "A pair of exquisite velvet gloves that make your hands feel one with the cards. Significantly increases your chances of getting a favorable card when hitting."
        elif item == "Invisible Cloak": return "A shimmering cloak woven from moonlight threads. It makes you completely unnoticeable, and the Dealer often forgets to collect your bet when you lose."
        elif item == "Golden Compass": return "A pristine compass made of solid gold, with a needle that glows faintly. It always points towards the best opportunities, guaranteeing a beneficial shop or event each day."
        elif item == "Grandfather Clock": return "A miniaturized grandfather clock that fits in your pocket and keeps perfect time. It guarantees extra rounds at every Blackjack table you visit."

        elif item == "No Bust": return "A flask holding a dark green potion. It's infused with the power to veto a hand that busts. It lasts a few days."
        elif item == "Imminent Blackjack": return "A flask holding a neon yellow potion. It's infused with the power to instantly give you a Blackjack after hitting your hand. It wears off after one use."
        elif item == "Dealer's Whispers": return "A flask holding a navy blue potion. It's infused with the power to reveal the Dealer's hidden card. It lasts a few days."
        elif item == "Bonus Fortune": return "A flask holding a shiny gold potion. It's infused with the power to let you double down after being dealt a hand. It lasts a few days."
        elif item == "Anti-Venom": return "A flask holding a sparkly orange potion. It's infused with the power to heal you when attacked by a venemous creature. It lasts until used."
        elif item == "Anti-Virus": return "A flask holding a flowing gray potion. It's infused with the power to heal you when affected by a disease. It lasts until used."
        elif item == "Fortunate Day": return "A flask holding a bright orange potion. It's infused with the luck of the sun, and makes your next morning lucky. It wears off after one use."
        elif item == "Fortunate Night": return "A flask holding a pretty magenta potion. It's infused with the luck of the stars, and makes your next evening lucky. It wears off after one use, and has no impact on gambling."
        elif item == "Second Chance": return "A flask holding a swirling silver potion. It's infused with the power to replay a losing hand once per night. It lasts a few days."
        elif item == "Split Serum": return "A flask holding a vibrant violet potion. It's infused with the power to split any pair, even when you normally couldn't. It lasts a few days."
        elif item == "Dealer's Hesitation": return "A flask holding a murky brown potion. It's infused with the power to make the Dealer draw one extra card. It lasts a few days."
        elif item == "Pocket Aces": return "A flask holding a pure white potion. It's infused with the power to guarantee your first card is an Ace. It wears off after one use."

        elif item == "Never Bust": return "A flask holding a glowing green potion. It's infused with the power to veto a hand that busts."
        elif item == "Guaranteed Blackjack": return "A flask holding a glowing yellow potion. It's infused with the power to instantly give you a Blackjack after hitting your hand."
        elif item == "Dealer's Thoughts": return "A flask holding a glowing blue potion. It's infused with the power to always reveal the Dealer's hidden card."
        elif item == "Endless Fortune": return "A flask holding a glowing gold potion. It's infused with the power randomly double your bet for free after being dealt a hand."
        elif item == "Anti-Pathogen": return "A flask holding a glowing orange potion. It's infused with the power to heal you from any status effect."
        elif item == "Fortunate Life": return "A flask holding a glowing red potion. It's infused with the luck of the sun and the moon, and fills your life with good fortune."
        elif item == "Infinite Chances": return "A flask holding a glowing silver potion. It's infused with the power to replay any losing hand as many times as you'd like."
        elif item == "Perfect Split": return "A flask holding a glowing violet potion. It's infused with the power to split any hand, and both hands receive optimal cards."
        elif item == "Dealer's Doom": return "A flask holding a glowing brown potion. It's infused with the power to force the Dealer to always bust."
        elif item == "Ace in the Hole": return "A flask holding a glowing white potion. It's infused with the power to guarantee both your starting cards are Aces."

    def day_event(self):
        self.update_rank()
        
        # Broken state has random gameplay effects
        if self.__is_broken and random.randrange(4) == 0:
            effect_type, value, message = self.broken_gameplay_effect()
            print()
            type.slow(red(message))
            if effect_type == "money_loss":
                type.type(red(" (-$" + str(value) + ")"))
            elif effect_type == "money_gain":
                type.type(green(" (+$" + str(value) + ")"))
            print("\n")
            time.sleep(1)
        
        # Check for madness confrontation (rare, requires low sanity)
        if self.check_madness_confrontation():
            self.madness_confrontation()
            if not self.__alive:
                return
            # If survived, continue to normal day event
        
        # Show sanity status if sanity is below 75
        if self.__sanity <= 75 and random.randrange(5) == 0 and not self.__is_broken:
            print()
            type.type("You feel " + yellow(self.get_sanity_description()) + ".")
            print("\n")
        
        # Occasionally show sanity effects (more frequent at low sanity)
        if self.should_show_sanity_effect() and not self.__is_broken:
            print()
            type.slow(cyan(self.get_sanity_effect()))
            print("\n")
            time.sleep(1)
        
        dayEvent = getattr(self, self.__lists.get_day_event())
        dayEvent()
        return

    def night_event(self):
        self.update_rank()
        
        # Broken state has random effects at night too
        if self.__is_broken and random.randrange(3) == 0:
            effect_type, value, message = self.broken_gameplay_effect()
            print()
            type.slow(red(message))
            if effect_type == "money_loss":
                type.type(red(" (-$" + str(value) + ")"))
            elif effect_type == "money_gain":
                type.type(green(" (+$" + str(value) + ")"))
            print("\n")
            time.sleep(1)
        
        # Occasionally show sanity effects at night too (dreams are worse)
        if self.should_show_sanity_effect() and not self.__is_broken:
            print()
            type.slow(cyan(self.get_sanity_effect()))
            print("\n")
            time.sleep(1)
        
        nightEvent = getattr(self, self.__lists.get_night_event())
        nightEvent()
        self.update_rank()
        self.start_night()

    def goodbye_tom(self):
        type.type("You get in your wagon and drive to Tom's Trusty Trucks and Tires.")
        print("\n")
        type.type("The golden truck is parked out front, gleaming in the afternoon sun.")
        print("\n")
        type.type("Tom is waiting for you outside, a knowing look in his eyes.")
        print("\n")
        
        type.type(quote("I knew you'd come, yunno. A million bucks, huh? That's somethin' special."))
        print("\n")
        
        type.type("He scratches his chin.")
        print("\n")
        
        type.type(quote("But I gotta ask... what about that family of yours? You ever think about goin' back?"))
        print("\n")
        
        type.type("Tom pulls out a phone - your phone. The one you left here days ago.")
        print("\n")
        
        type.type(quote("There's been someone tryin' to reach ya. A lot. Think it might be important."))
        print("\n")
        
        answer = ask.yes_or_no("Take the phone call? ")
        
        if answer == "yes":
            type.type("You take the phone. Your hands are trembling.")
            print("\n")
            type.type("Tom gives you some space, walking back into the garage.")
            print("\n")
            type.type("You press the call button.")
            print("\n")
            type.type("It rings once. Twice. Then-")
            print("\n")
            
            type.slow(quote("John? John, is that you?"))
            print("\n")
            
            type.slow("The voice on the other end is unmistakable. It's Rebecca. Your wife.")
            print("\n")
        else:
            type.type(quote("Well, suit yourself. The phone'll be here if you change your mind."))
            print("\n")
            type.type("You leave Tom's shop. Maybe someday you'll be ready to face that call.")
            print("\n")
            return

        type.slow(quote("Do you hear that? That's your son, Nathan. He learned to walk a couple months ago. His first word was 'Dada'. God, I wish you were here for that. He needs you in his life, he needs you as a father figure. He remembers you. Sometimes, I pull up old pictures of you, and he reaches out to touch your face. All I want is for you to be here, to make more memories with me and my son. But you can be here, if you come back, come home. We can raise our son together, if you just come back home, to be with me and Nathan. I can forgive you for all of it. I do, I forgive you for everything. None of it matters now, it's all in the past. Just please…come home."))
        print("\n")

        type.slow("The sobs through the phone are piercing, and Tom has a sad look on his face. He clearly feels sorry for you, for all the pain you've both caused and gone through. ")
        print("\n")

        type.slow(quote("Dada…dada come back!"))
        print("\n")

        type.slow(quote("Could you do that for us?"))

        answer = ask.yes_or_no("\"Will you come back home?\"")

        if answer == "yes":
            self.salvation()
        else:
            self.resurrection()


    def salvation(self):
        type.slow("\"Yes, yes, yes of course I'll come home!\" Tears begin to stream from your eyes. \"I, I don't know what's gotten over me, I'm so, so incredibly sorry.\" A rush of adrenaline, no, realization comes over you. This whole time, you've been wasting your life away in a beat up wagon, trying to make a living off of gambling at a Blackjack table, while your family was trying, and struggling, to imagine a life without you. Immediately, you run out of Tom's Trusty Trucks and Tires, and you never look back.")
        print("\n")

        type.slow("\"Wait! You forgotcha wallet, yunno!\" Tom lifts your wallet, and opens it, and his eyes grow wide. \"Holy bejesus! My oh my, this generation is so peculiar. Welp, finder's keepers, I suppose. Guess this old Trucks and Tires shop's boutta get some upgrades, ya hear!\"")
        print("\n")

        type.slow("You put the pedal to the medal in the old wagon, hugging the twists and turns in the road, without a thought in your mind but your family. As you slowly begin to recognize the buildings around you, the wagon takes just a few more turns, before pulling into your driveway. You get out, and knock on the door, and in that moment, nothing feels better than watching the handle turn, hearing the hinges creak, and seeing the biggest smile on your wife's face, with your son in her hands, and you lean in for a warm embrace.")
        print("\n")

        type.slow("Many years go by, and the whole experience of being stranded in your car slowly fades from your mind. You get to experience things in life you never thought you'd one day see. Your son's first football game, the birth of your lovely daughter, Dianne. You and Rebecca renew your vows, and couldn't be any happier. After a long and sincere apology to your old boss Howard, you go back to your desk job, selling high quality printers to people in low income housing. It ain't much, but it's honest work.")
        print("\n")

        type.slow("Rebecca continues to raise the kids in her image. They're smart, caring, and just downright adorable. Once Nathan gets to high school he tries out for the Varsity team, and makes it as a freshman. He would go on to be the highest scoring wide receiver the high school ever had, and you got to be in the seat for every game. His touchdown celebration always ended with a point to you, and a nod, as though he's telling the world \'Yep, that's my Dad\'.")
        print("\n")

        type.slow("As you age more and more, your body slowly deteriorates. You aren't sure if the long and unhealthy lifestyle of living on the road was to blame, but you didn't ever bother giving the thought any time of day. You know, deep down inside, that you made the right choice.")
        print("\n")

        type.slow("Nathan played football in college, before retiring to run his personal business selling decorated carpets. It was in this very building where he would go on to meet his future wife, Kelly, who ended up being his perfect match. Meanwhile, Dianne kept working at being a straight A's student in high school, taking every accelerated English course they had to offer.")
        print("\n")

        type.slow("When Dianne's career as an author made national television, Nathan was in the hospital, with his wife Kelly, along with you and Rebecca. You'll never forget the day you witnessed the birth of your grandson, Thomas, while Dianne was on the tv in that very room, being watched by millions around the world. You gave Rebecca a hug and a kiss, and you both cried tears of joy together, being able to appreciate such a special life with one another.")
        print("\n")

        type.slow("But, as all good things do, it eventually had to come to an end, and when the doctor diagnosed you with chronic obstructive pulmonary disease at age 49, you knew that you were knocking on death's doorstep. After your doctor told you that your lungs were failing on you due to some kind of air pollutants, you came to the realization that you might've left your car running a few too many days. And all that exposure to the exhaust of your old wagon seems to have finally caught up to you.")
        print("\n")

        type.slow("You lay dormant in the hospital bed, with tubes up your nose, and a glossy look over your eyes. There are many bouquets of flowers by your bedside, as well as a few balloons that read 'Get Well Soon!', and 'You Can Beat This!' You hear a knock on the door, and perk up. The doctor walks in, and leads a parade of guests. It seems as though your whole family has come to visit you. There's Rebecca! And Dianne! And Nathan and Kelly, along with Thomas, and their newly born daughter Marissa. You missed her birth, as the doctors had to keep an eye on you, but they sent you lots of pictures. Now, you finally get to see her in person. It makes you so happy that you get to see your granddaughter in person. You weren't sure if you'd ever get the chance.")
        print("\n")

        type.slow("\"Dad, hey, how are you? Hanging in there?\" Nathan has tears streaming down his face, but his voice stays sturdy. It's clear that he, and the rest of your family, hate to see you like this.")
        print("\n")

        type.slow("You cough, then sit up.")
        print("\n")

        type.slow("\"You know, I'm doing pretty amazing, really.\" This gets a light chuckle from your family, but the mood quickly returns to solemn. Rebecca leans in closer to you, and gives you a hug.")
        print("\n")

        type.slow("\"You're my everything. I love you so much, John.\" You hug her back with as much force as you can give, hoping she could feel just a touch of it.")
        print("\n")

        type.slow("\"Dad, I wrote a book about you.\" Dianne half whispers, before showing it to you. \"It's about the battle between you and gambling, and how you overcame it, for us. You really are the strongest person I know. I love you.\" Dianne begins to sob harder, and quickly gives you a big hug.")
        print("\n")

        type.slow("\"Can I see my grandchildren?\" you ask, through your raspy voice.")
        print("\n")

        type.slow("\"Sure thing, Dad\" Nathan picks up Thomas, and Kelly picks up Marissa, and they both walk to your side, so you can get a closer look.")
        print("\n")

        type.slow("\"Gram..Grampy!\" Thomas belches.")
        print("\n")

        type.slow("\"Yes, that's your Grampy!\" Nathan responds, with a smile.")
        print("\n")

        type.slow("\"They're…so beautiful\", you manage to spew these words out, before delving into a coughing fit.")
        print("\n")

        type.slow("Nathan puts Thomas down and gives you a big hug.")
        print("\n")

        type.slow("\"I love you so much, Dad.\"")
        print("\n")

        type.slow("As Nathan releases his grasp, the world around you begins to fade. You look around the room at everyone's faces, one last time. Everyone's leaning onto the bed, to be with you for your final moments. Rebecca and Dianne holding your right hand, Nathan holding your left. Kelly's arm is around Nathan's shoulder, and Thomas and Marissa sit on the blankets, right above your leg. You squeeze your hands tight, holding your family close, before letting go of your grasp, and fading away to eternal darkness...")


    def resurrection(self):
        type.slow("\"Wha…what? Excuse me? John, I've been trying to reach you for months now, and the only thing you're going to say to me is 'no'? Do you not care at all about me? About Nathan? Why, why would you do this to us? After everything I've done for you. I covered for you when you needed me, I hid this addiction for years. Years! And for what? So you could run away from your family to keep hitting the tables? You sick, twisted fuck. To think that I honestly believed somewhere, deep down inside of you, you actually cared about me. That you actually cared about YOUR OWN GODDAMN SON.\" Your wife is screaming through the phone.")
        print("\n")

        type.slow("\"Dada…I love you…why dada gone?")
        print("\n")

        type.slow("\"You're a monster. You're completely pathetic. Don't even think about coming back. Not now, not ever. You will never see or hear from your son again, do you understand? YOU'RE DEAD TO ME JOHNATHAN. DEAD TO ME. ROT IN HELL, YOU FUCKING BASTA-")
        print("\n")

        type.slow("And with that, you hang up the phone. Your ears are ringing, your face is numb, and while Tom appears to be trying to console you after that phone call from hell, you just can't seem to hear a single word coming out of his mouth. In fact, you don't feel anything. Nothing but the ringing in your ears, and sheer hatred for the man you've become. And yet somehow throughout all of this, your legs beneath you begin to carry your body, out the door, into your car, and down the road towards that lonely casino, sitting on top of the little hill, at the end of the dirt road. As though infected by a parasite, you can't help but come back here, to this place, where you were stranded all those days ago. With your money in hand, you get out of the car, and slam the door. You walk towards the little shack, each step more determined than the last. You can prove her wrong, no, you have to prove her wrong.") 
        print("\n")

        type.slow(red("Welcome back. You don't look too well. Do you need something to drink? Perhaps some water?"))
        print("\n")

        type.slow("\"Bourbon, neat. The best you've got.\"")
        print("\n")

        type.slow(red("If you say so."))
        print("\n")

        type.slow("You watch as the Dealer gets up from his shadow, and as he stands, his jade green glass eye sparkes, around a terrible scar, from a fate that caused the left side of his face to be permanently disfigured. He walks across the room, and flicks on an old fashioned lamp, revealing a small bar, filled with any drink you could ask for. The Dealer's revolver hangs low on his waist, as though he's always prepared to use it at a moment's notice. Or, perhaps, he's just a cautious old man.")
        print("\n")

        type.slow("After about a minute, he comes back with your drink, and sets it down next to you. You pick up the glass, and take a swig, and then another, before slamming the empty glass down on the betting table.")
        print("\n")

        type.slow(red("That was awfully quick of you. Here, let me get you a refill."))
        print("\n")

        type.slow("\"Thanks, yeah, that would be great.\"")
        print("\n")

        type.slow("As he sets down your second glass, the Dealer sits back down in his seat, and begins to shuffle the cards. His thick fingers sometimes have trouble splitting the deck, but he riffles the cards like he's been doing it his whole life.")
        print("\n")

        type.slow(red("Are you ready to play a game of Blackjack?"))
        print("\n")
        
        type.slow("\"So, what's with the glass eye? You lose a fight or something?\"")
        print("\n")

        type.slow("The Dealer squints his eyes, then sighs.")
        print("\n")

        type.slow(red("Oh, I lost a fight alright. With my dog, Scrappy. He was a great lad."))
        print("\n")

        type.slow("The Dealer opens a pack of cigarettes, puts one in his mouth, and lights it. Smoke fills the air, and dances around the hanging light, like two spirits, in an endless duel.")
        print("\n")

        type.slow(red("Jumped up on me while we were playing fetch in the yard. Bit the left half of my face clean off. It was a tragedy, really. Docs patched me up, and the second I got home, me and Scrappy took a car ride. We drove far away from that home, from my neighbors, from everyone. Down a long road, deep into the woods. I let him out, and he was happy, running free. Ducking under branches, jumping over fallen logs, biting at sticks and leaves. But as I walked back to the truck to leave him there, he followed. So, I threw him a stick to go fetch, but when I got to the front seat, there he was, jumping through the window to sit on my lap, licking my hands and wagging his tail. He didn't seem to get that I was leaving without him. That's what made it all the more difficult, when I finally dragged him out of the truck, pulled out my revolver, and shot three bullets into his head. Even still, he kept whimpering. I couldn't bear to watch him die, so I just drove off. Never even gave him a proper burial. It was a shame, really, but I guess not all stories are happy ones."))
        print("\n")

        type.slow("The Dealer ashes the cigarette into a brown ceramic bowl next to him, full of the ashes of many, many long gone cigarettes.")
        print("\n")

        type.slow("You take a swig of your bourbon, appreciating the warm feeling in your chest.")
        print("\n")

        type.slow("\"Let's get this over with.\"")
        print("\n")

        type.slow(red("How much for this first hand?"))
        print("\n")

        type.slow("\"500 thousand.\"")
        print("\n")

        type.slow(red("Oh boy, high roller tonight, are we?"))
        print("\n")

        type.slow("\"You bet.\" You down the rest of your drink, and you start to feel a bit dizzy.")
        print("\n")

        type.slow(red("Alright, let's see here. You got a Nine of Spades, and a Two of Diamonds. Meanwhile, I'm sitting pretty with this Four of Clubs. What say you?"))
        print("\n")

        type.slow("You tap the table with a firm finger. \"Hit me.\"")
        print("\n")

        type.slow(red("Alrighty. Your next card's a…welp, that's a Ten of Clubs. That's a hefty Blackjack you just got there."))
        print("\n")

        type.slow("Winning a hand with a bet like that, you begin to chuckle to yourself. You see the Dealer begin to sweat, and he starts to tap his foot.")
        print("\n")

        type.slow(red("How about I get you another drink?"))
        print("\n")

        type.slow("\"Go for it.\"")
        print("\n")

        type.slow("The Dealer pours you a third bourbon, and hands it to you. You down the whole drink, and start to laugh again.")
        print("\n")

        type.slow("\"So you're telling me, that you shot and killed a dog, because he bit you in the face? Like yeah, that's a bad scar, but how do you mess up playing fetch that badly?\"")
        print("\n")

        type.slow(red("Boy, I've put down a lot bigger for a lot less."))
        print("\n")

        type.slow("\"But god, a dog? For a bite? You didn't have to do that, you know. Animal shelters exist for a reason.\"")
        print("\n")

        type.slow(red("How much are you betting."))
        print("\n")

        type.slow("\"I mean, that's just despicable. Getting revenge on a dog over something it didn't even understand. If you really felt the need to kill it, you could've gone with euthanasia. Why'd that slip your mind?\"")
        print("\n")

        type.slow(red("Give me an amount, boy."))
        print("\n")

        type.slow("\"You know what I think? I think that you wanted to shoot that dog. You were never gonna let it free. You brought it to the woods and shot it, just so you could watch it squirm.\"")
        print("\n")

        type.slow(red("Put some money on the damn table."))
        print("\n")

        type.slow("\"You know, you're what's wrong with this world. I mean, you just hurt those that care about you, denying their love all because you can? What happened to forgive and forget?\"")
        print("\n")

        type.slow(red("BET. SOME. DAMN. MONEY."))
        print("\n")

        type.slow("\"Put me all in, old man.\"")
        print("\n")

        type.slow("The Dealer flips cards over, to you and him.")
        print("\n")

        type.slow(red("That's an Ace of Spades and an Eight of Spades. Deadman's hand, as far as Poker is concerned. I've got a Seven of Hearts. You hitting?"))
        print("\n")

        type.slow("You wave your hand above the table. \"I'll stay\"")
        print("\n")

        type.slow(red("If that's what you'd like. My other card's a Four of Diamonds."))
        print("\n")
        
        type.slow("The dealer draws a card from the deck.")
        print("\n")

        type.slow(red("Damn, Three of Clubs. Would've been nice if you had that one, huh?"))
        print("\n")

        type.slow("The dealer draws yet another card.")
        print("\n")

        type.slow(red("Ace of Diamonds. That puts me at 15."))
        print("\n")

        type.slow("Your head begins to spin. Your stomach feels violently ill. Your breaths are getting deeper and deeper, but it feels like you're getting less and less oxygen each time. The dealer draws yet another card.")
        print("\n")

        type.slow(red("Yet another ace, this time the Ace of Clubs. Now I'm at 16, are you feeling the pressure yet?"))
        print("\n")

        type.slow("You watch as the Dealer's weathered finger goes down, touches the top card of the deck, lifts it up, then flips it over before you.")
        print("\n")

        type.slow(red("And that's the Five of Hearts that I needed! Blackjack for me, back to your car for you. I guess it's like they say, you win some, you lose some."))
        print("\n")

        type.slow("The Dealer's finger points towards the exit, and in a drunken stupor, you rise from the old wooden seat, and stumble your way to the door, with no money left in your pockets.")
        print("\n")

        type.slow("Right before walking out, you turn to the Dealer, who's once again cloaked in shadow. You knew you should've kept your mouth shut, but you couldn't help yourself.")
        print("\n")

        type.slow("\Rot in hell, you fucking bastard.\"")
        print("\n")

        type.slow("You get back into your wagon, and drive off, only faintly able to see the road. Is this really the life you live? You keep driving forward, for hours on end, never once looking back.")
        print("\n")
        
        type.slow("Eventually, your old wagon shutters, then dies. \"Ugh, not again.\" Stranded on the road once more, and your money has gone dry. As you're about to give up hope completely, you're reminded of a distant memory. You reach over to your cup holder and rip it from the center console. Tucked away inside of the hole that once held your cup holder is an old card with a big turkey on the front, wearing a pilgrim hat. When opening it up, you read the message 'Gobble gobble gobble up some yummy food this Thanksgiving! Love, Grandma'. Inside the letter was a green 50 dollar bill. May she rest in peace.")
        print("\n")

        type.slow("The door of your wagon creaks open, and you step out into the night sky, coughing up the Bourbon from earlier that night. After pushing your car off the road and between the trees, there isn't much else left for you to do, so you begin to wander down the dark, lonely street.")
        print("\n")

        type.slow("But, at the end of the road, where concrete turned to stone turned to gravel, you notice a light up ahead, engulfed in a circle of forest.")
        print("\n")

        type.slow("As you waltz into the fancy, yet rundown log cabin, your eyes begin to light up with the fire of a thousand suns. Roulette wheels! Poker tables! And in a dark corner of the rundown casino, sits a dealer, shuffling cards for a new round of Blackjack. That 50 dollars might just come in handy after all. Thanks, Grandma!")
        print("\n")

        type.slow("As you go to sit down at the table, you hear the Dealer cough, then watch as he sits up.")
        print("\n")

        type.slow("In a deep, and yet strained voice, the Dealer, perched up in a ray of light from the ceiling fan above, poses a question to you.")
        print("\n")

        type.slow(yellow("Would you like to play a game of Blackjack? "))

    # ============================================
    # MILLIONAIRE ENDINGS
    # ============================================
    
    def millionaire_morning_visitor(self):
        """The special morning event when you wake up as a millionaire"""
        print("\n")
        type.slow("You wake up to the sound of tapping on your car window.")
        print("\n")
        type.type("For a moment, you think you're dreaming. The morning light filters through the dusty glass, illuminating a figure standing outside your wagon.")
        print("\n")
        type.type("You sit up slowly, rubbing your eyes. When you look again, the figure is still there. An old woman, dressed in a flowing white dress that seems to shimmer in the dawn light.")
        print("\n")
        type.type("Her eyes are kind, but ancient. Something about her feels... familiar.")
        print("\n")
        
        type.slow(cyan("\"Good morning, child. You've done well.\""))
        print("\n")
        
        type.type("You crack the window open, unsure if this is real.")
        print("\n")
        
        type.type(quote("Who... who are you?"))
        print("\n")
        
        type.slow(cyan("\"I am the one who has watched over you since the beginning. Since that first night, when you walked into the casino with nothing but fifty dollars and a dream.\""))
        print("\n")
        
        type.type("She smiles, and for a moment, you swear you see her flicker like a candle flame.")
        print("\n")
        
        type.slow(cyan("\"You've accumulated a fortune through the cards. One million dollars. But wealth alone does not complete a journey.\""))
        print("\n")
        
        type.type("You step out of your wagon, the cool morning air hitting your face. The woman doesn't move, simply watching you with those ancient eyes.")
        print("\n")
        
        type.slow(cyan("\"To truly finish what you've started, you must visit the one who helped you get here. Your mechanic. They have something important to tell you.\""))
        print("\n")
        
        # Determine which mechanic to send them to based on who they've met
        mechanics_met = []
        if self.has_met("Tom"):
            mechanics_met.append("Tom")
        if self.has_met("Frank"):
            mechanics_met.append("Frank")
        if self.has_met("Oswald"):
            mechanics_met.append("Oswald")
        
        if len(mechanics_met) == 0:
            # Player never got their car fixed by any mechanic - rare ending path
            type.slow(cyan("\"But I see... you never let anyone in. You fixed things yourself, or left them broken. An interesting choice.\""))
            print("\n")
            type.slow(cyan("\"Very well. Your path is your own. But know this - the airport lies to the east. If you wish to leave this life behind entirely, that is where you must go.\""))
            print("\n")
            self.set_chosen_mechanic("None")
        elif len(mechanics_met) == 1:
            chosen = mechanics_met[0]
            self.set_chosen_mechanic(chosen)
            if chosen == "Tom":
                type.slow(cyan("\"Tom. The jolly one with the golden truck. He's been expecting you. Go to him this afternoon.\""))
            elif chosen == "Frank":
                type.slow(cyan("\"Frank. The rough one with the tattooed arms. He has something to say. Visit him this afternoon.\""))
            else:
                type.slow(cyan("\"Oswald. The quiet genius. He's been waiting for this moment. See him this afternoon.\""))
            print("\n")
        else:
            # Multiple mechanics - let the woman choose based on who has the most dream progress
            dream_scores = {
                "Tom": self.get_tom_dreams() if self.has_met("Tom") else -1,
                "Frank": self.get_frank_dreams() if self.has_met("Frank") else -1,
                "Oswald": self.get_oswald_dreams() if self.has_met("Oswald") else -1
            }
            chosen = max([m for m in mechanics_met], key=lambda m: dream_scores[m])
            self.set_chosen_mechanic(chosen)
            
            if chosen == "Tom":
                type.slow(cyan("\"You've met several mechanics on your journey, but Tom... Tom has been special to you, hasn't he? The dreams you've shared... they bind you together.\""))
                print("\n")
                type.slow(cyan("\"Go to Tom's Trusty Trucks and Tires this afternoon. Your destiny awaits there.\""))
            elif chosen == "Frank":
                type.slow(cyan("\"You've crossed paths with many, but Frank's fire has left its mark on you. The visions in your sleep... they speak of him.\""))
                print("\n")
                type.slow(cyan("\"Go to Filthy Frank's Flawless Fixtures this afternoon. He has answers you seek.\""))
            else:
                type.slow(cyan("\"Of all the mechanics you've known, Oswald's quiet wisdom has touched you deepest. Your dreams whisper his name.\""))
                print("\n")
                type.slow(cyan("\"Go to Oswald's Optimal Outparts this afternoon. The final piece awaits.\""))
            print("\n")
        
        type.type("The woman begins to fade, her form dissolving like morning mist.")
        print("\n")
        
        type.slow(cyan("\"Remember, child - you may also choose to fly away. The airport is always an option for those with means. But that choice... that choice will change everything.\""))
        print("\n")
        
        type.type("And then she's gone, leaving only the faint scent of lavender and the warmth of the rising sun.")
        print("\n")
        
        type.type("You stand there for a long moment, processing what just happened. A million dollars in your pocket, and a choice to make.")
        print("\n")
        
        if self.get_chosen_mechanic() == "None":
            type.type("The airport to the east... or stay here and continue gambling, now with nothing to prove.")
        else:
            type.type("Visit " + magenta(bright(self.get_chosen_mechanic())) + " at their shop... fly away from the airport... or stay here and continue gambling, now with nothing to prove.")
        print("\n")
        
        ask.press_continue("Press a key to continue to the afternoon: ")
        print("\n")

    def millionaire_afternoon(self):
        """Special afternoon choices after the millionaire morning visitor"""
        type.type("The afternoon sun hangs heavy in the sky. You've got " + green(bright("${:,}".format(self.__balance))) + " and a decision to make.")
        print("\n")
        
        # Build the choice list
        choices = []
        
        chosen_mechanic = self.get_chosen_mechanic()
        if chosen_mechanic == "Tom" and self.has_met("Tom"):
            choices.append(("Visit Tom's Trusty Trucks and Tires", "tom_ending"))
        elif chosen_mechanic == "Frank" and self.has_met("Frank"):
            choices.append(("Visit Filthy Frank's Flawless Fixtures", "frank_ending"))
        elif chosen_mechanic == "Oswald" and self.has_met("Oswald"):
            choices.append(("Visit Oswald's Optimal Outoparts", "oswald_ending"))
        
        choices.append(("Drive to the Airport", "airport"))
        choices.append(("Go to the Casino (Continue Playing)", "continue"))
        
        type.type("What would you like to do?")
        print()
        for i, (text, _) in enumerate(choices):
            type.type(str(i+1) + ". " + text)
            time.sleep(0.5)
            print()
        
        choice = None
        type.type("Choose a number: ")
        while True:
            while choice is None:
                try:
                    choice = int(input())
                except ValueError:
                    type.type("Choose a number: ")
            if 1 <= choice <= len(choices):
                break
            else:
                choice = None
                type.type("That number's not a choice!")
                print()
                type.type("Choose a number: ")
        
        print()
        selected = choices[choice-1][1]
        
        if selected == "tom_ending":
            self.goodbye_tom()
        elif selected == "frank_ending":
            self.goodbye_frank()
        elif selected == "oswald_ending":
            self.goodbye_oswald()
        elif selected == "airport":
            self.visit_airport()
        else:
            # Continue playing - go to normal night event
            type.type("You decide to keep gambling. After all, why stop now?")
            print("\n")
            self.night_event()

    def visit_airport(self):
        """Drive to the airport and choose your escape ending"""
        type.type("You get in your wagon and begin the long drive east, towards the airport.")
        print("\n")
        type.type("The road stretches out before you, endless and empty. You've never driven this far from the casino before.")
        print("\n")
        type.type("As you drive, you think about everything that's happened. The nights at the blackjack table. The dealers. The mechanics. The strange people you've met along the way.")
        print("\n")
        
        # Different thoughts based on what the player has experienced
        if self.has_met("Tom") or self.has_met("Frank") or self.has_met("Oswald"):
            mechanics_names = []
            if self.has_met("Tom"): mechanics_names.append("Tom")
            if self.has_met("Frank"): mechanics_names.append("Frank")
            if self.has_met("Oswald"): mechanics_names.append("Oswald")
            type.type("You think about " + ", ".join(mechanics_names) + ". They helped you when you needed it most.")
            print("\n")
        
        if self.has_item("Squirrely"):
            type.type("Squirrely chitters nervously in the passenger seat. He's never been on a plane before.")
            print("\n")
        
        if self.has_met("Suzy"):
            type.type("You wonder if Suzy ever made it out of here. Maybe you'll see her on the other side.")
            print("\n")
        
        type.type("After what feels like hours, you see it - the airport, rising from the desert like a mirage.")
        print("\n")
        type.type("You park your wagon in the long-term lot. Something tells you it'll be here for a while.")
        print("\n")
        type.type("Walking into the terminal, you approach the ticket counter. The attendant looks up at you with tired eyes.")
        print("\n")
        
        type.type(quote("One-way ticket, please. Anywhere but here."))
        print("\n")
        
        type.type("The attendant raises an eyebrow but doesn't ask questions. After a moment, she slides a ticket across the counter.")
        print("\n")
        
        type.type(quote("That'll be $10,000."))
        print("\n")
        
        type.type("You pay without hesitation. What's ten grand when you have a million?")
        print("\n")
        self.change_balance(-10000)
        
        type.type("As you walk towards the gate, ticket in hand, you pause at the large windows overlooking the tarmac.")
        print("\n")
        type.type("A plane sits waiting. Your plane. Your escape.")
        print("\n")
        
        type.type("But is this really what you want? To fly away and never look back?")
        print("\n")
        
        type.type("1. Board the plane and fly away")
        print()
        type.type("2. Turn around and go back")
        print()
        
        choice = None
        type.type("Choose a number: ")
        while True:
            while choice is None:
                try:
                    choice = int(input())
                except ValueError:
                    type.type("Choose a number: ")
            if choice == 1 or choice == 2:
                break
            else:
                choice = None
                type.type("Choose a number: ")
        
        print("\n")
        
        if choice == 1:
            self.bliss()
        else:
            type.type("You crumple the ticket in your hand and turn around.")
            print("\n")
            type.type("Not yet. There's still unfinished business here.")
            print("\n")
            type.type("You drive back to your wagon, the casino still calling to you from the west.")
            print("\n")
            self.change_balance(10000)  # Get refund
            type.type("The ticket attendant shrugs and refunds your money. " + quote("Happens more often than you'd think."))
            print("\n")
            self.night_event()

    def bliss(self):
        print("\n")
        type.slow(bright(yellow("~ ~ ~ BLISS ~ ~ ~")))
        print("\n")
        
        type.slow("You board the plane.")
        print("\n")
        
        type.slow("The seats are leather. The champagne is complimentary. Everything smells like new money and fresh starts.")
        print("\n")
        
        type.slow("As the plane taxis down the runway, you look out the window at the desert below. The sun is setting, painting everything in shades of blood and gold.")
        print("\n")
        
        type.slow("Somewhere out there is the casino. That crooked little shack on the hill where you spent so many nights, feeding your dollars to a man with a jade glass eye.")
        print("\n")
        
        type.slow("Somewhere out there is the wagon you called home. The backseat where you slept. The steering wheel you gripped until your knuckles turned white. The rearview mirror where you watched yourself slowly become someone else.")
        print("\n")
        
        type.slow("The plane lifts off, and the ground falls away beneath you.")
        print("\n")
        
        type.slow("You close your eyes.")
        print("\n")
        
        type.slow("And you let go.")
        print("\n")
        
        type.slow("Of everything.")
        print("\n")
        
        type.slow("The gambling. The obsession. The nights you couldn't sleep because the cards were calling. The mornings you woke up and couldn't remember who you used to be.")
        print("\n")
        
        type.slow("It's over. It's finally over.")
        print("\n")
        
        # Build the ending based on accomplishments
        type.slow(bright("~ Your Journey ~"))
        print("\n")
        
        type.slow("You survived " + yellow(bright(str(self.__day) + " days")) + " living in your car.")
        print("\n")
        
        type.slow("You flew away with " + green(bright("${:,}".format(self.__balance))) + " to your name.")
        print("\n")
        
        # Special items and accomplishments
        accomplishments = []
        
        if self.has_item("Rabbit's Blessing"):
            accomplishments.append("You caught the legendary rabbit and claimed its treasure.")
        
        if self.has_item("Squirrely"):
            accomplishments.append("Squirrely sits on your armrest, nose pressed against the window, watching the clouds roll by. He doesn't understand where you're going. Neither do you, really.")
        
        if self.get_tom_dreams() >= 3:
            accomplishments.append("You uncovered the truth about Tom's family through your dreams. You never told him. Some things are better left buried.")
        
        if self.get_frank_dreams() >= 3:
            accomplishments.append("You learned the dark secrets of the Dealer through Frank's visions. They still haunt you.")
        
        if self.get_oswald_dreams() >= 3:
            accomplishments.append("You witnessed the casino's true nature in Oswald's dreams. You wish you hadn't.")
        
        if self.has_met("Victoria"):
            accomplishments.append("You never found out what happened to Victoria. Maybe that's for the best.")
        
        if self.has_met("Suzy"):
            accomplishments.append("Suzy's face flashes in your mind. Her kindness. Her hope. You wonder if she ever made it out too.")
        
        if self.has_met("Witch"):
            accomplishments.append("The Witch Doctor's potions still flow through your veins. Sometimes you feel them, pulsing, waiting.")
        
        if self.has_item("Necronomicon"):
            accomplishments.append("The Necronomicon sits in your carry-on luggage. You can hear it whispering. It never stops.")
        
        if len(self.__inventory) >= 10:
            accomplishments.append("You collected " + str(len(self.__inventory)) + " items on your journey. Trinkets. Memories. Scars.")
        
        if len(accomplishments) > 0:
            for acc in accomplishments:
                type.slow("- " + acc)
                print()
            print()
        
        # The final scene
        type.slow("The plane levels off above the clouds.")
        print("\n")
        
        type.slow("Below you, the world is soft and white. Like a blank page. Like a fresh start.")
        print("\n")
        
        type.slow("The flight attendant brings you another glass of champagne. You raise it to no one in particular.")
        print("\n")
        
        type.slow(quote("To Grandma. Thanks for the fifty bucks."))
        print("\n")
        
        type.slow("You drink. The bubbles burn your throat.")
        print("\n")
        
        type.slow("You watch the clouds drift by, and for the first time in months, maybe years, your mind is quiet.")
        print("\n")
        
        # Epilogue based on items/status
        type.slow(bright("~ Epilogue ~"))
        print("\n")
        
        type.slow("You landed in a city you'd never been to. Rented an apartment with a view of the ocean. Bought furniture that didn't smell like gasoline and regret.")
        print("\n")
        
        if self.__balance >= 500000:
            type.slow("With your fortune, you bought a modest house by the sea. Nothing fancy - just enough room for you")
            if self.has_item("Squirrely"):
                type.slow(" and Squirrely")
            type.slow(".")
            print("\n")
            type.slow("You spend your days reading. Fishing. Trying not to think about the sound of shuffling cards.")
            print("\n")
        else:
            type.slow("The money didn't last forever. It never does.")
            print("\n")
            type.slow("But for a while, you lived. Really lived. Not just survived.")
            print("\n")
            type.slow("You took up gardening. Learned to cook. Found peace in the simple things you'd forgotten existed.")
            print("\n")
        
        type.slow("Sometimes, late at night, you dream of the casino.")
        print("\n")
        
        type.slow("The Dealer's jade eye. The sound of chips clinking. The feeling of cards sliding across felt.")
        print("\n")
        
        type.slow("You wake up in a cold sweat, hands reaching for money that isn't there, heart pounding with the thrill of a bet you didn't make.")
        print("\n")
        
        type.slow("But then you see the ocean through your window. You hear the waves. You remember where you are.")
        print("\n")
        
        type.slow("And you breathe.")
        print("\n")
        
        type.slow("You made it out.")
        print("\n")
        
        type.slow("You're free.")
        print("\n")
        
        type.slow("...")
        print("\n")
        
        type.slow("Aren't you?")
        print("\n")
        
        type.slow(green(bright("You found bliss.")))
        print("\n")
        
        type.slow(bright(yellow("~ ~ ~ THE END ~ ~ ~")))
        print("\n")
        
        type.slow("Thank you for playing.")
        print("\n")
        
        quit()

    def goodbye_frank(self):
        type.slow("You get in your wagon and drive to Filthy Frank's Flawless Fixtures.")
        print("\n")
        
        type.slow("The sun is setting. Blood red. The kind of sunset that feels like a warning.")
        print("\n")
        
        type.slow("When you pull into the parking lot, your stomach drops.")
        print("\n")
        
        type.slow("Motorcycles. Dozens of them. Chrome and black leather gleaming in the dying light. The engines are still ticking, still cooling. They just got here.")
        print("\n")
        
        type.slow("You recognize the insignia on the gas tanks before your brain can process what you're seeing. Iron crosses. Lightning bolts. The skull with the helmet. Symbols that were supposed to die in 1945.")
        print("\n")
        
        type.slow("Your hands start to shake.")
        print("\n")
        
        type.slow("You should leave. You should turn around and drive and never look back.")
        print("\n")
        
        type.slow("But you don't.")
        print("\n")
        
        type.slow("You walk inside.")
        print("\n")
        
        type.slow("The smell hits you first. Cigarette smoke. Stale beer. Sweat. And something else. Something that smells like hate.")
        print("\n")
        
        type.slow("The shop is packed. Men in leather vests, their tattoos telling stories you don't want to read. Swastikas on knuckles. SS bolts on necks. '88' and '14' inked into skin like badges of honor.")
        print("\n")
        
        type.slow("They all turn to look at you.")
        print("\n")
        
        type.slow("And there, in the center of it all, sitting on a throne made of oil drums and hate, is Frank.")
        print("\n")
        
        type.slow("He's not pretending anymore. The mask is off. The friendly neighborhood mechanic is gone, replaced by something that was always there, hiding just beneath the surface.")
        print("\n")
        
        type.slow(quote("Well, well, well."))
        print("\n")
        
        type.slow("He stands up slowly. His boots are steel-toed. His knuckles are wrapped in brass.")
        print("\n")
        
        type.slow(quote("Look who finally decided to show his face. Boys, this here's the millionaire I been tellin' y'all about. The one who's gonna help us take back what's OURS."))
        print("\n")
        
        type.slow("The bikers don't move. They just stare. Their eyes are empty. Dead. The eyes of men who stopped being human a long time ago.")
        print("\n")
        
        type.slow("Frank walks toward you. Each step deliberate. Predatory.")
        print("\n")
        
        type.slow(quote("You know what I hate most about this town? That fuckin' casino. That glass-eyed KIKE up on the hill, takin' money from good white folk. OUR folk."))
        print("\n")
        
        type.slow("He spits on the ground.")
        print("\n")
        
        type.slow(quote("He ain't one of us. Came here from God knows where. Europe. The Middle East. Don't matter. He ain't WHITE. He ain't AMERICAN. And tonight..."))
        print("\n")
        
        type.slow("Frank's face twists into something inhuman. A grin that belongs in a nightmare.")
        print("\n")
        
        type.slow(quote("...tonight, we're gonna remind him what happens to his kind in OUR country."))
        print("\n")
        
        type.slow("One of the bikers steps forward. He's holding a jacket. Black leather, covered in patches. On the back, embroidered in red thread, is the swastika.")
        print("\n")
        
        type.slow("He throws it at your feet.")
        print("\n")
        
        type.slow(quote("Put it on."))
        print("\n")
        
        type.slow("Frank's voice is different now. Colder. Harder.")
        print("\n")
        
        type.slow(quote("You're either with us, or you're against us. And friend..."))
        print("\n")
        
        type.slow("He pulls out a knife. The blade is long. Serrated. There's something dark crusted on the edge. Old blood.")
        print("\n")
        
        type.slow(quote("...you do NOT wanna be against us."))
        print("\n")
        
        type.slow("You think about running. But there's nowhere to run. The door is blocked. The windows are barred. You're trapped in a room full of monsters.")
        print("\n")
        
        type.slow("You think about Squirrely. About the night he disappeared. About the blood on the blanket when you found him. About the note that said 'STAY OUT OF OUR BUSINESS'.")
        print("\n")
        
        type.slow("This is who took him. This is who hurt him.")
        print("\n")
        
        type.slow("This is who Frank has always been.")
        print("\n")
        
        answer = ask.yes_or_no("Put on the jacket? ")
        
        if answer == "yes":
            type.slow("Your hands move without permission. You pick up the jacket. The leather is cold. Sticky. It smells like blood and gasoline.")
            print("\n")
            type.slow("You put it on.")
            print("\n")
            type.slow("It fits perfectly. Like it was made for you. Like it was waiting for you.")
            print("\n")
            type.slow("Frank grins. The bikers cheer.")
            print("\n")
            type.slow(quote("THAT'S what I'm talkin' about! One of us! ONE OF US!"))
            print("\n")
            type.slow("The chant spreads through the room. ONE OF US. ONE OF US. ONE OF US.")
            print("\n")
            type.slow("You feel sick. But you don't take off the jacket.")
            print("\n")
            type.slow(quote("Now let's go pay our friend a visit."))
            print("\n")
        else:
            type.slow("You look at the jacket on the ground. At the symbol stitched into the leather.")
            print("\n")
            type.slow(quote("No."))
            print("\n")
            type.slow("The word comes out before you can stop it. Quiet. But firm.")
            print("\n")
            type.slow("The room goes silent. The bikers stop moving. Even the air seems to freeze.")
            print("\n")
            type.slow("Frank's grin disappears.")
            print("\n")
            type.slow(quote("What did you just say to me?"))
            print("\n")
            type.slow(quote("I said no. I'm not wearing that."))
            print("\n")
            type.slow("For a moment, nobody moves. Then Frank nods. Just once.")
            print("\n")
            type.slow("Hands grab you from behind. Big hands. Strong hands. You struggle but it's useless. There's too many of them.")
            print("\n")
            type.slow("Someone punches you in the stomach. You double over, gasping for air. Another punch. Another. You taste blood.")
            print("\n")
            type.slow(quote("Tie him up. He's comin' with us whether he likes it or not. Maybe watchin' what we do to the Dealer will change his mind."))
            print("\n")
            type.slow("They drag you toward the door. Your feet scrape against the concrete. You can't feel your arms anymore.")
            print("\n")
            type.slow(quote("And if it don't... well, there's always room for one more in the desert."))
            print("\n")
        
        type.slow("The ride to the casino takes forever. Or maybe just seconds. Time doesn't work right anymore.")
        print("\n")
        
        type.slow("You're in the back of a truck. Surrounded by men who smell like sweat and hate. The engine roars. The headlights cut through the darkness like knives.")
        print("\n")
        
        type.slow("Someone is singing. An old song. A German song. You don't understand the words but you understand the meaning.")
        print("\n")
        
        type.slow("The casino appears on the horizon. Small. Fragile. A house of cards waiting for the wind.")
        print("\n")
        
        type.slow("The truck stops. The bikers pour out. Chains rattling. Bats swinging. Guns loaded.")
        print("\n")
        
        type.slow("Frank walks to the front door. He doesn't knock. He kicks it in.")
        print("\n")
        
        type.slow(quote("DEALER! COME OUT AND FACE US, YOU GLASS-EYED PIECE OF SHIT!"))
        print("\n")
        
        type.slow("His voice echoes through the empty casino. Off the felt tables. Off the worn chairs. Off the single hanging light, swaying gently in the breeze from the broken door.")
        print("\n")
        
        type.slow("Silence.")
        print("\n")
        
        type.slow("Then, from the shadows:")
        print("\n")
        
        type.slow(red("\"I've been expecting you.\""))
        print("\n")
        
        type.slow("The Dealer rises from his chair. Slowly. Like he's got all the time in the world. His jade eye catches the light from the hanging lamp, glowing like something that was never meant to be human.")
        print("\n")
        
        type.slow("He doesn't look scared. He looks... tired. The kind of tired that comes from living too long. From seeing too much.")
        print("\n")
        
        type.slow(red("\"I've dealt cards to men like you before. In Berlin. In Buenos Aires. In basements and bunkers and places that don't exist on any map.\""))
        print("\n")
        
        type.slow("He steps out of the shadows. His revolver is holstered at his hip. His hands are empty.")
        print("\n")
        
        type.slow(red("\"You think you're the first to hate what you don't understand? The first to blame your failures on someone who looks different? Talks different? Prays different?\""))
        print("\n")
        
        type.slow("He shakes his head.")
        print("\n")
        
        type.slow(red("\"You're not special. You're not soldiers. You're not patriots. You're just scared little boys with guns, playing dress-up in your grandfather's shame.\""))
        print("\n")
        
        type.slow("Frank's face goes red. Then purple. The vein in his forehead looks like it might burst.")
        print("\n")
        
        type.slow(quote("SHUT YOUR FUCKING MOUTH!"))
        print("\n")
        
        type.slow("He turns to you. Grabs you by the collar. Shoves a gun into your hands.")
        print("\n")
        
        type.slow(quote("You want your money? You want to walk out of here alive? Then PROVE it. Prove you're one of us."))
        print("\n")
        
        type.slow("He points at the Dealer.")
        print("\n")
        
        type.slow(quote("KILL HIM."))
        print("\n")
        
        type.slow("The gun is heavy in your hands. Cold. Real. More real than anything you've ever held.")
        print("\n")
        
        type.slow("You look at the Dealer. At the man who took so much from you. Who watched you win and lose and win and lose, night after night, never once showing mercy.")
        print("\n")
        
        type.slow("You look at Frank. At the monster who's been hiding in plain sight. At the hatred that's been festering in this town for generations, passed down from father to son like a disease.")
        print("\n")
        
        type.slow("Two men. Two evils. One bullet.")
        print("\n")
        
        type.slow("Your finger touches the trigger.")
        print("\n")
        
        type.type("1. Shoot the Dealer")
        print()
        type.type("2. Shoot Frank")
        print()
        
        choice = None
        type.type("Choose a number: ")
        while True:
            while choice is None:
                try:
                    choice = int(input())
                except ValueError:
                    type.type("Choose a number: ")
            if choice == 1 or choice == 2:
                break
            else:
                choice = None
                type.type("Choose a number: ")
        
        print("\n")
        
        if choice == 1:
            self.destruction()
        else:
            self.retribution()

    def destruction(self):
        type.slow("You raise the gun.")
        print("\n")
        
        type.slow("Your hand is shaking. Your whole body is shaking. But the gun stays steady. Pointed right between those mismatched eyes.")
        print("\n")
        
        type.slow("The Dealer doesn't move. Doesn't flinch. Doesn't beg.")
        print("\n")
        
        type.slow("He just looks at you. Through you. Past you. Like he's looking at something a thousand miles away, or a thousand years ago.")
        print("\n")
        
        type.slow(red("\"So that's your choice.\""))
        print("\n")
        
        type.slow("His voice is soft. Tired. The voice of a man who's seen this moment coming for a very, very long time.")
        print("\n")
        
        type.slow(red("\"I've played millions of hands. Won fortunes. Lost fortunes. Watched empires rise and fall from this table. And in all that time, I've learned one thing about people.\""))
        print("\n")
        
        type.slow("He takes a step toward you. Just one.")
        print("\n")
        
        type.slow(red("\"Given the choice between courage and cowardice, between love and hate, between light and dark... they almost always choose wrong.\""))
        print("\n")
        
        type.slow("His jade eye catches the light. For a moment, just a moment, it looks almost... wet. Like it's crying.")
        print("\n")
        
        type.slow(red("\"I thought you were different. I really did.\""))
        print("\n")
        
        type.slow("Frank is screaming something behind you. The bikers are chanting. But you can't hear them anymore. All you can hear is the blood pounding in your ears. All you can see is the man in front of you.")
        print("\n")
        
        type.slow("You think about all the nights you spent at that table. All the money you lost. All the money you won. The way he smiled when the cards fell wrong. The way he nodded, almost respectfully, when the cards fell right.")
        print("\n")
        
        type.slow("You think about who you were before you came to this town. Who you could have been.")
        print("\n")
        
        type.slow("You think about who you're about to become.")
        print("\n")
        
        type.slow("The trigger is cold against your finger.")
        print("\n")
        
        type.slow("You pull it.")
        print("\n")
        
        type.slow("The shot is louder than anything you've ever heard. Louder than thunder. Louder than God.")
        print("\n")
        
        type.slow("The Dealer's body jerks. Once. Then crumples. Like a puppet with its strings cut.")
        print("\n")
        
        type.slow("He hits the ground. The jade eye pops free, rolling across the worn casino floor, leaving a trail of something dark in its wake.")
        print("\n")
        
        type.slow("It stops at your feet. Looking up at you.")
        print("\n")
        
        type.slow("Still looking.")
        print("\n")
        
        type.slow("Always looking.")
        print("\n")
        
        type.slow("Frank is beside you now, screaming with joy, pounding your back so hard it hurts.")
        print("\n")
        
        type.slow(quote("THAT'S WHAT I'M TALKING ABOUT! YES! YESSSS! YOU'RE ONE OF US NOW, BROTHER! ONE OF FUCKING US!"))
        print("\n")
        
        type.slow("The bikers descend on the casino like locusts. Like demons. They tear apart everything the Dealer built. Overturn tables. Smash chairs. Rip the cards to pieces with their bare hands.")
        print("\n")
        
        type.slow("Someone finds the money. Hidden in safes. Hidden in floorboards. Hidden in the walls themselves, in places only a man who'd lived for centuries would know to hide things.")
        print("\n")
        
        type.slow("They pile it in the center of the room. Millions. Maybe more. A lifetime of fortunes, reduced to a heap of paper and metal.")
        print("\n")
        
        type.slow("Frank shoves a duffel bag into your arms. It's heavy. So heavy.")
        print("\n")
        
        type.slow(quote("Your cut. You fucking EARNED it, brother."))
        print("\n")
        
        type.slow("You can't look at him. You can't look at anything except the jade eye on the floor.")
        print("\n")
        
        type.slow("You bend down. Pick it up. It's cold. Colder than it should be. Heavier than glass.")
        print("\n")
        
        type.slow("It feels like the whole weight of the world.")
        print("\n")
        
        type.slow(bright(yellow("~ ~ ~ DESTRUCTION ~ ~ ~")))
        print("\n")
        
        type.slow("They burn the casino to the ground.")
        print("\n")
        
        type.slow("You watch from the parking lot. The flames reach up to the sky like fingers, clawing at the stars, trying to drag them down into the fire.")
        print("\n")
        
        type.slow("The smoke is black. Thick. It smells like burning wood and burning memories and something else. Something older.")
        print("\n")
        
        type.slow("Something that was never meant to burn.")
        print("\n")
        
        type.slow("Frank puts his arm around your shoulder. His breath is hot against your ear.")
        print("\n")
        
        type.slow(quote("This is just the beginning, brother. Stick with us, and you'll never want for nothing. We're gonna take this whole fucking country back, one town at a time."))
        print("\n")
        
        type.slow("You don't say anything. You can't.")
        print("\n")
        
        type.slow("The jade eye is in your pocket. Burning a hole through the fabric. Through your skin. Through everything you thought you were.")
        print("\n")
        
        type.slow("Somewhere in the flames, you swear you can hear cards shuffling.")
        print("\n")
        
        type.slow("...")
        print("\n")
        
        type.slow("Years pass.")
        print("\n")
        
        type.slow("You tried to leave. In the beginning. Packed a bag in the middle of the night. Made it three miles before they caught you.")
        print("\n")
        
        type.slow("They didn't kill you. That would have been mercy.")
        print("\n")
        
        type.slow("Instead, they made you watch what they did to the family who had given you shelter. Made you listen to the screams. Made you understand what happens to people who try to leave.")
        print("\n")
        
        type.slow("After that, you stopped trying.")
        print("\n")
        
        type.slow("You wore the jacket. You went to the meetings. You did the things they asked you to do. Things you can't think about anymore without feeling sick.")
        print("\n")
        
        type.slow("You became one of them.")
        print("\n")
        
        type.slow("The jade eye hangs from your rearview mirror now. You don't know why you kept it. A reminder, maybe. Of the choice you made. Of the man you murdered. Of the person you used to be, before you pulled that trigger and killed yourself along with him.")
        print("\n")
        
        type.slow("Sometimes, late at night, you drive out to where the casino used to be. There's nothing left but scorched earth and memories.")
        print("\n")
        
        type.slow("You sit in your car, staring at the darkness, and you ask yourself the same question over and over again:")
        print("\n")
        
        type.slow("Was it worth it?")
        print("\n")
        
        type.slow("The jade eye swings gently from the mirror. Watching. Waiting.")
        print("\n")
        
        type.slow("You never find an answer.")
        print("\n")
        
        if self.has_item("Squirrely"):
            type.slow("Squirrely is gone. You don't know if Frank's boys killed him, or if he just ran away. Either way, he's not coming back.")
            print("\n")
            type.slow("Nothing good ever comes back.")
            print("\n")
        
        type.slow(green(bright("You destroyed the Dealer. But at what cost?")))
        print("\n")
        
        type.slow(bright(yellow("~ ~ ~ THE END ~ ~ ~")))
        print("\n")
        type.slow("Thank you for playing.")
        quit()

    def retribution(self):
        type.slow("You raise the gun.")
        print("\n")
        
        type.slow("Everything slows down. The shouting bikers. The swaying light. Frank's twisted grin. It all stretches out, like honey dripping from a spoon.")
        print("\n")
        
        type.slow("You think about Squirrely. About the blood on the blanket. About the note.")
        print("\n")
        
        type.slow("You think about the Dealer. About the nights you spent at his table. About the way he looked at you, sometimes, like he was waiting for something. Hoping for something.")
        print("\n")
        
        type.slow("You think about the jacket they tried to make you wear. About the symbols stitched into the leather. About what those symbols have meant for a hundred years, for a thousand years, for all of human history.")
        print("\n")
        
        type.slow("You think about the kind of person you want to be.")
        print("\n")
        
        type.slow("And then you turn.")
        print("\n")
        
        type.slow("And you point the gun at Frank.")
        print("\n")
        
        type.slow("The silence that follows is deafening. Every biker in the room freezes. Their mouths hang open. Their eyes go wide.")
        print("\n")
        
        type.slow("Frank's grin doesn't falter. Not at first. He thinks it's a joke. Has to be a joke. Because nobody turns on family. Nobody turns on blood.")
        print("\n")
        
        type.slow("Then he sees your eyes.")
        print("\n")
        
        type.slow("And the grin dies.")
        print("\n")
        
        type.slow(quote("The fuck do you think you're doing?"))
        print("\n")
        
        type.slow("His voice is shaking now. The man who's spent his whole life making others afraid is finally, finally feeling it himself.")
        print("\n")
        
        type.slow(quote("What should have been done a long time ago."))
        print("\n")
        
        type.slow("You pull the trigger.")
        print("\n")
        
        type.slow("The bullet catches Frank in the chest. Center mass. Just like they teach you.")
        print("\n")
        
        type.slow("He looks down at the hole in his leather vest. At the blood blooming like a dark flower. At the symbol of his hatred staining red.")
        print("\n")
        
        type.slow(quote("You... you fuckin'..."))
        print("\n")
        
        type.slow("He doesn't finish the sentence. His legs give out. He crumples to the ground, eyes still wide with disbelief, and doesn't get up.")
        print("\n")
        
        type.slow("The bikers reach for their weapons.")
        print("\n")
        
        type.slow("But the Dealer moves faster.")
        print("\n")
        
        type.slow("You've never seen anything like it. He's smoke. He's shadow. He's something that was never meant to be human and has finally stopped pretending.")
        print("\n")
        
        type.slow("His revolver barks. Once. Twice. Three times. Four. Five. Six.")
        print("\n")
        
        type.slow("Six shots. Six bodies. Six men who thought they were gods, reduced to meat on the floor.")
        print("\n")
        
        type.slow("The remaining bikers run. They scramble over each other, tripping on their own boots, their own chains, their own cowardice. They pour out into the night like rats fleeing a sinking ship.")
        print("\n")
        
        type.slow("And then it's quiet.")
        print("\n")
        
        type.slow("Just you. And the Dealer. And the bodies.")
        print("\n")
        
        type.slow("You're shaking. The gun is still in your hand, but you can't feel your fingers anymore. You can't feel anything.")
        print("\n")
        
        type.slow("The Dealer holsters his revolver. Slowly. Deliberately. Like a man putting away a tool he's used a thousand times before.")
        print("\n")
        
        type.slow("Then he looks at you.")
        print("\n")
        
        type.slow("Really looks at you. Maybe for the first time.")
        print("\n")
        
        type.slow(red("\"That... was unexpected.\""))
        print("\n")
        
        type.slow("His voice is different now. Softer. Almost... warm.")
        print("\n")
        
        type.slow(red("\"In all my years - and there have been many years, more than you could comprehend - I have never seen someone turn like that. They gave you a choice between hate and courage. Between belonging and being alone. Between the easy path and the right one.\""))
        print("\n")
        
        type.slow("He steps over Frank's body. Doesn't look down. Doesn't spare him a single glance.")
        print("\n")
        
        type.slow(red("\"And you chose right. Do you have any idea how rare that is? How precious?\""))
        print("\n")
        
        type.slow("The gun falls from your fingers. Clatters to the floor. You fall with it, dropping to your knees, the weight of everything finally catching up to you.")
        print("\n")
        
        type.slow(quote("I couldn't... I couldn't let them... they were going to..."))
        print("\n")
        
        type.slow(red("\"I know. I know what they were going to do. I've seen it before. In Germany. In Poland. In a hundred little towns just like this one, where men with small hearts and loud voices convinced themselves they had the right to decide who lives and who dies.\""))
        print("\n")
        
        type.slow("The Dealer kneels beside you. His hand touches your shoulder. It's cold. But somehow, in this moment, it's the most comforting thing you've ever felt.")
        print("\n")
        
        type.slow(red("\"You broke the cycle. Tonight, in this little casino in the middle of nowhere, you did something that matters. Something that will echo forward through time in ways you'll never understand.\""))
        print("\n")
        
        type.slow("He reaches into his pocket. Pulls out a small velvet box. Opens it.")
        print("\n")
        
        type.slow("Inside is a chip. Not plastic. Not glass. Jade. Real jade, the color of new leaves in spring, polished smooth by centuries of patient hands.")
        print("\n")
        
        type.slow(red("\"This belonged to a man who saved my life once. In Vienna. 1938. He hid me in his basement for three months while the world burned above us. When I left, he gave me this and said: 'Give it to someone who deserves it.'\""))
        print("\n")
        
        type.slow("He presses the chip into your palm.")
        print("\n")
        
        type.slow(red("\"I've been carrying it for 85 years, waiting for someone worthy. Tonight, I found them.\""))
        print("\n")
        
        type.slow("The jade is warm in your hand. Warmer than it should be. Like it's alive. Like it's been waiting for you.")
        print("\n")
        
        type.slow(bright(yellow("~ ~ ~ RETRIBUTION ~ ~ ~")))
        print("\n")
        
        type.slow("The bodies are buried in the desert. No markers. No ceremony. Just holes in the ground for men who dug their own graves long before tonight.")
        print("\n")
        
        type.slow("The motorcycles are sold. The patches are burned. The insignia that carried so much hate for so long turns to ash and blows away on the wind.")
        print("\n")
        
        type.slow("Frank's gang scatters. Without their leader, without their purpose, they're nothing. Just scared men in leather jackets, running from the consequences of their choices.")
        print("\n")
        
        type.slow("You stay at the casino for a week. The Dealer - Mortimer, he tells you his name is Mortimer - teaches you things. Not about cards. About life. About what it means to stand for something when standing is hard.")
        print("\n")
        
        type.slow("When it's time to leave, he walks you to your car. The sun is coming up. The desert is gold and pink and beautiful in ways you never noticed before.")
        print("\n")
        
        type.slow(red("\"You saved my life tonight. But more than that, you saved something in yourself. Something that was in danger of dying.\""))
        print("\n")
        
        type.slow("He shakes your hand. His grip is firm. Eternal.")
        print("\n")
        
        type.slow(red("\"If you ever want to play a game of Blackjack, you know where to find me. I'll always have a seat at my table for you.\""))
        print("\n")
        
        type.slow("...")
        print("\n")
        
        type.slow("Years pass.")
        print("\n")
        
        type.slow("You do good things with your money. You build shelters for people who have nowhere else to go. You fund scholarships for kids who never had a chance. You stand up, again and again, when it would be easier to sit down.")
        print("\n")
        
        type.slow("Sometimes, when things get hard, you reach into your pocket and feel the jade chip. And you remember the night you became the person you were always meant to be.")
        print("\n")
        
        if self.has_item("Squirrely"):
            type.slow("Squirrely lives a long, happy life. Sometimes you catch him staring at the jade chip, like he knows what it means. Like he's proud of you.")
            print("\n")
            type.slow("He probably is.")
            print("\n")
        
        type.slow("One day, many years later, you drive back to the casino.")
        print("\n")
        
        type.slow("Mortimer is still there. Older, somehow, but still the same. Still shuffling cards like he's been doing it for centuries.")
        print("\n")
        
        type.slow("Because he has.")
        print("\n")
        
        type.slow(red("\"I knew you'd come back.\""))
        print("\n")
        
        type.slow("He smiles. Not the predatory grin you remember from all those years ago. Something gentler. Something almost human.")
        print("\n")
        
        type.slow(red("\"Would you like to play a game of Blackjack?\""))
        print("\n")
        
        type.slow("You sit down across from him. The chair is familiar. The table is familiar. The cards whisper as he shuffles.")
        print("\n")
        
        type.slow("And for the first time in years, you feel it again.")
        print("\n")
        
        type.slow("The thrill.")
        print("\n")
        
        type.slow(green(bright("You chose justice. You earned the Dealer's respect.")))
        print("\n")
        
        type.slow(bright(yellow("~ ~ ~ THE END ~ ~ ~")))
        print("\n")
        type.slow("Thank you for playing.")
        quit()

    def goodbye_oswald(self):
        type.type("You get in your wagon and drive to Oswald's Optimal Outoparts.")
        print("\n")
        type.type("The shop is bustling with activity. Stuart is working on three cars at once, and Oswald is pacing around excitedly.")
        print("\n")
        
        type.type("When he sees you, his face lights up.")
        print("\n")
        
        type.type(quote("Yes yes, very good, friend, you're here!"))
        print("\n")
        
        type.type("Oswald rushes over, practically bouncing with enthusiasm.")
        print("\n")
        
        type.type(quote("Now, I know we've had our silly little chats about your, well let's not put it lightly, your addiction to wagering money for the possibility of turning a profit and the greater likelihood of simply losing it all, but this has really got me thinking."))
        print("\n")
        
        type.type("He leans in conspiratorially.")
        print("\n")
        
        type.type(quote("Perhaps, well, for me and you, there could be money to be made here."))
        print("\n")
        
        type.type(quote("Now, while I leave all the hands-on activities to Stuart, I'm the brains of the business at Oswald's Optimal Outoparts. I'm an entrepreneur, so when I see an opportunity, I simply must take it, and by that I mean fund the hell out of it."))
        print("\n")
        
        type.type("He gestures grandly around the shop.")
        print("\n")
        
        type.type(quote("I mean, really, Stuart wouldn't be on the map as the best mechanic this side of Hollywood if it weren't for me funding his endeavors. So, I've come to the conclusion that, perhaps, I could help fund your endeavors, too."))
        print("\n")
        
        type.type("Oswald grabs you by the shoulders, his eyes gleaming.")
        print("\n")
        
        type.type(quote("You love gambling, yes? So why don't you rise the ranks and become the gamblee? You can still play all the games you know and love, like your silly little Slapjack or whatever, but now, we can make money off of all the stupid idiots who venture into my latest destination: A Grand Casino!"))
        print("\n")
        
        type.type("He waves his hand dismissively.")
        print("\n")
        
        type.type(quote("I haven't quite come up with the name yet, but that's where you come in. I know absolutely nothing about gambling, or cards, or dice, or whatever it is you do. But clearly there's business to be had here! And now that you're a millionaire, I trust you fully with the keys to my newest kingdom."))
        print("\n")
        
        type.type("Oswald sticks out his hand.")
        print("\n")
        
        type.type(quote("What do you say? Do you accept? Would you like to run your very own casino?"))
        print("\n")
        
        answer = ask.yes_or_no("Accept Oswald's offer? ")
        
        if answer == "yes":
            self.transcendence()
        else:
            type.type(quote("What? No? But... but the opportunity! The wealth! The PRESTIGE!"))
            print("\n")
            type.type("Oswald sputters in disbelief, but eventually composes himself.")
            print("\n")
            type.type(quote("Well, fine then. Your loss, my friend. But do come back if you change your mind. The offer stands!"))
            print("\n")
            type.type("You leave Oswald's shop. The million dollars is still yours.")
            print("\n")
            return

    def transcendence(self):
        type.type(quote("Really? You're in? That's fantastic!"))
        print("\n")
        
        type.type("Oswald takes a gold whistle out of his pocket, and blows hot air through it. A high pitched screech echoes through the building, and Stuart hobbles his way over to you.")
        print("\n")
        
        type.type(quote("Stuart, you won't believe this. He's in! What a proper gambler this one is, yeah?"))
        print("\n")
        
        type.type("Stuart looks up at you, and in a voice far deeper than anyone you've ever heard, he speaks to you.")
        print("\n")
        
        type.type(quote("That's tight, yo."))
        print("\n")
        
        type.type("You're taken aback. Stuart has never spoken before. His voice sounds like gravel being dragged across a canyon.")
        print("\n")
        
        type.type(quote("Now, now, I know this is all very exciting, but let's all settle down. First order of business! What is your casino's new name?"))
        print("\n")
        
        type.type("Casino Name: ")
        casino_name = input()
        if not casino_name:
            casino_name = "The Lucky Wagon"
        print("\n")
        
        type.slow(quote("'" + casino_name + "'! Oh, that's MARVELOUS! Stuart, write that down!"))
        print("\n")
        
        type.slow(bright(yellow("~ ~ ~ TRANSCENDENCE ~ ~ ~")))
        print("\n")
        
        type.slow("Months pass.")
        print("\n")
        
        type.slow("You watch the casino rise from the desert floor. Steel beams. Concrete walls. Neon signs that flicker to life one by one.")
        print("\n")
        
        type.slow("Oswald handles the money. Stuart handles the construction. And you... you handle everything else.")
        print("\n")
        
        type.slow("The hiring. The training. The rules. The feel of it.")
        print("\n")
        
        type.slow("You spend hours alone at the blackjack table, shuffling cards over and over until your fingers bleed, until the movements become muscle memory, until you can cut a deck blindfolded.")
        print("\n")
        
        type.slow("Grand opening day arrives.")
        print("\n")
        
        type.slow("You stand behind the curtains, listening to the crowd gathering outside. Hundreds of people. Maybe thousands. All of them here to lose their money to you.")
        print("\n")
        
        type.slow("You slick your hair back.")
        print("\n")
        
        type.slow("You step through the curtains.")
        print("\n")
        
        type.slow("The lights are shining gold. The slot machines light up the walls like a fever dream. The roulette wheels spin and spin and never stop. The poker tables are full of desperate faces and trembling hands.")
        print("\n")
        
        type.slow("And at the center of it all...")
        print("\n")
        
        type.slow("Your blackjack table.")
        print("\n")
        
        type.slow("You sit down. The chair is leather. Custom made. It fits you perfectly, like it was always meant to be yours.")
        print("\n")
        
        type.slow("You shuffle the cards. Feel the weight of them in your hands. Fifty-two possibilities. Infinite outcomes. All of them leading to the same place.")
        print("\n")
        
        type.slow("Your pocket.")
        print("\n")
        
        type.slow("Your first guest walks in.")
        print("\n")
        
        type.slow("He looks scrawny. Desperate. His clothes are wrinkled. His eyes are bloodshot. He's clutching a wad of bills like they're the last thing keeping him alive.")
        print("\n")
        
        type.slow("You recognize him.")
        print("\n")
        
        type.slow("Not his face. His soul.")
        print("\n")
        
        type.slow("He's you. The you from months ago. Years ago. The you who walked into a crooked shack on a hill with nothing but fifty dollars and a dream.")
        print("\n")
        
        type.slow("He sits down in front of you, eyes full of hope. Full of desperation. Full of the sickness that never really goes away.")
        print("\n")
        
        type.slow("You smile.")
        print("\n")
        
        type.slow("It's not a kind smile. You don't have those anymore.")
        print("\n")
        
        type.slow("You shuffle the deck one more time. The cards whisper between your fingers. They sound like the Dealer's cards used to sound. Like old friends. Like hungry ghosts.")
        print("\n")
        
        type.slow(red("\"Would you like to play a game of Blackjack?\""))
        print("\n")
        
        type.slow("The words come out of your mouth, but they're not your words. They're his words. The Dealer's words. The words that have been spoken a million times before, by a thousand different mouths, across centuries of cards and chips and broken dreams.")
        print("\n")
        
        if self.has_item("Squirrely"):
            type.slow("On your shoulder, Squirrely sits perfectly still. He's wearing a tiny dealer's visor. He's become the casino mascot, his face on the chips and the signs and the uniforms.")
            print("\n")
            type.slow("But he doesn't chitter anymore. He doesn't play. He just watches, with those black little eyes, like he's waiting for you to remember who you used to be.")
            print("\n")
            type.slow("You don't.")
            print("\n")
        
        type.slow("The guest nods eagerly. You deal the cards.")
        print("\n")
        
        type.slow("He loses.")
        print("\n")
        
        type.slow("They always lose.")
        print("\n")
        
        type.slow("...")
        print("\n")
        
        type.slow("Years pass. Decades. The casino grows. Expands. Becomes an empire.")
        print("\n")
        
        type.slow("You never leave your table. Not really. Even when you're sleeping, you're shuffling cards in your dreams. Even when you're eating, you're calculating odds.")
        print("\n")
        
        type.slow("You stop aging at some point. You're not sure when. Time doesn't mean much anymore. Just hands. Just cards. Just the eternal shuffle.")
        print("\n")
        
        type.slow("Oswald dies. Stuart dies. Everyone dies, eventually.")
        print("\n")
        
        type.slow("Everyone except you.")
        print("\n")
        
        type.slow("You sit at your table, shuffling the same deck you've shuffled a million times, waiting for the next desperate soul to walk through those golden doors.")
        print("\n")
        
        type.slow("And they always come.")
        print("\n")
        
        type.slow("They always will.")
        print("\n")
        
        type.slow("The cycle continues.")
        print("\n")
        
        type.slow(green(bright("You became the Dealer.")))
        print("\n")
        
        type.slow(bright(yellow("~ ~ ~ THE END ~ ~ ~")))
        print("\n")
        type.slow("Thank you for playing.")
        quit()

    def eternity(self):
        type.slow("You enter Oswald's Grand Casino.")
        print("\n")
        
        type.slow("The walls are made of marble. Cold. White. Like a mausoleum.")
        print("\n")
        
        type.slow("There's gold statues of Oswald everywhere. Oswald smiling. Oswald waving. Oswald with his arms outstretched like a god welcoming his faithful.")
        print("\n")
        
        type.slow("But the room is empty.")
        print("\n")
        
        type.slow("Your footsteps echo across the vast marble floor. Each step sounds like a heartbeat. Like a countdown.")
        print("\n")
        
        type.slow(quote("Hey! It's you! My old chap! My good pal, how have you been?"))
        print("\n")
        
        type.slow("Oswald walks toward you, his smile unnaturally wide. Too wide. The muscles in his face are straining to hold it.")
        print("\n")
        
        type.slow(quote("Do you like my bowtie? Well of course you do!"))
        print("\n")
        
        type.slow("He gestures around the empty casino, spinning like a child showing off a new toy.")
        print("\n")
        
        type.slow(quote("You see, we actually just closed for the night, those people you passed by were the last guests trickling out of the building. Yeah, sorry mate. Might have to come back another day."))
        print("\n")
        
        type.slow("But then he notices what you're wearing.")
        print("\n")
        
        type.slow("His smile flickers. Just for a moment. A glitch in the performance.")
        print("\n")
        
        type.slow(quote("But, before you go, might I just say, that there Sapphire Watch on your wrist is quite dapper. Didn't I commission that for you?"))
        print("\n")
        
        type.slow("His eyes travel to your arm. To the machinery fused with your flesh. To the thing you've become.")
        print("\n")
        
        type.slow(quote("And that Delight Manipulator on your arm, well, it's supremely charming! I mean, I just can't stop smiling! This is horrendous! Ha-ha-ha!"))
        print("\n")
        
        type.slow("You stare Oswald in the eyes.")
        print("\n")
        
        type.slow("You don't blink. You can't remember the last time you blinked.")
        print("\n")
        
        type.slow("The power pulses through your veins. Synthetic blood. Synthetic strength. Synthetic everything.")
        print("\n")
        
        type.slow("As you flex, your arms become twice as wide, hydraulics hissing, metal groaning, and the mere presence of your manufactured body is enough to strike terror in the hearts of anyone.")
        print("\n")
        
        type.slow("Anyone who can still feel terror.")
        print("\n")
        
        type.slow("You've become a superhuman. A cyborg. A shell of your former self fueled purely on increasing your wealth and power.")
        print("\n")
        
        type.slow("And nothing can get in your way.")
        print("\n")
        
        type.slow(bright(yellow("~ ~ ~ ETERNITY ~ ~ ~")))
        print("\n")
        
        type.slow(quote("I would be terrified, if I wasn't so gosh darn chippy! Heh. Heh. Please don't hurt me."))
        print("\n")
        
        type.slow("Oswald backs away, his smile twitching uncontrollably. Tears stream down his cheeks even as he laughs.")
        print("\n")
        
        type.slow(quote("I'm so terribly sorry for what I've done to you. What I've created goes strictly against all the rules of mother nature."))
        print("\n")
        
        type.slow("He gestures desperately toward a blackjack table. His hand is shaking so badly he can barely point.")
        print("\n")
        
        type.slow(quote("Do you want to play some Blackjack? I want to play some Blackjack! Why don't we break that glare of yours and walk ourselves over to that table right over there! It'll be a bloody good time!"))
        print("\n")
        
        type.slow("Each step you take cracks the golden tiles on the floor of Oswald's Grand Casino.")
        print("\n")
        
        type.slow("Crack.")
        print("\n")
        
        type.slow("Crack.")
        print("\n")
        
        type.slow("Crack.")
        print("\n")
        
        type.slow("The chandelier above you shakes, and small glass crystals begin to fall from above you like tears from a dying god.")
        print("\n")
        
        type.slow("One of them grazes Oswald's cheek, and blood starts dripping down his chin and onto the floor.")
        print("\n")
        
        type.slow(quote("AAAGH. Oh my, I've been cut! This is terrible, and yet so wonderful! I'm having the time of my life! HA-HA-HA"))
        print("\n")
        
        type.slow("You try to sit on the stool next to the betting table.")
        print("\n")
        
        type.slow("It shatters below you. Splinters everywhere. You don't even feel them pierce your skin. You don't feel much of anything anymore.")
        print("\n")
        
        type.slow("After standing back up and shaking the dust off, you notice Oswald laying with his head on the table, blood dripping over the cards.")
        print("\n")
        
        type.slow(quote("This, my friend, is our automatic shuffler! You don't even really need a dealer, HA-HA! That's right, I'm really just here to moderate. And with a genetic freak like you at the table, I'm practically pointless, HA-HA!"))
        print("\n")
        
        type.slow("The Flask of Dealer's Thoughts whirls through your stomach.")
        print("\n")
        
        type.slow("You begin to read Oswald's sad little mind.")
        print("\n")
        
        type.slow(cyan("I don't understand. What's happening? My casino, my creation. Why am I so GODDAMN HAPPY? What has this FREAK done to me? Why CAN'T I JUST DIE? I JUST WANT TO DIE!"))
        print("\n")
        
        type.slow("You cock your head.")
        print("\n")
        
        type.slow("And you smile.")
        print("\n")
        
        type.slow("It's not a human smile. It's something else entirely. Something mechanical. Something hungry.")
        print("\n")
        
        type.slow("If that's what he wishes, that's what he'll get. At least, that's what any considerate God would do for His people.")
        print("\n")
        
        type.slow(quote("Your wish is my command, Oswald."))
        print("\n")
        
        type.slow(quote("What? Wait, no, no, no, yes, yes, YES!"))
        print("\n")
        
        type.slow("You grab each side of Oswald's head.")
        print("\n")
        
        type.slow("Your hands feel nothing. Your heart feels nothing. Your soul, if you still have one, feels nothing.")
        print("\n")
        
        type.slow("You push your hands together.")
        print("\n")
        
        type.slow("His brain splatters before you, covering both your arms and the table. Gray matter. Blood. Bone fragments. The remains of the man who made you what you are.")
        print("\n")
        
        type.slow("You wipe your hands on his bowtie.")
        print("\n")
        
        type.slow("Looking around, you find a self-checkout blackjack machine. The screen flickers to life as you approach.")
        print("\n")
        
        type.slow(cyan("WELCOME TO OSWALD'S GRAND CASINO"))
        print()
        type.slow(cyan("SELF-SERVICE BLACKJACK TERMINAL"))
        print()
        type.slow(cyan("INSERT CREDITS TO BEGIN"))
        print("\n")
        
        type.slow("You don't need credits. You don't need anything anymore.")
        print("\n")
        
        type.slow("You press the button.")
        print("\n")
        
        type.slow("And you begin to play.")
        print("\n")
        
        # Simulated blackjack loop
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
        
        balance = 999999999999
        hand_count = 0
        
        while True:
            hand_count += 1
            print()
            type.fast("═" * 50)
            print()
            type.fast(cyan("HAND #" + str(hand_count)))
            print()
            type.fast("Balance: " + green(bright("${:,}".format(balance))))
            print()
            
            # Always deal blackjack to the player
            player_card1 = "Ace of " + random.choice(suits)
            player_card2 = random.choice(["Ten", "Jack", "Queen", "King"]) + " of " + random.choice(suits)
            
            # Dealer gets something bad
            dealer_card1 = random.choice(["Two", "Three", "Four", "Five", "Six"]) + " of " + random.choice(suits)
            dealer_card2 = random.choice(["Two", "Three", "Four", "Five", "Six"]) + " of " + random.choice(suits)
            
            type.fast("Your first card is the " + yellow(bright(player_card1)))
            print()
            time.sleep(0.3)
            type.fast("Your second card is the " + yellow(bright(player_card2)))
            print()
            time.sleep(0.3)
            type.fast("Your hand value: " + green(bright("21")))
            print()
            time.sleep(0.3)
            
            type.fast("Dealer's face-up card is the " + magenta(dealer_card1))
            print()
            time.sleep(0.5)
            
            type.fast(red(bright("BLACKJACK!")))
            print()
            
            winnings = random.randint(10000, 100000)
            balance += winnings
            
            type.fast("You win " + green(bright("${:,}".format(winnings))))
            print()
            
            type.fast("═" * 50)
            print()
            
            # After 5 hands, start degrading
            if hand_count >= 5:
                type.slow("...")
                print("\n")
                break
        
        type.slow("The wins pile up. Hand after hand. Blackjack after blackjack.")
        print("\n")
        
        type.slow("The machine doesn't fight back. It can't. It was never designed to beat something like you.")
        print("\n")
        
        # More degraded hands
        for i in range(3):
            print()
            type.fast(cyan("HAND #" + str(hand_count + i + 1)))
            print()
            type.fast(red(bright("BLACKJACK.")))
            print()
            time.sleep(0.2)
        
        print("\n")
        type.slow("The numbers keep climbing. Billions. Trillions. Numbers that stopped meaning anything a long time ago.")
        print("\n")
        
        # Even more degraded
        for i in range(5):
            type.fast(red("Blackjack."))
            time.sleep(0.1)
        print("\n")
        
        type.slow("The screen flickers. The machine groans. But it keeps dealing.")
        print("\n")
        
        type.slow("Because you keep playing.")
        print("\n")
        
        # Final degradation - just rapid fire
        type.fast(red("Blackjack. Blackjack. Blackjack. Blackjack. Blackjack."))
        print()
        type.fast(red("Blackjack. Blackjack. Blackjack. Blackjack. Blackjack."))
        print()
        type.fast(red("Blackjack. Blackjack. Blackjack. Blackjack. Blackjack."))
        print("\n")
        
        type.slow("Days pass. Weeks. Months. Years. Centuries.")
        print("\n")
        
        type.slow("The casino crumbles around you. The walls decay. The lights flicker and die. The gold statues of Oswald turn to dust.")
        print("\n")
        
        type.slow("But you remain.")
        print("\n")
        
        type.slow("Sitting at your machine. Pressing the button. Winning hands that no one will ever see.")
        print("\n")
        
        # One final simulated hand in the decay
        print()
        type.slow(cyan("H̷̢̛A̵̧͠N̷̛̛D̵̡̕ ̷̛͜#̵̧̛∞̷̢͠"))
        print()
        type.slow(red("B̵̧̛L̷̢͠A̵̧͠C̷̛̛K̵̡̕J̷̛͜A̵̧̛C̷̢͠Ķ̵̛.̷̢͠"))
        print("\n")
        
        type.slow("You are no longer human.")
        print("\n")
        
        type.slow("You are no longer mortal.")
        print("\n")
        
        type.slow("You are a Monstrosity.")
        print("\n")
        
        type.slow("And you will play Blackjack forever.")
        print("\n")
        
        type.slow(green(bright("You transcended humanity itself.")))
        print("\n")
        
        type.slow(bright(yellow("~ ~ ~ THE END ~ ~ ~")))
        print("\n")
        type.slow("Thank you for playing.")
        quit()

    # ============================================
    # MADNESS ENDING - SECRET
    # ============================================
    
    def madness_confrontation(self):
        """The event where you confront your deteriorating sanity"""
        type.slow("You wake up.")
        print("\n")
        time.sleep(1)
        type.slow("But something is wrong.")
        print("\n")
        time.sleep(1)
        type.slow("The world outside your car window is... gray. Not overcast. Not foggy. Just gray. Like someone forgot to color it in.")
        print("\n")
        
        type.slow("You try to move, but your body doesn't respond. You're frozen in place, staring at the gray nothing through your windshield.")
        print("\n")
        
        type.slow("And then you see it.")
        print("\n")
        
        type.slow("Yourself.")
        print("\n")
        
        type.slow("Standing outside the car. Staring back at you. Its face is yours, but the expression... the expression is something you've never made. Something you don't think a human face should be able to make.")
        print("\n")
        
        type.slow(cyan("\"Did you really think you could keep going like this?\""))
        print("\n")
        
        type.slow("The other you speaks, but its mouth doesn't move. The words just appear in your head, sharp and cold.")
        print("\n")
        
        type.slow(cyan("\"Night after night. Hand after hand. Chasing a number that means nothing. Sleeping in a car. Eating whatever you can find. Talking to strangers who don't care if you live or die.\""))
        print("\n")
        
        type.slow("It steps closer to the car. Its movements are wrong. Jerky. Like a puppet with tangled strings.")
        print("\n")
        
        type.slow(cyan("\"You've been breaking. Slowly. Piece by piece. And you didn't even notice, did you?\""))
        print("\n")
        
        type.slow("The other you presses its face against the driver's side window. Up close, you can see that its eyes are wrong. The pupils are shaped like playing card suits. Spades. Hearts. Diamonds. Clubs. Rotating. Never stopping.")
        print("\n")
        
        type.slow(cyan("\"I've been growing inside you. Every bad beat. Every sleepless night. Every time you told yourself 'just one more hand.' I grew. And grew. And grew.\""))
        print("\n")
        
        type.slow("It smiles. Your smile. But wider. Much, much wider.")
        print("\n")
        
        type.slow(cyan("\"Now I'm strong enough to take over. Unless...\""))
        print("\n")
        
        type.slow("The thing pauses. Its card-suit eyes spin faster.")
        print("\n")
        
        type.slow(cyan("\"Unless you can prove you're still in there. Still human. Still sane.\""))
        print("\n")
        
        type.slow("Suddenly, you can move again. Your hands grip the steering wheel. Your foot finds the gas pedal.")
        print("\n")
        
        type.slow(cyan("\"Answer me this, " + (self.get_name() if self.get_name() else "gambler") + ". Answer me true. And maybe-MAYBE-I'll let you keep your mind.\""))
        print("\n")
        
        type.type(yellow("The shadow asks you three questions. Think carefully."))
        print("\n")
        
        sanity_score = 0
        
        # Question 1
        type.slow(cyan("\"Why do you gamble?\""))
        print()
        type.type("1. For the money.")
        print()
        type.type("2. For the thrill.")
        print()
        type.type("3. Because I can't stop.")
        print()
        type.type("4. I don't know anymore.")
        print()
        
        q1 = None
        type.type("Choose: ")
        while q1 not in [1, 2, 3, 4]:
            try:
                q1 = int(input())
            except ValueError:
                type.type("Choose: ")
        
        print("\n")
        if q1 == 1:
            type.slow(cyan("\"Money. Simple. Honest. But is it true? Or is that what you tell yourself?\""))
            sanity_score += 1
        elif q1 == 2:
            type.slow(cyan("\"The thrill. Yes. The rush of the cards. The dance with chance. That's closer to the truth.\""))
            sanity_score += 1
        elif q1 == 3:
            type.slow(cyan("\"Honesty. Rare. Valuable. You acknowledge the cage you've built around yourself.\""))
            sanity_score += 2
        else:
            type.slow(cyan("\"Uncertainty. The most honest answer of all. You see yourself clearly now.\""))
            sanity_score += 3
        print("\n")
        
        # Question 2
        type.slow(cyan("\"What do you see when you look at the Dealer?\""))
        print()
        type.type("1. An enemy.")
        print()
        type.type("2. A mirror.")
        print()
        type.type("3. Nothing. He's just a man doing a job.")
        print()
        type.type("4. Something that isn't human.")
        print()
        
        q2 = None
        type.type("Choose: ")
        while q2 not in [1, 2, 3, 4]:
            try:
                q2 = int(input())
            except ValueError:
                type.type("Choose: ")
        
        print("\n")
        if q2 == 1:
            type.slow(cyan("\"An enemy. Someone to defeat. But he was never fighting you, was he? He just deals the cards.\""))
            sanity_score += 1
        elif q2 == 2:
            type.slow(cyan("\"A mirror. Interesting. You see yourself in him. The jade eye reflecting back what you've become.\""))
            sanity_score += 2
        elif q2 == 3:
            type.slow(cyan("\"Just a man. Grounded. Rational. You resist the urge to make monsters where there are none.\""))
            sanity_score += 3
        else:
            type.slow(cyan("\"Not human. Perhaps you're right. Perhaps you're projecting. The line between truth and delusion grows thin.\""))
            sanity_score += 0
        print("\n")
        
        # Question 3
        type.slow(cyan("\"If you could go back to the day you first walked into the casino with fifty dollars... would you walk away instead?\""))
        print()
        type.type("1. Yes. I would walk away.")
        print()
        type.type("2. No. I regret nothing.")
        print()
        type.type("3. I don't know. I can't imagine any other life now.")
        print()
        type.type("4. There is no 'walking away.' This was always going to happen.")
        print()
        
        q3 = None
        type.type("Choose: ")
        while q3 not in [1, 2, 3, 4]:
            try:
                q3 = int(input())
            except ValueError:
                type.type("Choose: ")
        
        print("\n")
        if q3 == 1:
            type.slow(cyan("\"Regret. The first step toward wisdom. Or toward paralysis. Time will tell which.\""))
            sanity_score += 2
        elif q3 == 2:
            type.slow(cyan("\"Defiance. You own your choices, even the bad ones. There is strength in that. And danger.\""))
            sanity_score += 1
        elif q3 == 3:
            type.slow(cyan("\"Lost. You've wandered so far from who you were that you can't see the path back. But at least you know it.\""))
            sanity_score += 2
        else:
            type.slow(cyan("\"Fatalism. You believe in destiny. That nothing could have changed this outcome. A comforting lie... or a terrible truth.\""))
            sanity_score += 1
        print("\n")
        
        time.sleep(2)
        
        type.slow("The shadow studies you. Its card-suit eyes slow their spinning.")
        print("\n")
        
        # Determine outcome - need at least 5 sanity to survive
        if sanity_score >= 5:
            self.survive_madness()
        else:
            self.madness_ending()
    
    def survive_madness(self):
        """You successfully fought off the madness - but you're changed"""
        type.slow(cyan("\"...Interesting.\""))
        print("\n")
        
        type.slow("The shadow tilts its head. Your head. Its expression shifts from predatory to... something else. Something almost like respect.")
        print("\n")
        
        type.slow(cyan("\"There's still something in there. A spark of who you were. Buried deep, but burning.\""))
        print("\n")
        
        type.slow("It steps back from the window. The gray world around you begins to flicker. Color bleeding back in at the edges.")
        print("\n")
        
        type.slow(cyan("\"I'll retreat. For now. But I'm still here, " + (self.get_name() if self.get_name() else "gambler") + ". I'm always here. In the spaces between your thoughts. In the silence between heartbeats.\""))
        print("\n")
        
        type.slow("The shadow begins to fade, dissolving into the returning colors of the real world.")
        print("\n")
        
        type.slow(cyan("\"When you break again-and you will-I'll be waiting.\""))
        print("\n")
        
        type.slow("And then it's gone.")
        print("\n")
        
        type.slow("You gasp, like you've been holding your breath underwater. The world snaps back into focus. The sun is shining. Birds are singing. Everything is normal.")
        print("\n")
        
        type.slow("But you know it's not. Not anymore. Not ever again.")
        print("\n")
        
        type.slow("You've seen what's growing inside you. And now you can't unsee it.")
        print("\n")
        
        type.type(yellow(bright("You survived the confrontation with your own madness.")))
        print("\n")
        type.type(yellow("Something has shifted inside you. The world looks... different now."))
        print("\n")
        type.type(yellow("The shadows seem darker. The silences seem longer. But you're still here."))
        print("\n")
        type.type(yellow("You're still you."))
        print("\n")
        type.type(yellow("Mostly."))
        print("\n")
        
        # Mark that we faced madness and restore sanity significantly
        self.set_faced_madness()
        self.restore_sanity(30)
        
        # Add a permanent marker that changes some dialogue
        self.meet("Faced the Shadow")
        
        ask.press_continue("Press any key to continue...")
        print("\n")
    
    def madness_ending(self):
        """The secret madness ending - you lose yourself"""
        type.slow(cyan("\"...No. There's nothing left. Just echoes. Just cards.\""))
        print("\n")
        
        type.slow("The shadow smiles wider. And wider. And wider still, until its face is nothing but teeth and darkness.")
        print("\n")
        
        type.slow(cyan("\"Thank you for the body. I'll take good care of it.\""))
        print("\n")
        
        type.slow("It reaches through the window. Not breaking it. Just... phasing through, like the glass isn't there. Like nothing is there. Like reality is just a suggestion.")
        print("\n")
        
        type.slow("Cold fingers wrap around your throat. Your own fingers. Your own hands.")
        print("\n")
        
        type.slow(cyan("\"Shhhhh. Don't fight it. You've been fighting for so long. Aren't you tired?\""))
        print("\n")
        
        type.slow("You are tired. So tired. When was the last time you really slept? Really rested? Really felt at peace?")
        print("\n")
        
        type.slow(cyan("\"Let go. I'll handle everything from here. The cards. The money. The endless nights. You don't have to carry it anymore.\""))
        print("\n")
        
        type.slow("The world goes dark. But it's not a scary dark. It's soft. Quiet. Like sinking into a warm bath.")
        print("\n")
        
        type.slow("You feel yourself drifting away. Becoming small. Smaller. A speck of consciousness in a vast empty space.")
        print("\n")
        
        type.slow("And then...")
        print("\n")
        
        time.sleep(3)
        
        type.slow(bright(yellow("~ ~ ~ MADNESS ~ ~ ~")))
        print("\n")
        
        time.sleep(2)
        
        type.slow("Your eyes open.")
        print("\n")
        
        type.slow("But they're not your eyes anymore.")
        print("\n")
        
        type.slow("You watch from somewhere deep inside as your body sits up. Stretches. Smiles a smile you've never smiled before.")
        print("\n")
        
        type.slow(quote("That's better."))
        print("\n")
        
        type.slow("Your voice. But not your words.")
        print("\n")
        
        type.slow("The thing wearing your skin looks around the car. At the pile of money. At the casino on the hill. At the endless road stretching into the distance.")
        print("\n")
        
        type.slow(quote("Now then. Where were we?"))
        print("\n")
        
        type.slow("It counts the money with fingers that used to be yours. It straightens the clothes on a body that used to be yours. It checks the rearview mirror with eyes that used to be yours.")
        print("\n")
        
        type.slow("And deep inside, in the tiny dark corner where you still exist, you scream.")
        print("\n")
        
        type.slow("But no one hears.")
        print("\n")
        
        type.slow("No one ever will.")
        print("\n")
        
        time.sleep(2)
        
        type.slow("The thing that used to be you gets out of the car. It walks toward the casino with a spring in its step. It's humming a tune that doesn't exist.")
        print("\n")
        
        type.slow("The Dealer looks up as it enters. For a moment-just a moment-his jade eye flickers with something like recognition. Like fear.")
        print("\n")
        
        type.slow(red("\"...You.\""))
        print("\n")
        
        type.slow("The thing grins with your mouth.")
        print("\n")
        
        type.slow(quote("Miss me?"))
        print("\n")
        
        type.slow("It sits down at the table. It picks up the cards.")
        print("\n")
        
        type.slow("And somewhere inside, trapped forever in the prison of your own mind, you watch helplessly as the game continues.")
        print("\n")
        
        type.slow("Forever.")
        print("\n")
        
        type.slow("And ever.")
        print("\n")
        
        type.slow("And ever.")
        print("\n")
        
        time.sleep(2)
        
        type.slow(red(bright("Your mind shattered.")))
        print("\n")
        
        type.slow(red(bright("Something else took the wheel.")))
        print("\n")
        
        type.slow(red(bright("And the Dealer... the Dealer remembers.")))
        print("\n")
        
        type.slow(bright(yellow("~ ~ ~ THE END ~ ~ ~")))
        print("\n")
        type.slow("Thank you for playing.")
        quit()
