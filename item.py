import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, effect=None):
        super().__init__()
        # Initialize sprite attributes
        self.image = pygame.image.load('graphics/items/orbs/Orb_09.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.effect = effect

    def move(self, x_shift, y_shift):
        self.rect.move_ip(x_shift, y_shift)

