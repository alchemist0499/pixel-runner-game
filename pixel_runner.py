import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    player_walk1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
    player_walk2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
    self.player_walk = [player_walk1, player_walk2]
    self.player_index = 0
    self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

    self.image = self.player_walk[self.player_index]
    self.rect = self.image.get_rect(midbottom = (80, 300))
    self.gravity = 0

    self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
    self.jump_sound.set_volume(0.5)

  def player_input(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
      self.gravity = -20
      self.jump_sound.play()

  def player_gravity(self):
    self.gravity += 1
    self.rect.y += self.gravity
    if self.rect.bottom >= 300: self.rect.bottom = 300

  def animation_state(self):
    if self.rect.bottom < 300:
      self.image = self.player_jump
    else:
      self.player_index += 0.1
      if self.player_index >= len(self.player_walk): self.player_index = 0 
      self.image = self.player_walk[int(self.player_index)] 

  def update(self):
    self.player_input()
    self.player_gravity()
    self.animation_state()

class Obstacle(pygame.sprite.Sprite):
  def __init__(self, type):
    super().__init__()
    if type == 'fly':
      fly_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
      fly_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
      self.frames = [fly_1, fly_2]
      y_pos = 210
    else:
      snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
      snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
      self.frames = [snail_1, snail_2]
      y_pos = 300

    self.animation_index = 0
    self.image = self.frames[self.animation_index]
    self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

  def animation_state(self):
    self.animation_index += 0.1
    if self.animation_index >= len(self.frames): self.animation_index = 0
    self.image = self.frames[int(self.animation_index)]

  def destroy(self):
    if self.rect.x <= -100:
      self.kill()

  def update(self):
    self.animation_state()
    self.rect.x -= 6
    self.destroy()

def display_score():
  current_time = int((pygame.time.get_ticks() - start_time) / 1000)
  score_surf = text_font.render(f"Score : {current_time}", False, (64, 64, 64))
  score_rect = score_surf.get_rect(center = (400, 50))
  pygame.draw.rect(screen, "#c0e8cf", score_rect)
  pygame.draw.rect(screen, "#c0e8cf", score_rect, 10)
  screen.blit(score_surf, score_rect)
  return current_time

def collision_sprite():
  if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
    obstacle_group.empty()
    return False
  return True

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Pixel Runner")
clock = pygame.time.Clock()
text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.play(loops= -1)

# groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surf = pygame.image.load("graphics/Sky.png").convert()
ground_surf = pygame.image.load("graphics/ground.png").convert()

# intro
game_name = text_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_message = text_font.render("Press space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 330))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

    if game_active:
      # obstacle_rect
      if event.type == obstacle_timer:
        obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
    else:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        game_active = True
        start_time = pygame.time.get_ticks()

  if game_active:
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, 300))
    score = display_score()

    player.draw(screen)
    player.update()

    obstacle_group.draw(screen)
    obstacle_group.update()

    # collision
    game_active = collision_sprite()
  else:
    screen.fill((94, 129, 162))
    screen.blit(game_name, game_name_rect)
    screen.blit(player_stand, player_stand_rect)

    game_score = text_font.render(f"Your score : {score}", False, (111, 196, 169))
    game_score_rect = game_score.get_rect(center = (400, 330))

    if score: screen.blit(game_score, game_score_rect)
    else: screen.blit(game_message, game_message_rect)

  pygame.display.update()
  clock.tick(60)























# import pygame
# from sys import exit
# from random import randint

# def display_score():
#   current_time = int((pygame.time.get_ticks() - start_time) / 1000)
#   score_surf = text_font.render(f"Score : {current_time}", False, (64, 64, 64))
#   score_rect = score_surf.get_rect(center = (400, 50))
#   pygame.draw.rect(screen, "#c0e8cf", score_rect)
#   pygame.draw.rect(screen, "#c0e8cf", score_rect, 10)
#   screen.blit(score_surf, score_rect)
#   return current_time

# def player_animation():
#   global player_surf, player_index
#   if player_rect.bottom < 300:
#     player_surf = player_jump
#   else:
#     player_index += 0.1
#     if player_index > len(player_walk): player_index = 0
#     player_surf = player_walk[int(player_index)]

