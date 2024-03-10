import blackjack
import story

def main():
    player = story.Player()
    blackjackGame = blackjack.Blackjack(player)


    # Set Custom Balance
    player.set_balance(789654)
    print("Set Balance: " + str(player.get_balance()))
    player.add_item("Car")
    player.add_item("Faulty Insurance")
    player.add_item("Delight Indicator")
    player.hurt(95)
    player.add_item("Health Indicator")
    player.add_item("Dirty Old Hat")
    player.add_item("Golden Watch")
    player.add_item("Sneaky Peeky Glasses")

    # Do whatever
    player.visit_witch_doctor()

    # while(True):
    #     blackjackGame.play_round()
    #     player.end_day()
    #     player.day_event()
    #     player.afternoon()

    # Useful Functions
    """
    player.day_event()
    player.afternoon()
    player.update_status()
    player.increment_day()
    player.add_item()
    """

    # Implemented Items
    """
    player.add_item("Faulty Insurance")
    player.add_item("Delight Indicator")
    player.add_item("Health Indicator")
    player.add_item("Dirty Old Hat")
    player.add_item("Golden Watch")
    player.add_item("Sneaky Peeky Glasses")
    """


if __name__ == "__main__":
    main()