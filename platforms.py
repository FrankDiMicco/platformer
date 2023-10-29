import pygame

PLATFORM = '#374b43'


class Platform:
    def __init__(self, x, y, width, height, color=PLATFORM):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, x_shift, y_shift=0):
        self.rect.move_ip(x_shift, y_shift)


pf_01 = Platform(0, 550, 200, 20)
pf_02 = Platform(200, 510, 200, 20)
pf_03 = Platform(500, 550, 600, 20)
pf_04 = Platform(-300, 510, 300, 20)
pf_05 = Platform(600, 400, 300, 20)
pf_06 = Platform(1000, 350, 800, 20)
pf_07 = Platform(1750, 250, 800, 20)

platform_list = [pf_01, pf_02, pf_03, pf_04, pf_05, pf_06, pf_07]
