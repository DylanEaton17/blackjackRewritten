import blackjack
import story

def main():
    player = story.Player()
    blackjackGame = blackjack.Blackjack(player)


    # Set Custom Balance
    player.set_balance(10000)
    print("Set Balance: " + str(player.get_balance()))
    player.add_item("Car")
    player.add_item("Faulty Insurance")
    player.add_item("Delight Indicator")
    player.add_item("Health Indicator")
    player.add_item("Dirty Old Hat")
    player.add_item("Golden Watch")
    player.add_item("Sneaky Peeky Glasses")
    player.break_item("Golden Watch")
    player.break_item("Delight Indicator")
    player.break_item("Dirty Old Hat")
    player.meet("Witch")
    player.meet("Tom")


    while(True):
        player.afternoon()
        blackjackGame.play_round()
        player.end_day()
        player.day_event()

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