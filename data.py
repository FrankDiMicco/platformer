import pygame


# Create the player idle animation lists
player_idle_1 = pygame.image.load('graphics/player/idle01.png').convert_alpha()
player_idle_2 = pygame.image.load('graphics/player/idle02.png').convert_alpha()
player_idle_3 = pygame.image.load('graphics/player/idle03.png').convert_alpha()
player_idle_4 = pygame.image.load('graphics/player/idle04.png').convert_alpha()
player_idle = [player_idle_1, player_idle_2, player_idle_3, player_idle_4]
player_idle_flip = [pygame.transform.flip(frame, True, False) for frame in player_idle]


# Create player jump animation - running vs stationary, start-mid-end sequences too
player_jump_01 = pygame.image.load('graphics/player/jump.png')
player_jump = [player_jump_01]
player_jump_flip = [pygame.transform.flip(frame, True, False) for frame in player_jump]


# Create the player run animation lists
player_run_1 = pygame.image.load('graphics/player/run01.png').convert_alpha()
player_run_2 = pygame.image.load('graphics/player/run02.png').convert_alpha()
player_run_3 = pygame.image.load('graphics/player/run03.png').convert_alpha()
player_run_4 = pygame.image.load('graphics/player/run04.png').convert_alpha()
player_run_5 = pygame.image.load('graphics/player/run05.png').convert_alpha()
player_run_6 = pygame.image.load('graphics/player/run06.png').convert_alpha()
player_run_7 = pygame.image.load('graphics/player/run07.png').convert_alpha()
player_run_8 = pygame.image.load('graphics/player/run08.png').convert_alpha()
player_run_9 = pygame.image.load('graphics/player/run09.png').convert_alpha()
player_run_10 = pygame.image.load('graphics/player/run10.png').convert_alpha()

player_run = [player_run_1, player_run_2, player_run_3, player_run_4, player_run_5,
              player_run_6, player_run_7, player_run_8, player_run_9, player_run_10]
player_run_flip = [pygame.transform.flip(frame, True, False) for frame in player_run]


# Create the platforms
platform_long = pygame.Rect(0, 550, 200, 20)
platform_long2 = pygame.Rect(200, 500, 200, 20)
platform_long3 = pygame.Rect(500, 550, 600, 20)
platform_long4 = pygame.Rect(-300, 500, 300, 20)
platform_long5 = pygame.Rect(600, 400, 300, 20)
platform_list = [platform_long, platform_long2, platform_long3, platform_long4, platform_long5]

