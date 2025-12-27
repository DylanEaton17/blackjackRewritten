"""
Web-adapted story system from story.py
This module contains the WebPlayer class and story progression logic
adapted for the Flask web application.
"""

import random
from typing import Dict, List, Set, Any, Optional


class WebLists:
    """Web-adapted version of Lists class from lists.py"""
    
    def __init__(self, player):
        self.player = player
        self.quote_list = []
        self.cheers_list = []
        self.advice_list = []
        self.dealer_welcome_list = []
        self.prayers_list = []
        self.quote_setup_list = []
        
        # Event lists organized by rank
        self.poor_day_events = []
        self.cheap_day_events = []
        self.modest_day_events = []
        self.rich_day_events = []
        self.doughman_day_events = []
        self.nearly_day_events = []
        
        self.poor_night_events = []
        self.cheap_night_events = []
        self.modest_night_events = []
        self.rich_night_events = []
        self.doughman_night_events = []
        self.nearly_night_events = []
        
        self.shop_list = []
        
        self._init_all_lists()
    
    def _init_all_lists(self):
        """Initialize all lists with content extracted from lists.py"""
        self._make_quote_list()
        self._make_cheers_list()
        self._make_advice_list()
        self._make_dealer_welcome_list()
        self._make_quote_setup_list()
        self._make_event_lists()
        self._make_shop_list()
    
    def _make_quote_list(self):
        """Quotes from lists.py"""
        self.quote_list = [
            "\"Give a man a fish, he'll eat for a day. Teach a man to fish, and he'll eat for a lifetime.\"",
            "\"The only way to do great work is to love what you do.\"",
            "\"In the middle of difficulty lies opportunity.\"",
            "\"Success is not final, failure is not fatal: it is the courage to continue that counts.\"",
            "\"The best time to plant a tree was 20 years ago. The second best time is now.\"",
            "\"Fortune favors the bold.\"",
            "\"What doesn't kill you makes you stronger.\"",
            "\"Every saint has a past, and every sinner has a future.\"",
        ]
    
    def _make_cheers_list(self):
        """Cheers from lists.py"""
        self.cheers_list = [
            "Yippee!",
            "Woohoo!",
            "Hooray!",
            "Congrats!",
            "Well done!",
            "Nice work!",
            "You made it!",
            "Another day!",
        ]
    
    def _make_advice_list(self):
        """Advice from lists.py"""
        self.advice_list = [
            "Keep your head up.",
            "Stay focused.",
            "Don't give up now.",
            "You're doing great!",
            "One day at a time.",
            "Fortune is fickle.",
            "The cards will turn.",
            "Trust your instincts.",
        ]
    
    def _make_dealer_welcome_list(self):
        """Dealer welcome messages"""
        self.dealer_welcome_list = [
            "Back for more, are we?",
            "Ready to lose some money?",
            "Let's see if your luck holds.",
            "The house always wins... eventually.",
            "Welcome back to the table.",
            "Feeling lucky tonight?",
        ]
    
    def _make_quote_setup_list(self):
        """Quote setup phrases"""
        self.quote_setup_list = [
            "Remember: ",
            "Keep in mind: ",
            "Never forget: ",
            "As they say: ",
            "Words to live by: ",
        ]
    
    def _make_event_lists(self):
        """Create event lists organized by rank (wealth tier)"""
        # Poor Events ($1 - $999)
        self.poor_day_events = [
            "seat_cash", "left_window_down", "estranged_dog", "freight_truck",
            "sore_throat", "spider_bite", "hungry_cockroach",
            "lone_cowboy", "whats_my_name", "interrogation"
        ]
        self.poor_night_events = [
            "ditched_wallet", "went_jogging", "woodlands_path"
        ]
        
        # Cheap Events ($1,000 - $9,999)
        self.cheap_day_events = [
            "sun_visor_bills", "strong_winds", "got_a_cold",
            "turn_to_god", "hungry_cow"
        ]
        self.cheap_night_events = [
            "woodlands_river", "woodlands_field", "swamp_stroll"
        ]
        
        # Modest Events ($10,000 - $99,999)
        self.modest_day_events = [
            "left_door_open", "another_spider_bite", "squirrel_invasion",
            "further_interrogation"
        ]
        self.modest_night_events = [
            "swamp_wade", "swamp_swim", "beach_stroll"
        ]
        
        # Rich Events ($100,000 - $499,999)
        self.rich_day_events = [
            "left_trunk_open", "rat_bite", "hungry_termites", "starving_cow"
        ]
        self.rich_night_events = [
            "beach_swim", "beach_dive", "city_streets"
        ]
        
        # Doughman Events ($500,000 - $899,999)
        self.doughman_day_events = [
            "thunderstorm", "likely_death", "even_further_interrogation"
        ]
        self.doughman_night_events = [
            "city_stroll", "city_park"
        ]
        
        # Nearly There Events ($900,000+)
        self.nearly_day_events = [
            "cow_army", "final_interrogation"
        ]
        self.nearly_night_events = [
            "woodlands_adventure", "swamp_adventure", "beach_adventure",
            "underwater_adventure", "city_adventure"
        ]
    
    def _make_shop_list(self):
        """Shop names"""
        self.shop_list = [
            "Doctor's Office",
            "Witch Doctor's Tower",
            "Trusty Tom's Trucks and Tires",
            "Filthy Frank's Flawless Fixtures",
            "Oswald's Optimal Autoparts",
            "Convenience Store",
            "Marvin's Mystical Merchandise"
        ]
    
    def get_quote(self):
        if not self.quote_list:
            self._make_quote_list()
        return random.choice(self.quote_list)
    
    def get_cheer(self):
        if not self.cheers_list:
            self._make_cheers_list()
        return random.choice(self.cheers_list)
    
    def get_advice(self):
        if not self.advice_list:
            self._make_advice_list()
        return random.choice(self.advice_list)
    
    def get_dealer_welcome(self):
        if not self.dealer_welcome_list:
            self._make_dealer_welcome_list()
        return random.choice(self.dealer_welcome_list)
    
    def get_quote_setup(self):
        if not self.quote_setup_list:
            self._make_quote_setup_list()
        return random.choice(self.quote_setup_list)
    
    def get_day_events(self, rank):
        """Get day events for current rank"""
        events_map = {
            0: self.poor_day_events,
            1: self.cheap_day_events,
            2: self.modest_day_events,
            3: self.rich_day_events,
            4: self.doughman_day_events,
            5: self.nearly_day_events
        }
        return events_map.get(rank, self.poor_day_events)
    
    def get_night_events(self, rank):
        """Get night events for current rank"""
        events_map = {
            0: self.poor_night_events,
            1: self.cheap_night_events,
            2: self.modest_night_events,
            3: self.rich_night_events,
            4: self.doughman_night_events,
            5: self.nearly_night_events
        }
        return events_map.get(rank, self.poor_night_events)
    
    def make_shop_list(self):
        """Get available shops"""
        return self.shop_list.copy()


