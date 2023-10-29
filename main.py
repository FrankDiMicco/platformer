import pygame
import sys
from platforms import Platform, platform_list

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
gravity = 0.9
grounded = False
facing_right = True
player_state = "idle"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = "#00ca99"
PLATFORM = '#374b43'

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")
from data import *

# Create the player
player_animation_index = 0
player_surf = player_idle[player_animation_index]
player_rect = pygame.Rect(300, 50, 28, 40)

player_x_velocity = 0
player_y_velocity = 0


def scroll_map(direction):
    for platform in platform_list:
        if direction == 'left':
            platform.move(player_x_velocity, 0)
        elif direction == 'right':
            platform.move(-player_x_velocity, 0)


def player_animation():
    global player_surf, player_animation_index
    if grounded:
        if facing_right:
            if player_state == 'idle':
                player_animation_index += 0.1
                if player_animation_index >= len(player_idle):
                    player_animation_index = 0
                player_surf = player_idle[int(player_animation_index)]

            elif player_state == 'right':
                player_animation_index += 0.20
                if player_animation_index >= len(player_run):
                    player_animation_index = 0
                player_surf = player_run[int(player_animation_index)]
        else:
            if player_state == 'idle':
                player_animation_index += 0.1
                if player_animation_index >= len(player_idle):
                    player_animation_index = 0
                player_surf = player_idle_flip[int(player_animation_index)]

            elif player_state == 'left':
                player_animation_index += 0.20
                if player_animation_index >= len(player_run):
                    player_animation_index = 0
                player_surf = player_run_flip[int(player_animation_index)]
    else:
        if facing_right:
            player_animation_index += 0.1
            if player_animation_index >= len(player_jump):
                player_animation_index = 0
            player_surf = player_jump[int(player_animation_index)]

        else:
            player_animation_index += 0.1
            if player_animation_index >= len(player_jump):
                player_animation_index = 0
            player_surf = player_jump_flip[int(player_animation_index)]

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
                player_y_velocity = jump_power

    # Horizontal movement and screen scroll
    # region
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        facing_right = False
        player_state = "left"
        if player_rect.left > SCROLL_THRESH:
            player_x_velocity = move_speed
            player_rect.x -= player_x_velocity
        else:
            player_rect.left = SCROLL_THRESH
            scroll_map('left')
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        facing_right = True
        player_state = "right"
        if player_rect.right < SCREEN_WIDTH - SCROLL_THRESH:
            player_x_velocity = move_speed
            player_rect.x += player_x_velocity
        else:
            player_rect.right = SCREEN_WIDTH - SCROLL_THRESH
            scroll_map('right')
    else:
        player_state = 'idle'
    # endregion

    # Gravity
    player_y_velocity += gravity
    player_rect.y += player_y_velocity

    # Collision with platforms
    for platform in platform_list:
        if player_rect.colliderect(platform.rect):
            if player_rect.top < platform.rect.top:
                player_rect.bottom = platform.rect.top
                player_y_velocity = 0
                grounded = True
            elif player_rect.top > platform.rect.top:
                player_rect.top = platform.rect.bottom
                player_y_velocity = 0
                grounded = True
            elif player_rect.left < platform.rect.left:
                player_rect.right = platform.rect.left
            elif player_rect.right > platform.rect.right:
                player_rect.left = platform.rect.right

    # Clear the screen
    screen.fill(GREEN)

    # Draw game elements
    player_animation()
    blit_position = (
    player_rect.centerx - player_surf.get_width() // 2, (player_rect.centery - player_surf.get_height() // 2) - 5)
    screen.blit(player_surf, blit_position)

    # Blit the platforms
    for platform in platform_list:
        platform.draw(screen)

    # Show player_rect - for debugging
    # pygame.draw.rect(screen, (0, 0, 255), player_rect, 2)
    # pygame.draw.rect(screen, (255, 0, 0), player_rect, 2)

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
