from player import Player
from reel import *
from settings import *
from ui import UI
from wins import *
import pygame
import random

class Machine:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.machine_balance = 10000.00
        self.reel_index = 0
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.can_animate = False
        self.win_animation_ongoing = False

        # Results
        self.prev_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}

        # Free Spin attributes
        self.free_spin_active = False
        self.free_spins = 0
        self.auto_spin_active = False  # New flag for automatic spins

        self.spawn_reels()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)

        # Import sounds
        self.spin_sound = pygame.mixer.Sound('audio/spinclipo.mp3')
        self.spin_sound.set_volume(0.15)
        self.win_three = pygame.mixer.Sound('audio/winthree.wav')
        self.win_three.set_volume(0.5)
        self.win_four = pygame.mixer.Sound('audio/winthree.wav')
        self.win_four.set_volume(0.5)
        self.win_five = pygame.mixer.Sound('audio/winthree.wav')
        self.win_five.set_volume(0.5)

    def start_bonus_game(self):
        """Initiates the bonus game, sets free spins, and updates the UI."""
        self.free_spin_active = True
        self.free_spins += 5  # You can adjust this number based on your game design
        self.ui.update_free_spins(self.free_spins)  # Update the UI with the free spins count
        print("Bonus game started! Free spins:", self.free_spins)

    def cooldowns(self):
        # Only lets player spin if all reels are NOT spinning
        for reel in self.reel_list:
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True
            self.spin_result = self.get_result()

            if self.check_wins(self.spin_result):
                self.win_data = self.check_wins(self.spin_result)
                self.play_win_sound(self.win_data)
                self.pay_player(self.win_data, self.currPlayer)
                self.win_animation_ongoing = True
                self.ui.win_text_angle = random.randint(-4, 4)

    def input(self):
        keys = pygame.key.get_pressed()

        if self.free_spin_active and self.free_spins > 0:
            # If in bonus game, pressing space should trigger auto-spin if it's not active
            if keys[pygame.K_SPACE] and self.can_toggle:
                self.auto_spin_active = True  # Enable auto-spin
                self.toggle_spinning()
                self.spin_time = pygame.time.get_ticks()

        elif keys[pygame.K_SPACE] and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
            # Regular spin logic when not in free spin mode
            self.toggle_spinning()
            self.spin_time = pygame.time.get_ticks()
            self.currPlayer.place_bet()  # This now works because the Player class has place_bet
            self.machine_balance += self.currPlayer.bet_size
            self.currPlayer.last_payout = None

    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)

    def spawn_reels(self):
        if not self.reel_list:
            x_topleft, y_topleft = 10, -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (300 + X_OFFSET), y_topleft

            self.reel_list[self.reel_index] = Reel((x_topleft, y_topleft))  # Need to create reel class
            self.reel_index += 1

    def toggle_spinning(self):
        if self.can_toggle and (self.free_spins > 0 or not self.free_spin_active):
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.can_toggle = False

            for reel in self.reel_list:
                self.reel_list[reel].start_spin(int(reel) * 200)
                self.spin_sound.play()
                self.win_animation_ongoing = False

            if self.free_spin_active:  # If in free spins, decrement the free spins counter
                self.free_spins -= 1
                self.ui.update_free_spins(self.free_spins)  # Update the UI with the new free spins count
                if self.free_spins == 0:
                    self.free_spin_active = False  # End the bonus game
                    self.ui.reset_free_spins()  # Reset the UI to regular state
                    print("Bonus game over!")

    def get_result(self):
        for reel in self.reel_list:
            self.spin_result[reel] = self.reel_list[reel].reel_spin_result()
        return self.spin_result

    def check_wins(self, result):
        hits = {}
        horizontal = flip_horizontal(result)
        bonus_hits = 0  # Counter for bonus symbols
        for row in horizontal:
            for sym in row:
                if row.count(sym) > 2:  # Potential win
                    possible_win = [idx for idx, val in enumerate(row) if sym == val]

                    if len(longest_seq(possible_win)) > 2:
                        if sym == '0_kristof':  # Changed from 'bonus' to 'star'
                            bonus_hits += 1
                        else:
                            # Check for regular symbols (as before)
                            symbol_multiplier = symbol_payout_multipliers.get(sym, 1)
                            hits[horizontal.index(row) + 1] = [sym, longest_seq(possible_win), symbol_multiplier]

        if bonus_hits >= 3:  # If 3 or more 'star' symbols are detected, trigger the bonus game
            self.start_bonus_game()  # Now this method exists

        if hits:
            self.can_animate = True
            return hits

    def pay_player(self, win_data, curr_player):
        total_payout = 0
        for v in win_data.values():
            symbol, win_sequence, multiplier = v
            # Multiply the length of the winning sequence by the bet size and the symbol's multiplier
            total_payout += len(win_sequence) * curr_player.bet_size / 2 * multiplier  # Apply multiplier here

        curr_player.balance += total_payout  # Add total payout to the player's balance
        self.machine_balance -= total_payout  # Subtract from the machine balance
        curr_player.last_payout = total_payout  # Save the last payout amount
        curr_player.total_won += total_payout  # Add to total won

    def play_win_sound(self, win_data):
        sum = 0
        for item in win_data.values():
            sum += len(item[1])
        if sum == 3:
            self.win_three.play()
        elif sum == 4:
            self.win_four.play()
        elif sum > 4:
            self.win_five.play()

    def win_animation(self):
        if self.win_animation_ongoing and self.win_data:
            for k, v in list(self.win_data.items()):
                if k == 1:
                    animationRow = 3
                elif k == 3:
                    animationRow = 1
                else:
                    animationRow = 2
                animationCols = v[1]
                for reel in self.reel_list:
                    if reel in animationCols and self.can_animate:
                        self.reel_list[reel].symbol_list.sprites()[animationRow].fade_in = True
                    for symbol in self.reel_list[reel].symbol_list:
                        if not symbol.fade_in:
                            symbol.fade_out = True

    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.display_surface)
            self.reel_list[reel].symbol_list.update()
        self.ui.update_ui()
        self.win_animation()

