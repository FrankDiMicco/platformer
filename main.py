import pygame
from pygame.sprite import Sprite
import sys
from platforms import platform_sprites, moving_platform_group, Moving_Platform, mov_plat01, mov_plat02
from item import Item

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
H_SCROLL_THRESH = 250
V_SCROLL_THRESH = 200
PLATFORM_BUFFER = 15  # Helps avoid top collision from the side

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


class Player(Sprite):
    def __init__(self):
        super().__init__()
        # Initialize sprite attributes
        self.image = player_idle[0]  # Initial image for the player
        self.player_width = 20  # used to be 28, lets wait for weird stuff to happen
        self.player_height = 40
        self.rect = pygame.Rect(300, 50, self.player_width, self.player_height)
        self.rect.topleft = (300, 50)
        self.blit_pos = None

        self.move_speed = 5
        self.jump_power = -15
        self.double_jump_unlocked = True
        self.double_jump = False
        self.wall_cling_unlocked = False
        self.wall_cling = False

        self.x_velocity = 0
        self.y_velocity = 0
        self.y_velocity_max = 18

        self.grounded = False
        self.facing_right = True
        self.on_moving_obstacle = False
        self.keypress_moving = False  # used for animation of running state
        self.is_falling = True
        self.is_jumping = False
        self.state = "idle"
        self.animation_index = 0
        self.mouse_buttons = pygame.mouse.get_pressed()

    def update(self):

        # Gravity is added to player up to y_velocity_max
        self.y_velocity += gravity
        if self.y_velocity < self.y_velocity_max:
            self.rect.y += self.y_velocity
        else:
            self.rect.y += self.y_velocity_max

        # Collision with platforms
        self.check_collisions(platform_sprites)
        self.check_collisions(moving_platform_group)

        # Check to see if falling
        if self.grounded and self.y_velocity > 2.9:  # 2.9 seems to prevent animation glitches
            self.grounded = False
            self.is_falling = True

        # Check to see if player has reached top of jump and has started falling
        if self.is_jumping and self.y_velocity >= 0:
            self.is_jumping = False
            self.is_falling = True

        # Animation
        self.handle_animation()

        # Calculate position to blit player
        self.blit_pos = (self.rect.centerx - self.image.get_width() // 2,
                         (self.rect.centery - self.image.get_height() // 2) - 5)

    def check_collisions(self, platforms):
        # Check to see if player is attempting a wall_cling or grapple(future)
        self.mouse_buttons = pygame.mouse.get_pressed()

        for platform in platforms:
            if self.rect.colliderect(platform.rect):

                # Handle top collision
                if self.rect.top + PLATFORM_BUFFER < platform.rect.top and not self.is_jumping:
                    self.rect.bottom = platform.rect.top
                    self.y_velocity = 0
                    self.grounded = True
                    self.is_jumping = False
                    self.is_falling = False
                    if self.double_jump_unlocked:
                        self.double_jump = True

                    if isinstance(platform, Moving_Platform):
                        self.on_moving_obstacle = True
                        self.x_velocity = platform.x_speed
                    else:
                        self.on_moving_obstacle = False
                    self.wall_cling = False

                # Handle left collision
                elif self.rect.left < platform.rect.left:
                    self.rect.right = platform.rect.left
                    # if self.mouse_buttons[2] and self.wall_cling_unlocked:
                    if self.wall_cling_unlocked and not isinstance(platform, Moving_Platform):
                        self.y_velocity = 0
                        self.y_velocity -= gravity
                        self.wall_cling = True

                # Handle right collision
                elif self.rect.right > platform.rect.right:
                    self.rect.left = platform.rect.right
                    # Handle Wall Cling
                    # if self.mouse_buttons[2] and self.wall_cling_unlocked:
                    if self.wall_cling_unlocked and not isinstance(platform, Moving_Platform):
                        self.y_velocity = 0
                        self.y_velocity -= gravity
                        self.wall_cling = True

                # Handle bottom collision
                elif self.y_velocity < 0 and self.rect.top <= platform.rect.bottom:
                    self.rect.top = platform.rect.bottom
                    self.y_velocity = 0
                    self.wall_cling = False
        for i in items:
            if self.rect.colliderect(i.rect):
                if i.effect == 'vert boost':
                    self.y_velocity = -20
                # i.kill()

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
            if self.facing_right and self.is_jumping:
                self.animation_index += 0.1
                if self.animation_index >= len(player_jump):
                    self.animation_index = 0
                self.image = player_jump[int(self.animation_index)]
            elif not self.facing_right and self.is_jumping:  # if not grounded and not facing right
                self.animation_index += 0.1
                if self.animation_index >= len(player_jump):
                    self.animation_index = 0
                self.image = player_jump_flip[int(self.animation_index)]
            elif self.facing_right and self.is_falling:
                self.animation_index += 0.1
                if self.animation_index > len(player_fall):
                    self.animation_index = 0
                self.image = player_fall[int(self.animation_index)]
            elif not self.facing_right and self.is_falling:
                self.animation_index += 0.1
                if self.animation_index > len(player_fall):
                    self.animation_index = 0
                self.image = player_fall_flip[int(self.animation_index)]

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
            if not self.on_moving_obstacle or not self.grounded:
                self.stop_moving()

        self.move_horizontal(scroll_callback)
        self.move_vertical(scroll_callback)

    def jump(self):
        if self.grounded or self.double_jump:
            if not self.grounded:
                self.double_jump = False
            self.y_velocity = self.jump_power
            self.grounded = False  # Immediately set grounded to False after a jump
            self.is_jumping = True
            self.on_moving_obstacle = False

    def variable_jump(self):
        if self.y_velocity < 0:
            self.y_velocity = 0

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


class Enemy(Sprite):
    def __init__(self, x, y, width, height, life):
        super().__init__()
        self.image = pygame.image.load('graphics/enemies/ufo.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y
        self.life = life
        self.x_velocity = -1
        self.y_velocity = 0
        self.original_pos = self.rect.topleft
        self.cumulative_scrolling_x_shift = 0
        self.cumulative_scrolling_y_shift = 0

    def update(self):
        self.y_velocity += gravity
        self.rect.y += self.y_velocity
        self.move()
        self.check_collisions()

    def check_collisions(self):
        for platform in platform_sprites:
            if self.rect.colliderect(platform.rect):
                self.handle_platform_collisions(platform)

    def handle_platform_collisions(self, platform):

        # For top of platform interaction
        if self.rect.top < platform.rect.top:
            self.y_velocity = 0
            # Check for right edge of platform
            if self.rect.right > platform.rect.right:
                self.x_velocity *= -1
            # Check for left edge of platform
            elif self.rect.left < platform.rect.left:
                self.rect.left = platform.rect.left  # Prevent moving past the platform edge
                self.x_velocity *= -1  # Change direction
            self.rect.bottom = platform.rect.top

        # For left collisions
        elif self.rect.left < platform.rect.right:
            self.x_velocity *= -1
            self.rect.left = platform.rect.right

        # For right collisions
        elif self.rect.right > platform.rect.left:
            self.x_velocity *= -1
            self.rect.right = platform.rect.left

    def move(self, x_shift=0, y_shift=0):

        self.rect.x += self.x_velocity

        self.rect.move_ip(x_shift, y_shift)

        self.cumulative_scrolling_x_shift += x_shift
        self.cumulative_scrolling_y_shift += y_shift


def scroll_map(direction):
    for platform in platform_sprites:
        if direction == 'left':
            platform.move(-player.x_velocity, 0)
        elif direction == 'right':
            platform.move(-player.x_velocity, 0)
        elif direction == 'up':
            platform.move(0, 2)
            if player.wall_cling:
                player.rect.y += .5
        elif direction == 'down':
            platform.move(0, -3)

    for platform in moving_platform_group:
        if direction == 'left':
            platform.move(-player.x_velocity, 0)
        elif direction == 'right':
            platform.move(-player.x_velocity, 0)
        elif direction == 'up':
            platform.move(0, 2)
        elif direction == 'down':
            platform.move(0, -3)

    for item in items:
        if direction == 'left':
            item.move(-player.x_velocity, 0)
        elif direction == 'right':
            item.move(-player.x_velocity, 0)
        elif direction == 'up':
            item.move(0, 2)
        elif direction == 'down':
            item.move(0, -3)

    for enemy in enemies:
        if direction == 'left':
            enemy.move(-player.x_velocity, 0)
        elif direction == 'right':
            enemy.move(-player.x_velocity, 0)
        elif direction == 'up':
            enemy.move(0, 2)
        elif direction == 'down':
            enemy.move(0, -3)


def check_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Jump Logic
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.variable_jump()


# Game loop
clock = pygame.time.Clock()
running = True
player = Player()

# test code for item creation
orb_boost = Item(50, 50, 32, 32, 'vert boost')
items = pygame.sprite.Group()
items.add(orb_boost)

# test code for enemies
ufo = Enemy(200, 100, 42, 32, 10)
enemies = pygame.sprite.Group()
enemies.add(ufo)

while running:
    # Event handling
    check_events()

    # Horizontal movement
    player.handle_input(scroll_map)

    # Clear the screen
    screen.fill(GREEN)

    # Update the moving platform
    moving_platform_group.update()

    # Blit the platforms
    platform_sprites.draw(screen)
    moving_platform_group.draw(screen)

    # Blit the items
    items.draw(screen)

    # Update player - should only happen once per frame
    player.update()
    screen.blit(player.image, player.blit_pos)

    print(player.wall_cling)


    # Blit the enemies
    ufo.update()
    screen.blit(ufo.image, ufo.rect)

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
