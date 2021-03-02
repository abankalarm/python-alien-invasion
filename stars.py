import pygame


#relative path
import os
from pygame.sprite import Sprite

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, '') # The resource folder path
image_path = os.path.join(resource_path, '') # The image folder path

class Stars(Sprite):
    def __init__(self, ai_game):
        super().__init__()    
        self.screen=ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load((os.path.join(image_path,'star1.gif')))
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)