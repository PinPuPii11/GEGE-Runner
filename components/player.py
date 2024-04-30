import pygame

player_walk_pic_1 = "graphics/Player/player_walk_1.png"
player_walk_pic_2 = "graphics/Player/player_walk_2.png"
player_jump_pic = "graphics/Player/jump.png"
player_stand_pic = "graphics/Player/player_stand.png"
jumpmp3 = "audio/jump.mp3"

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load(player_walk_pic_1).convert_alpha()
		player_walk_2 = pygame.image.load(player_walk_pic_2).convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0
		self.player_jump = pygame.image.load(player_jump_pic).convert_alpha()

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound(jumpmp3)
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