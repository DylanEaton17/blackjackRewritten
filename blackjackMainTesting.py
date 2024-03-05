import blackjack
import story

def main():
    player = story.Player()
    blackjackGame = blackjack.Blackjack(player)


    # Set Custom Balance
    player.set_balance(200)
    print("Set Balance: " + str(player.get_balance()))
    player.add_item("Car")

    # Do whatever
    while(True):
        player.day_event()
        player.update_status()
        player.increment_day()

if __name__ == "__main__":
    main()