# IMPORT STATEMENTS:
from random import randint
from IPython.display import clear_output

# FUNCTION DEFINITIONS:

def main():
    # Defined main function.
    # Invokes a Game class object and activates its "play" method (the game thus begins).
    
    game = Game()
    game.play()

# CLASS DEFINTIONS:

class Game:
    # A class that contains a game from start to finish.
    
    def __init__(self):
        # Initial method that contains Game class attributes:
        # "self.deck" is a Deck class object,
        # "self.players_hand" and "self.dealers_hand" are lists in which player's and dealer's cards are inserted,
        # "self.bank_account" is the amount with which the player enters the game,
        # "self.repeat" is a variable that indicates whether the player wants the cards dealt again.
        
        self.deck = Deck()
        self.players_hand = []
        self.dealers_hand = []
        self.bank_account = 0
        self.repeat = '1'
    
    def play(self):
        # This is the method that starts the first and each subsequent game.
        
        new_game = input("Do you want to start the game? Press '1' for 'yes': ")
        
        # A loop that starts the second and each subsequent game
        # and empties the hands of player and dealer and mixes the deck again every time a new game starts.
        while new_game == '1':
            self.players_hand.clear()
            self.dealers_hand.clear()
            self.deck.side_deck.clear()
            self.money_manager()
            new_game = input("\nDo you want to start a new game? Press '1' for 'yes': ")
            clear_output()
        else:
            print('Come again!')
    
    def money_manager(self):
        # A method that takes into account the player's money,
        # calls "investing_flow" method and
        # gives notification if any of the conditions are not met.
        
        # A loop that asks the player how much money he enters the game with, until he enters a good value.
        while True:
            try:
                self.bank_account = int(input('How much money do you enter the game with? $'))
            except:
                print('You must enter an integer (a rounded number) value!')
            else:
                break
        
        clear_output()
        print(f'Player, your current account balance is now: ${self.bank_account}.')
        
        self.investing_flow()   # Calling of "investing_flow" method.
        
        # Notifications if any of the conditions are not met.
        if self.bank_account == 0:
            print("\nGame over! You're broke!")
        elif self.repeat != '1':
            print("OK.")
        elif len(self.deck.side_deck) > 48:
            print("\nThe deck is empty.")
        
        print(f'You came out with ${self.bank_account}.')
    
    def investing_flow(self):
        # A method with a loop in which the investment, cards drawing flow method and
        # the option for re-dealing cards are located.
        
        self.repeat = '1'
        
        while (self.bank_account > 0) and (self.repeat == '1') and (len(self.deck.side_deck) <= 48):
            
            # A loop that asks the player how much he wants to invest from the money he entered the game with.
            while True:
                try:
                    invest = int(input('\nHow much do you invest? $'))
                    if invest > self.bank_account:
                        print('Your bet is higher than your account balance!')
                        continue
                except:
                    print('You must enter an integer (a rounded number) value!')
                else:
                    break
            
            
            clear_output()
            self.bank_account -= invest
            self.short_notice(invest)
            self.drawing_flow(invest)   # Cards drawing flow method.
            
            # A statement that asks the player if he wants the cards dealt again, if the conditions are met.
            if (self.bank_account > 0) and (len(self.deck.side_deck) <= 48):
                self.repeat = input("\nAre you brave for a new dealing of cards? Press '1' for 'yes': ")
                if self.repeat == '1':
                    self.players_hand.clear()
                    self.dealers_hand.clear()
                    clear_output()
                    print(f'Player, your current account balance is now: ${self.bank_account}.')
    
    def short_notice(self, invest):
        # Notification to the player of his funds which is repeated during the game.
        # "invest" is the amount the player has invested.
        
        print(f'Player, your account balance was ${self.bank_account + invest}.')
        print(f'You deposited ${invest} and now you have ${self.bank_account} left.')
    
    def drawing_flow(self, invest):
        # A method that follows the drawing of cards by a player and dealer and announces the result.
        # "invest" is the amount the player has invested.
        
        self.card_drawing(self.dealers_hand)
        self.card_drawing(self.dealers_hand)
        self.dealers_secret()
        
        self.card_drawing(self.players_hand)
        self.card_drawing(self.players_hand)
        self.on_the_table(self.players_hand)
        
        # A loop that asks the player if he wants another card.
        while (self.deck.sum_counting(self.players_hand) <= 21):
            answer = input("\nDo you want a card? Press '1' for 'yes': ")
            if (answer == '1') and (len(self.deck.side_deck) < 52):
                clear_output()
                self.short_notice(invest)
                self.dealers_secret()
                self.card_drawing(self.players_hand)
                self.on_the_table(self.players_hand)
            else:
                break
        
        # A loop that deals cards to the dealer while the sum in his hand is less than 17.
        while (self.deck.sum_counting(self.dealers_hand) < 17) and (len(self.deck.side_deck) < 52):
            self.card_drawing(self.dealers_hand)
        
        # The final look of the board.
        clear_output()
        if len(self.deck.side_deck) >= 52:
            print("No cards more!\n")
        self.short_notice(invest)
        self.on_the_table(self.dealers_hand)
        self.on_the_table(self.players_hand)
        
        # Publishing of game results.
        win = self.win_check(self.players_hand, self.dealers_hand)
        self.win_note(win, invest)
    
    def card_drawing(self, hand):
        # A method that draws one card, gives it value and puts it in the "hand" of the player or dealer.
        # "hand" can be either a "self.dealers_hand" or "self.players_hand".
        
        # A loop that draws a card until a card that has not already been drawn is obtained.
        while True:
            card_data = self.deck.get_card()
            if card_data in self.deck.side_deck:
                continue
            else:
                self.deck.side_deck.append(card_data)
                break
        
        card_name = card_data[0] + card_data[1]
        value = self.deck.ace_check(card_data, hand)
        card = [card_name, value]
        hand.append(card)
    
    def dealers_secret(self):
        # A method for hiding the dealer's second card.
        
        print("\n" + "\033[1m" + "Dealer's hand:" + "\033[0m")
        print(self.dealers_hand[0][0])
        print("XX card")
        print("The sum is: ??.")
    
    def on_the_table(self, hand):
        # A method that shows the cards from the hand of the player or dealer and their sum.
        # "hand" can be either a "self.dealers_hand" or "self.players_hand".
        
        if hand == self.players_hand:
            name = "Player's hand:"
        else:
            name = "Dealer's hand:"
        
        print("\n" + "\033[1m" + name + "\033[0m")
        
        for card in hand:
            print(card[0])
        
        sum_value = self.deck.sum_counting(hand)
        
        print(f"The sum is: {sum_value}.")
    
    def win_check(self, hand_1, hand_2):
        # Checks who has the larger sum in hand and returns the result in the form of a variable "win".
        # "hand_1" can be a "self.players_hand".
        # "hand_2" can be a "self.dealers_hand".
        
        if self.deck.sum_counting(hand_2) > 21:
            if self.deck.sum_counting(hand_1) > 21:
                win = 1
            else:
                win = 2
        
        elif self.deck.sum_counting(hand_1) > 21:
            win = 3
        
        elif self.deck.sum_counting(hand_1) > self.deck.sum_counting(hand_2):
            win = 4
        
        elif self.deck.sum_counting(hand_1) < self.deck.sum_counting(hand_2):
            win = 5
        
        else:
            win = 6
        
        return win
    
    def win_note(self, win, invest):
        # Depending on the value of the variable "win",
        # this method gives notification of the result of the game and
        # calculates the balance on the player's account.
        # "win" is a variable returned by "win_check" method.
        # "invest" is the amount the player has invested.
        
        if win == 1:
            notification = 'You both broke through!'
            self.bank_account += invest
        
        elif win == 2:
            notification = 'The dealer broke through!'
            self.bank_account += (2 * invest)
        
        elif win == 3:
            notification = 'The player broke through!'
        
        elif win == 4:
            notification = 'The player has a better hand!'
            self.bank_account += (2 * invest)
        
        elif win == 5:
            notification = 'The dealer has a better hand!'
        
        elif win == 6:
            notification = 'It is a draw!'
            self.bank_account += invest
        
        print('\n' + notification)
        if (self.bank_account > 0) and (len(self.deck.side_deck) <= 48):
            print(f'\nPlayer, your current account balance is now: ${self.bank_account}.')