# def obstacle_movement(obstacle_list):
#   if obstacle_list:
#     for obstacle_rect in obstacle_list:
#       obstacle_rect.x -= 5

#       if obstacle_rect.bottom == 300:screen.blit(snail_surf, obstacle_rect)
#       else:screen.blit(fly_surf, obstacle_rect)

#     obstacle_list = [obstacle for obstacle in obstacle_list if obstacle_rect.x > -100]
#     return obstacle_list
#   return []

# def collisions(player, obstacle_list):
#   if obstacle_list:
#     for obstacle_rect in obstacle_list:
#       if player.colliderect(obstacle_rect):
#         return False
#   return True

# pygame.init()
# screen = pygame.display.set_mode((800, 400))
# pygame.display.set_caption("Pixel Runner")
# clock = pygame.time.Clock()
# text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
# game_active = False
# start_time = 0
# score = 0

# sky_surf = pygame.image.load("graphics/Sky.png").convert()
# ground_surf = pygame.image.load("graphics/ground.png").convert()

# # snail
# snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
# snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
# snail_frames = [snail_1, snail_2]
# snail_index = 0
# snail_surf = snail_frames[snail_index]

# # fly
# fly_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
# fly_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
# fly_frames = [fly_1, fly_2]
# fly_index = 0
# fly_surf = fly_frames[fly_index]

# obstacle_rect_list = []

# # player
# player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
# player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
# player_walk = [player_walk_1, player_walk_2]
# player_index = 0
# player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
# player_surf = player_walk[player_index]
# player_rect = player_surf.get_rect(bottomleft = (80, 300))

# player_gravity = 0

# # timer
# obstacle_timer = pygame.USEREVENT + 1
# pygame.time.set_timer(obstacle_timer, 1500)

# snail_animation_timer = pygame.USEREVENT + 2
# pygame.time.set_timer(snail_animation_timer, 500)

# fly_animation_timer = pygame.USEREVENT + 3
# pygame.time.set_timer(fly_animation_timer, 200)

# # intro
# game_name = text_font.render("Pixel Runner", False, (111, 196, 169))
# game_name_rect = game_name.get_rect(center = (400, 80))

# player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
# player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
# player_stand_rect = player_stand.get_rect(center = (400, 200))

# game_message = text_font.render("Press space to run", False, (111, 196, 169))
# game_message_rect = game_message.get_rect(center = (400, 330))

# while True:
#   for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#       pygame.quit()
#       exit()

#     if game_active:
#       # controll
#       if event.type == pygame.MOUSEBUTTONDOWN:
#         if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
#           player_gravity = -20
#       if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_SPACE and player_rect.bottom == 300:
#           player_gravity = -20

#       # obstacle_rect
#       if event.type == obstacle_timer:
#         if randint(0, 2):
#           obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100), 300)))
#         else:
#           obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100), 210)))

#       # obstacle animation
#       if event.type == snail_animation_timer:
#         if snail_index == 0: snail_index = 1
#         else: snail_index == 0
#         snail_surf = snail_frames[snail_index]

#       if event.type == fly_animation_timer:
#         if fly_index == 0: fly_index = 1
#         else: fly_index = 0
#         fly_surf = fly_frames[fly_index]
#     else:
#       if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#         game_active = True
#         start_time = pygame.time.get_ticks()

#   if game_active:
#     screen.blit(sky_surf, (0, 0))
#     screen.blit(ground_surf, (0, 300))
#     score = display_score()

#     # snail movement
#     obstacle_rect_list = obstacle_movement(obstacle_rect_list)

#     # player movement
#     player_gravity += 1
#     player_rect.bottom += player_gravity
#     if player_rect.bottom >= 300: player_rect.bottom = 300
#     player_animation()
#     screen.blit(player_surf, player_rect)

#     # collision
#     game_active = collisions(player_rect, obstacle_rect_list)
#   else:
#     screen.fill((94, 129, 162))
#     screen.blit(game_name, game_name_rect)
#     screen.blit(player_stand, player_stand_rect)

#     obstacle_rect_list.clear()
#     player_rect.bottomleft = (80, 300)
#     player_gravity = 0

#     game_score = text_font.render(f"Your score : {score}", False, (111, 196, 169))
#     game_score_rect = game_score.get_rect(center = (400, 330))

#     if score: screen.blit(game_score, game_score_rect)
#     else: screen.blit(game_message, game_message_rect)

#   pygame.display.update()
#   clock.tick(60)
























# import pygame
# from sys import exit
# from random import randint

# def score_diplay():
#   current_time = int((pygame.time.get_ticks() - start_time) / 1000)
#   score_surf = text_font.render(f'Score: {current_time}', False, (64, 64, 64))
#   score_rect = score_surf.get_rect(center = (400, 50))
#   pygame.draw.rect(screen, "#c0e8cf", score_rect)
#   pygame.draw.rect(screen, "#c0e8cf", score_rect, 10)
#   screen.blit(score_surf, score_rect)
#   return current_time

# def obstacle_movement(obstacle_list):
#   if obstacle_list:
#     for obstacle_rect in obstacle_list:
#       obstacle_rect.x -= 5

#       if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
#       else: screen.blit(fly_surf, obstacle_rect)

#     obstacle_list = [obstacle for obstacle in obstacle_list if obstacle_rect.x > -100]
#     return obstacle_list
#   else: return []

# def collisions(player, obstacles):
#   if obstacles:
#     for obstacle_rect in obstacles:
#       if player.colliderect(obstacle_rect):
#         return False
#   return True

# def player_animation():
#   global player_surf, player_index
#   if player_rect.bottom < 300:
#     player_surf = player_jump
#   else: 
#     player_index += 0.1 
#     if player_index >= len(player_walk): player_index = 0
#     player_surf = player_walk[int(player_index)]

# pygame.init()
# screen = pygame.display.set_mode((800, 400))
# pygame.display.set_caption("Runner")
# clock = pygame.time.Clock()
# text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
# game_active = False
# start_time = 0
# score = 0

# sky_surf = pygame.image.load("graphics/Sky.png").convert()
# ground_surf = pygame.image.load("graphics/ground.png").convert()


# # snail
# snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
# snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
# snail_frames = [snail_1, snail_2]
# snail_index = 0
# snail_surf = snail_frames[snail_index]

# # fly
# fly_1 = pygame.image.load("graphics/Fly/Fly1.png")
# fly_2 = pygame.image.load("graphics/Fly/Fly2.png")
# fly_frames = [fly_1, fly_2]
# fly_index = 0
# fly_surf = fly_frames[fly_index]


# obstacle_rect_list = []

# # player
# player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
# player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
# player_walk = [player_walk_1, player_walk_2]
# player_index = 0
# player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

# player_surf = player_walk[player_index]
# player_rect = player_surf.get_rect(midbottom = (80, 300))
# player_gravity = 0

# # player intro
# player_stand = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
# player_stand = pygame.transform.rotozoom(player_stand, 0, 2 )
# player_stand_rect = player_stand.get_rect(center = (400, 200))

# player_name = text_font.render("Pixel Runner", False, (111, 196, 169))
# player_name_rect = player_name.get_rect(center = (400, 80))

# game_message = text_font.render("Press space to run", False, (111, 196, 169))
# game_message_rect = game_message.get_rect(center = (400, 330))

# # timer
# obstacle_timer = pygame.USEREVENT + 1
# pygame.time.set_timer(obstacle_timer, 1500)

# snail_animation_timer = pygame.USEREVENT + 2
# pygame.time.set_timer(snail_animation_timer, 500)

# fly_animation_timer = pygame.USEREVENT + 3
# pygame.time.set_timer(fly_animation_timer, 200)

# while True:
#   for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#       pygame.quit()
#       exit()

#     if game_active:
#       # control
#       if event.type == pygame.MOUSEBUTTONDOWN:
#         if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
#           player_gravity = -20
#       if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
#           player_gravity = -20

#       # obstacle spawn
#       if event.type == obstacle_timer:
#         if randint(0, 2):
#           obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100), 300)))
#         else:
#           obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100), 210)))

