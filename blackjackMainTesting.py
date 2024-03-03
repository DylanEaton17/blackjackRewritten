import blackjack
import story

def main():
    player = story.Player()

    # Set Custom Balance
    player.set_balance(50)
    print("Set Balance: " + str(player.get_balance()))
    player.add_item("Map")
    player.meet("Witch")
    player.add_item("Car")
    player.add_item("Pest Control")
    player.add_danger("Cockroach")
    player.add_status("Spider Bite")

    # Do whatever
    player.afternoon()


if __name__ == "__main__":
    main()