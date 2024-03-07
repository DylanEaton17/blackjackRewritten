import blackjack
import story

def main():
    player = story.Player()
    blackjackGame = blackjack.Blackjack(player)
    # player.first_setup()
    player.add_item("Delight Indicator")
    player.add_item("Golden Watch")
    player.add_item("Dirty Old Hat")
    # player.opening_lines()
    while(True):
        blackjackGame.play_round()
        player.end_day()
        player.day_event()
        player.afternoon()


if __name__ == "__main__":
    main()