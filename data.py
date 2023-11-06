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


# For when player is falling animation
player_fall_01 = pygame.image.load('graphics/player/fall01.png').convert_alpha()
player_fall_02 = pygame.image.load('graphics/player/fall02.png').convert_alpha()
player_fall_03 = pygame.image.load('graphics/player/fall03.png').convert_alpha()
player_fall_04 = pygame.image.load('graphics/player/fall04.png').convert_alpha()
player_fall = [player_fall_01, player_fall_02, player_fall_03, player_fall_04]
player_fall_flip = [pygame.transform.flip(frame, True, False) for frame in player_fall]

# For parallax background eventually
bg1 = pygame.image.load('graphics/bg/FarBG.png').convert_alpha()
bg2 = pygame.image.load('graphics/bg/FarBottomBG.png').convert_alpha()
bg3 = pygame.image.load('graphics/bg/FarTopBG.png').convert_alpha()
bg4 = pygame.image.load('graphics/bg/TreesBG.png').convert_alpha()
bg5 = pygame.image.load('graphics/bg/TreesFG.png').convert_alpha()
level_01_image_list = [bg1, bg2, bg3, bg4, bg5]





