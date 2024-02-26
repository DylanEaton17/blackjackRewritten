import blackjack

def test_deck_len():
    # Setup
    deck = blackjack.Deck()
    expected = 52

    # Invoke
    actual = len(deck)

    # Analyze
    assert actual == expected

def test_card_repr():
    # Setup
    name = "Ace"
    suit = "Spades"
    value = 1
    card = blackjack.Card(name, suit, value)
    expected = "Ace of Spades"

    # Invoke
    actual = repr(card)

    # Analyze
    assert actual == expected