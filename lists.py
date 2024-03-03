import random

class Lists:
    def __init__(self, player):
        self.__player = player
        self.__quote_list = self.make_quote_list()
        self.__cheers_list = self.make_cheers_list()
        self.__advice_list = self.make_advice_list()
        self.__quote_setup_list = self.make_quote_setup_list()
        self.__quote_setup_list = self.make_quote_setup_list()
        self.__poor_day_events = self.make_poor_day_events_list()
        self.__cheap_day_events = self.make_cheap_day_events_list()
        self.__modest_day_events = self.make_modest_day_events_list()
        self.__rich_day_events = self.make_rich_day_events_list()
        self.__doughman_day_events = self.make_doughman_day_events_list()
        self.__nearly_day_events = self.make_nearly_day_events_list()
        self.__poor_night_events = self.make_poor_night_events_list()
        self.__cheap_night_events = self.make_cheap_night_events_list()
        self.__modest_night_events = self.make_modest_night_events_list()
        self.__rich_night_events = self.make_rich_night_events_list()
        self.__doughman_night_events = self.make_doughman_night_events_list()
        self.__nearly_night_events = self.make_nearly_night_events_list()
        self.__shop_list = self.make_shop_list()




# This is a lot of similar code, but each list is a unique set of events
# That happen in each rank.
        
# If the list is empty, it recreates the list.
# Each event specifically has a chance of not triggering if certain
# conditions arent met
        
# Poor Events (1 - 1,000)
    def make_poor_day_events_list(self):
        a_list = []
        a_list.append("seat_cash")
        a_list.append("left_window_down")
        a_list.append("spider_bite")
        a_list.append("hungry_cockroach")
        random.shuffle(a_list)
        return a_list
    
    def make_poor_night_events_list(self):
        a_list = []
        return a_list

    def get_poor_day_event(self):
        if len(self.__poor_day_events)==0:
            self.__poor_day_events = self.make_poor_day_events_list()
        return self.__poor_day_events.pop()
    
    def get_poor_night_event(self):
        if len(self.__poor_night_events)==0:
            self.__poor_night_events = self.make_poor_night_events_list()
        return self.__poor_night_events.pop()
    

# Cheap Events (1,000 - 10,000)
    def make_cheap_day_events_list(self):
        a_list = []
        return a_list
    
    def make_cheap_night_events_list(self):
        a_list = []
        return a_list

    def get_cheap_day_event(self):
        if len(self.__cheap_day_events)==0:
            self.__cheap_day_events = self.make_cheap_day_events_list()
        return self.__cheap_day_events.pop()
    
    def get_cheap_night_event(self):
        if len(self.__cheap_night_events)==0:
            self.__cheap_night_events = self.make_cheap_night_events_list()
        return self.__cheap_night_events.pop()

    
# Modest Events (10,000 - 100,000)
    def make_modest_day_events_list(self):
        a_list = []
        return a_list
    
    def make_modest_night_events_list(self):
        a_list = []
        return a_list

    def get_modest_day_event(self):
        if len(self.__modest_day_events)==0:
            self.__modest_day_events = self.make_modest_day_events_list()
        return self.__modest_day_events.pop()
    
    def get_modest_night_event(self):
        if len(self.__modest_night_events)==0:
            self.__modest_night_events = self.make_modest_night_events_list()
        return self.__modest_night_events.pop()
    

# Rich Events (100,000 - 500,000)
    def make_rich_day_events_list(self):
        a_list = []
        return a_list
    
    def make_rich_night_events_list(self):
        a_list = []
        return a_list

    def get_rich_day_event(self):
        if len(self.__rich_day_events)==0:
            self.__rich_day_events = self.make_rich_day_events_list()
        return self.__rich_day_events.pop()
    
    def get_rich_night_event(self):
        if len(self.__rich_night_events)==0:
            self.__rich_night_events = self.make_rich_night_events_list()
        return self.__rich_night_events.pop()


# Doughman Events (500,000 - 900,000)
    def make_doughman_day_events_list(self):
        a_list = []
        return a_list
    
    def make_doughman_night_events_list(self):
        a_list = []
        return a_list

    def get_doughman_day_event(self):
        if len(self.__doughman_day_events)==0:
            self.__doughman_day_events = self.make_doughman_day_events_list()
        return self.__doughman_day_events.pop()

    def get_doughman_night_event(self):
        if len(self.__doughman_night_events)==0:
            self.__doughman_night_events = self.make_doughman_night_events_list()
        return self.__doughman_night_events.pop()
    

