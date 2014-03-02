# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
wins = 0
losses = 0

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
        self.cards = []

    def __str__(self):
        card_print = ""
        for card in self.cards:
            card_print += str(card) + " "
        return  "Hand contains " + card_print

    def add_card(self, card):
        self.cards.append(card)
        
    def get_value(self):
        value = 0
        aces = False
        for card in self.cards:
            rank = card.get_rank()
            value += VALUES[rank]
            if rank == 'A':
                aces = True
        
        if aces == False:
            return value
        else:
            if value + 10 <= 21:
                return value + 10
            else:
                return value       
                  
    def draw(self, canvas, pos):
        card_pos = pos
        for card in self.cards:
            card.draw(canvas, card_pos)
            card_pos[0] +=100
                        
 
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))

    def shuffle(self):
        return random.shuffle(self.deck)

    def deal_card(self):
        return random.choice(self.deck)
          
    def __str__(self):
        card_print = ""
        for card in self.deck:
            card_print += str(card) + " "
        return  "Deck contains " + card_print

#define event handlers for buttons
def deal():
    global outcome, in_play, losses
    global deck, dealer_hand, player_hand
    
    if in_play == True:
        losses += 1
        
    deck = Deck()
    deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()
    
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
     
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
   
    in_play = True
    outcome = "Hit or Stand ?"
    
def hit():
    global in_play, outcome, player_hand, losses
    
    if in_play == True:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You have busted! New deal?"
            in_play = False   
            losses += 1
    
def stand():
    global in_play, outcome, player_hand, dealer_hand, wins, losses
   
    if in_play == True:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        in_play = False
        
        if dealer_hand.get_value() > 21:
            outcome = "Dealer has busted. You win! New deal?"
            wins +=1
        else:
            if player_hand.get_value() < dealer_hand.get_value():
                outcome = "You lose! New deal?"
                losses +=1
            else:
                outcome = "You win! New deal?"
                wins +=1
                
    
# draw handler    
def draw(canvas):
    global score, outcome, dealer_hand, player_hand
    
    canvas.draw_text("BLACKJACK", [170, 50], 50, "Black", "sans-serif")
    
    canvas.draw_text("Dealer", [100, 120], 30, "Black", "sans-serif")
    dealer_hand.draw(canvas, [100, 150])
    
    canvas.draw_text("Player", [100, 280], 30, "Black", "sans-serif")
    player_hand.draw(canvas, [100, 300])
    
    canvas.draw_text("Wins : " + str(wins), [140, 570], 30, "Black", "sans-serif")
    canvas.draw_text("Losses : " + str(losses), [340, 570], 30, "Black", "sans-serif")
    
    canvas.draw_text(outcome, [70, 490], 30, "Black", "sans-serif")
    
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [CARD_BACK_CENTER[0] + 100, CARD_BACK_CENTER[1] + 150], 
                          CARD_BACK_SIZE)
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric