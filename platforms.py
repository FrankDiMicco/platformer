import pygame

PLATFORM = '#374b43'
level = 1


class Platform(pygame.sprite.Sprite):
    def __init__(self, level, x, y, width, height, color=PLATFORM):
        super().__init__()  # Initialize the parent Sprite class
        self.level = level
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

    def move(self, x_shift, y_shift=0):
        self.rect.move_ip(x_shift, y_shift)


# Create some platforms
# region
pf_01 = Platform(0,0, 550, 200, 20, 'red')
pf_02 = Platform(0,200, 520, 200, 20, 'blue')
pf_03 = Platform(0,500, 550, 600, 20, 'green')
pf_04 = Platform(0,-300, 10, 300, 2000, 'purple') # far left
pf_05 = Platform(0,600, 400, 300, 20, 'orange')
pf_06 = Platform(0,1000, 350, 800, 20, 'brown')
pf_07 = Platform(0,1750, 250, 800, 20, 'yellow')
pf_08 = Platform(0,175, 175, 200, 20)
pf_09 = Platform(0,-300, -300, 300, 20, 'black')

pf_01_01 = Platform(1, -800, 600, 1200, 500, 'red')  # red big
pf_01_02 = Platform(1, -300, 350, 300, 250, 'red')  # red barrier
pf_01_03 = Platform(1, 600, 600, 200, 500, 'blue')  # 1st blue
pf_01_04 = Platform(1, 800, 500, 1000, 600, 'blue')  # 2nd blue
pf_01_05 = Platform(1, 1800, 650, 100, 450, 'blue')  # small 3rd blue
pf_01_06 = Platform(1, 2100, 600, 300, 500, 'green')  # 1st green
pf_01_07 = Platform(1, 2400, 450, 600, 650, 'green')
pf_01_08 = Platform(1, 3000, 300, 600, 800, 'green')
pf_01_09 = Platform(1, 4100, 0, 600, 1100, 'purple')
pf_g = Platform(1, -800, 1150, 5000, 20, 'black')


if level == 0:
    platform_sprites = pygame.sprite.Group(pf_01, pf_02, pf_03, pf_04, pf_05, pf_06, pf_07, pf_08, pf_09)
elif level == 1:
    platform_sprites = pygame.sprite.Group(pf_01_01, pf_01_02, pf_01_03, pf_01_04, pf_01_05, pf_01_06, pf_01_07, pf_g,
    pf_01_08, pf_01_09)


# endregion

class Moving_Platform(Platform):
    def __init__(self, level, x, y, width, height, x_speed, y_speed, distance, color=PLATFORM ):
        super().__init__(level, x, y, width, height)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.image.fill(color)
        self.distance = distance
        self.original_pos = self.rect.topleft
        self.cumulative_scrolling_x_shift = 0
        self.cumulative_scrolling_y_shift = 0

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Adjust for cumulative shift from scrolling when checking distance
        effective_x = self.rect.x - self.cumulative_scrolling_x_shift
        effective_y = self.rect.y - self.cumulative_scrolling_y_shift

        if abs(effective_x - self.original_pos[0]) >= self.distance:
            self.x_speed *= -1

        if abs(effective_y - self.original_pos[1]) >= self.distance:
            self.y_speed *= -1

    def move(self, x_shift, y_shift=0):
        super().move(x_shift, y_shift)
        # Increase cumulative shift
        self.cumulative_scrolling_x_shift += x_shift
        self.cumulative_scrolling_y_shift += y_shift


mov_plat01 = Moving_Platform(0, 300, 300, 50, 20,1, 0, 200)
mov_plat02 = Moving_Platform(0, 410, 50, 50, 20, 0, 1, 100, 'orange')
mov_plat03 = Moving_Platform(0, 150, -50, 50, 20, 0, 1, 100, 'black')
mov_plat04 = Moving_Platform(0, 75, -240, 50, 20, 0, 2, 100, 'black')


moving_platform_group = pygame.sprite.Group(mov_plat01, mov_plat02, mov_plat03, mov_plat04)