#       # obstacle animation
#       if event.type == snail_animation_timer:
#         if snail_index == 0: snail_index = 1
#         else: snail_index = 0
#         snail_surf = snail_frames[snail_index]
#       if event.type == fly_animation_timer:
#         if fly_index == 0: fly_index = 1
#         else: fly_index = 0
#         fly_surf = fly_frames[fly_index]
        
#     else:
#       if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#         game_active = True
#         start_time = pygame.time.get_ticks()

#   if game_active:
#     screen.blit(sky_surf, (0, 0))
#     screen.blit(ground_surf, (0, 300))
#     score = score_diplay()

#     # player
#     player_gravity += 1
#     player_rect.bottom += player_gravity
#     if player_rect.bottom >= 300: player_rect.bottom = 300
#     player_animation()
#     screen.blit(player_surf, player_rect)
    
#     # obstacle movement
#     obstacle_rect_list = obstacle_movement(obstacle_rect_list)

#     # collision
#     game_active = collisions(player_rect, obstacle_rect_list)

#   else:
#     screen.fill((94, 129, 162))
#     screen.blit(player_stand, player_stand_rect)
#     screen.blit(player_name, player_name_rect)
#     obstacle_rect_list.clear()
#     player_rect.midbottom = (80, 300)
#     player_gravity = 0

#     score_message = text_font.render(f"Your score: {score}", False, (111, 196, 169))
#     score_message_rect = score_message.get_rect(center = (400, 330))

#     if score == 0: screen.blit(game_message, game_message_rect)
#     else: screen.blit(score_message, score_message_rect)

#   pygame.display.update()
#   clock.tick(60)















# import pygame
# from sys import exit
# from random import randint

# def display_score():
#   current_time = int((pygame.time.get_ticks() - start_time) / 1000)
#   score_surf = text_font.render(f'Score: {current_time}', False, (64, 64, 64))
#   score_rect = score_surf.get_rect(center = (400, 50))
#   screen.blit(score_surf, score_rect)
#   return current_time

# def obstacle_movement(obstacle_list):
#   if obstacle_list:
#     for obstacle_rect in obstacle_list:
#       obstacle_rect.x -= 5
      
#       if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
#       else: screen.blit(fly_surf, obstacle_rect)

#     obstacle_list = [obstacle for obstacle in obstacle_list if obstacle_rect.x > -100]
#     return obstacle_list
#   return []

# def collisions(player, obstacle_list):
#   if obstacle_list:
#     for obstacle_rect in obstacle_list:
#       if player.colliderect(obstacle_rect):
#         return False
#   return True

# pygame.init()
# screen = pygame.display.set_mode((800, 400))
# pygame.display.set_caption("Runner")
# clock = pygame.time.Clock()
# text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
# game_active = False
# start_time = 0
# score = 0

# sky_surf = pygame.image.load("graphics/Sky.png").convert()
# ground_surf = pygame.image.load("graphics/ground.png").convert()

# # obstacles
# snail_surf = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
# fly_surf = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()

# obstacle_rect_list = []

# # player
# player_surf = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
# player_rect = player_surf.get_rect(midbottom = (80, 300))
# player_gravity = 0

# # game over
# game_name = text_font.render("Pixel Runner", False, (111, 196, 169))
# game_name_rect = game_name.get_rect(center = (400, 80)) 

# player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
# player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
# player_stand_rect = player_stand.get_rect(center = (400, 200))

# game_message = text_font.render("Press space to play", False, (111, 196, 169))
# game_message_rect = game_message.get_rect(center = (400, 330))

# # timer
# obstacle_timer = pygame.USEREVENT + 1
# pygame.time.set_timer(obstacle_timer, 1500)

# while True:
#   for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#       pygame.quit()
#       exit()
#     if game_active:
#       if event.type == pygame.MOUSEBUTTONDOWN:
#         if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
#           player_gravity = -20
#       if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
#           player_gravity = -20
#       if event.type == obstacle_timer:
#         if randint(0, 2):
#           obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100), 300)))
#         else:
#           obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100), 210)))
#     else:
#       if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#         game_active = True
#         start_time = pygame.time.get_ticks()

