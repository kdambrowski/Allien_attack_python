import pygame

from pygame.sprite import Sprite

class Ship(Sprite):
    """class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize the ship into game"""

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # reference to class settings
        self.screen_rect = ai_game.screen.get_rect()

        # load image of ship
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # place of ship after restart or destroy
        self.rect.midbottom = self.screen_rect.midbottom

        # change position of ship like a decinumerous
        self.x = float(self.rect.x)

        # move ship in right
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ current ship position"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # change ship position based on parameter self.x
        self.rect.x = self.x


    def blitme(self):
        """showing ship in current position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """recalled ship on the screen after collision and set in in center of bottom"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
