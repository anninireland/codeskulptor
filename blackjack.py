
Blackjack
Built by Lisa Cavern as part of the Introduction to
Interactive Programming in Python course on Coursera.
course website: https://www.coursera.org/course/interactivepython2
project template: http://www.codeskulptor.org/#examples-blackjack_template.py


Goal: Have a higher value hand than the dealer without going over 21.

Cards in Blackjack have the following values: an ace may be valued as
either 1 or 11 (player's choice), face cards (kings, queens and jacks)
are valued at 10 and the value of the remaining cards corresponds to
their number. During a round of Blackjack, the players plays against
a dealer with the goal of building a hand (a collection of cards)
whose cards have a total value that is higher than the value of the
dealer's hand, but not over 21.

"""

# Mini-project #6 - Blackjack


import simplegui

import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
message = ""
score = 0
player_hand = 0
dealer_hand = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        s = ""
        for i in range(len(self.hand)):
            s += str(self.hand[i]) + "  "
        return s

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)
        return self.hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        aces = False
        for card in self.hand:
            value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                aces = True
        if aces:
            if value + 10 <= 21:
                value += 10

        return value

    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.hand:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(card.get_rank()),
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(card.get_suit()))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            # change pos to next slot over
            pos[0] += CARD_SIZE[0]

# define deck class
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        # for each suit, loop through the ranks and append the pair to the deck
        for s in SUITS:
            for r in RANKS:
                new_card = Card(s,r)
                self.deck.append(new_card)

    def shuffle(self):
        # shuffle the deck
        # use random.shuffle()
        random.shuffle(self.deck)
        return self.deck

    def deal_card(self):
        # deal a card object from the deck
        # pick out the first card in the deck list
        dealt_card = self.deck[-1]
        # pop out that card from the deck
        self.deck.pop(-1)
        return dealt_card

    def __str__(self):
        # return a string representing the deck
        decklist = ""
        for c in self.deck:
            decklist += str(c)
            decklist += " "
        return "Deck Contains: " + decklist


#define event handlers for buttons

def deal():		# create deck, hands; shuffle deck, deal 2 cards to each hand
    global outcome, in_play,player_hand, dealer_hand, deck, message, score
    outcome = ""
    print "New Hand"
    if in_play == True:
        outcome = "You have forfeited that last hand."
        score -= 1
    message = "Hit or Stand?"
    in_play = True
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    deck.shuffle()
    pc1 = deck.deal_card()
    player_hand.add_card(pc1)
    pc2 = deck.deal_card()
    player_hand.add_card(pc2)
    dc1 = deck.deal_card()
    dealer_hand.add_card(dc1)
    dc2 = deck.deal_card()
    dealer_hand.add_card(dc2)
    print "Player's Hand: ",  player_hand, "Dealer's Hand", dealer_hand
    print "Player's value: ",  player_hand.get_value(), "     Dealer's value", dealer_hand.get_value()
    print outcome

def hit():
    global in_play, outcome, player_hand, deck, score, dealer_hand, message
    print "Player Hits"
    outcome = ""
    # if the hand is in play, hit the player
    if in_play == True:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            outcome = "You Busted!  Dealer Wins"
            message = "Try Again?"
            in_play = False
            score -= 1
    else:
        outcome = "You can't hit. Click Deal to play again."
    print "Player's Hand: ",  player_hand, "Dealer's Hand", dealer_hand
    print "Player's value: ",  player_hand.get_value(), "     Dealer's value", dealer_hand.get_value()
    print outcome
    print

def stand():
    global in_play, outcome, player_hand, dealer_hand, deck, score, message
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        print "Player Stands"
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
    # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
            outcome = "Dealer Busts! You win!"
            score += 1
        else:
            if player_hand.get_value() <= dealer_hand.get_value():
                outcome = "Dealer Wins"
                score -= 1
            else:
                outcome = "You Win!"
                score += 1
        in_play = False
        message = "New Deal?"
        print outcome
        print

# draw handler
def draw(canvas):
    global in_play, outcome, player_hand, dealer_hand, deck, score, card_back
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", [100,100], 36, "Yellow", "sans-serif")
    canvas.draw_text(("Score: " + str(score)), [400,100], 36, "Black", "sans-serif")
    canvas.draw_text("Dealer", [100,150], 24, "Black", "sans-serif")
    canvas.draw_text("Player", [100,350], 24, "Black", "sans-serif")
    canvas.draw_text(str(message), [200,350], 24, "Black", "sans-serif")
    canvas.draw_text(str(outcome), [50,500], 24, "Black", "sans-serif")
    player_hand.draw(canvas, [100,375])
#    dealer_hand.draw(canvas, [100,175])
    if in_play == True:
        dealer_hand.draw(canvas, [100,175])
        canvas.draw_image(card_back, [CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]], CARD_BACK_SIZE, [136,223], CARD_BACK_SIZE)
    else:
        dealer_hand.draw(canvas, [100,175])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling

frame.start()
deal()