#   if game_active:
#     screen.blit(sky_surf, (0, 0))
#     screen.blit(ground_surf, (0, 300))
#     # pygame.draw.rect(screen, "#c0e8cf", score_rect)
#     # pygame.draw.rect(screen, "#c0e8cf", score_rect, 10)
#     # screen.blit(score_surf, score_rect)
#     score = display_score()

#     # obstacle movement
#     obstacle_rect_list = obstacle_movement(obstacle_rect_list)

#     # player
#     player_gravity += 1
#     player_rect.bottom += player_gravity
#     if player_rect.bottom >= 300: player_rect.bottom = 300
#     screen.blit(player_surf, player_rect)

#     # collision
#     game_active = collisions(player_rect, obstacle_rect_list)

#   else:
#     screen.fill((94, 129, 162))
#     screen.blit(game_name, game_name_rect)
#     screen.blit(player_stand, player_stand_rect)

#     obstacle_rect_list.clear()
#     player_rect.midbottom = (80, 300)
#     player_gravity = 0

#     score_message = text_font.render(f"Your score: {score}", False, (111, 196, 169))
#     score_message_rect = score_message.get_rect(center = (400, 330))

#     if score: screen.blit(score_message, score_message_rect)
#     else: screen.blit(game_message, game_message_rect)
  
#   pygame.display.update()
#   clock.tick(60)






















# import pygame
# from sys import exit

# def display_score():
#   current_time = int((pygame.time.get_ticks() - start_time) / 1000)
#   score_surf = text_font.render(f'Score: {current_time}', False, (64, 64, 64))
#   score_rect = score_surf.get_rect(center = (400, 50))
#   screen.blit(score_surf, score_rect)

# pygame.init()
# screen = pygame.display.set_mode((800, 400))
# pygame.display.set_caption("Runner")
# clock = pygame.time.Clock()
# text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
# game_active = False
# start_time = 0

# sky_surf = pygame.image.load("graphics/Sky.png").convert()
# ground_surf = pygame.image.load("graphics/ground.png").convert()

# # score_surf = text_font.render("Score : 0", False, (64, 64, 64))
# # score_rect = score_surf.get_rect(center = (400, 50))

# snail_surf = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
# snail_rect = snail_surf.get_rect(bottomright = (600, 300))

# # player
# player_surf = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
# player_rect = player_surf.get_rect(midbottom = (80, 300))
# player_gravity = 0

# # game over
# game_over_surf = text_font.render("press to play", False, "white")
# game_over_rect = game_over_surf.get_rect(center = (400, 300))

# while True:
#   for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#       pygame.quit()
#       exit()
#     if game_active:
#       if event.type == pygame.MOUSEBUTTONDOWN:
#         if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
#           player_gravity = -20
#       if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
#           player_gravity = -20
#     else:
#       if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#         game_active = True
#         snail_rect.left = 800
#         start_time = pygame.time.get_ticks()

#   if game_active:
#     screen.blit(sky_surf, (0, 0))
#     screen.blit(ground_surf, (0, 300))
#     # pygame.draw.rect(screen, "#c0e8cf", score_rect)
#     # pygame.draw.rect(screen, "#c0e8cf", score_rect, 10)
#     # screen.blit(score_surf, score_rect)
#     display_score()

#     snail_rect.x -= 4
#     if snail_rect.right <= 0: snail_rect.left = 800
#     screen.blit(snail_surf, snail_rect)

#     # player
#     player_gravity += 1
#     player_rect.bottom += player_gravity
#     if player_rect.bottom >= 300: player_rect.bottom = 300
#     screen.blit(player_surf, player_rect)

#     # collision
#     if player_rect.colliderect(snail_rect):
#       game_active = False

#   else:
#     screen.fill((94, 129, 162))
#     screen.blit(player_surf, player_surf.get_rect(center = (400, 200)) )
#     screen.blit(game_over_surf, game_over_rect)
  
#   pygame.display.update()
#   clock.tick(60)













# import pygame
# from sys import exit

# pygame.init()
# screen = pygame.display.set_mode((800, 400))
# pygame.display.set_caption("Runner")
# clock = pygame.time.Clock()
# text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
# game_active = True