class Deck:
    # A class that forms the deck of cards and everything related to it.
    
    def __init__(self):
        # Initial method that contains Deck class attributes:
        # "self.signs" is a list of possible cards characters,
        # "self.symbols" is a tuple of possible cards symbols,
        # "self.values" is a dictionary of values of the possible cards characters,
        # "self.side_deck" is a list of already drawn cards.
        
        self.signs = [value for value in range(2, 11)] + ['A', 'J', 'Q', 'K']
        self.symbols = ('♥ (heart)', '♠ (peak)', '♣ (treff)', '♦ (caro)')
        self.values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
        self.side_deck = []
    
    def get_card(self):
        # A method that creates a card by randomly selecting a sign (character) and a symbol.
        
        card_data = [str(self.signs[randint(0, 12)]), self.symbols[randint(0, 3)]]
        return card_data
    
    def ace_check(self, card_data, hand):
        # A method that returns the value of the card and
        # assigns a value of 1 or 11 to the Ace depending on the sum in the hand.
        # "card_data" is a two-element list returned by "get_card" method. The first element of the list is
        # a sign and the second is a symbol of the card.
        # "hand" can be either a "self.dealers_hand" or "self.players_hand".
        
        if card_data[0] == 'A':
            
            sum_value = self.sum_counting(hand)
            
            if sum_value > 10:
                value = 1
            else:
                value = 11
        else:
            value = self.values[card_data[0]]
        
        return value
    
    def sum_counting(self, hand):
        # A method that returns the sum of the cards in the hand.
        # "hand" can be either a "self.dealers_hand" or "self.players_hand".
        
        sum_value = 0
        
        for card in hand:
            sum_value += card[1]
        
        return sum_value

main()   # Calling of the main function.