import random
import pygame
from settings import *

class Symbol(pygame.sprite.Sprite):
    def __init__(self, pathToFile, pos, idx):
        super().__init__()

        self.sym_type = pathToFile.split('/')[3].split('.')[0]  # Friendly name
        self.pos = pos
        self.idx = idx
        self.image = pygame.image.load(pathToFile).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.x_val = self.rect.left

        self.size_x = 300
        self.size_y = 300
        self.alpha = 255
        self.fade_out = False
        self.fade_in = False

    def update(self):
        # Slightly increases size of winning symbols
        if self.fade_in:
            if self.size_x < 320:
                self.size_x += 1
                self.size_y += 1
                self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))

        # Fades out non-winning symbols
        elif not self.fade_in and self.fade_out:
            if self.alpha > 115:
                self.alpha -= 7
                self.image.set_alpha(self.alpha)


class Reel:
    def __init__(self, pos):
        self.symbol_list = pygame.sprite.Group()

        # List of symbols to choose from based on their weights
        self.weighted_symbols = list(symbol_weights.keys())  # List of symbols (keys from symbol_weights)
        self.weighted_probabilities = list(symbol_weights.values())  # Corresponding weights (values from symbol_weights)

        # Initialize the reel with 5 random symbols based on their weighted probabilities
        self.shuffled_keys = random.choices(self.weighted_symbols, weights=self.weighted_probabilities, k=5)

        # Add the selected symbols to the reel
        for idx, item in enumerate(self.shuffled_keys):
            self.symbol_list.add(Symbol(symbols[item], pos, idx))
            pos = list(pos)
            pos[1] += 300  # Adjust vertical spacing for next symbol
            pos = tuple(pos)

        self.reel_is_spinning = False

    def animate(self, delta_time):
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = False

            if self.spin_time < 0:
                reel_is_stopping = True

            if self.delay_time <= 0:
                for symbol in self.symbol_list:
                    symbol.rect.bottom += 100

                    if symbol.rect.top == 1200:
                        if reel_is_stopping:
                            self.reel_is_spinning = False

                        symbol_idx = symbol.idx
                        symbol.kill()

                        # Dynamically pick a new symbol for the reel during the spin
                        new_symbol = random.choices(
                            self.weighted_symbols, weights=self.weighted_probabilities, k=1
                        )[0]

                        self.symbol_list.add(
                            Symbol(symbols[new_symbol], ((symbol.x_val), -300), symbol_idx)
                        )

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    def reel_spin_result(self):
        spin_symbols = []
        for i in GAME_INDICES:
            spin_symbols.append(self.symbol_list.sprites()[i].sym_type)
        return spin_symbols[::-1]
