
from random import uniform
import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button

class AlienInvasion:
    '''this class deals with basic game assets and behaviour'''

    def __init__(self):
        '''this is used to initialize the game'''
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion v1.0")
        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        '''start the main loop for the game'''

        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()

    def _check_events(self):
        '''response to key strokes'''
                    # watch for keyboard and mouse input
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

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right.
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            # Move the ship to the left.
            self.ship.moving_left = True
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
            # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Check for any bullets that have hit aliens.
        #If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
        # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
                    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
        
        #makes most recently drawnj screen visible


        pygame.display.flip()

    def _create_fleet(self):
        '''create a fleet of aliens'''
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # Determine the number of rows of aliens that fit on the screen.
        
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)


        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # Create the first row of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row.
                random_number = uniform(1.2, 2.5)
                alien = Alien(self)
                alien.x = alien_width + random_number * alien_width * alien_number
                alien.rect.x = alien.x
                alien.rect.y = alien.rect.height + random_number * alien.rect.height * row_number
                self.aliens.add(alien)

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            pygame.mouse.set_visible(True)

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            
            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            # Reset the game statistics.
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
            self.stats.reset_stats()
            self.stats.game_active = True
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

