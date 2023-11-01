import pygame

PLATFORM = '#374b43'


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=PLATFORM):
        super().__init__()  # Initialize the parent Sprite class
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

    def move(self, x_shift, y_shift=0):
        self.rect.move_ip(x_shift, y_shift)


# Create some platforms
# region
pf_01 = Platform(0, 550, 200, 20)
pf_02 = Platform(200, 510, 200, 20)
pf_03 = Platform(500, 550, 600, 20)
pf_04 = Platform(-300, 510, 300, 20)
pf_05 = Platform(600, 400, 300, 20)
pf_06 = Platform(1000, 350, 800, 20)
pf_07 = Platform(1750, 250, 800, 20)

platform_sprites = pygame.sprite.Group(pf_01, pf_02, pf_03, pf_04, pf_05, pf_06, pf_07)


# endregion

class Moving_Platform(Platform):
    def __init__(self, x, y, width, height, x_speed, y_speed, distance):
        super().__init__(x, y, width, height)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.distance = distance
        self.original_pos = self.rect.topleft
        self.cumulative_scrolling_shift = 0

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Adjust for cumulative shift from scrolling when checking distance
        effective_x = self.rect.x - self.cumulative_scrolling_shift

        if abs(effective_x - self.original_pos[0]) >= self.distance:
            self.x_speed *= -1

    def move(self, x_shift, y_shift=0):
        super().move(x_shift, y_shift)
        # Increase cumulative shift
        self.cumulative_scrolling_shift += x_shift


mov_plat = Moving_Platform(300, 300, 50, 20, 1, 0, 200)
mov_platform_sprites = pygame.sprite.Group(mov_plat)
