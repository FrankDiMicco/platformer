import pygame
from pygame.sprite import Sprite
import sys
from platforms import Platform, platform_list

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
H_SCROLL_THRESH = 250

# Variables
move_speed = 6
jump_power = -20
gravity = 0.9
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


# player_x_velocity = 0
# player_y_velocity = 0

class Player(Sprite):
    def __init__(self):
        super().__init__()
        # Initialize sprite attributes
        self.image = player_idle[0]  # Initial image for the player
        self.rect = pygame.Rect(300, 50, 28, 40)
        self.rect.topleft = (300, 50)

        self.x_velocity = 0
        self.y_velocity = 0
        self.jump_buffer = 0

        self.grounded = False
        self.facing_right = True
        self.state = "idle"
        self.animation_index = 0

    def update(self):
        # Player movement logic, animations, etc. can go here
        # Gravity
        self.y_velocity += gravity
        self.rect.y += self.y_velocity

        # Animation
        self.handle_animation()

    def handle_animation(self):
        # Player animation handling logic goes here.
        pass  # Placeholder, fill this in with your animation logic from above.

    def jump(self):
        if self.grounded:
            self.y_velocity = jump_power
            self.grounded = False  # Immediately set grounded to False after a jump
            self.jump_buffer = 5
            print("jump button pressed")
            print(self.y_velocity)

    def move_left(self):
        self.facing_right = False
        self.state = "left"
        self.x_velocity = move_speed

    def move_right(self):
        self.facing_right = True
        self.state = "right"
        self.x_velocity = -move_speed

    def stop_moving(self):
        self.state = "idle"
        self.x_velocity = 0


def scroll_map(direction):
    for platform in platform_list:
        if direction == 'left':
            platform.move(player.x_velocity, 0)
        elif direction == 'right':
            platform.move(-player.x_velocity, 0)


def player_animation():
    global player_surf, player_animation_index
    if player.grounded:
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
player = Player()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Jump Logic
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # Horizontal movement and screen scroll
    # region
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.move_left()
        if player.rect.left > H_SCROLL_THRESH:
            player.x_velocity = move_speed
            player.rect.x -= player.x_velocity
        else:
            player.rect.left = H_SCROLL_THRESH
            scroll_map('left')
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.facing_right = True
        player.state = "right"
        if player.rect.right < SCREEN_WIDTH - H_SCROLL_THRESH:
            player.x_velocity = move_speed
            player.rect.x += player.x_velocity
        else:
            player.rect.right = SCREEN_WIDTH - H_SCROLL_THRESH
            scroll_map('right')
    else:
        player.state = 'idle'
    # endregion

    # Clear the screen
    screen.fill(GREEN)

    # player_animation()

    # Blit the platforms
    for platform in platform_list:
        platform.draw(screen)
    blit_position = (
        player.rect.centerx - player.image.get_width() // 2, (player.rect.centery - player.image.get_height() // 2) - 5)
    player.update()
    screen.blit(player.image, blit_position)

    # Draw game elements

    # Collision with platforms
    # region
    for platform in platform_list:
        if player.rect.colliderect(platform.rect):
            if player.rect.top < platform.rect.top and player.jump_buffer <= 0:
                player.rect.bottom = platform.rect.top
                player.y_velocity = 0
                player.grounded = True

            elif player.y_velocity < 0 and player.rect.top <= platform.rect.bottom:
                player.rect.top = platform.rect.bottom
                player.y_velocity = 0
            elif player.rect.left < platform.rect.left:
                player.rect.right = platform.rect.left
            elif player.rect.right > platform.rect.right:
                player.rect.left = platform.rect.right
    # endregion

    # DEBUGGING ------------------------------------------------
    # pygame.draw.rect(screen, (0, 0, 255), player.rect, 2)
    # pygame.draw.rect(screen, (255, 0, 0), player.rect, 2)
    # print(player.grounded)
    # print(player.y_velocity)

    # If player falls off map
    if player.rect.y > 600:
        player.rect.y = 0
        player.rect.x = 300

    # Count down jump_buffer
    player.jump_buffer = max(0, player.jump_buffer - 1)

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