# sky_surface = pygame.image.load("graphics/Sky.png").convert()
# ground_surface = pygame.image.load("graphics/ground.png").convert()

# score_num = 0
# score_surf = text_font.render("My game", False, (64, 64, 64))
# score_rect = score_surf.get_rect(center = (400, 50))

# # asset
# snail_surf = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
# snail_rect = snail_surf.get_rect(bottomright = (600, 300))

# #player
# player_surf = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
# player_rect = player_surf.get_rect(midbottom = (80, 300))
# player_gravity = 0

# # game over
# game_over_surf = text_font.render("Game Over", False, "white")
# game_over_rect = game_over_surf.get_rect(center = (400, 200))

# while True:
#   for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#       pygame.quit()
#       exit()
#     if game_active:
#       if event.type == pygame.MOUSEBUTTONDOWN:
#         if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
#           player_gravity = -20
#       if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
#           player_gravity = -20
#     else:
#       if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#         game_active = True
#         snail_rect.left = 800

#   if game_active:
#     screen.blit(sky_surface, (0, 0))
#     screen.blit(ground_surface, (0, 300))
#     pygame.draw.rect(screen, "#c0e8ec", score_rect)
#     pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
#     screen.blit(score_surf, score_rect)

#     snail_rect.x -= 4
#     if snail_rect.right <= 0: snail_rect.left = 800
#     screen.blit(snail_surf, snail_rect)

#     # player
#     player_gravity += 1
#     player_rect.y += player_gravity
#     if player_rect.bottom >= 300: player_rect.bottom = 300
#     screen.blit(player_surf, player_rect)

#     # collision
#     if snail_rect.colliderect(player_rect):
#       game_active = False
#   else:
#     screen.fill("black")
#     screen.blit(game_over_surf, game_over_rect)
    

#   pygame.display.update()
#   clock.tick(60)






















# import pygame
# from sys import exit

# pygame.init()
# screen = pygame.display.set_mode((800, 400))
# pygame.display.set_caption("Runner")
# clock = pygame.time.Clock()
# text_font = pygame.font.Font('font/pixeltype.ttf', 50)

# sky_surface = pygame.image.load('graphics/Sky.png').convert()
# ground_surface = pygame.image.load('graphics/ground.png').convert()
# text_surface = text_font.render("My game", False, 'black')

# snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
# snail_rectangle = snail_surface.get_rect(bottomright = (600, 300))

# player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
# player_rectangle = player_surface.get_rect(midbottom = (80, 300))

# while True:
#   for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#       pygame.quit()
#       exit()
#     # if event.type == pygame.MOUSEMOTION:
#     #   if player_rectangle.collidepoint(event.pos): print("collision")

#   screen.blit(sky_surface, (0, 0))
#   screen.blit(ground_surface, (0, 300))
#   screen.blit(text_surface, (300, 50))

#   snail_rectangle.x -= 4
#   if snail_rectangle.right <= 0: snail_rectangle.left = 800
#   screen.blit(snail_surface, snail_rectangle)
#   screen.blit(player_surface, player_rectangle)

#   # if player_rectangle.colliderect(snail_rectangle):
#   #   print("collision")

#   # mouse_position = pygame.mouse.get_pos()
#   # if player_rectangle.collidepoint(mouse_position):
#   #   print("collision")

#   pygame.display.update()
#   clock.tick(60)














# import pygame
# from sys import exit

# pygame.init()
# screen = pygame.display.set_mode((800, 400))
# pygame.display.set_caption("Runner")
# clock = pygame.time.Clock()

# # test_surface = pygame.Surface((100, 200))
# # test_surface.fill((123, 223, 121))
# test_font = pygame.font.Font('font/Pixeltype.ttf', 60)

# sky_surface = pygame.image.load('graphics/Sky.png')
# ground_surface = pygame.image.load('graphics/ground.png')
# text_surface = test_font.render('My game', False, 'green')

# while True:
#   for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#       pygame.quit()
#       exit()

#   screen.blit(sky_surface, (0,0))
#   screen.blit(ground_surface, (0, 300))
#   screen.blit(text_surface, (300, 50))

#   pygame.display.update()
#   clock.tick(60)