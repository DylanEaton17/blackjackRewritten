import blackjack
import story

def main():
    player = story.Player()
    blackjackGame = blackjack.Blackjack(player)
    # player.first_setup()
    # player.opening_lines()
    while(True):
        blackjackGame.play_round(1)
        player.end_day()
        player.day_event()
        blackjackGame.update_player(player)
        print("\n")



if __name__ == "__main__":
    main()