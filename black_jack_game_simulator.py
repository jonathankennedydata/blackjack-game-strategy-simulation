import random
import pandas as pd
import math
import matplotlib.pyplot as plt
import statistics


class Black_Jack:
    """
    Black_Jack Game Engine
    
    This Class simulates a Balckjack game with support for:
    -Manual Play
    -Automated Play (simple strategy, basic strategy, and card counting)
    -Handles splits
    -Simulation over many rounds for statistical analysis
    
    Designed for multi stategy comparison """


    def __init__(self,name,num_decks):
        """Initialize game
        Parameters:
        name(str): player name
        num_decks (int): Number of dcks used in the shoe
        """

        self.name = name
        self.num_decks = num_decks

        #player financial state
        self.money = 3000
        self.bet = 0

        #card counting variable
        self.running_count = 0
        self.true_count = 0

        #game state
        self.player_hand = [[]]
        self.dealer_hand = []
        self.deck = []


    def intro(self):
        #display game introduction message
        print(f'Thank you for joining the game {self.name}. \n You will be playing with {self.num_decks} of decks.')

    
    def create_deck(self):
        #create and shuffle a deck(or multiple decks).
        ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        #each card will represent a rank suit
        suits = ['Heart','Club','Spades','Diamond']
        for rank in ranks:
            for suit in suits:
                self.deck.append(rank + f'-{suit}')
        #multiply deck by the number of decks used        
        self.deck = self.deck * self.num_decks
        #Suffle the shoe
        random.shuffle(self.deck)

    def card_points(self,hand):
        """Calculate total Blackjack value of a hand."""
        points = 0
        aces = 0
        for card in hand:
            rank = card.split('-')[0]
            #Handling soft aces (11 or 1)
            if rank == 'A':
                points += 11
                aces += 1
            elif rank in ['J','Q','K']:
                points += 10
            else:
                points += int(rank)
        #adjusts for aces from 11 to 1 if player bust
        while points >21 and aces:
            points -= 10
            aces -= 1
        return points

    def deal_card(self,hand):
        """Deal one card from the deck and updates running count.
        Insurance if the deck runs out to ensure new shoe is created for simulation"""
        if len(self.deck) == 0:
            self.create_deck()
            self.running_count = 0
            self.true_count = 0
        card = self.deck.pop()
        hand.append(card)
        rank = card.split('-')[0]
        #implements hi-low counting system
        #+1 for low cards (2-6)
        if rank in ['2','3','4','5','6']:
            self.running_count += 1
        #-1 for high cards (10-Ace)
        elif rank in ['10','J','Q','K','A']:
            self.running_count -= 1

    def can_split(self,hand):
        #returns True if hand is able to be split.
        if len(hand) != 2:
            return False
        return hand[0].split('-')[0] == hand[1].split('-')[0]
    
    def split_hand(self,hand_index):
        """Split a pair into two seperate hands.
        Automatically deals one additonal card to each new hand."""
        hand = self.player_hand[hand_index]

        #create two hands
        new_hand1 = [hand[0]]
        new_hand2 = [hand[1]]

        #replace orginal hand
        self.player_hand[hand_index] = new_hand1
        self.player_hand.insert(hand_index +1, new_hand2)

        #deal on extra card to each
        self.deal_card(new_hand1)
        self.deal_card(new_hand2)
        

    def show_hand(self, reveal_dealer = False):
        """Shows player hand and dealer up card until the end of round
          when dealer cards are revealed"""
        for i, hand in enumerate(self.player_hand):
            print(f"\nPlayer Hand {i+1}: {hand} Score: {self.card_points(hand)}")
        #Reveales dealers full hand.
        if reveal_dealer:
            print("Dealer hand:", self.dealer_hand, "Score:", self.card_points(self.dealer_hand))
        #Dealers up card only    
        else:
            print("Dealer Hand:", [self.dealer_hand[0], "?"])



    def ace(self,hand):
        #Determines if there is an ace present in the player's hand
        for card in hand:
            if card.split('-')[0] == 'A':
                return True
        return False
    

    def basic_strategy(self):
        """Returns recommended move for player based on basic strategy
        used during game play."""
        check_dealer = ['2','3','4','5','6','7','8','9']
        dealer = self.dealer_hand[0].split('-')[0]
        for hand in self.player_hand:
            points = self.card_points(hand)
            # Hard scoring no aces present
            if self.ace(hand) != True:
                if points == 11 and dealer != 'A':
                    print(f'Strategy: You have {points} the dealer has {self.dealer_hand[0]} you should <Double>.')
                elif points == 10 and dealer in check_dealer:
                    print(f'Strategy: You have {points} the dealer has {self.dealer_hand[0]} you should <Double>.') 
                elif points == 9 and dealer in check_dealer[1:5]:
                    print(f'Strategy: You have {points} the dealer has {self.dealer_hand[0]} you should <Double>.')
                elif self.can_split(hand):
                        r = hand[0].split('-')[0]
                        if r in ['A','8']:
                            print("Strategy: Always split A's and 8's, never split 10's and 5's, can split others if you want")  
                elif points >= 17:
                    print(f'Strategy: You have {points} the delear has {self.dealer_hand[0]} you should <Stand>.')
                elif points >= 12 and points <= 16 and dealer in ['2','3','4','5','6']:
                    print(f'Strategy: You have {points} the dealer has {self.dealer_hand[0]} you should <Stand>.')
                elif points >= 12 and points <= 16 and dealer not in ['2','3','4','5','6']:
                    print(f'Strategy: You have {points} the dealer has {self.dealer_hand[0]} you should <Hit>.')
                elif points <= 11:
                    print(f'Strategy: You have {points} the dealer has {self.dealer_hand[0]} you should <Hit>.')
            #Soft scoring aces are presnet
            elif self.ace(hand) == True:
                if points >= 19:
                    print(f'Strategy: You have a soft {points} the dealer has {self.dealer_hand[0]} you should <Stay>.')
                elif points == 18 and dealer in ['2','7','8']:
                    print(f'Strategy: You have a soft {points} the dealer has {self.dealer_hand[0]} you should <Stay>.')
                elif points == 18 and dealer in check_dealer[1:5]:
                    print(f'Strategy: You have a soft {points} the dealer has {self.dealer_hand[0]} you should <Double>.')
                elif points == 18 and dealer in ['9','10','A']:
                    print(f'Strategy: You have a soft {points} the dealer has {self.dealer_hand[0]} you should <Hit>.')
                elif points == 13 or points == 14 and dealer in ['5','6']:
                    print(f'Strategy: You have a soft {points} the dealer has {self.dealer_hand[0]} you should <Double>.')
                elif points == 15 or points == 16 and dealer in ['4','5','6']:
                    print(f'Strategy: You have a soft {points} the dealer has {self.dealer_hand[0]} you should <double>.')
                elif points == 17 and dealer in ['3','4','5','6']:
                    print(f'Strategy: You have a soft {points} the dealer has {self.dealer_hand[0]} you should <Double>.')
                else:
                    print(f'Strategy: You have a soft {points} the dealer has {self.dealer_hand[0]} you should <Hit>.')

    def basic_strategy_move(self, hand):
        """Returns all possible strategy moves for basic strategy for simulation
        purposes only."""
        dealer = self.dealer_hand[0].split('-')[0]
        points = self.card_points(hand)
        #Hard points splits and doubles
        check_dealer = ['2','3','4','5','6','7','8','9']
        if self.ace(hand) != True:
            if self.can_split(hand):
                    r = hand[0].split('-')[0]
                    if r in ['8']:
                        return "split"
                    elif r in ['2','3','7'] and dealer in ['2','3','4','5','6','7']:
                        return "split"
                    elif r in ['6'] and dealer in ['2','3','4','5','6']:
                        return "split"
                    elif r in ['4'] and dealer in ['5','6']:
                        return "split"
                    elif r in ['9'] and dealer in ['7']:
                        return "split"
            elif points == 11 and dealer != 'A':
                return "double"
            elif points == 10 and dealer in check_dealer:
                return "double"
            elif points == 9 and dealer in ['3','4','5','6']:
                return "double"
            elif points >= 17:
                return "stand"
            elif points > 12 and points <= 16 and dealer in ['2','3','4','5','6']:
                return "stand"
            elif points > 12 and points <= 16 and dealer not in ['2','3','4','5','6']:
                return "hit"
            elif points == 12 and dealer in ['4','5','6']:
                return 'stand'
            elif points == 12 and dealer not in ['4','5','6']:
                return 'hit'
            elif points <= 8:
                return "hit"
            else:
                return "hit"
        #Soft scoring splits and doubles
        elif self.ace(hand) == True:
            if self.can_split(hand):
                    r = hand[0].split('-')[0]
                    if r in ['A']:
                        return "split"
            elif points == 18 and dealer in ['3','4','5','6']:
                return "double"
            elif points in [13,14] and dealer in ['5','6']:
                return "double"
            elif points in [15,16] and dealer in ['4','5','6']:
                return "double"
            elif points == 17 and dealer in ['3','4','5','6']:
                return "double"
            elif points == 18 and dealer in ['9','10','A']:
                return "hit"
            if points >= 19:
                return "stand"
            elif points == 18 and dealer in ['2','7','8']:
                return "stand"
            else:
                return "hit"
        
    def auto_player_turn_basic(self):
        """Execute automated player decisions using basic strategy.
        Handles splitting and doubling"""
        i = 0

        while i < len(self.player_hand):
            hand = self.player_hand[i]

            while self.card_points(hand) < 21:
                move = self.basic_strategy_move(hand)

                if move == "hit":
                    self.deal_card(hand)
    
                elif move == "double":
                    self.bet *= 2
                    self.deal_card(hand)
                    break
    
                elif move == "split" and self.can_split(hand):
                    self.split_hand(i)
                    hand = self.player_hand[i]  # restart current hand
                    continue
    
                else:  # stand
                    break
    
            i += 1
    
    def auto_player_turn_simple(self):
        """Executes automated player decisions using simple strategy."""
        dealer_up = self.card_points([self.dealer_hand[0]])
        
        for hand in self.player_hand:
            while self.card_points(hand) <= (dealer_up + 10) and self.card_points(hand) < 17:
                self.deal_card(hand)

    def determine_winner_auto(self):
        """Determines winner based on higher points or whether a bust has occured.
        Handles 3:2 blackjack payouts for simulation"""
        dealer_score = self.card_points(self.dealer_hand)
        dealer_blackjack = dealer_score == 21 and len(self.dealer_hand) == 2
        results = []

        for hand in self.player_hand:
            player_score = self.card_points(hand)
            player_blackjack = player_score == 21 and len(hand)==2

            if player_score > 21:
                results.append(-self.bet)
            #player blackjack payout 3:2
            elif player_blackjack and not dealer_blackjack:
                results.append(self.bet*1.5)
            elif dealer_blackjack and not player_blackjack:
                results.append(-self.bet)
            elif dealer_blackjack and player_blackjack:
                results.append(0)
            elif dealer_score > 21 or player_score > dealer_score:
                results.append(self.bet)
            elif dealer_score > player_score:
                results.append(-self.bet)
            else:
                results.append(0)

        return sum(results)





    def player_turn(self):
        """Player turn is for game play only providing an inputs to the player.
        Handles doubles, splits, stands, and hits"""
        i = 0
        while i < len(self.player_hand):
            hand = self.player_hand[i]

            while self.card_points(hand) < 21:
                self.show_hand()
                if self.card_points(self.dealer_hand) == 21:
                    break
                self.basic_strategy()
                if self.can_split(hand):
                    choice = input("Hit, stand, double, or split? ").lower()
                else:
                    choice = input("Hit, stand, or double? ").lower()

                if choice == "hit":
                    self.deal_card(hand)

                elif choice == "double":
                    self.deal_card(hand)
                    #self.bet *= 2
                    break
                elif choice == "split" and self.can_split(hand):
                    self.split_hand(i)
                    #Restarts hand with for each split
                    hand = self.player_hand[i] 
                    continue
                else:
                    break

            i += 1


    def dealer_turn(self):
        #Dealer follows hit until reaching 17 or higher
        while self.card_points(self.dealer_hand) < 17:
            self.deal_card(self.dealer_hand)
         

    def true_count_total(self):
        """Converting running count to true count:
        True count is running count / remaining decks
        This provides direct information to player to let them know when to bet
        big or small"""
        num_card = len(self.deck)
        num_deck = num_card / 52
        count = self.running_count / num_deck
        self.true_count = round(count)
        if self.true_count < 1:
            print(f"True Count is {self.true_count} you should bet $25")
        elif self.true_count == 1:
            print(f"True Count is {self.true_count} you should double bet to $50")
        elif self.true_count == 2:
            print(f"True Count is {self.true_count} you should increase bet to $250")
        elif self.true_count == 3:
            print(f"True Count is {self.true_count} you should increase bet to half table limit $500")
        elif self.true_count > 3:
            print(f"True count is {self.true_count} time to go big bet table limit $1000")

    def true_count_sim(self):
        """Determines true count and is used to determine bet sizing during
        counting simulation"""
        num_card = len(self.deck)
        num_deck = num_card / 52
        if num_deck == 0:
            num_deck = 0.25
        count = self.running_count / num_deck
        self.true_count = math.floor(count)
        if self.true_count < 1:
            return 25
        elif self.true_count == 1:
            return 30
        elif self.true_count == 2:
            return 50
        elif self.true_count == 3:
            return 250
        elif self.true_count > 3:
            return 500
        else:
            return 25


    def determine_winner(self):
        """Determines winner for gameplay only informing 
        the player who won the round"""
        dealer_score = self.card_points(self.dealer_hand)
        for i,hand in enumerate(self.player_hand):
            player_score = self.card_points(hand)
            print(f"\nResult for Hand {i+1}:")
            print("Player:",hand,player_score)
            print("Dealer:",dealer_score)
            print("\nFinal Results:")
            self.show_hand(reveal_dealer=True)

            if player_score >21:
                print("You Bust. Dealer Wins.")
                self.money -= self.bet
            elif dealer_score >21:
                print("Dealer busts. You win!")
                self.money += self.bet
            elif player_score > dealer_score:
                print("You win!")
                self.money += self.bet
            elif dealer_score > player_score:
                print("Dealer wins.")
                self.money -= self.bet
            else:
                print("Push (tie).")

    def simulate(self,strategy='basic',counting = "Yes",rounds=1000,bet_size=25):
        """
        Blackjack simulation for a specific number of rounds.
        Returns:
        Pandas DataFrame containing:
        -Round number
        -Player bankroll after each hand
        -True Count
        -Bet size
        """
        self.create_deck()
        history = []
        
        for round_number in range(1, rounds + 1):
            #Reshuffles if card number is low in shoot
            if len(self.deck) < (52 * self.num_decks * 0.25):
                self.deck = []
                self.create_deck()
                #Resets true and running count
                self.running_count = 0
                self.true_count = 0
            #Determines if counting cards with basic strategy is used.
            if strategy == 'count_basic':
                count_bet = self.true_count_sim()
                #Adjust bet size based on true count
                self.bet = count_bet
            else:
                self.bet = bet_size
            self.player_hand = [[]]
            self.dealer_hand = []

            #initial deal
            self.deal_card(self.player_hand[0])
            self.deal_card(self.dealer_hand)
            self.deal_card(self.player_hand[0])
            self.deal_card(self.dealer_hand)

            #Choosing which strategy plays
            if strategy == "basic":
                self.auto_player_turn_basic()
            elif strategy == "count_basic":
                self.auto_player_turn_basic()
            else:
                self.auto_player_turn_simple()
            
            self.dealer_turn()

            change = self.determine_winner_auto()
            self.money += change
            #Creates the pandas dataframe
            history.append({
                "round": round_number,
                "money": self.money,
                "count": self.true_count,
                "bet" : self.bet,
                "results": change
            })
        return pd.DataFrame(history)

    #Function for play game user input
    def play(self):
        """Follows same principle as simulator but for player input"""
        self.create_deck()
        round_number = 1
        #Allows for enough cards to play hand before stopping game.
        while len(self.deck) > 10:
            if self.money <= 0:
                print('Sorry you are out of money. No more bets')
                break
            print(f"Round{round_number}")
            #Provides true count information to player
            self.true_count_total()
            new_bet = input(f"What would you like to bet? You have ${self.money} ")
            self.bet = int(new_bet)
            self.player_hand = [[]]
            self.dealer_hand = []
            #Single cards are delt
            self.deal_card(self.player_hand[0])
            self.deal_card(self.dealer_hand)
            self.deal_card(self.player_hand[0])
            self.deal_card(self.dealer_hand)
            #Player and dealer turns and detemine which is winner of hand
            self.player_turn()
            self.dealer_turn()
            self.determine_winner()

            round_number += 1
        #Stops game with final results
        print(f"\nDeck is out of cards. Game over! You have ${self.money}")


