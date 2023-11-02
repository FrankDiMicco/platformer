import pygame
from pygame.sprite import Sprite
import sys
from platforms import Platform, platform_sprites, mov_plat, mov_platform_sprites, Moving_Platform

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
H_SCROLL_THRESH = 250
V_SCROLL_THRESH = 200

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
        self.blit_pos = None

        self.move_speed = 6
        self.jump_power = -18
        self.double_jump = False

        self.x_velocity = 0
        self.y_velocity = 0
        self.y_velocity_max = 20

        self.grounded = False
        self.facing_right = True
        self.on_moving_obstacle = False
        self.keypress_moving = False
        self.is_falling = True
        self.is_jumping = False
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

        # Collision with platforms
        self.check_collisions(platform_sprites)
        self.check_collisions(mov_platform_sprites)

        # Check to see if falling
        if self.grounded and self.y_velocity > 1:
            self.grounded = False

        # Animation
        self.handle_animation()

        # Calculate position to blit player
        self.blit_pos = (self.rect.centerx - self.image.get_width() // 2,
                         (self.rect.centery - self.image.get_height() // 2) - 5)

    def check_collisions(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Handle top collision
                if self.rect.top < platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.y_velocity = 0
                    self.grounded = True
                    self.is_jumping = False

                    if isinstance(platform, Moving_Platform):
                        self.on_moving_obstacle = True
                        self.x_velocity = platform.x_speed
                    else:
                        self.on_moving_obstacle = False
                # Handle left collision
                elif self.rect.left < platform.rect.left:
                    self.rect.right = platform.rect.left
                # Handle right collision
                elif self.rect.right > platform.rect.right:
                    self.rect.left = platform.rect.right
                # Handle bottom collision
                elif self.y_velocity < 0 and self.rect.top <= platform.rect.bottom:
                    self.rect.top = platform.rect.bottom
                    self.y_velocity = 0

    def handle_animation(self):
        if self.grounded:
            if self.keypress_moving:  # Only show running animation if player is actively moving
                if self.facing_right:
                    self.animation_index += 0.20
                    if self.animation_index >= len(player_run):
                        self.animation_index = 0
                    self.image = player_run[int(self.animation_index)]
                else:  # if not facing right and moving
                    self.animation_index += 0.20
                    if self.animation_index >= len(player_run):
                        self.animation_index = 0
                    self.image = player_run_flip[int(self.animation_index)]
            else:  # if not moving
                if self.facing_right:
                    self.animation_index += 0.1
                    if self.animation_index >= len(player_idle):
                        self.animation_index = 0
                    self.image = player_idle[int(self.animation_index)]
                else:  # if not facing right and not moving
                    self.animation_index += 0.1
                    if self.animation_index >= len(player_idle):
                        self.animation_index = 0
                    self.image = player_idle_flip[int(self.animation_index)]
        else:  # if not grounded
            if self.facing_right:
                self.animation_index += 0.1
                if self.animation_index >= len(player_jump):
                    self.animation_index = 0
                self.image = player_jump[int(self.animation_index)]
            else:  # if not grounded and not facing right
                self.animation_index += 0.1
                if self.animation_index >= len(player_jump):
                    self.animation_index = 0
                self.image = player_jump_flip[int(self.animation_index)]

    def handle_input(self, scroll_callback):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_left()
            self.keypress_moving = True  # User is pressing a movement key
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_right()
            self.keypress_moving = True  # User is pressing a movement key
        else:
            self.keypress_moving = False  # No movement key is pressed
            if not self.on_moving_obstacle:
                self.stop_moving()

        self.move_horizontal(scroll_callback)
        self.move_vertical(scroll_callback)

    def jump(self):
        if self.grounded:
            self.y_velocity = self.jump_power
            self.grounded = False  # Immediately set grounded to False after a jump
            self.is_jumping = True

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

    def move_vertical(self, scroll_callback):
        if V_SCROLL_THRESH < self.rect.top < SCREEN_HEIGHT - V_SCROLL_THRESH:
            pass
        elif self.rect.top < V_SCROLL_THRESH:
            scroll_callback('up')
        elif self.rect.top > SCREEN_HEIGHT - V_SCROLL_THRESH:
            scroll_callback('down')

    def stop_moving(self):
        self.state = "idle"
        self.x_velocity = 0


def scroll_map(direction):
    for platform in platform_sprites:
        if direction == 'left':
            platform.move(-player.x_velocity, 0)
        elif direction == 'right':
            platform.move(-player.x_velocity, 0)
        elif direction == 'up':
            platform.move(0, 1)
        elif direction == 'down':
            platform.move(0, -2)

    for platform in mov_platform_sprites:
        if direction == 'left':
            platform.move(-player.x_velocity, 0)
        elif direction == 'right':
            platform.move(-player.x_velocity, 0)
        elif direction == 'up':
            platform.move(0, 1)
        elif direction == 'down':
            platform.move(0, -2)


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

    # Update the moving platform
    mov_plat.update()

    # Blit the platforms
    platform_sprites.draw(screen)
    screen.blit(mov_plat.image, (mov_plat.rect.x, mov_plat.rect.y))

    # Update player - should only happen once per frame
    player.update()
    screen.blit(player.image, player.blit_pos)

    # DEBUGGING ------------------------------------------------
    # print(player.grounded)
    # print(player.y_velocity)

    # If player falls off map
    if player.rect.top > 2 * SCREEN_HEIGHT:
        player.rect.y = 10
        player.rect.x = 300

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
