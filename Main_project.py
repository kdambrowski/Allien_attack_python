import sys
from time import sleep

import pygame

from Settings import Settings
from game_stats import GameStats
from scoreboard import ScoreBoard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien



class AlienInvasion:
    """"General class for manage sources and elements of the game"""

    def __init__(self):
        """initialize of the game"""
        pygame.init()
        # upload settings to launch game
        self.settings = Settings()

        # settings relate with screed dimensions
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # settings relate with game name
        pygame.display.set_caption("Inwazja obcych")
        # statistic data
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)
        self.ship = Ship(self)
        # add recall group of object
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        # create copy of alien
        self._create_fleet()


        self.play_button = Button(self, "ROZPOCZNIJ GRĘ")


    def run_game(self):
        """Start of the game"""
        while True:
            # react for the press any button
            self._check_events()

            if self.stats.game_active:
                # refresh ship position
                self.ship.update()
                # refresh bullets position acc ship position and remove invisible bullets
                self._update_bullets()
                self._update_aliens()
                # refreshing screen
            self._update_screen()

    def _check_events(self):
        """Waited for press any button"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """start game after click play on the screen via mouse"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:

            self.settings.initialize_dynamic_setting()

            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """reaction after push a keyboard"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Reaction for release keyboard button"""
        if event.key == pygame.K_RIGHT:
            # move ship in right direction
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create new projectile and append it to the group of bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        # information for remove invisible bullets form the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_point * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
    def _update_aliens(self):
        """Update alien position and verification touch alien to edge"""
        self._check_fleet_edges()
        self.aliens.update()

        # collision between ship and alien
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """check collision alien with bottom screen edge"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """ reaction at collision alien with ship"""

        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.sb.prep_ships()
            # removing alien from alien's list
            self.aliens.empty()
            self.bullets.empty()
            # create new fleet and ship after restart
            self._create_fleet()
            self.ship.center_ship()
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """ Create full alien fleet"""
        # Create alien object and define quantity of object that would be fill all screen
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # define how many rows would be fitted into screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (4 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # create first row of alien
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create alien and set it into row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Reaction fleet on screen edge"""
        for alien in self.aliens.sprites():
            # błąd działa ale pobierany jest z podklasy i system go nie widzi
            if alien.check_edges():
                self._change_fleet_direction()
                break



    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """update screen relate to any objects"""
        # refreshed screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            # ten blad dziala poprawnie bo pobiera moduł z podklasy bullet
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button._draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Create and lunch game
    ai = AlienInvasion()
    ai.run_game()
