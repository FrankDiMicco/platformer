import pygame

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

