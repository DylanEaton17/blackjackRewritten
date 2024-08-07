import blackjack
import story

def main():
    player = story.Player()
    blackjackGame = blackjack.Blackjack(player)


    # Set Custom Balance
    player.set_balance(500)
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
    # player.break_item("Delight Indicator")
    player.break_item("Dirty Old Hat")
    player.break_item("Health Indicator")
    player.meet("Witch")
    player.meet("Frank")
    player.increment_day()
    

    test = "basic"
    match test:
            case "basic":
                blackjackGame.play_round(1)
                player.end_day()
                player.start_day()
                player.afternoon()
            case "thunderstorm":
                player.thunderstorm()
                player.afternoon()
                player.end_day()
            case "end_day":
                player.increment_day()
                player.end_day()
                player.start_day()
            case "afternoon":
                player.add_item("Car")
                player.add_item("Map")
                player.meet("Frank")
                player.meet("Oswald")
                player.meet("Tom")
                player.meet("Witch")
                player.afternoon()
            case "guess_the_number":
                

    
    # blackjackGame.play_round(1)
    # player.set_balance(1000)
    # blackjackGame.play_round(1)
    # player.set_balance(10000)
    # blackjackGame.play_round(1)
    # player.set_balance(100000)
    # blackjackGame.play_round(1)
    # player.set_balance(500000)
    # blackjackGame.play_round(1)
    # player.set_balance(900000)



    # Useful Functions
    """
    player.start_day()
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