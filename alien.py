import pygame
import os
from pygame.sprite import Sprite

class Alien(Sprite):
    '''this class is to manage the alien'''
    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.settings = ai_game.settings
        current_path = os.path.dirname(__file__) # Where your .py file is located
        resource_path = os.path.join(current_path, '') # The resource folder path
        image_path = os.path.join(resource_path, '') # The image folder path

        self.image = pygame.image.load((os.path.join(image_path,'ufo.png')))
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien to the right."""
        """Move the alien right or left."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True