class WebPlayer:
    """
    Web-adapted Player class from story.py
    Manages all player state, progression, events, items, health, etc.
    """
    
    def __init__(self):
        # Core attributes
        self.name = None
        self.alive = True
        self.health = 100
        self.balance = 50
        self.previous_balance = 50
        self.day = 1
        self.round_count = 3  # 3 rounds of blackjack per night
        
        # Rank system (wealth tiers)
        # 0: Poor (1-999), 1: Cheap (1k-10k), 2: Modest (10k-100k)
        # 3: Rich (100k-500k), 4: Doughman (500k-900k), 5: Nearly There (900k+)
        self.rank = 0
        
        # Status and conditions
        self.is_sick = False
        self.is_injured = False
        self.is_religious = False
        
        # Sets for tracking states
        self.status_effects: Set[str] = set()
        self.injuries: Set[str] = set()
        self.inventory: Set[str] = set()
        self.broken_inventory: Set[str] = set()
        self.repairing_inventory: Set[str] = set()
        self.dangers: Set[str] = set()
        self.met: Set[str] = set()
        self.travel_restrictions: Set[str] = set()
        self.flask_effects: Set[str] = set()
        
        # Item durability tracking
        self.item_durability = [0, 0, 0, 0, 0, 0, 0]
        self.flask_durability = [0, 0, 0, 0, 0, 0, 0]
        
        # Event tracking
        self.counting_days = [0] * 11
        self.prereqs = [False] * 5
        self.prereqs_done = [False] * 5
        self.mechanic_visits = 0
        self.convenience_store_inventory = []
        
        # Status flags
        self.clear_status = False
        self.clear_all_status = False
        
        # Lists manager
        self.lists = WebLists(self)
    
    # ===== Core Status Methods =====
    
    def kill(self, cause_of_death=None):
        """Player death"""
        self.alive = False
        return self.get_death_message()
    
    def get_death_message(self):
        """Generate death message"""
        if not self.alive:
            day_text = f"{self.day} day" if self.day == 1 else f"{self.day} days"
            return {
                "title": "Game Over",
                "text": [
                    "You have died!",
                    f"You lasted {day_text}.",
                    f"Final balance: ${self.balance:,}",
                    "The police were able to recover your body, but nobody cared enough to show up to your funeral."
                ]
            }
        elif self.balance == 0:
            day_text = f"{self.day} day" if self.day == 1 else f"{self.day} days"
            return {
                "title": "Game Over - Bankruptcy",
                "text": [
                    "You have run out of money!",
                    f"You lasted {day_text}.",
                    "With no cash left to play Blackjack, your source of income has been rendered useless.",
                    "You spend your remaining days going hungry, wondering what life could've been."
                ]
            }
        elif self.balance >= 1000000:
            return {
                "title": "Victory!",
                "text": [
                    "You did it! You're a millionaire!",
                    f"Final balance: ${self.balance:,}",
                    "Against all odds, you made it."
                ]
            }
        return None
    
    def check_status(self):
        """Check if game should end"""
        if not self.alive or self.balance == 0 or self.balance >= 1000000:
            return self.get_death_message()
        return None
    
    # ===== Health Methods =====
    
    def hurt(self, value):
        """Take damage"""
        if self.health - value <= 0:
            self.health = 0
            self.kill()
        else:
            self.health -= value
        return self.health
    
    def heal(self, value):
        """Heal health"""
        if self.health + value >= 100:
            self.health = 100
        else:
            self.health += value
        return self.health
    
    def set_health(self, value):
        self.health = value
    
    def get_health(self):
        return self.health
    
    # ===== Balance & Rank Methods =====
    
    def get_balance(self):
        return self.balance
    
    def set_balance(self, value):
        self.balance = value
    
    def change_balance(self, value):
        """Change balance and return result"""
        if (self.balance + value) <= 0:
            self.balance = 0
            return {"old": self.balance - value, "change": value, "new": 0}
        else:
            old_balance = self.balance
            self.balance += value
            return {"old": old_balance, "change": value, "new": self.balance}
    
    def get_rank(self):
        return self.rank
    
    def update_rank(self):
        """Update wealth rank based on balance"""
        if 1 <= self.balance < 1000:
            self.rank = 0  # Poor
        elif 1000 <= self.balance < 10000:
            self.rank = 1  # Cheap
        elif 10000 <= self.balance < 100000:
            self.rank = 2  # Modest
        elif 100000 <= self.balance < 500000:
            self.rank = 3  # Rich
        elif 500000 <= self.balance < 900000:
            self.rank = 4  # Doughman
        elif 900000 <= self.balance < 1000000:
            self.rank = 5  # Nearly There
        else:
            return self.check_status()
    
    def get_rank_name(self):
        """Get rank name as string"""
        rank_names = {
            0: "Poor",
            1: "Cheap",
            2: "Modest",
            3: "Rich",
            4: "Doughman",
            5: "Nearly There"
        }
        return rank_names.get(self.rank, "Unknown")
    
    # ===== Inventory & Items =====
    
    def has_item(self, item):
        return item in self.inventory
    
    def add_item(self, item):
        self.inventory.add(item)
    
    def use_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
    
    def has_broken_item(self, item):
        return item in self.broken_inventory
    
    def break_item(self, item):
        if item in self.inventory:
            self.broken_inventory.add(item)
            self.inventory.remove(item)
    
    def fix_item(self, item):
        self.inventory.add(item)
        if item in self.repairing_inventory:
            self.repairing_inventory.remove(item)
        if item in self.broken_inventory:
            self.broken_inventory.remove(item)
    
    def is_repairing_item(self, item):
        return item in self.repairing_inventory
    
    def repair_item(self, item):
        if item in self.broken_inventory:
            self.repairing_inventory.add(item)
            self.broken_inventory.remove(item)
    
    def return_item(self, item):
        if item in self.repairing_inventory:
            self.repairing_inventory.remove(item)
            self.broken_inventory.add(item)
    
    # ===== Status Effects & Injuries =====
    
    def has_status(self, status):
        return status in self.status_effects
    
    def add_status(self, status):
        self.status_effects.add(status)
    
    def remove_status(self, status):
        if status in self.status_effects:
            self.status_effects.remove(status)
    
    def has_injury(self, injury):
        return injury in self.injuries
    
    def add_injury(self, injury):
        self.injuries.add(injury)
    
    def heal_injury(self, injury):
        if injury in self.injuries:
            self.injuries.remove(injury)
    
    def len_status(self):
        return len(self.status_effects)
    
    # ===== Dangers & NPCs =====
    
    def has_danger(self, danger):
        return danger in self.dangers
    
    def add_danger(self, danger):
        self.dangers.add(danger)
    
    def lose_danger(self, danger):
        if danger in self.dangers:
            self.dangers.remove(danger)
    
    def has_met(self, person):
        return person in self.met
    
    def meet(self, person):
        self.met.add(person)
    
    # ===== Travel Restrictions =====
    
    def has_travel_restriction(self, restriction):
        return restriction in self.travel_restrictions
    
    def add_travel_restriction(self, restriction):
        self.travel_restrictions.add(restriction)
    
    def remove_travel_restriction(self, restriction):
        if restriction in self.travel_restrictions:
            self.travel_restrictions.remove(restriction)
    
    # ===== Flask Effects =====
    
    def has_flask_effect(self, flask):
        return flask in self.flask_effects
    
    def add_flask(self, flask):
        self.flask_effects.add(flask)
    
    def remove_flask_effect(self, flask):
        if flask in self.flask_effects:
            self.flask_effects.remove(flask)
    
    def len_flasks(self):
        return len(self.flask_effects)
    
    # ===== Day Tracking & Marks =====
    
    def get_mark_index(self, mark):
        """Get index for day tracking"""
        marks = {
            "Spider Bite": 0,
            "Hepatitis": 1,
            "Squirrel Bite": 2,
            "Squirrely Fed": 3,
            "Rabies": 4,
            "Rat Bite": 5,
            "Snake Bite": 6,
            "Sore Throat": 7,
            "Cold": 8,
            "Mechanic": 9
        }
        return marks.get(mark, 0)
    
    def mark_day(self, mark, time="day"):
        """Mark a day for event tracking"""
        i = self.get_mark_index(mark)
        if time == "day":
            self.counting_days[i] = self.day
        elif time == "night":
            self.counting_days[i] = self.day - 1
    
    def get_days_elapsed(self, mark):
        """Get days elapsed since mark"""
        i = self.get_mark_index(mark)
        return self.day - self.counting_days[i]
    
    # ===== Round Count =====
    
    def get_rounds(self):
        return self.round_count
    
    def set_rounds(self, value):
        self.round_count = value
    
    # ===== Serialization =====
    
    def to_dict(self):
        """Convert player state to dictionary for JSON"""
        return {
            "name": self.name,
            "alive": self.alive,
            "health": self.health,
            "balance": self.balance,
            "previous_balance": self.previous_balance,
            "day": self.day,
            "rank": self.rank,
            "rank_name": self.get_rank_name(),
            "round_count": self.round_count,
            "is_sick": self.is_sick,
            "is_injured": self.is_injured,
            "is_religious": self.is_religious,
            "status_effects": list(self.status_effects),
            "injuries": list(self.injuries),
            "inventory": list(self.inventory),
            "broken_inventory": list(self.broken_inventory),
            "repairing_inventory": list(self.repairing_inventory),
            "dangers": list(self.dangers),
            "met": list(self.met),
            "travel_restrictions": list(self.travel_restrictions),
            "flask_effects": list(self.flask_effects),
            "item_durability": self.item_durability,
            "flask_durability": self.flask_durability,
            "counting_days": self.counting_days,
            "prereqs": self.prereqs,
            "prereqs_done": self.prereqs_done,
            "mechanic_visits": self.mechanic_visits,
            "convenience_store_inventory": self.convenience_store_inventory,
            "clear_status": self.clear_status,
            "clear_all_status": self.clear_all_status
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create player from dictionary"""
        player = cls()
        player.name = data.get("name")
        player.alive = data.get("alive", True)
        player.health = data.get("health", 100)
        player.balance = data.get("balance", 50)
        player.previous_balance = data.get("previous_balance", 50)
        player.day = data.get("day", 1)
        player.rank = data.get("rank", 0)
        player.round_count = data.get("round_count", 3)
        player.is_sick = data.get("is_sick", False)
        player.is_injured = data.get("is_injured", False)
        player.is_religious = data.get("is_religious", False)
        player.status_effects = set(data.get("status_effects", []))
        player.injuries = set(data.get("injuries", []))
        player.inventory = set(data.get("inventory", []))
        player.broken_inventory = set(data.get("broken_inventory", []))
        player.repairing_inventory = set(data.get("repairing_inventory", []))
        player.dangers = set(data.get("dangers", []))
        player.met = set(data.get("met", []))
        player.travel_restrictions = set(data.get("travel_restrictions", []))
        player.flask_effects = set(data.get("flask_effects", []))
        player.item_durability = data.get("item_durability", [0] * 7)
        player.flask_durability = data.get("flask_durability", [0] * 7)
        player.counting_days = data.get("counting_days", [0] * 11)
        player.prereqs = data.get("prereqs", [False] * 5)
        player.prereqs_done = data.get("prereqs_done", [False] * 5)
        player.mechanic_visits = data.get("mechanic_visits", 0)
        player.convenience_store_inventory = data.get("convenience_store_inventory", [])
        player.clear_status = data.get("clear_status", False)
        player.clear_all_status = data.get("clear_all_status", False)
        return player
    
    # ===== CORE PROGRESSION METHODS =====
    # These are the main story progression flows from blackjackMain.py
    
    def opening_lines(self):
        """
        Opening sequence from story.py - the game's introduction
        Extracted directly from story.py lines 420-440
        """
        return {
            "title": "Welcome to Blackjack",
            "text": [
                "\"Ugh, not again,\" you spout as the old wagon shutters, then dies.",
                "Stranded on the road again, but this time, your money has gone dry.",
                "All but your 50 dollar bill that Grandma gave you on her last Christmas.",
                "You've been saving it for when you needed it most, but surely, it won't be enough.",
                "",
                "The door creaks open, and you step out into the night sky, coughing up the smoke from your fried vehicle.",
                "After pushing your car off the road and between the trees, there isn't much else left for you to do,",
                "so you begin to wander down the dark, lonely street.",
                "",
                "But at the end of the road, where concrete turned to stone turned to dirt, you notice a light up ahead, on the top of a hill.",
                "",
                "As you waltz into the old, wooden shack, your eyes begin to light up with the fire of a thousand suns.",
                "Roulette wheels! Poker tables! And in a dark corner of the abandoned casino, sits a dealer, shuffling cards for a new round of Blackjack.",
                "That 50 dollars might just come in handy after all. Thanks, Grandma!",
                "",
                "As you go to sit down at the table, you hear the Dealer cough, then watch as he sits up.",
                "",
                "In a deep, and yet strained voice, the Dealer, cloaked in darkness, poses a question to you."
            ],
            "state": self.to_dict()
        }
    
    def start_night(self):
        """
        Start of night (casino) phase
        Based on story.py lines 469-498
        """
        if self.day == 1:
            # First night special message
            return {
                "title": "The Dealer Speaks",
                "text": [
                    "Would you like to play a game of Blackjack?"
                ],
                "dealer_message": True,
                "state": self.to_dict()
            }
        elif self.has_travel_restriction("Wind"):
            return self._end_day_wind()
        elif not self.has_item("Car"):
            # Walking to casino
            return {
                "title": "Walking to the Casino",
                "text": [
                    "As the sun begins to set, and the stars light up in the night sky, you walk to the casino, eager to play more Blackjack.",
                    "",
                    self.lists.get_dealer_welcome()
                ],
                "dealer_message": True,
                "state": self.to_dict()
            }
        else:
            # Driving to casino
            return {
                "title": "Driving to the Casino",
                "text": [
                    "As the sun begins to set, and the stars light up in the night sky, you drive over to the casino, eager to play more Blackjack.",
                    "",
                    self.lists.get_dealer_welcome()
                ],
                "dealer_message": True,
                "state": self.to_dict()
            }
    
    def end_day(self):
        """
        End of day sequence - extracted from story.py lines 309-380
        Called after casino session ends
        """
        # Special end day messages
        if self.has_danger("Angry Dealer"):
            self.lose_danger("Angry Dealer")
            return self._end_day_angry_dealer()
        elif self.day == 1:
            return self._end_day_1()
        elif not self.has_item("Car"):
            return self._end_day_car_broken()
        else:
            return self._end_day_car_fixed()
    
    def _end_day_1(self):
        """First end of day"""
        return {
            "title": f"End of Day {self.day}",
            "text": [
                "After playing a few rounds of Blackjack, the dealer points to the door.",
                "Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep after such a long day.",
                "Making it back to your car, ditched on the side of the road, but no longer engulfed in smoke, you lay down, and close your eyes. It's time to rest."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def _end_day_car_broken(self):
        """End day with broken car"""
        return {
            "title": f"End of Day {self.day}",
            "text": [
                "After playing a few rounds of Blackjack, the dealer points to the door.",
                "Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep.",
                "Making it back to your car, ditched on the side of the road, you lay down, and close your eyes. It's time to rest."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def _end_day_car_fixed(self):
        """End day with working car"""
        return {
            "title": f"End of Day {self.day}",
            "text": [
                "After playing a few rounds of Blackjack, the dealer points to the door.",
                "Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep.",
                "You make it to your car and drive away from the casino, and you park in a little alcove on the side of the road. You lay down, and close your eyes. It's time to rest."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def _end_day_wind(self):
        """End day with wind restriction"""
        self.remove_travel_restriction("Wind")
        return {
            "title": f"End of Day {self.day}",
            "text": [
                "After playing a few rounds of Blackjack, the dealer points to the door.",
                "Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep.",
                "Stepping outside, you notice that the wind has calmed down. That's a relief.",
                "Making it back to your car, ditched on the side of the road, you lay down, and close your eyes. It's time to rest."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def _end_day_angry_dealer(self):
        """End day with angry dealer"""
        return {
            "title": f"End of Day {self.day}",
            "text": [
                "You've never seen the dealer quite so angry. Fortunately, you make it back to your car, and immediately pass out for the night. It's time to rest."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def end_day_stats(self):
        """
        Display end of day statistics - from story.py lines 322-379
        """
        # Cheer
        cheer = self.lists.get_cheer()
        
        # Day count message
        day_message = f"You've survived {self.day} day" if self.day == 1 else f"You've survived {self.day} days"
        day_message += "!"
        
        # Previous balance message
        if self.day == 1:
            balance_yesterday = f"You started your journey with just ${self.previous_balance}."
        else:
            balance_yesterday = f"Yesterday, at this time, you had ${self.previous_balance:,}."
        
        # Increment day BEFORE calculating change
        self.day += 1
        
        # Calculate balance change
        change_in_balance = self.balance - self.previous_balance
        if change_in_balance > 0:
            change_message = f"Since then, you've accumulated ${change_in_balance:,}."
        elif change_in_balance < 0:
            change_message = f"Since then, you've managed to lose ${abs(change_in_balance):,}."
        else:
            change_message = "Somehow, your net earnings today was 0. Goose egg. No money. Disappointing."
        
        # Set previous balance for next day
        self.previous_balance = self.balance
        
        # Current balance message
        current_message = f"That brings you to a grand total of ${self.balance:,}!"
        
        # Rank-specific message
        rank_messages = {
            0: "Let's not get too far ahead of ourselves though, you're still quite poor.",
            1: "You definitely have some money. The keyword is 'some'.",
            2: "You've amassed significant earnings. Nicely done.",
            3: "You must have some heavy pockets, huh.",
            4: "Where do you even keep all that?",
            5: "So close to being a millionaire! Can you do it?"
        }
        rank_message = rank_messages.get(self.rank, "")
        
        # Advice
        advice = self.lists.get_advice()
        
        # Quote
        quote_setup = self.lists.get_quote_setup()
        quote = self.lists.get_quote()
        
        # Heal before next day
        heal_amount = random.choice([1, 3, 5])
        self.heal(heal_amount)
        
        return {
            "title": "End of Day Summary",
            "text": [
                cheer,
                day_message,
                "",
                balance_yesterday,
                "",
                change_message,
                "",
                current_message,
                rank_message,
                "",
                advice,
                "",
                quote_setup,
                quote,
                "",
                f"You rest and recover {heal_amount} health."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def start_day(self):
        """
        Morning phase - from story.py lines 2336-2365
        """
        self.update_rank()
        
        # Get appropriate day event based on rank
        day_events = self.lists.get_day_events(self.rank)
        if day_events:
            event_name = random.choice(day_events)
            return self.trigger_event(event_name, "day")
        
        # Fallback to generic morning
        return {
            "title": f"Morning, Day {self.day}",
            "text": [
                "The sun rises on another day.",
                "You wake up, stretch, and prepare for what lies ahead."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def afternoon(self):
        """
        Afternoon phase - from story.py lines 2681-2796
        Includes shop visits or night events
        """
        self.update_rank()
        
        # Check for travel restrictions
        if self.has_travel_restriction("Wind"):
            return self._afternoon_wind()
        elif self.has_travel_restriction("Rain"):
            return self._afternoon_rain()
        
        # If player has car, they can visit shops
        if self.has_item("Car"):
            # For now, trigger a night event
            # TODO: Add shop selection UI
            return self.trigger_night_event()
        else:
            return self.trigger_night_event()
    
    def _afternoon_wind(self):
        """Afternoon with wind restriction"""
        wind_messages = [
            "You watch the wind pull twigs and branches from the trees all afternoon.",
            "One branch falls, and lands on the hood of your wagon. Had it been any bigger, that could've been bad.",
            "You hear a loud crash in the distance. A tree must've fallen nearby.",
            "The wind pushes the light gray clouds across the sky, and you watch them all afternoon."
        ]
        
        dealer_messages = [
            "It's a windy one today. Now, let us gamble.",
            "Surprised you made it here in one piece, given the weather. It's time to bet.",
            "It's nice to see you tonight. Shows commitment. You ready?",
            "Wind didn't blow any of your money away, did it? Anyways, let's play."
        ]
        
        return {
            "title": "Afternoon - Windy",
            "text": [
                random.choice(wind_messages),
                "",
                "As the sun begins to fall, you collect your money, and leave the warmth of your wagon. You barrel out into the wind, trudging your way to the casino.",
                "",
                random.choice(dealer_messages)
            ],
            "dealer_message": True,
            "continue": True,
            "state": self.to_dict()
        }
    
    def _afternoon_rain(self):
        """Afternoon with rain restriction (skips multiple days)"""
        days_to_skip = random.choice([3, 4])
        self.day += days_to_skip
        
        return {
            "title": "Afternoon - Rainstorm",
            "text": [
                "You watch, as the rain pours, and pours, and pours. By nightfall, the rain hasn't let up, and the flooding in the streets has only gotten worse. Unfortunately, you're gonna have to skip out on Blackjack for the night.",
                "",
                f"You get cozy in your car, and begin to doze off. You sleep through {days_to_skip} days...",
                "",
                f"As you awake on Day {self.day}, you notice the raindrops begin to slow down, clouds begin to clear, and a golden ray of sunshine fills your soaked wagon.",
                "",
                "As the sun begins to fall, you collect your money, and leave the safety of your wagon. You barrel out into the damp air, up the muddy dirt road, and into the casino.",
                "",
                random.choice([
                    "Wipe those shoes. It's difficult to wash these carpets.",
                    "Long time no see, yeah? Let's get back to it.",
                    "You broke the streak you had going. Wanna make up for it in bets?",
                    "Glad the rain didn't permanently wash you away. That would have been a shame."
                ])
            ],
            "dealer_message": True,
            "continue": True,
            "state": self.to_dict()
        }
    
    def trigger_event(self, event_name, event_type="day"):
        """
        Trigger a specific story event
        Returns event data by calling the event method
        """
        # Check if the event method exists and call it
        if hasattr(self, event_name):
            event_method = getattr(self, event_name)
            return event_method()
        
        # Fallback if event not implemented yet
        return {
            "title": event_name.replace("_", " ").title(),
            "text": [
                f"Event: {event_name}",
                "This event is being implemented..."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def trigger_night_event(self):
        """Trigger a night event based on rank"""
        night_events = self.lists.get_night_events(self.rank)
        if night_events:
            event_name = random.choice(night_events)
            return self.trigger_event(event_name, "night")
        
        # Fallback
        return self.start_night()
    
    # ==================== STORY EVENT METHODS ====================
    # All events extracted from story.py with authentic dialogue
    # Organized by rank: Poor (0), Cheap (1), Modest (2), Rich (3), Doughman (4), Nearly There (5)
    
    # RANK 0 (POOR: $1-$999) DAY EVENTS
    
    def seat_cash(self):
        """Find money in car seat"""
        bill = random.choice([5, 10, 20, 50, 100])
        return {
            "title": "Found Money",
            "text": [
                "You wake up in the front seat, covered in sweat.",
                "As the sun shines through the car window, you notice a bright green bill tucked between the seat cushions. Must be your lucky day.",
                "",
                f"That's another ${bill} dollars."
            ],
            "balance_change": bill,
            "continue": True,
            "state": self.to_dict()
        }
    
    def left_window_down(self):
        """Window left open overnight"""
        random_chance = random.randrange(5)
        if random_chance == 0:
            self.add_danger("Spider")
        elif random_chance == 1:
            self.add_danger("Cockroach")
        
        return {
            "title": "Open Window",
            "text": [
                "You wake up in the front seat, with a chill going down your spine.",
                "Had the window really been open all night?",
                "Hopefully nothing had gotten in.",
                "You roll the window up, just to be safe."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def estranged_dog(self):
        """Encounter with friendly dog"""
        heal_amount = random.choice([5, 10])
        text_lines = [
            "You wake up to the sound of barking outside your car. You get up, to see a golden retriever licking your window.",
            "You open the door, and pet the doggo on the head. He seems happy. You're happy, too.",
            ""
        ]
        
        if self.has_item("Dog Treat"):
            self.use_item("Dog Treat")
            text_lines.extend([
                "You throw your Dog Treat into the air, and the dog jumps up, and catches it in his mouth. He wags his tail in excitement. It's super cute.",
                ""
            ])
            heal_amount = random.choice([15, 20])
        
        text_lines.append("Before you get a chance to check the dog's collar to see where it came from, the dog bolts down the road, eager to cheer up someone else. It was a good dog.")
        
        return {
            "title": "Friendly Dog",
            "text": text_lines,
            "health_change": heal_amount,
            "continue": True,
            "state": self.to_dict()
        }
    
    def freight_truck(self):
        """Rude trucker wakes you up"""
        return {
            "title": "Rude Awakening",
            "text": [
                "You are jolted awake by the sound of a horn blaring outside your car. Looking out your window, you see a man, in a bright red hat, inside of a freight truck that's parked just outside of your vehicle.",
                "",
                "\"Hey, you. Wake the fuck up! Hahahaha!\"",
                "",
                "You watch as the man honks his horn one more time, laughs, and drives off into the distance. What a jerk."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def sore_throat(self):
        """Develop sore throat"""
        if self.has_status("Sore Throat"):
            # Skip this event, trigger another
            return self.trigger_day_event()
        
        text_lines = [
            "You wake up, and begin to have a coughing fit. Your throat is dry, and super sore."
        ]
        
        if self.has_item("Cough Drops"):
            self.use_item("Cough Drops")
            text_lines.extend([
                "Luckily, you have some Cough Drops on hand, and you empty the box into your mouth. Almost like magic, your throat doesn't hurt anymore."
            ])
        else:
            self.add_status("Sore Throat")
            self.mark_day("Sore Throat")
            text_lines.extend([
                "You cough, and cough, and cough some more, but the burning itch in your throat just won't go away."
            ])
        
        return {
            "title": "Sore Throat",
            "text": text_lines,
            "continue": True,
            "state": self.to_dict()
        }
    
    def spider_bite(self):
        """Spider bite event"""
        if not self.has_danger("Spider") or self.has_status("Spider Bite"):
            return self.trigger_day_event()
        
        text_lines = [
            "You wake up to a sharp pain on your arm!",
            "Swinging your arm to scratch the pain, you watch as a spider jumps to your dashboard."
        ]
        
        if self.has_item("Pest Control"):
            self.kill_pests()
            text_lines.extend([
                "You grab your Pest Control and spray in the direction of the spider.",
                "A cloud of white liquid covers the spider, and you watch as it slows, and dies.",
                "Hopefully, that's the end of your spider problems."
            ])
        else:
            text_lines.append("You attempt to swat it with your hand, but it sneaks into your heater.")
            self.add_status("Spider Bite")
            self.mark_day("Spider Bite")
            text_lines.extend([
                "",
                "Later, you notice a red bump on your arm. The bite left a nasty mark.",
                "You should get that checked out."
            ])
        
        return {
            "title": "Spider Bite",
            "text": text_lines,
            "continue": True,
            "state": self.to_dict()
        }
    
    def hungry_cockroach(self):
        """Cockroach eating food"""
        if not self.has_danger("Cockroach") or self.has_status("Cockroach Illness"):
            return self.trigger_day_event()
        
        text_lines = [
            "You wake up to the sight of a cockroach munching on some of the food you left out.",
            "Disgusting."
        ]
        
        if self.has_item("Pest Control"):
            self.kill_pests()
            text_lines.extend([
                "You grab your Pest Control and chase the cockroach around your car.",
                "Eventually, you corner it, and spray. The cockroach twitches, then stops moving.",
                "Good riddance."
            ])
        else:
            self.add_status("Cockroach Illness")
            self.mark_day("Cockroach Illness")
            text_lines.extend([
                "You try to stomp on it, but it scurries away into a crack in your car.",
                "",
                "Later, you eat some of that same food. You immediately regret it.",
                "Your stomach churns. This isn't good."
            ])
        
        return {
            "title": "Cockroach",
            "text": text_lines,
            "continue": True,
            "state": self.to_dict()
        }
    
    def lone_cowboy(self):
        """Encounter with mysterious cowboy"""
        return {
            "title": "The Cowboy",
            "text": [
                "You wake up to the sound of hooves clopping on pavement.",
                "Looking out your window, you see a man on horseback, wearing a wide-brimmed hat and a poncho.",
                "He tips his hat at you as he rides by.",
                "",
                "\"Morning, stranger. Fine day for it.\"",
                "",
                "You wave back, confused. Where did he come from? Where's he going?",
                "Before you can ask, he's already disappeared down the road.",
                "Strange encounter."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def whats_my_name(self):
        """Existential moment"""
        return {
            "title": "Reflection",
            "text": [
                "You wake up, and for a moment, you can't remember your name.",
                "You sit there, staring at the ceiling of your car, trying to recall.",
                "",
                "Then it comes to you. Of course.",
                "",
                f"Your name is {self.name if self.name else 'You'}.",
                "",
                "How could you forget something like that?",
                "This whole situation is really getting to you."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def interrogation(self):
        """First interrogation from mysterious figure"""
        if self.prereqs_done[0]:
            return self.trigger_day_event()
        
        self.prereqs[0] = True
        
        return {
            "title": "Interrogation",
            "text": [
                "You wake up to a sharp knock on your window.",
                "Standing outside is a figure in a dark coat. You can't make out their face.",
                "",
                "\"You lost?\" they ask.",
                "",
                "You nod, unsure what else to say.",
                "",
                "\"Figures. Everyone who comes here is lost.\"",
                "",
                "The figure pauses, looking you up and down.",
                "",
                "\"Word of advice: don't get too comfortable. This place has a way of keeping people.\"",
                "",
                "Before you can respond, they turn and walk away, disappearing into the desert heat."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    # RANK 0 (POOR) NIGHT EVENTS
    
    def ditched_wallet(self):
        """Find wallet on the road"""
        random_chance = random.randrange(2)
        if random_chance == 0:
            worth = random.randint(65, 120)
        else:
            worth = random.randint(7, 50)
        
        return {
            "title": "Found Wallet",
            "text": [
                "Bored out of your mind, you decide to wander along the side of the road, just to get a change of scenery from the dusty leather seats of your wagon.",
                "As you take step after step over the asphalt, you notice a ditched wallet, just laying there. I guess it's yours now.",
                "",
                f"Inside the wallet, you find ${worth} dollars."
            ],
            "balance_change": worth,
            "continue": True,
            "state": self.to_dict()
        }
    
    def went_jogging(self):
        """Go jogging - can result in injury or healing"""
        random_chance = random.randrange(3)
        
        text_lines = [
            "After spending an hour sitting in your car doing nothing, you feel like you should get some exercise. You get out of the wagon, and begin to jog down the road.",
            "",
            "A couple hours go by, and while jogging back, you see the wagon in the distance."
        ]
        
        if random_chance == 0:
            heal_amount = random.choice([5, 10, 15])
            text_lines.extend([
                "But, right as you get to your car, you trip over a stone on the ground, and scrape your knee hard. Blood begins to drip down your leg. That's a bummer."
            ])
            self.add_injury("Scraped Knee")
            return {
                "title": "Jogging Accident",
                "text": text_lines,
                "health_change": -heal_amount,
                "continue": True,
                "state": self.to_dict()
            }
        else:
            heal_amount = random.choice([5, 10, 15])
            text_lines.extend([
                "You get back to the car, and get in, out of breath from your trip. You start the wagon and run the AC, and you feel good inside."
            ])
            return {
                "title": "Good Jog",
                "text": text_lines,
                "health_change": heal_amount,
                "continue": True,
                "state": self.to_dict()
            }
    
    def woodlands_path(self):
        """Explore woodland path with multiple outcomes"""
        random_chance = random.randrange(3)
        
        base_text = [
            "After wandering from your vehicle, you find yourself deep in the woods. Squirrels run by and up into the trees. The sun hits every branch and casts a shadow below. And you wander on a natural path, journeying into the unknown.",
            ""
        ]
        
        if random_chance == 0:
            # Deer encounter
            return {
                "title": "Woodland Path - Deer",
                "text": base_text + [
                    "As you walk along the path, you find a mother deer, with two children, walking the path towards you. As you get closer, the mother appears cautious, but then runs in your direction, before stopping before you.",
                    "Her two children follow behind, and before you know it, the three of them wait in front of you.",
                    "",
                    "You put your hand out, and pet the mother deer. She makes a happy squeak noise, and wags her tail. She touches her head to yours, then continues down the path, with her two children following.",
                    "",
                    "Eventually, you get to the end of the path, and find the main road. You follow it back to your wagon, and take a seat, to rest for a moment."
                ],
                "continue": True,
                "state": self.to_dict()
            }
        elif random_chance == 1:
            # Dead body encounter - needs choice
            return {
                "title": "Woodland Path - Discovery",
                "text": base_text + [
                    "As you walk along the path, you notice someone leaning against a tree in front of you. As you get closer, you notice that the person's face is blue, their eyes are bloodshot, and they don't appear to be breathing.",
                    "",
                    "You begin to panic, before thinking through the situation. They're already dead, so there's nothing you can do to help them. Maybe they had some money on them? I mean, they're not gonna use it. Why shouldn't you?"
                ],
                "choices": [
                    {"text": "Search the body", "action": "search_body"},
                    {"text": "Leave them alone", "action": "leave_body"}
                ],
                "state": self.to_dict()
            }
        else:
            # Uneventful walk
            return {
                "title": "Woodland Path",
                "text": base_text + [
                    "You walk, and walk, and walk further down the path, before the forest opens up to the main road. You follow the road back to your wagon, wondering if there was anything you missed. At least you made it back safe and sound."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def handle_search_body(self):
        """Handle the choice to search the dead body"""
        random_chance = random.randrange(4)
        
        if random_chance == 0:
            self.add_status("Hepatitis")
            return {
                "title": "Body Search - Infected!",
                "text": [
                    "You rummage through the pockets, trying to find anything worthwhile.",
                    "As you do so, you notice the body begin to move. It looks up at you, screams, then coughs blood all over you. You freak out, before running back down the path the way you came.",
                    "",
                    "You make it back to your car, and find some old clothes to wipe the blood off your face. Great, just great. You already start to feel under the weather."
                ],
                "continue": True,
                "state": self.to_dict()
            }
        else:
            worth = random.randint(100, 150)
            return {
                "title": "Body Search - Success",
                "text": [
                    "After a minute of digging, you manage to find a wallet. Score!",
                    "",
                    f"Inside the wallet, you find ${worth} dollars.",
                    "You leave the dead body, and continue down the path, until the forest opens up to the main road. You follow the road back to your wagon, with your winnings in hand."
                ],
                "balance_change": worth,
                "continue": True,
                "state": self.to_dict()
            }
    
    def handle_leave_body(self):
        """Handle the choice to leave the body alone"""
        return {
            "title": "Body Left Alone",
            "text": [
                "While this body might be the body of a rich man, judging by the situation, it's very unlikely. Plus, dead bodies tend to be unsanitary. No, this body was simply not worth searching.",
                "",
                "You continue down the path, before the forest opens up to the main road. You follow the road back to your wagon, and sit. You rest for a while."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    # ===================
    # RANK 1: CHEAP ($1,000 - $9,999) - Day Events
    # ===================
    
    def sun_visor_bills(self):
        """Day event - Finding money in sun visor"""
        self.meet("Sun Visor Bills Event")
        bills = random.choice([3, 15, 30, 60, 150, 300])
        self.change_balance(bills)
        
        return {
            "title": "Hidden Money",
            "text": [
                "You wake up in the front seat, dripping in sweat.",
                "",
                "As the sun shines through the car window, you notice a few bright green bills above you, peeking out of the sun visor. How long have they been there?",
                "",
                f"That's another ${bills} dollars."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def strong_winds(self):
        """Day event - Bad weather forces staying in"""
        self.meet("Strong Winds Event")
        self.add_travel_restriction("Wind")
        
        return {
            "title": "Dangerous Weather",
            "text": [
                "You wake up to a loud snap above you, followed by a massive branch crashing down from the treetops and into the street. The wind echoes throughout the trees around you, and many of them look to be on the verge of falling.",
                "",
                "With the weather being this bad, you make the executive decision to just chill in the wagon for the day."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def got_a_cold(self):
        """Day event - Catch a cold (conditional)"""
        if self.has_status("Cold"):
            return self.day_event()
        
        self.meet("Got a Cold Event")
        self.add_status("Cold")
        self.mark_day("Cold")
        
        return {
            "title": "Feeling Sick",
            "text": [
                "You wake up to a sneeze, followed by your nose running, droplets falling down from your chin and onto your shirt.",
                "",
                "Damn, must be a cold."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def turn_to_god(self):
        """Day event - Father Ezekiel offers bible (one-time)"""
        if self.has_met("Ezekiel"):
            return self.day_event()
        
        self.meet("Ezekiel")
        
        return {
            "title": "A Spiritual Visitor",
            "text": [
                "You wake up to someone knocking on your window. You sit up, and see a man, holding a bible, and wearing a cross on a chain around his neck.",
                "",
                '"Hello! I\'m Father Ezekiel. You seem to be in a tough spot, living in your car? I was just wondering if you wanted me to give you my copy of The Bible. It has the word of God, and I hope it could help you understand that you aren\'t alone on this journey of life."',
                "",
                '"Do you accept my offer, and Jesus as your savior?"'
            ],
            "choices": [
                {"id": "accept_jesus", "text": "Accept the Bible"},
                {"id": "decline_jesus", "text": "Politely decline"}
            ],
            "state": self.to_dict()
        }
    
    def handle_accept_jesus(self):
        """Handle accepting Father Ezekiel's offer"""
        self.is_religious = True
        
        return {
            "title": "Blessed",
            "text": [
                '"Why, that\'s wonderful!"',
                "",
                "Father Ezekiel hands you his bible.",
                "",
                '"I will pray for you, and I know that Jesus will always be with you. Amen."',
                "",
                "And with that, Father Ezekiel walks down the road, and out of sight."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def handle_decline_jesus(self):
        """Handle declining Father Ezekiel's offer"""
        return {
            "title": "Respected Choice",
            "text": [
                '"Well, to each their own. I certainly cast no judgments."',
                "",
                '"I will pray for you, and I know that Jesus will always be with you. Amen."',
                "",
                "And with that, Father Ezekiel walks down the road, and out of sight."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def hungry_cow(self):
        """Day event - Betsy the cow demands money (one-time)"""
        if self.has_met("Betsy"):
            return self.day_event()
        
        self.meet("Betsy")
        self.add_danger("Betsy Tractor")
        
        return {
            "title": "An Aggressive Visitor",
            "text": [
                "You wake up to your whole car shaking. As you jump up from your seat, you see a beautiful black and white cow, staring you down through your window.",
                "",
                "The cow moos at you aggressively, and you open the door. On its back is a note that reads 'This is Betsy. Betsy gets hungry. Please feed Betsy.'",
                "",
                "Betsy stares into your soul, then looks over at the seat next to you. It appears Betsy is interested in your pile of money.",
                "",
                "Do you feed Betsy?"
            ],
            "choices": [
                {"id": "feed_betsy", "text": "Feed Betsy $100"},
                {"id": "refuse_betsy", "text": "Refuse"}
            ],
            "state": self.to_dict()
        }
    
    def handle_feed_betsy(self):
        """Handle feeding Betsy the cow"""
        self.change_balance(-100)
        
        # Betsy might want more
        random_chance = random.randrange(4)
        if (random_chance == 0) or (self.balance < 500):
            return {
                "title": "Satisfied Cow",
                "text": [
                    "You put a $100 dollar bill into Betsy's mouth. She chews it up, then spits it out in front of you.",
                    "",
                    "Betsy moos, then smiles. She walks down the road, happy as can be."
                ],
                "continue": True,
                "state": self.to_dict()
            }
        else:
            return {
                "title": "Still Hungry",
                "text": [
                    "You put a $100 dollar bill into Betsy's mouth. She chews it up, then spits it out in front of you.",
                    "",
                    "Betsy moos, then stares you down. She doesn't seem to be done with you.",
                    "",
                    "Do you feed Betsy again?"
                ],
                "choices": [
                    {"id": "feed_betsy", "text": "Feed Betsy another $100"},
                    {"id": "refuse_betsy", "text": "No more"}
                ],
                "state": self.to_dict()
            }
    
    def handle_refuse_betsy(self):
        """Handle refusing to feed Betsy"""
        damage = random.randint(30, 50)
        self.hurt(damage)
        
        return {
            "title": "Angry Cow",
            "text": [
                "You refuse to feed Betsy. She gets angry.",
                "",
                "Betsy charges at you, ramming into your car and you with incredible force. You're thrown back, badly hurt.",
                "",
                f"You take {damage} damage!",
                "",
                "Eventually, Betsy calms down and wanders off, leaving you bruised and battered."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    # ===================
    # RANK 1: CHEAP ($1,000 - $9,999) - Night Events
    # ===================
    
    def woodlands_river(self):
        """Night event - River bear encounter"""
        self.meet("Woodlands River Event")
        
        random_chance = random.randrange(3)
        if random_chance == 0:
            # Bear encounter
            if self.has_item("Quiet Sneakers"):
                self.update_quiet_sneakers_durability()
                return {
                    "title": "Close Call",
                    "text": [
                        "After wandering from your vehicle, you find yourself deep in the woods. Deer dart by you. Tree branches sway back and forth. And you wander along a river, journeying into the unknown.",
                        "",
                        "As you walk further, you stumble across a large brown bear, bathing in the river.",
                        "",
                        "Thank goodness you're wearing your Quiet Sneakers!",
                        "",
                        "You turn and run back up the riverbank, never looking back. Eventually, you make it out of the woods, and return to your car, safe and sound."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            else:
                # Bear attack chance
                random_chance_2 = random.randrange(2)
                if random_chance_2 == 0:
                    self.hurt(75)
                    self.add_injury("Severed Skin")
                    return {
                        "title": "Bear Attack",
                        "text": [
                            "After wandering from your vehicle, you find yourself deep in the woods. Deer dart by you. Tree branches sway back and forth. And you wander along a river, journeying into the unknown.",
                            "",
                            "As you walk further, you stumble across a large brown bear, bathing in the river.",
                            "",
                            "Right as you're about to turn around, you step on a branch, which makes a loud crunching noise.",
                            "",
                            "The bear sits up from the water, and glares at you. Before you get a chance to react, the bear charges at you. He swipes at your leg. He bites your arm. He punches your neck. My, what a beating he gave you.",
                            "",
                            "Thankfully, you're able to play dead, just long enough for the bear to walk away without killing you. Somehow, you get up, and limp your way back to your wagon.",
                            "",
                            "The damage inflicted from the bear is serious and severe. It's probably a good idea to see the doctor tomorrow, when they're open again. In the meantime, you wrap yourself up with spare clothes, and go on with your life."
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
                else:
                    return {
                        "title": "Lucky Escape",
                        "text": [
                            "After wandering from your vehicle, you find yourself deep in the woods. Deer dart by you. Tree branches sway back and forth. And you wander along a river, journeying into the unknown.",
                            "",
                            "As you walk further, you stumble across a large brown bear, bathing in the river.",
                            "",
                            "Right as you're about to turn around, you step on a branch, which makes a loud crunching noise.",
                            "",
                            "The bear looks up, but seems disinterested. It goes back to bathing. You slowly back away and return to safety."
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
        else:
            # Peaceful river walk
            return {
                "title": "Peaceful Walk",
                "text": [
                    "After wandering from your vehicle, you find yourself deep in the woods. Deer dart by you. Tree branches sway back and forth. And you wander along a river, journeying into the unknown.",
                    "",
                    "The night is calm and beautiful. You enjoy the peaceful sounds of nature before returning to your wagon."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def woodlands_field(self):
        """Night event - Field with fox, duffle, or campsite"""
        self.meet("Woodlands Field Event")
        
        event = random.choice(["fox", "duffle", "campsite", "none"])
        
        if event == "fox":
            if random.random() < 0.5:
                reward = random.randint(200, 600)
                self.change_balance(reward)
                return {
                    "title": "Mischievous Fox",
                    "text": [
                        "You step into a vast, golden field at dusk. The wild grass is waist-high, swaying in the wind, and the sky is painted with streaks of orange and violet. The air is thick with the scent of earth and distant rain.",
                        "",
                        "A sudden rustle in the grass makes you freeze. A sleek, red fox emerges, its eyes glinting with mischief. It circles you, then snatches a shiny object from your bag and bolts into the tall grass.",
                        "",
                        "You give chase, heart pounding, the grass slapping your legs. The fox leads you on a wild run, then vanishes. In its place, you find a hollow with your item—and a stash of old, silver coins, half-buried in the dirt.",
                        "",
                        f"You recover your item and pocket the coins (+${reward}), feeling the thrill of the hunt."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            else:
                return {
                    "title": "Clever Thief",
                    "text": [
                        "You step into a vast, golden field at dusk. The wild grass is waist-high, swaying in the wind, and the sky is painted with streaks of orange and violet. The air is thick with the scent of earth and distant rain.",
                        "",
                        "A sudden rustle in the grass makes you freeze. A sleek, red fox emerges, its eyes glinting with mischief. It circles you, then snatches a shiny object from your bag and bolts into the tall grass.",
                        "",
                        "You lose sight of the fox. Whatever it took is gone, and you're left with only the sound of your own breath and the wind. The field feels emptier now."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
        
        elif event == "duffle":
            outcome = random.choice(["cash", "note", "trap"])
            
            if outcome == "cash":
                reward = random.randint(500, 1500)
                self.change_balance(reward)
                return {
                    "title": "Hidden Treasure",
                    "text": [
                        "You step into a vast, golden field at dusk. The wild grass is waist-high, swaying in the wind, and the sky is painted with streaks of orange and violet.",
                        "",
                        "Your foot strikes something hard. You kneel and uncover a battered duffle bag, caked in mud. The zipper is stuck, but with effort, you force it open.",
                        "",
                        f"Inside, you find bundles of cash, waterlogged but real. You count quickly, nerves tingling, and pocket your find (+${reward}) before anyone can see."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            
            elif outcome == "note":
                self.add_item("Cryptic Note")
                return {
                    "title": "Mysterious Message",
                    "text": [
                        "You step into a vast, golden field at dusk. The wild grass is waist-high, swaying in the wind, and the sky is painted with streaks of orange and violet.",
                        "",
                        "Your foot strikes something hard. You kneel and uncover a battered duffle bag, caked in mud. The zipper is stuck, but with effort, you force it open.",
                        "",
                        "Inside, you find a single, bloodstained note: 'The roots run deep where the sun never shines. Trust no one.'",
                        "",
                        "You shiver and pocket the note, feeling watched."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            
            else:  # trap
                damage = random.randint(10, 25)
                self.hurt(damage)
                return {
                    "title": "Painful Surprise",
                    "text": [
                        "You step into a vast, golden field at dusk. The wild grass is waist-high, swaying in the wind, and the sky is painted with streaks of orange and violet.",
                        "",
                        "Your foot strikes something hard. You kneel and uncover a battered duffle bag, caked in mud. The zipper is stuck, but with effort, you force it open.",
                        "",
                        f"As you dig deeper, a swarm of angry hornets bursts from the bag! You sprint away, stung and cursing, your skin burning. (-{damage} health)"
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
        
        elif event == "campsite":
            return {
                "title": "Abandoned Camp",
                "text": [
                    "You step into a vast, golden field at dusk. The wild grass is waist-high, swaying in the wind, and the sky is painted with streaks of orange and violet.",
                    "",
                    "You stumble upon an old campsite, the fire long cold. Someone left in a hurry—a tent still stands, flapping in the wind.",
                    "",
                    "You search the tent but find nothing of value. The field keeps its secrets."
                ],
                "continue": True,
                "state": self.to_dict()
            }
        
        else:  # none
            return {
                "title": "Quiet Evening",
                "text": [
                    "You step into a vast, golden field at dusk. The wild grass is waist-high, swaying in the wind, and the sky is painted with streaks of orange and violet. The air is thick with the scent of earth and distant rain. You feel both exposed and alive, as if the world is holding its breath.",
                    "",
                    "You wander for a while, lost in thought. The night is gentle, and you return to your wagon with a clear mind."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def swamp_stroll(self):
        """Night event - Swamp with snake, frog, or witch"""
        self.meet("Swamp Stroll Event")
        
        event = random.choice(["snake", "frog", "witch", "none"])
        
        if event == "snake":
            return {
                "title": "Serpent Path",
                "text": [
                    "You pick your way along a narrow, winding path through the swamp. The air is thick with mist and the croak of unseen frogs. Every step is a gamble—roots twist underfoot, and the water hides secrets.",
                    "",
                    "A sudden hiss makes you freeze. A massive snake, thick as your arm, slithers across your path, its eyes fixed on you.",
                    "",
                    "Do you try to catch it?"
                ],
                "choices": [
                    {"id": "catch_snake", "text": "Try to catch the snake"},
                    {"id": "avoid_snake", "text": "Back away slowly"}
                ],
                "state": self.to_dict()
            }
        
        elif event == "frog":
            return {
                "title": "The Riddle Frog",
                "text": [
                    "You pick your way along a narrow, winding path through the swamp. The air is thick with mist and the croak of unseen frogs.",
                    "",
                    "A luminous green frog sits on a log, watching you with ancient, golden eyes. It croaks, and you feel compelled to listen.",
                    "",
                    "The frog speaks: 'Answer my riddle and I shall grant you a boon. Fail, and you shall be cursed.'",
                    "",
                    "'What has roots as nobody sees, is taller than trees, up, up it goes, and yet never grows?'"
                ],
                "choices": [
                    {"id": "answer_mountain", "text": "A mountain"},
                    {"id": "answer_tree", "text": "A tree"},
                    {"id": "answer_skip", "text": "Refuse to answer"}
                ],
                "state": self.to_dict()
            }
        
        elif event == "witch":
            return {
                "title": "Swamp Witch",
                "text": [
                    "You pick your way along a narrow, winding path through the swamp. The air is thick with mist and the croak of unseen frogs.",
                    "",
                    "A figure emerges from the mist—a witch, her eyes glowing faintly. She offers you a choice: a curse or a blessing.",
                    "",
                    "Do you accept her offer?"
                ],
                "choices": [
                    {"id": "accept_witch", "text": "Accept"},
                    {"id": "refuse_witch", "text": "Refuse"}
                ],
                "state": self.to_dict()
            }
        
        else:  # none
            return {
                "title": "Misty Path",
                "text": [
                    "You pick your way along a narrow, winding path through the swamp. The air is thick with mist and the croak of unseen frogs. Every step is a gamble—roots twist underfoot, and the water hides secrets.",
                    "",
                    "Tonight, the swamp is quiet. You make your way through safely and return to your wagon."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def handle_catch_snake(self):
        """Handle trying to catch the snake"""
        if random.random() < 0.4:
            self.add_item("Rare Snakeskin")
            return {
                "title": "Successful Capture",
                "text": [
                    "You lunge and grab the snake behind the head. It writhes, but you hold firm.",
                    "",
                    "Eventually, it calms, and you harvest its skin—a valuable prize."
                ],
                "continue": True,
                "state": self.to_dict()
            }
        else:
            damage = random.randint(15, 30)
            self.hurt(damage)
            self.add_status("Poisoned")
            return {
                "title": "Snake Bite",
                "text": [
                    "The snake strikes, sinking its fangs into your arm. You stagger back, dizzy, as venom burns through your veins.",
                    "",
                    f"You take {damage} damage and are now poisoned!"
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def handle_avoid_snake(self):
        """Handle backing away from the snake"""
        return {
            "title": "Wise Choice",
            "text": [
                "You back away, heart pounding, and let the snake disappear into the shadows.",
                "",
                "Sometimes, caution is the better part of valor."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def handle_answer_mountain(self):
        """Handle correct answer to riddle"""
        self.add_status("Lucky")
        return {
            "title": "Wisdom Rewarded",
            "text": [
                "The frog nods. 'Wisdom is yours.'",
                "",
                "You feel luckier, as if the swamp itself is on your side."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def handle_answer_tree(self):
        """Handle wrong answer to riddle"""
        self.add_status("Cursed")
        return {
            "title": "Wrong Answer",
            "text": [
                "The frog croaks angrily. 'Foolish mortal!'",
                "",
                "You feel a dark weight settle over you. You have been cursed."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def handle_answer_skip(self):
        """Handle refusing to answer riddle"""
        return {
            "title": "Avoided",
            "text": [
                "You back away from the frog, unwilling to play its game.",
                "",
                "It watches you leave, its golden eyes unblinking."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    def handle_accept_witch(self):
        """Handle accepting witch's offer"""
        if random.random() < 0.5:
            self.add_status("Protected")
            return {
                "title": "Blessed",
                "text": [
                    "The witch smiles and touches your forehead. You feel a warm energy flow through you.",
                    "",
                    "You have been blessed with protection."
                ],
                "continue": True,
                "state": self.to_dict()
            }
        else:
            self.add_status("Cursed")
            return {
                "title": "Cursed",
                "text": [
                    "She grins wickedly. 'Luck is a fickle thing.'",
                    "",
                    "You feel a cold shiver run down your spine. You have been cursed."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def handle_refuse_witch(self):
        """Handle refusing witch's offer"""
        return {
            "title": "Declined",
            "text": [
                "The witch shrugs and disappears into the mist, her laughter echoing across the water.",
                "",
                "You return to your wagon, wondering what might have been."
            ],
            "continue": True,
            "state": self.to_dict()
        }
    
    # ======================
    # RANK 2 (MODEST) EVENTS: $10,000 - $99,999
    # ======================
    
    # RANK 2 DAY EVENTS
    def left_door_open(self):
        """Rank 2 day event - door left open overnight"""
        result = {
            "title": "Left Door Open",
            "text": [
                "You wake up in the front seat, with a chill throughout your body.",
                "Had the passenger door really been open all night?",
                "Hopefully nothing had gotten in.",
                "",
                "You reach over and close the door, just to be safe."
            ],
            "continue": True
        }
        
        # Random chance of danger
        chance = random.randint(0, 5)
        if chance <= 2:
            self.dangers.add("Spider")
        elif chance == 3:
            self.dangers.add("Squirrel")
            
        result["state"] = self.to_dict()
        return result
    
    def another_spider_bite(self):
        """Rank 2 day event - spider bite (conditional on Spider danger)"""
        # Check prerequisites
        if "Spider" not in self.dangers or "Spider Bite" in self.status_effects:
            return self.day_event()
        
        result = {
            "title": "Another Spider Bite!",
            "text": [
                "You wake up to a sharp pain on your neck!",
                "Swinging your arm to scratch the pain, you watch as a spider jumps to the backseat."
            ]
        }
        
        if "Pest Control" in self.inventory:
            self.inventory.pop("Pest Control")
            result["text"].extend([
                "",
                "You grab your Pest Control and spray in the direction of the spider.",
                "A cloud of white liquid covers the spider, and you watch as it slows, and dies.",
                "",
                "Hopefully, that's the end of your spider problems."
            ])
        else:
            result["text"].extend([
                "",
                "The spider, now out of reach, crawls off the seat and onto the floor.",
                "You stick your head out back, but you aren't sure where the spider went, or if it has a family nearby.",
                "",
                "This is unfortunate."
            ])
        
        self.status_effects.add("Spider Bite")
        result["continue"] = True
        result["state"] = self.to_dict()
        return result
    
    def squirrel_invasion(self):
        """Rank 2 day event - squirrel invasion (conditional)"""
        # Check prerequisites
        if "Squirrel" not in self.dangers or "Squirrel Bite" in self.status_effects or "Rabies" in self.status_effects or "Squirrely" in self.inventory or "Squirrely" in self.met_people:
            return self.day_event()
        
        self.dangers.discard("Squirrel")
        
        if "Bag of Acorns" in self.inventory:
            self.inventory.pop("Bag of Acorns")
            
            if "Dead Squirrely" in self.met_people:
                return {
                    "title": "Squirrel Visitor",
                    "text": [
                        "You wake up to the sound of something rummaging through your car.",
                        "Looking in the backseat, you notice a little squirrel, chewing through your Bag of Acorns.",
                        "He looks pretty cute.",
                        "",
                        "The squirrel notices you, and jumps from the bag, and over to your center console.",
                        "He peers up at you, but your eyes are filled with tears.",
                        "",
                        "Nothing can ever replace Squirrely.",
                        "",
                        "You pick up the squirrel, open the door, and let it free."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            else:
                self.inventory["Squirrely"] = {"durability": None}
                self.met_people.add("Squirrely")
                return {
                    "title": "Squirrel Friend",
                    "text": [
                        "You wake up to the sound of something rummaging through your car.",
                        "Looking in the backseat, you notice a little squirrel, chewing through your Bag of Acorns.",
                        "He looks pretty cute.",
                        "",
                        "The squirrel notices you, and jumps from the bag, and over to your center console.",
                        "He peers up at you, with an acorn in hand, holding it up in your direction.",
                        "",
                        "You stick your hand out, and the squirrel gives you the acorn.",
                        "This must be a sign of peace.",
                        "",
                        "After an hour of watching the squirrel eat the acorns, climb around your car,",
                        "and jump from your arm to the dashboard over and over,",
                        "you decide that this squirrel is now yours.",
                        "",
                        "You name him 'Squirrely', in honor of him being a squirrel."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
        else:
            # Squirrel bite
            self.status_effects.add("Squirrel Bite")
            if random.randint(0, 3) == 1:
                self.status_effects.add("Rabies")
                
            return {
                "title": "Squirrel Attack!",
                "text": [
                    "You wake up to a sharp pain on your leg!",
                    "You swing the hurt leg, and you watch as a squirrel goes flying into the air.",
                    "",
                    "The little rodent starts climbing around your car, scurrying around the walls,",
                    "desperately trying to get out.",
                    "",
                    "You open the backseat windows, and the squirrel jumps out, and darts into the woods.",
                    "",
                    "Hopefully, that bite isn't too serious."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def further_interrogation(self):
        """Rank 2 day event - further interrogation (conditional)"""
        if "Interrogator" not in self.met_people or "Further Interrogation" not in self.dangers:
            return self.day_event()
        
        self.dangers.discard("Further Interrogation")
        self.dangers.add("Even Further Interrogation")
        
        return {
            "title": "Further Interrogation",
            "text": [
                "You wake up, and through your windshield, you see a car parked right in front of you.",
                "Tired, and concerned, you sit up.",
                "",
                "As you open the door and get out of your car, you notice a man you've met before,",
                "in his bright red suit, once again peering into your trunk.",
                "",
                "The man sees you, and walks up to you, with a clipboard in his hand.",
                "",
                "\"You. You're awake. Good. You see this clipboard? It says you can't be here.\"",
                "",
                "You begin to read the paper on the clipboard. It's a message, written in Comic Sans:",
                "",
                "'This offical message from the government and the military and the army says that you can't be here.",
                "That's right, you, the person reading this message right now, living on this land right here.",
                "It's not for you. It won't ever be for you. So, you can't live here.",
                "You need to move right now, or I'll be very very angry.'",
                "",
                "\"Did you read it?\"",
            ],
            "choices": [
                {"id": "yes", "text": "Yes"},
                {"id": "no", "text": "No"}
            ],
            "state": self.to_dict()
        }
    
    def handle_further_interrogation(self, choice):
        """Handle further interrogation choice"""
        if choice == "yes":
            return {
                "title": "Interrogation Response",
                "text": [
                    "\"Good, so you know that all these powerful people want yo- are demanding",
                    "that you move from where you're currently living, right this instant!",
                    "I'd suggest you do so. I certainly wouldn't want to upset the government.\"",
                    "",
                    "After the man tells you this, he looks up, and stares at the sun.",
                    "And after about 25 seconds, he rubs his eyes, walks back to his car, and drives off."
                ],
                "continue": True,
                "state": self.to_dict()
            }
        else:  # no
            return {
                "title": "Interrogation Response",
                "text": [
                    "\"You didn't read it? Come on, I worked so hard on it.",
                    "You really should read a clipboard with words on it if someone asks you to.",
                    "Regardless, it says that you need to move! Or the consequences will be scary!\"",
                    "",
                    "After the man tells you this, he looks up, and stares at the sun.",
                    "And after about 25 seconds, he rubs his eyes, walks back to his car, and drives off."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    # RANK 2 NIGHT EVENTS
    def swamp_wade(self):
        """Rank 2 night event - wade through swamp"""
        self.met_people.add("Swamp Wade Event")
        
        event_type = random.choice(["leech", "nectar", "witch", "none"])
        
        if event_type == "leech":
            damage = random.randint(10, 25)
            self.health = max(0, self.health - damage)
            return {
                "title": "Swamp Wade - Leeches!",
                "text": [
                    "You wade waist-deep through the swamp, the water cold and thick with silt.",
                    "Every step is a struggle, and unseen things brush against your legs.",
                    "The air is heavy with the scent of decay and blooming lilies.",
                    "",
                    "You feel a dozen sharp stings—leeches!",
                    "You thrash and claw at your skin, but they cling tight, draining your strength.",
                    "",
                    f"You lose {damage} health.",
                    "",
                    "You stagger out of the water, pale and shivering, vowing never to return."
                ],
                "continue": True,
                "state": self.to_dict()
            }
        elif event_type == "nectar":
            return {
                "title": "Swamp Wade - Healing Nectar",
                "text": [
                    "You wade waist-deep through the swamp, the water cold and thick with silt.",
                    "Every step is a struggle, and unseen things brush against your legs.",
                    "The air is heavy with the scent of decay and blooming lilies.",
                    "",
                    "Your hand brushes against a jar tangled in roots.",
                    "Inside is a glowing nectar, pulsing with golden light.",
                    "",
                    "Do you drink it?"
                ],
                "choices": [
                    {"id": "drink", "text": "Drink the healing nectar"},
                    {"id": "save", "text": "Save it for later"}
                ],
                "state": self.to_dict()
            }
        elif event_type == "witch":
            return {
                "title": "Swamp Wade - The Witch",
                "text": [
                    "You wade waist-deep through the swamp, the water cold and thick with silt.",
                    "Every step is a struggle, and unseen things brush against your legs.",
                    "The air is heavy with the scent of decay and blooming lilies.",
                    "",
                    "The swamp witch appears, gliding over the water on a raft of bones.",
                    "She offers to read your fortune for a price.",
                    "",
                    "Her eyes are bottomless pits.",
                    "",
                    "Let her read your fortune?"
                ],
                "choices": [
                    {"id": "yes", "text": "Yes, read my fortune"},
                    {"id": "no", "text": "No, decline"}
                ],
                "state": self.to_dict()
            }
        else:  # none
            return {
                "title": "Swamp Wade",
                "text": [
                    "You wade waist-deep through the swamp, the water cold and thick with silt.",
                    "Every step is a struggle, and unseen things brush against your legs.",
                    "The air is heavy with the scent of decay and blooming lilies.",
                    "",
                    "You make it through, muddy but unharmed.",
                    "The swamp seems to sigh as you leave."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def handle_swamp_wade_nectar(self, choice):
        """Handle nectar choice in swamp wade"""
        if choice == "drink":
            heal_amount = random.randint(20, 40)
            self.health = min(100, self.health + heal_amount)
            self.status_effects.add("Invincible")
            return {
                "title": "Invincible!",
                "text": [
                    "Sweetness fills your mouth.",
                    "You feel your wounds close and your spirit soar.",
                    "",
                    f"You heal {heal_amount} health!",
                    "",
                    "For a moment, you are invincible."
                ],
                "continue": True,
                "state": self.to_dict()
            }
        else:  # save
            self.inventory["Healing Nectar Jar"] = {"durability": None}
            return {
                "title": "Saved",
                "text": [
                    "You pocket the jar for later.",
                    "",
                    "Who knows when it might save your life?"
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def handle_swamp_wade_fortune(self, choice):
        """Handle witch fortune reading"""
        if choice == "yes":
            fate = random.choice(["good", "bad", "cryptic"])
            if fate == "good":
                self.status_effects.add("Lucky")
                return {
                    "title": "Fortune Favors You",
                    "text": [
                        "She smiles, revealing sharp teeth.",
                        "",
                        "'Fortune favors you.'",
                        "",
                        "You feel luckier, as if the world has tilted in your favor."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            elif fate == "bad":
                self.status_effects.add("Unlucky")
                return {
                    "title": "Dark Fortune",
                    "text": [
                        "She frowns.",
                        "",
                        "'Beware the next crossing.'",
                        "",
                        "You feel a chill in your bones, and the world seems darker."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            else:  # cryptic
                self.inventory["Cryptic Riddle"] = {"durability": None}
                return {
                    "title": "Cryptic Riddle",
                    "text": [
                        "She whispers a riddle you can't quite remember.",
                        "",
                        "It haunts your dreams, surfacing at odd moments."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
        else:  # no
            return {
                "title": "Declined",
                "text": [
                    "The witch vanishes, leaving only ripples in the water",
                    "and a sense of foreboding."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def swamp_swim(self):
        """Rank 2 night event - swim in swamp"""
        self.met_people.add("Swamp Swim Event")
        
        event_type = random.choice(["alligator", "treasure", "witch", "none"])
        
        if event_type == "alligator":
            if random.random() < 0.4:
                return {
                    "title": "Swamp Swim - Alligator Escape",
                    "text": [
                        "You dive into the deeper waters of the swamp, the surface closing above you.",
                        "The world is muffled, green, and full of secrets.",
                        "",
                        "A pair of eyes breaks the surface—an alligator!",
                        "It surges toward you, jaws wide. You thrash and kick, desperate to escape.",
                        "",
                        "You manage to scramble to safety, heart pounding, lungs burning.",
                        "",
                        "You vow never to swim here again."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            else:
                damage = random.randint(20, 40)
                self.health = max(0, self.health - damage)
                return {
                    "title": "Swamp Swim - Alligator Attack!",
                    "text": [
                        "You dive into the deeper waters of the swamp, the surface closing above you.",
                        "The world is muffled, green, and full of secrets.",
                        "",
                        "A pair of eyes breaks the surface—an alligator!",
                        "It surges toward you, jaws wide. You thrash and kick, desperate to escape.",
                        "",
                        "The alligator snaps at you, its teeth grazing your leg.",
                        "You escape, but not unscathed.",
                        "",
                        f"You lose {damage} health!",
                        "",
                        "Blood clouds the water behind you."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
        elif event_type == "treasure":
            return {
                "title": "Swamp Swim - Sunken Chest",
                "text": [
                    "You dive into the deeper waters of the swamp, the surface closing above you.",
                    "The world is muffled, green, and full of secrets.",
                    "Every movement stirs up clouds of silt, and the water is alive with unseen creatures.",
                    "",
                    "Your hand brushes something cold and metallic—a sunken chest, half-buried in the muck.",
                    "",
                    "Do you try to open it?"
                ],
                "choices": [
                    {"id": "open", "text": "Open the chest"},
                    {"id": "leave", "text": "Leave it undisturbed"}
                ],
                "state": self.to_dict()
            }
        elif event_type == "witch":
            return {
                "title": "Swamp Swim - Witch's Charm",
                "text": [
                    "You dive into the deeper waters of the swamp, the surface closing above you.",
                    "The world is muffled, green, and full of secrets.",
                    "",
                    "The witch floats by on a log, humming a haunting tune.",
                    "She offers you a charm woven from reeds and bone.",
                    "",
                    "'For protection,' she says, 'or perhaps for something else.'",
                    "",
                    "Buy the witch's charm?"
                ],
                "choices": [
                    {"id": "buy", "text": "Buy the charm"},
                    {"id": "decline", "text": "Decline"}
                ],
                "state": self.to_dict()
            }
        else:  # none
            return {
                "title": "Swamp Swim",
                "text": [
                    "You dive into the deeper waters of the swamp, the surface closing above you.",
                    "The world is muffled, green, and full of secrets.",
                    "Every movement stirs up clouds of silt, and the water is alive with unseen creatures.",
                    "",
                    "You swim back, heart pounding, but nothing happens.",
                    "",
                    "The swamp keeps its secrets—for now."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def handle_swamp_swim_chest(self, choice):
        """Handle sunken chest choice"""
        if choice == "open":
            loot = random.choice(["coins", "artifact", "trap"])
            if loot == "coins":
                amount = random.randint(800, 2000)
                self.balance += amount
                return {
                    "title": "Treasure Found!",
                    "text": [
                        "Inside, you find a trove of old coins and jewelry.",
                        "",
                        f"You gain ${amount:,}!",
                        "",
                        "You're richer, but you wonder who lost it—and why."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            elif loot == "artifact":
                self.inventory["Swamp Artifact"] = {"durability": None}
                return {
                    "title": "Strange Artifact",
                    "text": [
                        "You find a strange artifact, humming with energy.",
                        "As you touch it, visions flash before your eyes—",
                        "",
                        "of the swamp, of danger, of destiny."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            else:  # trap
                damage = random.randint(10, 25)
                self.health = max(0, self.health - damage)
                return {
                    "title": "Trapped!",
                    "text": [
                        "A cloud of noxious gas bursts out!",
                        "You cough and swim away, your head spinning, your body weak.",
                        "",
                        f"You lose {damage} health!"
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
        else:  # leave
            return {
                "title": "Left Undisturbed",
                "text": [
                    "You leave the chest undisturbed,",
                    "wary of curses and the weight of history."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def handle_swamp_swim_charm(self, choice):
        """Handle witch's charm purchase"""
        if choice == "buy":
            charm_type = random.choice(["protection", "misfortune"])
            if charm_type == "protection":
                self.status_effects.add("Protected")
                return {
                    "title": "Protected",
                    "text": [
                        "She ties the charm around your wrist.",
                        "",
                        "'No harm shall come to you—tonight.'",
                        "",
                        "You feel a strange warmth,",
                        "as if the swamp itself is watching over you."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            else:  # misfortune
                self.status_effects.add("Cursed")
                return {
                    "title": "Cursed",
                    "text": [
                        "She grins wickedly.",
                        "",
                        "'Luck is a fickle thing.'",
                        "",
                        "You feel a cold shiver run down your spine."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
        else:  # decline
            return {
                "title": "Declined",
                "text": [
                    "The witch shrugs and disappears into the mist,",
                    "her laughter echoing across the water."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def beach_stroll(self):
        """Rank 2 night event - beach stroll"""
        self.met_people.add("Beach Stroll Event")
        
        event_type = random.choice(["sandman", "shells", "bonfire", "none"])
        
        if event_type == "sandman":
            return {
                "title": "Beach Stroll - The Sandman",
                "text": [
                    "You walk the moonlit shoreline, the sand cool beneath your feet",
                    "and the waves whispering secrets.",
                    "The night is alive with possibility, and every step feels like a story waiting to happen.",
                    "",
                    "A tall, robed figure—the Sandman—appears, his eyes twinkling.",
                    "",
                    "'Help me collect shells for my collection,' he asks, his voice like the tide.",
                    "",
                    "Do you help?"
                ],
                "choices": [
                    {"id": "help", "text": "Help the Sandman"},
                    {"id": "decline", "text": "Decline"}
                ],
                "state": self.to_dict()
            }
        elif event_type == "shells":
            self.inventory["Rare Shell"] = {"durability": None}
            self.status_effects.add("Calm")
            return {
                "title": "Beach Stroll - Rare Shell",
                "text": [
                    "You walk the moonlit shoreline, the sand cool beneath your feet",
                    "and the waves whispering secrets.",
                    "",
                    "You find a rare, perfect shell, its spiral gleaming in the moonlight.",
                    "",
                    "As you pick it up, a wave of calm and clarity washes over you."
                ],
                "continue": True,
                "state": self.to_dict()
            }
        elif event_type == "bonfire":
            return {
                "title": "Beach Stroll - Bonfire",
                "text": [
                    "You walk the moonlit shoreline, the sand cool beneath your feet",
                    "and the waves whispering secrets.",
                    "",
                    "A group of strangers invites you to join their bonfire.",
                    "They share stories, laughter, and roasted marshmallows.",
                    "",
                    "Do you join them?"
                ],
                "choices": [
                    {"id": "join", "text": "Join the bonfire"},
                    {"id": "watch", "text": "Watch from a distance"}
                ],
                "state": self.to_dict()
            }
        else:  # none
            return {
                "title": "Beach Stroll",
                "text": [
                    "You walk the moonlit shoreline, the sand cool beneath your feet",
                    "and the waves whispering secrets.",
                    "The night is alive with possibility, and every step feels like a story waiting to happen.",
                    "",
                    "You walk for a while, lost in thought, the ocean breeze clearing your mind.",
                    "",
                    "The night is gentle, and you feel at peace."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def handle_beach_stroll_sandman(self, choice):
        """Handle Sandman encounter"""
        if choice == "help":
            if random.random() < 0.7:
                self.inventory["Dream Token"] = {"durability": None}
                self.status_effects.add("Inspired")
                return {
                    "title": "Dream Token",
                    "text": [
                        "You gather a handful of beautiful shells.",
                        "The Sandman thanks you, pressing a Dream Token into your palm.",
                        "",
                        "That night, your sleep is deep and full of strange, hopeful dreams."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            else:
                return {
                    "title": "Empty Handed",
                    "text": [
                        "You search for shells but find only broken bits.",
                        "The Sandman shrugs, fading into the mist.",
                        "",
                        "You feel a pang of disappointment."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
        else:  # decline
            return {
                "title": "Declined",
                "text": [
                    "You decline, and the Sandman's smile fades.",
                    "He vanishes, leaving only footprints in the sand and a chill in the air."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def handle_beach_stroll_bonfire(self, choice):
        """Handle bonfire encounter"""
        if choice == "join":
            if random.random() < 0.5:
                heal_amount = random.randint(10, 20)
                self.health = min(100, self.health + heal_amount)
                self.status_effects.add("Happy")
                return {
                    "title": "New Friends",
                    "text": [
                        "You make new friends and leave with a full belly and a lighter heart.",
                        "",
                        f"You heal {heal_amount} health!",
                        "",
                        "The world feels a little less lonely."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            else:
                damage = random.randint(3, 8)
                self.health = max(0, self.health - damage)
                return {
                    "title": "Too Many Marshmallows",
                    "text": [
                        "You eat too many marshmallows and wake up with a stomachache,",
                        "but the memories are sweet.",
                        "",
                        f"You lose {damage} health."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
        else:  # watch
            return {
                "title": "From a Distance",
                "text": [
                    "You watch the fire from a distance,",
                    "the warmth and laughter just out of reach."
                ],
                "continue": True,
                "state": self.to_dict()
            }

    # Rank 3 (Rich): $100,000 - $499,999
    # DAY EVENTS
    def left_trunk_open(self):
        """Rich day event - trunk left open overnight"""
        result = {
            "title": "Left Trunk Open",
            "text": [
                "You wake up in the front seat, with a chill throughout the whole wagon.",
                "",
                "Had the trunk really been open all night?",
                "",
                "Hopefully nothing had gotten in.",
                "",
                "You get out of the car and close the trunk, just to be safe."
            ],
            "continue": True,
            "state": self.to_dict()
        }
        
        # Add dangers based on random chance
        random_chance = random.randint(0, 5)
        if random_chance < 2:
            self.dangers.add("Rat")
        elif random_chance < 4:
            self.dangers.add("Termite")
        
        return result
    
    def rat_bite(self):
        """Rich day event - rat bite (conditional on Rat danger)"""
        # Skip if already has status or no danger
        if "Rabies" in self.status_effects or "Rat" not in self.dangers or "Rat Bite" in self.status_effects:
            return self.trigger_event('day')
        
        result_text = [
            "You wake up to a sharp pain on your ankle!",
            "",
            "You look down to see a skinny gray rat nibbling your foot. You kick at it, but the little rodent runs under the seat.",
            "",
            "The rat jumps up onto your backseat, and begins to laugh at you. Now that's just cruel. This rat must be crazy.",
            ""
        ]
        
        if "Pest Control" in self.inventory:
            result_text.extend([
                f"You grab your **Pest Control** and spray the rat down.",
                "",
                "A cloud of white liquid covers the rat, and you watch as it spazzes out, and dies.",
                "",
                "Hopefully, that's it for your rat problems. Except for that bite. You might wanna get that checked out."
            ])
            # Remove dangers
            self.dangers.discard("Rat")
            self.dangers.discard("Termite")
        else:
            result_text.extend([
                "You jump at the seat towards the rat, but it sneaks back under the passenger seat, and you can't find it.",
                "",
                "That damn rat. Hopefully, the bite isn't too serious, but it's probably worth getting checked out."
            ])
        
        self.status_effects.add("Rat Bite")
        
        # 50% chance of rabies
        if random.randint(0, 1) == 1:
            self.status_effects.add("Rabies")
        
        return {
            "title": "Rat Bite",
            "text": result_text,
            "continue": True,
            "state": self.to_dict()
        }
    
    def hungry_termites(self):
        """Rich day event - termites eating money (conditional)"""
        if random.randint(0, 1) != 0 or "Termite" not in self.dangers:
            return self.trigger_event('day')
        
        result_text = [
            "You wake up to a clicking sound. Looking around, you notice that it's coming from your pile of money.",
            "",
            "You jump up to check your cash, and you find a termite eating away at your cash.",
            ""
        ]
        
        if "Pest Control" in self.inventory:
            result_text.extend([
                f"You grab your **Pest Control** and spray in the direction of the termite.",
                "",
                "A cloud of white liquid covers the termite, and you watch as it slows down, twitches, and dies.",
                "",
                "Hopefully, that's the end of your termite problems.",
                ""
            ])
            # Remove dangers
            self.dangers.discard("Rat")
            self.dangers.discard("Termite")
        else:
            result_text.extend([
                "You attempt to swat it with your hand, but it falls under your car seat.",
                "",
                "You stick your head under the seat, but you aren't sure where the termite went, or if it has a family nearby. This is just brutal.",
                ""
            ])
        
        # Lose 20-50% of money
        losses = int(self.balance * (random.randint(20, 50) / 100))
        self.balance -= losses
        
        result_text.extend([
            "The termite ate through a lot of your money.",
            "",
            f"You lost ${losses:,}."
        ])
        
        return {
            "title": "Hungry Termites",
            "text": result_text,
            "continue": True,
            "state": self.to_dict()
        }
    
    def starving_cow(self):
        """Rich day event - Betsy's return with tractor (conditional)"""
        if "Betsy" not in self.met_npcs or "Betsy Tractor" not in self.dangers:
            return self.trigger_event('day')
        
        self.dangers.add("Betsy Army")
        self.dangers.discard("Betsy Tractor")
        
        return {
            "title": "Starving Cow",
            "text": [
                "You wake up to the sound of a tractor barreling closer. As you jump up from your seat, you see the tractor getting closer to your wagon.",
                "",
                "The tractor drives beside your vehicle, and pushes right up against you, grinding the paint off your car. That's just mean.",
                "",
                "You look up at the driver to see a beautiful black and white cow. Good god, it's Betsy. Why, Betsy, why. The cow moos at you aggressively, and you roll down the window.",
                "",
                "Betsy stares into your soul, then looks over at the seat next to you. It appears Betsy is interested in your pile of money."
            ],
            "choices": [
                {"text": "Feed Betsy $10,000", "value": "feed"},
                {"text": "Refuse to feed Betsy", "value": "refuse"}
            ],
            "state": self.to_dict()
        }
    
    def starving_cow_choice(self, choice):
        """Handle Betsy feeding choices"""
        if choice == "feed":
            if self.balance < 10000:
                return {
                    "title": "Not Enough Money",
                    "text": [
                        "You don't have enough money to feed Betsy!",
                        "",
                        "She moos angrily at you."
                    ],
                    "choices": [
                        {"text": "Refuse to feed Betsy", "value": "refuse"}
                    ],
                    "state": self.to_dict()
                }
            
            self.balance -= 10000
            
            # Check if Betsy is satisfied
            if random.randint(0, 3) == 0 or self.balance < 50000:
                return {
                    "title": "Betsy is Satisfied",
                    "text": [
                        "You reach out your window, and put a stack of bills, worth $10,000 into Betsy's mouth. She chews them up, then spits them out into your wagon.",
                        "",
                        "Betsy moos, then smiles. She pulls away from the car, and drives the tractor down the road, happy as can be."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            else:
                return {
                    "title": "Betsy Wants More",
                    "text": [
                        "You reach out your window, and put a stack of bills, worth $10,000 into Betsy's mouth. She chews them up, then spits them out into your wagon.",
                        "",
                        "Betsy moos, then stares you down. She doesn't seem to be done with you."
                    ],
                    "choices": [
                        {"text": "Feed Betsy $10,000 again", "value": "feed"},
                        {"text": "Refuse to feed Betsy", "value": "refuse"}
                    ],
                    "state": self.to_dict()
                }
        else:  # refuse
            damage = random.randint(40, 60)
            self.health = max(0, self.health - damage)
            
            return {
                "title": "Betsy Attacks!",
                "text": [
                    "Betsy moos, then backs the tractor up. She then proceeds to step on the gas, and drives the tractor forward at your vehicle, slamming into the front of your wagon hard.",
                    "",
                    "She moos and moos and moos, pushing your car further back. The jolt of the vehicles smashing into each other kills, and your spine begins to fracture.",
                    "",
                    f"You take {damage} damage!",
                    "",
                    "Betsy finally backs away, satisfied with the destruction."
                ],
                "continue": True,
                "state": self.to_dict()
            }

    # NIGHT EVENTS
    def beach_swim(self):
        """Rich night event - swimming at the beach"""
        self.met_npcs.add("Beach Swim Event")
        
        event_type = random.choice(["jellyfish", "relaxation", "undertow"])
        
        if event_type == "jellyfish":
            return {
                "title": "Beach Swim",
                "text": [
                    "You slip into the moonlit surf, the water cool and alive around you. The ocean's pulse is steady, ancient, and you feel both small and infinite as you float beyond the breakers.",
                    "",
                    "A sudden, electric sting wraps around your leg—a jellyfish! The pain is sharp and immediate. Do you try to tough it out or rush back to shore?"
                ],
                "choices": [
                    {"text": "Tough it out", "value": "tough"},
                    {"text": "Rush to shore", "value": "shore"}
                ],
                "event_context": "jellyfish",
                "state": self.to_dict()
            }
        elif event_type == "relaxation":
            heal_amount = random.randint(15, 30)
            self.health = min(100, self.health + heal_amount)
            self.status_effects.add("Relaxed")
            
            return {
                "title": "Beach Swim - Relaxation",
                "text": [
                    "You slip into the moonlit surf, the water cool and alive around you. The ocean's pulse is steady, ancient, and you feel both small and infinite as you float beyond the breakers.",
                    "",
                    "You float on your back, the stars spinning above you. The water cradles you, washing away your worries. For a moment, you are at peace, and the world feels kind.",
                    "",
                    f"You heal {heal_amount} health!"
                ],
                "continue": True,
                "state": self.to_dict()
            }
        else:  # undertow
            return {
                "title": "Beach Swim - Undertow",
                "text": [
                    "You slip into the moonlit surf, the water cool and alive around you. The ocean's pulse is steady, ancient, and you feel both small and infinite as you float beyond the breakers.",
                    "",
                    "A sudden current tugs at your legs—the undertow! You struggle, panic rising. Do you fight the current or let it carry you?"
                ],
                "choices": [
                    {"text": "Fight the current", "value": "fight"},
                    {"text": "Let it carry you", "value": "carry"}
                ],
                "event_context": "undertow",
                "state": self.to_dict()
            }
    
    def beach_swim_choice(self, choice, event_context="jellyfish"):
        """Handle beach swim choices"""
        if event_context == "jellyfish":
            if choice == "tough":
                if random.random() < 0.5:
                    self.status_effects.add("Resilient")
                    return {
                        "title": "Endured the Pain",
                        "text": [
                            "You grit your teeth and float, letting the pain ebb with the tide.",
                            "",
                            "Eventually, the sting fades, and you feel stronger for having endured it."
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
                else:
                    damage = random.randint(15, 30)
                    self.health = max(0, self.health - damage)
                    return {
                        "title": "Pain Intensifies",
                        "text": [
                            "The pain intensifies, your vision blurs, and you barely make it back to shore, shivering and weak.",
                            "",
                            f"You take {damage} damage!"
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
            else:  # shore
                damage = random.randint(8, 18)
                self.health = max(0, self.health - damage)
                return {
                    "title": "Rush to Shore",
                    "text": [
                        "You thrash for shore, each stroke agony. You collapse on the sand, breathless, but alive.",
                        "",
                        f"You take {damage} damage."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
        else:  # undertow
            if choice == "fight":
                if random.random() < 0.5:
                    damage = random.randint(5, 10)
                    self.health = max(0, self.health - damage)
                    return {
                        "title": "Escaped the Current",
                        "text": [
                            "You swim parallel to the shore, remembering old advice. The current releases you, and you stagger back to the beach, exhausted but safe.",
                            "",
                            f"You take {damage} damage."
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
                else:
                    damage = random.randint(15, 25)
                    self.health = max(0, self.health - damage)
                    return {
                        "title": "Swept Away",
                        "text": [
                            "You fight, but the current is too strong. You're swept far down the beach, losing time and energy.",
                            "",
                            f"You take {damage} damage."
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
            else:  # carry
                self.status_effects.add("Oceanwise")
                return {
                    "title": "Trusting the Ocean",
                    "text": [
                        "You let the current carry you, trusting the ocean.",
                        "",
                        "Eventually, it spits you out far from where you started, but you're unharmed—and oddly exhilarated."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
    
    def beach_dive(self):
        """Rich night event - diving at the beach"""
        self.met_npcs.add("Beach Dive Event")
        
        event_type = random.choice(["pearl", "treasure", "shark"])
        
        if event_type == "pearl":
            self.inventory["Giant Pearl"] = 1
            self.status_effects.add("Lucky")
            
            return {
                "title": "Beach Dive - Pearl",
                "text": [
                    "You wade into the surf and dive beneath the waves, the world above replaced by a blue, sun-dappled silence. The ocean floor is a shifting landscape of sand, shells, and secrets.",
                    "",
                    "You spot a glimmer in the sand and dig with your hands. Your fingers close around a perfect, iridescent pearl, larger than any you've seen before.",
                    "",
                    "You surface, gasping, the pearl clutched in your hand. You feel luckier, as if the ocean itself has blessed you."
                ],
                "continue": True,
                "state": self.to_dict()
            }
        elif event_type == "treasure":
            return {
                "title": "Beach Dive - Sunken Chest",
                "text": [
                    "You wade into the surf and dive beneath the waves, the world above replaced by a blue, sun-dappled silence. The ocean floor is a shifting landscape of sand, shells, and secrets.",
                    "",
                    "You find the rotting remains of a wooden chest, half-buried in the sand. Do you try to open it?"
                ],
                "choices": [
                    {"text": "Open the chest", "value": "open"},
                    {"text": "Leave it alone", "value": "leave"}
                ],
                "state": self.to_dict()
            }
        else:  # shark
            if random.random() < 0.5:
                return {
                    "title": "Beach Dive - Shark Encounter",
                    "text": [
                        "You wade into the surf and dive beneath the waves, the world above replaced by a blue, sun-dappled silence. The ocean floor is a shifting landscape of sand, shells, and secrets.",
                        "",
                        "A shadow glides overhead—a massive shark, circling. You freeze, heart pounding, as it draws closer.",
                        "",
                        "You remain still, barely breathing, and the shark loses interest, vanishing into the blue."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            else:
                damage = random.randint(20, 40)
                self.health = max(0, self.health - damage)
                return {
                    "title": "Beach Dive - Shark Attack!",
                    "text": [
                        "You wade into the surf and dive beneath the waves, the world above replaced by a blue, sun-dappled silence. The ocean floor is a shifting landscape of sand, shells, and secrets.",
                        "",
                        "A shadow glides overhead—a massive shark, circling. You freeze, heart pounding, as it draws closer.",
                        "",
                        "The shark lunges! You kick and punch, barely escaping with your life, blood swirling in the water.",
                        "",
                        f"You take {damage} damage!"
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
    
    def beach_dive_choice(self, choice):
        """Handle beach dive treasure choices"""
        if choice == "open":
            loot_type = random.choice(["coins", "artifact", "trap"])
            
            if loot_type == "coins":
                money = random.randint(1000, 3000)
                self.balance += money
                return {
                    "title": "Treasure Found!",
                    "text": [
                        "Inside, you find gold coins and jeweled trinkets, their colors dulled by the sea. You stuff your pockets and swim for the surface.",
                        "",
                        f"You gain ${money:,}!"
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            elif loot_type == "artifact":
                self.inventory["Ocean Relic"] = 1
                return {
                    "title": "Strange Artifact",
                    "text": [
                        "You find a strange, barnacle-encrusted artifact. As you touch it, you feel a surge of energy—and a whisper in your mind."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
            else:  # trap
                damage = random.randint(15, 30)
                self.health = max(0, self.health - damage)
                return {
                    "title": "Jellyfish Trap!",
                    "text": [
                        "A cloud of stinging jellyfish bursts from the chest! You thrash and swim away, your skin burning.",
                        "",
                        f"You take {damage} damage!"
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
        else:  # leave
            return {
                "title": "Left Alone",
                "text": [
                    "You leave the chest alone, wary of curses and the weight of the deep."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def city_streets(self):
        """Rich night event - wandering city streets"""
        self.met_npcs.add("City Streets Event")
        
        event_type = random.choice(["drug_dealer", "stray_cat", "rent_bike", "none"])
        
        if event_type == "drug_dealer":
            return {
                "title": "City Streets - Drug Dealer",
                "text": [
                    "You wander the city's labyrinth of neon and shadow, where every alley whispers a different story. The air is thick with exhaust, music, and the promise of trouble. Tonight, the city feels alive—and hungry.",
                    "",
                    "A gaunt figure in a hoodie steps from a flickering doorway, eyes darting. 'Looking for a little edge?' he asks, holding out a small bag. The city seems to hold its breath. Do you accept?"
                ],
                "choices": [
                    {"text": "Accept the offer", "value": "accept"},
                    {"text": "Decline and move on", "value": "decline"}
                ],
                "event_context": "drug_dealer",
                "state": self.to_dict()
            }
        elif event_type == "stray_cat":
            return {
                "title": "City Streets - Stray Cat",
                "text": [
                    "You wander the city's labyrinth of neon and shadow, where every alley whispers a different story. The air is thick with exhaust, music, and the promise of trouble. Tonight, the city feels alive—and hungry.",
                    "",
                    "A scruffy, one-eyed cat weaves between your legs, meowing with a raspy voice. Its fur is matted, but its gaze is sharp. Do you kneel to pet it?"
                ],
                "choices": [
                    {"text": "Pet the cat", "value": "pet"},
                    {"text": "Ignore it", "value": "ignore"}
                ],
                "event_context": "stray_cat",
                "state": self.to_dict()
            }
        elif event_type == "rent_bike":
            return {
                "title": "City Streets - Rental Bikes",
                "text": [
                    "You wander the city's labyrinth of neon and shadow, where every alley whispers a different story. The air is thick with exhaust, music, and the promise of trouble. Tonight, the city feels alive—and hungry.",
                    "",
                    "You spot a row of battered rental bikes. The city's traffic is a snarl, but on two wheels, you could fly. Do you rent a bike and ride?"
                ],
                "choices": [
                    {"text": "Rent a bike", "value": "rent"},
                    {"text": "Walk instead", "value": "walk"}
                ],
                "event_context": "rent_bike",
                "state": self.to_dict()
            }
        else:  # none
            return {
                "title": "City Streets",
                "text": [
                    "You wander the city's labyrinth of neon and shadow, where every alley whispers a different story. The air is thick with exhaust, music, and the promise of trouble. Tonight, the city feels alive—and hungry.",
                    "",
                    "Tonight, the city is just a city. You wander, lost in thought, as the world spins on around you. But you can't shake the feeling that you're being watched."
                ],
                "continue": True,
                "state": self.to_dict()
            }
    
    def city_streets_choice(self, choice, event_context):
        """Handle city streets choices"""
        if event_context == "drug_dealer":
            if choice == "accept":
                outcome = random.choice(["buff", "bad_trip", "police"])
                
                if outcome == "buff":
                    self.status_effects.add("Energized")
                    return {
                        "title": "Enhanced",
                        "text": [
                            "You slip the contents under your tongue. The world sharpens—colors brighter, sounds clearer. For a while, you feel invincible, your luck uncanny."
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
                elif outcome == "bad_trip":
                    damage = random.randint(15, 30)
                    loss = random.randint(200, 800)
                    self.health = max(0, self.health - damage)
                    self.balance -= loss
                    return {
                        "title": "Bad Trip",
                        "text": [
                            "Your heart races, the world tilts, and you stagger into the street. You lose track of time—and some money.",
                            "",
                            "When you come to, your pockets are lighter and your head aches.",
                            "",
                            f"You take {damage} damage and lose ${loss:,}!"
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
                else:  # police
                    loss = random.randint(100, 400)
                    self.balance -= loss
                    return {
                        "title": "Police!",
                        "text": [
                            "Suddenly, blue lights flash. 'Police! Hands up!' You drop the bag and run, barely escaping.",
                            "",
                            f"You lose ${loss:,} in the chaos."
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
            else:  # decline
                return {
                    "title": "Declined",
                    "text": [
                        "You shake your head and move on, the dealer's gaze burning into your back. The city feels colder."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
        
        elif event_context == "stray_cat":
            if choice == "pet":
                fate = random.choice(["lucky", "scratch", "ally"])
                
                if fate == "lucky":
                    self.status_effects.add("Lucky")
                    return {
                        "title": "Lucky Whisker",
                        "text": [
                            "The cat purrs, rubbing its head against your hand. It leaves a whisker in your palm.",
                            "",
                            "You feel luckier, as if the city itself is watching over you."
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
                elif fate == "scratch":
                    damage = random.randint(3, 10)
                    self.health = max(0, self.health - damage)
                    return {
                        "title": "Scratched!",
                        "text": [
                            "The cat hisses and claws your hand before darting away. You wince, blood trickling from the scratch.",
                            "",
                            f"You take {damage} damage."
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
                else:  # ally
                    self.inventory["Stray Cat"] = 1
                    return {
                        "title": "Furry Companion",
                        "text": [
                            "The cat follows you for blocks, scaring off a would-be pickpocket.",
                            "",
                            "You gain a furry companion for the night."
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
            else:  # ignore
                return {
                    "title": "Ignored",
                    "text": [
                        "You ignore the cat, but its eyes follow you, unblinking, as you disappear into the city's maze."
                    ],
                    "continue": True,
                    "state": self.to_dict()
                }
        
        else:  # rent_bike
            if choice == "rent":
                outcome = random.choice(["fast", "crash", "theft"])
                
                if outcome == "fast":
                    self.status_effects.add("Refreshed")
                    return {
                        "title": "Exhilarating Ride",
                        "text": [
                            "You weave through traffic, the wind in your hair, dodging taxis and street vendors.",
                            "",
                            "You arrive at your next destination exhilarated and ahead of schedule."
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
                elif outcome == "crash":
                    damage = random.randint(8, 18)
                    loss = random.randint(50, 200)
                    self.health = max(0, self.health - damage)
                    self.balance -= loss
                    return {
                        "title": "Bike Crash!",
                        "text": [
                            "A pothole sends you flying. You limp away, bruised and battered, your wallet lighter from the repair fee.",
                            "",
                            f"You take {damage} damage and lose ${loss:,}!"
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
                else:  # theft
                    loss = random.randint(200, 600)
                    self.balance -= loss
                    return {
                        "title": "Bike Stolen!",
                        "text": [
                            "You stop for a snack, and when you return, the bike is gone—stolen.",
                            "",
                            f"You pay a hefty fine of ${loss:,} to the rental company."
                        ],
                        "continue": True,
                        "state": self.to_dict()
                    }
