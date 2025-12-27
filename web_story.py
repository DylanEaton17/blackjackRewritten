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
        Returns event data
        """
        # For now, return a placeholder
        # TODO: Implement all 47 events
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
