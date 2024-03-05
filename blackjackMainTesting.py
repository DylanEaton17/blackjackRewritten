import blackjack
import story

def main():
    player = story.Player()

    # Set Custom Balance
    player.set_balance(200)
    print("Set Balance: " + str(player.get_balance()))


    # Do whatever
    player.end_day()
    player.day_event()
    player.afternoon()


if __name__ == "__main__":
    main()