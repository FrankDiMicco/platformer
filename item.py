import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # Initialize sprite attributes
        self.image = pygame.image.load('graphics/items/orbs/Orb_04.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))