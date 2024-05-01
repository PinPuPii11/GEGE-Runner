import pygame
from random import choice

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.random_skin()
		self.player_index = 0
		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0
		self.jump_sound = pygame.mixer.Sound('./audio/jump.mp3')
		self.jump_sound.set_volume(0.5)

	def player_input(self,y,rj):
		# keys = pygame.key.get_pressed()
		print(y,rj)
		if y < 200 and rj == True and self.rect.bottom == 300:
			self.gravity = -20
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			self.rect.bottom = 300

	def animation_state(self):
		if self.rect.bottom < 300: 
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self,y,rj):
		self.player_input(y,rj)
		self.apply_gravity()
		self.animation_state()

	def random_skin(self):
		skin_type = choice([1, 2, 3])
		# print(skin_type)
		match skin_type:
			case 1:
				player_walk_1 = pygame.image.load('./graphics/Player/player_walk_1.png').convert_alpha()
				player_walk_2 = pygame.image.load('./graphics/Player/player_walk_2.png').convert_alpha()
				self.player_jump = pygame.image.load('./graphics/player/player_walk_1_copy.png').convert_alpha()
			case 2:
				player_walk_1 = pygame.image.load('./graphics/Player/stove_walk_1_zon.png').convert_alpha()
				player_walk_2 = pygame.image.load('./graphics/Player/stove_walk_2_zon.png').convert_alpha()
				self.player_jump = pygame.image.load('./graphics/player/stove_jump_zon.png').convert_alpha()
			case 3:
				player_walk_1 = pygame.image.load('./graphics/Player/art_walk_1_zon.png').convert_alpha()
				player_walk_2 = pygame.image.load('./graphics/Player/art_walk_2_zon.png').convert_alpha()
				self.player_jump = pygame.image.load('./graphics/player/art_jump_zon.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]