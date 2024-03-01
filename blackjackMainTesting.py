import blackjack
import story

def main():
    player = story.Player()
    player.set_balance(200)
    print("Set Balance: " + str(player.get_balance()))
    player.day_event()


if __name__ == "__main__":
    main()