import blackjack
import story

def main():
    player = story.Player()
    blackjackGame = blackjack.Blackjack(player)


    # Set Custom Balance
    player.set_balance(2000)
    print("Set Balance: " + str(player.get_balance()))
    player.add_item("Car")

    # Do whatever
    player.increment_day()
    player.afternoon()

    # Useful Functions
    # while(True):
    # player.day_event()
    # player.afternoon()
    # player.update_status()
    player.increment_day()
    # player.add_item()

if __name__ == "__main__":
    main()