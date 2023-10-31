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
gravity = 0.9

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


class Player(Sprite):
    def __init__(self):
        super().__init__()
        # Initialize sprite attributes
        self.image = player_idle[0]  # Initial image for the player
        self.player_width = 28
        self.player_height = 40
        self.rect = pygame.Rect(300, 50, self.player_width, self.player_height)
        self.rect.topleft = (300, 50)

        self.move_speed = 6
        self.jump_power = -20
        
        self.x_velocity = 0
        self.y_velocity = 0
        self.y_velocity_max = 20

        self.grounded = False
        self.facing_right = True
        self.state = "idle"
        self.animation_index = 0

    def update(self):
        # Player movement logic, animations, etc. can go here
        # Gravity
        self.y_velocity += gravity
        if self.y_velocity < self.y_velocity_max:
            self.rect.y += self.y_velocity
        else:
            self.rect.y += self.y_velocity_max

        # Animation
        self.handle_animation()

    def check_collisions(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Handle top collision
                if self.rect.top < platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.y_velocity = 0
                    self.grounded = True
                # Handle bottom collision
                elif self.y_velocity < 0 and self.rect.top <= platform.rect.bottom:
                    self.rect.top = platform.rect.bottom
                    self.y_velocity = 0
                # Handle left collision
                elif self.rect.left < platform.rect.left:
                    self.rect.right = platform.rect.left
                # Handle right collision
                elif self.rect.right > platform.rect.right:
                    self.rect.left = platform.rect.right

    def handle_animation(self):
        if self.grounded:
            if self.facing_right:
                if self.state == 'idle':
                    self.animation_index += 0.1
                    if self.animation_index >= len(player_idle):
                        self.animation_index = 0
                    self.image = player_idle[int(self.animation_index)]
                elif self.state == 'right':
                    self.animation_index += 0.20
                    if self.animation_index >= len(player_run):
                        self.animation_index = 0
                    self.image = player_run[int(self.animation_index)]
            else:  # if not facing right
                if self.state == 'idle':
                    self.animation_index += 0.1
                    if self.animation_index >= len(player_idle):
                        self.animation_index = 0
                    self.image = player_idle_flip[int(self.animation_index)]
                elif self.state == 'left':
                    self.animation_index += 0.20
                    if self.animation_index >= len(player_run):
                        self.animation_index = 0
                    self.image = player_run_flip[int(self.animation_index)]
        else:  # if not grounded
            if self.facing_right:
                self.animation_index += 0.1
                if self.animation_index >= len(player_jump):
                    self.animation_index = 0
                self.image = player_jump[int(self.animation_index)]
            else:
                self.animation_index += 0.1
                if self.animation_index >= len(player_jump):
                    self.animation_index = 0
                self.image = player_jump_flip[int(self.animation_index)]

    def handle_input(self, scroll_callback):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_left()
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_right()
        else:
            self.stop_moving()

        self.move_horizontal(scroll_callback)

    def jump(self):
        if self.grounded:
            self.y_velocity = self.jump_power
            self.grounded = False  # Immediately set grounded to False after a jump

    def move_left(self):
        self.facing_right = False
        self.state = "left"
        self.x_velocity = -self.move_speed

    def move_right(self):
        self.facing_right = True
        self.state = "right"
        self.x_velocity = self.move_speed

    def move_horizontal(self, scroll_callback):
        if self.facing_right:
            if self.rect.right < SCREEN_WIDTH - H_SCROLL_THRESH:
                self.rect.x += self.x_velocity
            else:
                scroll_callback('right')
        else:
            if self.rect.left > H_SCROLL_THRESH:
                self.rect.x += self.x_velocity
            else:
                scroll_callback('left')

    def stop_moving(self):
        self.state = "idle"
        self.x_velocity = 0


def scroll_map(direction):
    for platform in platform_list:
        if direction == 'left':
            platform.move(-player.x_velocity, 0)
        elif direction == 'right':
            platform.move(-player.x_velocity, 0)


def check_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Jump Logic
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()


# Game loop
clock = pygame.time.Clock()
running = True
player = Player()

while running:
    # Event handling
    check_events()

    # Horizontal movement
    player.handle_input(scroll_map)

    # Clear the screen
    screen.fill(GREEN)

    # Blit the platforms
    for platform in platform_list:
        platform.draw(screen)

    blit_pos = (
    player.rect.centerx - player.image.get_width() // 2, (player.rect.centery - player.image.get_height() // 2) - 5)
    player.update()
    screen.blit(player.image, blit_pos)

    # Collision with platforms
    player.check_collisions(platform_list)

    # DEBUGGING ------------------------------------------------
    # pygame.draw.rect(screen, (0, 0, 255), player.rect, 2)
    # pygame.draw.rect(screen, (255, 0, 0), player.rect, 2)
    # print(player.grounded)
    # print(player.y_velocity)

    # If player falls off map
    if player.rect.top > SCREEN_HEIGHT:
        player.rect.y = 0
        player.rect.x = 300

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
