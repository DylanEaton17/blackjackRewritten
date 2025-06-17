import blackjack
import story

def main():
    player = story.Player()
    blackjackGame = blackjack.Blackjack(player)
    player.set_balance(100000)
    player.update_rank()
    print(player.get_rank())


    # player.first_setup()
    # player.opening_lines()
    while(True):
        player.start_day()
        player.afternoon()
        blackjackGame.play_round()
        player.end_day()
        
        


if __name__ == "__main__":
    main()