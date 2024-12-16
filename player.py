# player.py
class Player:
    def __init__(self):
        self.balance = 1000.0  # Initial balance
        self.bet_size = 10.0  # Default bet size
        self.last_payout = None
        self.total_won = 0.0
        self.free_spins = 0  # Initialize free_spins attribute
        self.in_bonus_game = False  # Initialize in_bonus_game attribute

    def place_bet(self):
        """Places a bet by deducting the bet amount from the balance."""
        if self.balance >= self.bet_size:
            self.balance -= self.bet_size  # Deduct bet size from balance
            print(f"Placed bet of {self.bet_size}. Remaining balance: {self.balance}")
        else:
            print("Insufficient funds to place the bet.")

    def get_data(self):
        """Returns player data as a dictionary for debugging purposes."""
        return {
            'balance': self.balance,
            'bet_size': self.bet_size,
            'last_payout': self.last_payout,
            'total_won': self.total_won,
            'free_spins': self.free_spins,
            'in_bonus_game': self.in_bonus_game  # Include in_bonus_game in the returned data
        }

    def add_free_spins(self, spins):
        """Add free spins to the player."""
        self.free_spins += spins
        print(f"Player earned {spins} free spins. Total free spins: {self.free_spins}")

    def reset_free_spins(self):
        """Resets the free spins count."""
        self.free_spins = 0
        print("Player's free spins have been reset.")

    def start_bonus_game(self):
        """Start the bonus game for the player."""
        self.in_bonus_game = True
        print("Bonus game started!")

    def end_bonus_game(self):
        """End the bonus game for the player."""
        self.in_bonus_game = False
        print("Bonus game ended!")