# Nearly There Events (900,000 - 1,000,000)
    def make_nearly_day_events_list(self):
        a_list = []
        return a_list
    
    def make_nearly_night_events_list(self):
        a_list = []
        return a_list

    def get_nearly_day_event(self):
        if len(self.__nearly_day_events)==0:
            self.__nearly_day_events = self.make_nearly_day_events_list()
        return self.__nearly_day_events.pop()
    
    def get_nearly_night_event(self):
        if len(self.__nearly_night_events)==0:
            self.__nearly_night_events = self.make_nearly_night_events_list()
        return self.__nearly_night_events.pop()
    
    def make_shop_list(self):
        a_list = []
        a_list.append("Doctor's Office")
        if(self.__player.has_met("Witch")):
            a_list.append("Witch Doctor's Tower")
        a_list.append("Convenience Store")
        if(self.__player.has_item("Map")):
            a_list.append("Marvin's Mystical Merchandise")
        return a_list

    def get_shop(self, number):
        return 
    
    def make_marvin_inventory(self):
        a_list = []
        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Delight Indicator")):
            a_list.append("Delight Indicator")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Health Indicator")):
            a_list.append("Health Indicator")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Dirty Old Hat")):
            a_list.append("Dirty Old Hat")
        
        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Golden Watch")):
            a_list.append("Golden Watch")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Faulty Insurance")):
            a_list.append("Faulty Insurance")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Enchanting Silver Bar")):
            a_list.append("Enchanting Silver Bar")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Sneaky Peeky Glasses")):
            a_list.append("Sneaky Peeky Glasses")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Quiet Sneakers")):
            a_list.append("Quiet Sneakers")

        random.shuffle(a_list)
        return a_list

    def make_quote_list(self):
        a_list = []
        a_list.append("\"Stars aren't far away. They're just really small. They're so small that all 17 of them could fit into the earth. That's why we can't get to them. They move away so the planet doesn't eat them and only show up at night when the earth is sleeping.\"")
        a_list.append("\"You may have breathed the same air a dinosaur breathed 1000s of years ago. If you don't think that's the tightest shit then get out of my face.\"")
        a_list.append("\"Don't be afraid to fail. Be afraid to get emotionally invested and then fail.\"")
        a_list.append("\"Every corpse on Everest was once an extremely motivated person.\"")
        a_list.append("\"I honest to God thought Santa Claus was real for the longest time. Mom and Dad just never told me. My parents are fucking cruel.\"")
        a_list.append("\"Every tattoo is a temporary tattoo, because we are all slowly dying.\"")
        a_list.append("\"The reason you have to follow your dreams is because even your dreams are trying to get away from you.\"")
        a_list.append("\"If you give up on your dreams, that may free up some time to get some actual stuff done\"")
        a_list.append("\"If you hate yourself, remember that you are not alone. A lot of other people hate you too.\"")
        a_list.append("\"The trash gets picked up tomorrow. Be ready.\"")
        a_list.append("\"I'm not your fucking therapst, stop using me for emotional advice.\"")
        a_list.append("\"No matter how many motivational quotes you know, you will remain a pathetic loser. Yesterday, today, and tomorrow. No matter how much you make, what degree you earn or what lie you tell yourself. A big flop at life you will remain. Don't doubt it for a minute. That's not even addressing your disgustinly deformed physique.\"")
        a_list.append("\"Good Moms have sticky floors, messy kitchens, laundry piles, dirty ovens, and happy kids.\"")
        a_list.append("\"Before you can love someone else you have to learn to love yourself so there's no chance of that happening.\"")
        a_list.append("\"There was a safety meeting at work today. They asked me, 'What steps would you take in the event of a fire?' 'Fucking big ones' was the wrong answer.\"")
        a_list.append("\"I walk around like everything's fine, but deep down, inside my shoe, my sock is sliding off.\"")
        a_list.append("\"Life would be a lot easier if it wasn't so hard.\"")
        a_list.append("\"I can't brain today. I have the dumb.\"")
        a_list.append("\"If you don't want to be mistaken for a doormat, get off the damn floor.\"")
        a_list.append("\"You know it's cold outside when you go outside and it's cold.\"")
        a_list.append("\"If I had to rate you from 1 to 10, I'd give you a 9, because I'm the 1 you're missing.\"")
        a_list.append("\"Have you ever wondered why you can't taste your tongue?\"")
        a_list.append("\"Freedom means the right to yell, \"THEATRE!\" in a crowded fire.\"")
        a_list.append("\"Whatever you're doing, always give 100 percent. Unless you're donating blood.\"")
        a_list.append("\"Would you believe that my neighbor came ringing my doorbell at 2:00 this morning? Luckily for him, I was still up playing bagpipes.\"")
        a_list.append("\"If a man said he'll fix it, he'll fix it. There is no need to nag him every 6 months about it.\"")
        a_list.append("\"Every form has its own meaning. Every man creates his meaning and form and goal. Why is it so important - what others have done? Why does it become sacred by the mere fact of not being your own? Why is anyone and everyone right - so long as it's not yourself? Why does the number of those others take the place of truth? Why is truth made a mere matter of arithmetic - and only of addition at that? Why is everything twisted out of all sense to fit everything else? There must be some reason. I don't know. I've never known it. I'd like to understand.\"")
        a_list.append("\"Grief, I've learned, is really just love. It's all the love you want to give, but cannot. All that unspent love gathers up in the corners of your eyes, the lump in your throat, and in that hollow part of your chest. Grief is just love with no place to go.\"")
        a_list.append("\"Bananas! Bananas! Bananas! Bananas! Bananas! Bananas! Bananas! Bananas!\"")
        a_list.append("\"Remember, if you can't convince them, confuse them. It's like playing chess with a pigeon; no matter how good you are, the bird is going to knock over the pieces and strut around like it's victorious.\"")
        a_list.append("\"Why go the extra mile when you can just complain about the first one? After all, life is not about the journey or the destination; it's about finding a good parking spot.\"")
        a_list.append("\"Always borrow money from pessimists - they don't expect it back. Plus, it's a great way to test your invisibility cloak when they come to collect.\"")
        a_list.append("\"Remember, if at first you don't succeed, skydiving is not for you. Stick to ground-based failures where the stakes are low and the embarrassment is your only injury.\"")
        a_list.append("\"If life gives you lemons, keep them, because hey, free lemons. But if life gives you melons, you might be dyslexic.\"")
        a_list.append("\"Never do anything half-heartedly; always use your full heart, even if it's misguided, wrong, or downright bizarre. Full-hearted mistakes make the best stories.\"")
        a_list.append("\"Eat a live frog first thing in the morning, and nothing worse will happen to you the rest of the day. Except, of course, the haunting realization that you started your day by eating a live frog.\"")
        a_list.append("\"If you think nobody cares if you're alive, try missing a couple of car payments. Better yet, see how many friends you have left when you ask them to help you move.\"")
        a_list.append("\"If you can't beat them, dress better than them. If you can't dress better, at least be funnier. If you can't be funnier, just hide in the closet until they leave.\"")
        a_list.append("\"When one door closes, just open it again. It's a door; that's how they work. If it doesn't open, congratulations, you've found a wall.\"")
        a_list.append("\"Keep your friends close, your enemies closer, and receipts for all major purchases. You never know when you'll need to return something, or someone.\"")
        a_list.append("\"Remember, it's not paranoia if your plants are actually plotting against you. Keep them in check by pretending to water them with vinegar.\"")
        a_list.append("\"If you find yourself at a loss for words, try using someone else's. Plagiarism is just sharing with extra steps.\"")
        a_list.append("\"Why put off until tomorrow what you can avoid entirely? Remember, procrastination is not the problem, it's the solution.\"")
        a_list.append("\"Remember, if you can't handle me at my worst, then fair enough, I'm really unpleasant.\"")
        a_list.append("\"If life knocks you down, stay there and take a nap. The floor is already familiar with your failures; let it be your comfort.\"")
        a_list.append("\"A clear conscience is usually the sign of a bad memory. Keep forgetting your mistakes, and you'll achieve eternal peace.\"")
        a_list.append("\"Why walk when you can dance? Unless dancing is just walking with style, in which case, why not moonwalk everywhere and reverse your way through life's problems?\"")
        a_list.append("\"If at first you don't succeed, redefine success. Because if success is waking up at noon on a Wednesday thinking it's a Saturday, then congratulations, you've made it.\"")
        a_list.append("\"If a tree falls in the forest and no one is around to hear it, does it make a sound? More importantly, if a tree falls in your living room, can you blame it on the dog?\"")
        a_list.append("\"Life is short. Smile while you still have teeth.\"")
        a_list.append("\"Sometimes I wish I was a bird. So I could fly over certain people and poop on their heads.\"")
        a_list.append("\"In the grand tapestry of existence, one must consider the intricate dance of the cosmos, where each celestial body moves in perfect harmony, except when they don't, which is most of the time, really, leading one to ponder whether the stars are just freestyling it. This brings to mind the importance of breakfast, the most important meal of a day that is itself a construct, much like the notion that socks should always match or that cats have any respect for personal space, which is to say, it's all a matter of perspective, isn't it? And speaking of perspective, have you ever noticed how small a plane looks in the sky, which is itself a vast canvas of blue, or gray, or black, depending on the time, which, as we've established, is a construct?\"")
        a_list.append("\"Consider, if you will, the humble potato: a tuber, a starch, a veritable chameleon of the culinary world, which, much like our own journey through the winding corridors of life, starts underground, in the dark, unaware of its potential to become fries, mashed, or a gratin, which is really just a fancy way of saying 'baked with cheese.' And isn't that just like us? Starting out as raw potential, only to be shaped by our experiences, our trials, and yes, our cooking methods, until we emerge, golden.\"")
        a_list.append("\"Let's embark on a journey, a meandering path not unlike the serpentine wanderings of a leaf caught in a capricious autumn breeze, which, as it dances to the silent music of nature, reminds us of the unpredictable choreography of existence. This leaf, let's call it Gerald, flutters with an elegance borne of happenstance, a fragile vessel for the whims of the wind. Gerald's journey is not linear, nor is it bound by the rigid expectations of society's ceaselessly grinding gears. Instead, Gerald twirls, dips, and soars, embracing the chaos with a grace we can only aspire to. Now, consider the ant, industrious and steadfast, a creature of purpose and communal toil. Our ant, whom we'll name Beatrice, marches diligently on her quest for sustenance, her life a testament to the virtues of hard work and persistence. Yet, in the grand tapestry of the cosmos, what is Beatrice but a speck, a mere blip on the infinite canvas of the universe? And yet, does her insignificance in the face of the vast unknown render her efforts moot? I posit that it does not, for in the grand scheme, all actions, large and small, contribute to the intricate mosaic of existence. But back to Gerald, who by now has traversed the convoluted landscapes of our imagination, touching upon the existential questions that haunt the periphery of our consciousness. What can we learn from Gerald and Beatrice? Is it their resilience, their unyielding will to persist in the face of the insurmountable odds stacked against them by the very nature of their existence? Or is it, perhaps, the simple beauty of their dance, a reminder that life, in all its complexity and confusion, offers moments of sublime beauty, fleeting and precious, to be cherished and remembered? As Gerald finally comes to rest upon the earth, joining Beatrice in the eternal cycle of life and death, we are reminded that all journeys, whether they be of leaves or ants or the human heart, are interconnected in the grand, bewildering dance of the cosmos. So, what was the point of this story, you may ask? Well, that, my friend, is entirely up to you.\"")
        a_list.append("\"If the sky is the limit, then why is there footprints on the moon? Because sometimes cheese can fly, especially when clocks are melting and rabbits wear hats.\"")
        a_list.append("\"Why use a door when you can enter through an imaginary pineapple? Remember, only invisible keys can unlock hidden broccoli forests.\"")
        a_list.append("\"When life throws potatoes at you, make a spaceship. Because nothing says 'adventure' like a tuber in zero gravity, especially when sunglass-wearing fish pilot the craft.\"")
        a_list.append("\"If time is a circle, then are we all just rolling along like doughnuts in a bakery of eternity? Beware of the square bagels, they're time travelers in disguise.\"")
        a_list.append("\"Whisper to the rain and listen to the wind, for they tell tales of square watermelons and the secret life of shadows who are afraid of the dark.\"")
        a_list.append("\"Remember, if you ever get lost in the forest, turn left at the talking mushroom and wave hello to the sky. It's rude not to greet the blue, especially when it's wearing its fancy clouds.\"")
        a_list.append("\"Why ponder the meaning of life when you can dance with the whimsical ants under the moonlit spaghetti? It's all about finding the rhythm in the chaos of cereal whispers.\"")
        random.shuffle(a_list)
        return a_list

    def get_quote(self):
        if len(self.__quote_list)==0:
            self.__quote_list = self.make_quote_list()
        return self.__quote_list.pop()
    
    def make_cheers_list(self):
        a_list = []
        a_list.append("Congrats!")
        a_list.append("Hurray!")
        a_list.append("Yippee!")
        a_list.append("Woo-hoo!")
        a_list.append("Yessir!")
        a_list.append("Yesss!")
        a_list.append("Well done!")
        a_list.append("Bravo!")
        a_list.append("Fantastic!")
        a_list.append("Amazing!")
        a_list.append("Great job!")
        a_list.append("Excellent!")
        a_list.append("Superb!")
        a_list.append("Outstanding!")
        a_list.append("Impressive!")
        a_list.append("Keep it up!")
        a_list.append("Way to go!")
        a_list.append("You nailed it!")
        random.shuffle(a_list)
        return a_list

    def get_cheer(self):
        if len(self.__cheers_list)==0:
            self.__cheers_list = self.make_cheers_list()
        return self.__cheers_list.pop()
    
    def make_advice_list(self):
        a_list = []
        a_list.append("Good progress so far, pal. Keep it up.")
        a_list.append("For what it's worth, I think you're doing alright.")
        a_list.append("I mean, you could definately make more money, but hey it's a good start.")
        a_list.append("Congrats on all the hard work so far. It's nice to know you're still alive.")
        a_list.append("I would probably wipe that smile off that face if I were you. Just kidding, you're awesome.")
        a_list.append("Do you think maybe you could be a bit better at Blackjack? Just think about it.")
        a_list.append("I like your work ethic. Your grandma would be proud.")
        a_list.append("If there's one thing I've learned, it's that you must never back down, and never give up.")
        a_list.append("Your efforts haven't gone unnoticed. They're just not always mentioned.")
        a_list.append("Just so you know, your perseverance is more impressive than perfection.")
        a_list.append("Life's a garden, dig it. You're doing just that, and it's admirable.")
        a_list.append("You've got a unique path, and honestly, it's thrilling to watch it unfold.")
        a_list.append("Keep pushing the boundaries, even if it's just by a little every day.")
        a_list.append("Oh, look at you, making small changes like you're actually going to finish something. Adorable.")
        a_list.append("Look at you, using your full potential — just kidding, but seriously, nice effort today.")
        a_list.append("You might not be winning the race, but at least you're in the running, right? Sort of?")
        a_list.append("Your unique approach to life's challenges is so...inspiring? Yeah, let's go with that.")
        random.shuffle(a_list)
        return a_list

    def get_advice(self):
        if len(self.__advice_list)==0:
            self.__advice_list = self.make_advice_list()
        return self.__advice_list.pop()
    
    def make_quote_setup_list(self):
        a_list = []
        a_list.append("I'll leave you with a quote: ")
        a_list.append("Here's a little bit of inspiration for you: ")
        a_list.append("Here's a quote my dad used to say: ")
        a_list.append("This quote always gets me going: ")
        a_list.append("Something to ponder on your journey: ")
        a_list.append("If you ever feel lost, just remember: ")
        a_list.append("Take a moment to reflect on this: ")
        a_list.append("For those who enjoy a bit of bathroom philosophy: ")
        a_list.append("Don't forget what the bible taught you: ")
        a_list.append("If aliens could talk, they'd probably say: ")
        a_list.append("I read this once in a magazine: ")
        a_list.append("This one's straight from the fortune cookie in my lunch: ")
        a_list.append("Here's what my cat whispered to me last night: ")
        a_list.append("You know what you need right now? A quote, from the heart: ")
        a_list.append("As I tried to parallel park for the 10th time, I remember a passerby that yelled: ")
        a_list.append("As my doctor was putting me under, he whispered into my ear: ")
        random.shuffle(a_list)
        return a_list

    def get_quote_setup(self):
        if len(self.__quote_setup_list)==0:
            self.__quote_setup_list = self.make_quote_setup_list()
        return self.__quote_setup_list.pop()