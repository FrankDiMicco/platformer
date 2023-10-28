
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
SCROLL_THRESH = 250

# Variables
move_speed = 6
jump_power = -20
gravity = 1
grounded = False
facing_right = True

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = "#00ca99"
PLATFORM = '#374b43'

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

# Create the player
player_idle_1 = pygame.image.load('graphics/player/idle01.png').convert_alpha()
player_idle_2 = pygame.image.load('graphics/player/idle02.png').convert_alpha()
player_idle_3 = pygame.image.load('graphics/player/idle03.png').convert_alpha()
player_idle_4 = pygame.image.load('graphics/player/idle04.png').convert_alpha()
player_idle = [player_idle_1, player_idle_2, player_idle_3, player_idle_4]
player_idle_flip = [pygame.transform.flip(frame, True, False) for frame in player_idle]
player_animation_index = 0
player_surf = player_idle[player_animation_index]
#player_rect = player_surf.get_rect(midbottom=(300, 50))
player_rect = pygame.Rect(300, 50, 28, 40)

player_x_velocity = 0
player_y_velocity = 0

# Create the platforms
platform_long = pygame.Rect(0, 550, 200, 20)
platform_long2 = pygame.Rect(200, 500, 200, 20)
platform_long3 = pygame.Rect(500, 550, 600, 20)
platform_long4 = pygame.Rect(-300, 500, 300, 20)
platform_long5 = pygame.Rect(600, 400, 300, 20)
platform_list = [platform_long, platform_long2, platform_long3, platform_long4, platform_long5]


def scroll_map(direction):
    for platform in platform_list:
        if direction == 'left':
            platform.x += move_speed
        elif direction == 'right':
            platform.x -= move_speed


def player_animation():
    global player_surf, player_animation_index
    player_animation_index += 0.1
    if player_animation_index >= len(player_idle):
        player_animation_index = 0

    if facing_right:
        player_surf = player_idle[int(player_animation_index)]
    else:
        player_surf = player_idle_flip[int(player_animation_index)]

    # player_surf = pygame.transform.flip(player_surf, True, False)  # Flip the image horizontally




# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Jump Logic
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grounded:
                grounded = False
                gravity = jump_power

    # Horizontal movement and screen scroll
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        facing_right = False
        if player_rect.left > SCROLL_THRESH:
            player_rect.x -= move_speed
        else:
            player_rect.left = SCROLL_THRESH
            scroll_map('left')
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        facing_right = True
        if player_rect.right < SCREEN_WIDTH - SCROLL_THRESH:
            player_rect.x += move_speed
        else:
            player_rect.right = SCREEN_WIDTH - SCROLL_THRESH
            scroll_map('right')

    # Gravity
    gravity += 1
    player_rect.y += gravity

    # Collision with platforms
    for platform in platform_list:
        if player_rect.colliderect(platform):
            gravity = 0
            grounded = True
            if player_rect.top < platform.top:
                player_rect.bottom = platform.top
            elif player_rect.top > platform.top:
                player_rect.top = platform.bottom

    # Clear the screen
    screen.fill(GREEN)

    # Draw game elements
    player_animation()
    blit_position = (player_rect.centerx - player_surf.get_width() // 2, (player_rect.centery - player_surf.get_height() // 2) - 5)
    screen.blit(player_surf, blit_position)

    for platform in platform_list:
        pygame.draw.rect(screen, PLATFORM, platform)

    # Show player_rect - for debugging
    #pygame.draw.rect(screen, (0, 0, 255), player_rect, 2)
    #pygame.draw.rect(screen, (255, 0, 0), player_rect, 2)

    # If player falls off map
    if player_rect.y > 600:
        player_rect.y = 0
        player_rect.x = 300

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()