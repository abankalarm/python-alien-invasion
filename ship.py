import pygame


#relative path
import os

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, '') # The resource folder path
image_path = os.path.join(resource_path, '') # The image folder path


class Ship:
    ''' a class to manage our ship '''

    def __init__(self, ai_game):
        '''initaializes ship and its starting position'''

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load((os.path.join(image_path, 'ship.png')))
        # resize the image
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.x += self.settings.ship_speed
        if self.moving_left:
            if self.moving_left and self.rect.left > 0:
                self.x -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        