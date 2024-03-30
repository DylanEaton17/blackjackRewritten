import blackjack
import story

def main():
    player = story.Player()
    blackjackGame = blackjack.Blackjack(player)


    # Set Custom Balance
    player.set_balance(900000)
    print("Your current balance: " + str("${:,}".format(player.get_balance())))
    player.add_item("Car")
    player.add_item("Faulty Insurance")
    player.add_item("Delight Indicator")
    player.add_item("Health Indicator")
    player.add_item("Dirty Old Hat")
    player.add_item("Golden Watch")
    player.add_item("Sneaky Peeky Shades")
    player.add_item("Quiet Sneakers")
    player.break_item("Faulty Insurance")
    player.break_item("Sneaky Peeky Shades")
    player.break_item("Golden Watch")
    player.break_item("Quiet Sneakers")
    player.break_item("Delight Indicator")
    player.break_item("Dirty Old Hat")
    player.break_item("Health Indicator")
    player.meet("Witch")
    player.meet("Frank")
    player.increment_day()


    while(True):
        player.visit_frank()
        player.increment_day()
        player.increment_day()
        player.visit_frank()
        player.increment_day()


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