import blackjack
import story

def main():
    player = story.Player()
    blackjackGame = blackjack.Blackjack(player)
    # player.first_setup()
    # player.opening_lines()
    while(True):
        blackjackGame.play_round(3)
        player.end_day()
        player.day_event()
        print("\n")



if __name__ == "__main__":
    main()