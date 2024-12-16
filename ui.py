import pygame
import random
from settings import UI_FONT, UI_FONT_SIZE, WIN_FONT_SIZE, TEXT_COLOR  # Import constants


class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()  # This requires pygame to be initialized
        try:
            self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
            self.bet_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
            self.win_font = pygame.font.Font(UI_FONT, WIN_FONT_SIZE)
        except:
            print("Error loading font!")
            print(f"Currently, the UI_FONT variable is set to {UI_FONT}")
            print("Does the file exist?")
            quit()
        self.win_text_angle = random.randint(-4, 4)

    def format_currency(self, amount):
        """Helper function to format balance, bet size, and payout as currency"""
        return "${:.2f}".format(amount)  # Format to two decimal places, like "$1234.56"

    def display_info(self):
        player_data = self.player.get_data()

        # Format the balance and bet size as currency
        balance = self.format_currency(player_data['balance'])
        bet_size = self.format_currency(player_data['bet_size'])

        # Balance and bet size rendering
        balance_surf = self.font.render(f"Balance: {balance}", True, TEXT_COLOR, None)
        x, y = 20, self.display_surface.get_size()[1] - 30
        balance_rect = balance_surf.get_rect(bottomleft=(x, y))

        bet_surf = self.bet_font.render(f"Wager: {bet_size}", True, TEXT_COLOR, None)
        x = self.display_surface.get_size()[0] - 20
        bet_rect = bet_surf.get_rect(bottomright=(x, y))

        # Display the Free Spins counter if it's greater than 0
        if self.player.free_spins > 0:
            free_spins_surf = self.font.render(f"Free Spins: {self.player.free_spins}", True, TEXT_COLOR, None)
            x_free, y_free = 20, self.display_surface.get_size()[1] - 60
            free_spins_rect = free_spins_surf.get_rect(bottomleft=(x_free, y_free))

            self.display_surface.blit(free_spins_surf, free_spins_rect)

        # Draw player data
        pygame.draw.rect(self.display_surface, False, balance_rect)  # Placeholder rect for the balance
        pygame.draw.rect(self.display_surface, False, bet_rect)  # Placeholder rect for the bet
        self.display_surface.blit(balance_surf, balance_rect)  # Render balance
        self.display_surface.blit(bet_surf, bet_rect)  # Render bet size

        # Print last win if applicable (formatted as currency)
        if self.player.last_payout:
            last_payout = self.format_currency(player_data['last_payout'])
            win_surf = self.win_font.render(f"WIN! {last_payout}", True, TEXT_COLOR, None)
            x1 = 800
            y1 = self.display_surface.get_size()[1] - 60
            win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
            win_rect = win_surf.get_rect(center=(x1, y1))
            self.display_surface.blit(win_surf, win_rect)

        # Show the bonus game active message if the player is in a bonus game
        if self.player.in_bonus_game:
            bonus_surf = self.win_font.render("BONUS GAME ACTIVE!", True, TEXT_COLOR, None)
            x_bonus, y_bonus = self.display_surface.get_size()[0] // 2, 50
            bonus_rect = bonus_surf.get_rect(center=(x_bonus, y_bonus))
            self.display_surface.blit(bonus_surf, bonus_rect)

    def update_ui(self):
        """Update the UI elements on screen"""
        # Background rectangle
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 900, 1600, 100))

        # Update the display info (balance, wager, etc.)
        self.display_info()

    def update_free_spins(self, free_spins):
        """Updates the UI with the number of free spins left."""
        self.player.free_spins = free_spins  # Update the player’s free spins
        # Optionally call display_info() here, but it's already being called in `update_ui()`

    def reset_free_spins(self):
        """Reset the UI state when free spins are finished."""
        self.player.free_spins = 0  # Reset the free spins count
        self.update_ui()  # Update the UI to reflect changes