#Introduction to game to decide if user wants a simulation or blackjack game
intro_input = int(input("Hello welcome to this Blackjack game/simulator.\nIf you would like to play the game Enter 1.\nIf you would like to use simulator Enter 2.\n "))
num_deck = 0
if intro_input == 1:
    name = input("Please provide your name ")
    number_deck = int(input("Please provide the number of decks used in the game.\nEnter 1 for (2) decks.\nEnter 2 for (4) decks.\nEnter 3 for (6) decks. "))
    if number_deck == 1:
        num_deck = 2
    elif number_deck == 2:
        num_deck = 4
    elif number_deck == 3:
        num_deck = 6
    game = Black_Jack(name,num_deck)
    print(game.intro())
    game.play()
elif intro_input == 2:
    print("Please enjoy this Blackjack strategy simulation.")
    simple_list = []
    basic_list = []
    counting_list = []

    for _ in range(55):
        #Setting up (3) game simulations
        #Simple Edge Calculations
        game_simple = Black_Jack("Simple",2)
        df_simple = game_simple.simulate(strategy="simple",rounds= 10000)
        game_basic = Black_Jack("Basic",2)
        df_basic = game_basic.simulate(strategy="basic",rounds= 10000)
        game_counting = Black_Jack("Count",2)
        df_counting = game_counting.simulate(strategy="count_basic",rounds= 10000)
        
        #Simple Edge Calculations
        total_waged_simple = df_simple["bet"].sum()
        total_results_simple = df_simple["results"].sum()
        total_payout_simple = total_waged_simple + total_results_simple
        edge_simple = ((total_payout_simple - total_waged_simple)/total_waged_simple)*100
        simple_list.append(edge_simple)
        
        #Basic Edge Calculations
        total_waged_basic = df_basic["bet"].sum()
        total_results_basic = df_basic["results"].sum()
        total_payout_basic = total_waged_basic + total_results_basic
        edge_basic = ((total_payout_basic - total_waged_basic)/total_waged_basic)*100
        basic_list.append(edge_basic)
        
        #Counting Edge Calculations
        total_waged_counting = df_counting["bet"].sum()
        total_results_counting = df_counting["results"].sum()
        total_payout_counting = total_waged_counting + total_results_counting
        edge_counting = ((total_payout_counting- total_waged_counting)/total_waged_counting)*100
        counting_list.append(edge_counting)




    """Finding the (3) means of 35 iterations of house egde calculations"""
    avg_simple = statistics.mean(simple_list)
    stdev_simple = statistics.stdev(simple_list)
    se_simple = stdev_simple / math.sqrt(10000)
    print(f'The average player edge accounting for variance for simple strategy is {round(avg_simple,4)}% + or - {round(se_simple,4)}%')

    avg_basic = statistics.mean(basic_list)
    
    stdev_basic = statistics.stdev(basic_list)
    se_basic = stdev_basic / math.sqrt(10000)
    print(f'The average player edge accounting for variance for basic strategy is {round(avg_basic,4)}% + or - {round(se_basic,4)}%')

    avg_counting = statistics.mean(counting_list)
    stdev_counting = statistics.stdev(counting_list)
    se_counting = stdev_counting / math.sqrt(10000)
    print(f'The average player edge accounting for variance for counting strategy is {round(avg_counting,4)}% + or - {round(se_counting,4)}%')



    """Gather the average from each hand delt in all 25 iterations
      to create an average of each strategy line graph."""
    def average_strategy(strategy_name, runs=50, rounds=10000):
        money_columns = []
        
        for i in range(runs):
            game = Black_Jack(strategy_name, 2)
            df = game.simulate(strategy=strategy_name, rounds=rounds)
            money_columns.append(df["money"].reset_index(drop=True))
        
        combined = pd.concat(money_columns, axis=1)
        avg_money = combined.mean(axis=1)
        
        return avg_money


    #calling the funtion for each strategy
    avg_basic = average_strategy("basic")
    avg_simple = average_strategy("simple")
    avg_count = average_strategy("count_basic")


    plt.figure()
    #ploting the Simple, Basic, and Counting Strategies
    plt.plot(range(1, 10001), avg_basic, label="Basic")
    plt.plot(range(1, 10001), avg_simple, label="Simple")
    plt.plot(range(1, 10001), avg_count, label="Counting")

    plt.xlabel("Hand Number")
    plt.ylabel("Average Accumulated Money")
    plt.title("Blackjack Simulation: Average Bankroll Over 10,000 Hands (25 Runs)")
    plt.axhline(y=300, linestyle='-.')
    plt.legend()
    plt.show()