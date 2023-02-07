import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """ Class for manage projectile drawn by the ship"""

    def __init__(self, ai_game):
        """create bullet acc ship position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        # create square of projectile at position (0,0) and then define position for it
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # change bullet position for demidigit
        self.y = float(self.rect.y)

    def update(self):
        """ Move a projectile through the screen """

        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """drawn byllet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
