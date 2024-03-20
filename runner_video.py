import pygame
from sys import exit
from random import randint, choice
import cv2
import cv2.aruco as aruco
import numpy as np

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')


dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
parameters = aruco.DetectorParameters()
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

player_walk_pic_1 = "/Users/ant/very new junk program/GEGE-Runner/graphics/Player/player_walk_1.png"
player_walk_pic_2 = "/Users/ant/very new junk program/GEGE-Runner/graphics/Player/player_walk_2.png"
player_jump_pic = "/Users/ant/very new junk program/GEGE-Runner/graphics/Player/jump.png"
player_stand_pic = "/Users/ant/very new junk program/GEGE-Runner/graphics/Player/player_stand.png"
jumpmp3 = "/Users/ant/very new junk program/GEGE-Runner/audio/jump.mp3"
fly_pic_1 = "/Users/ant/very new junk program/GEGE-Runner/graphics/Fly/Fly1.png"
fly_pic_2 = "/Users/ant/very new junk program/GEGE-Runner/graphics/Fly/Fly2.png"
snail_pic_1 = "/Users/ant/very new junk program/GEGE-Runner/graphics/snail/snail1.png"
snail_pic_2 = "/Users/ant/very new junk program/GEGE-Runner/graphics/snail/snail2.png"
font_game = "/Users/ant/very new junk program/GEGE-Runner/font/Pixeltype.ttf"
music_game = "/Users/ant/very new junk program/GEGE-Runner/audio/music.wav"
ground_pic = "/Users/ant/very new junk program/GEGE-Runner/graphics/ground.png"
sky_pic = "/Users/ant/very new junk program/GEGE-Runner/graphics/Sky.png"



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

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load(fly_pic_1).convert_alpha()
			fly_2 = pygame.image.load(fly_pic_2).convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 210
		else:
			snail_1 = pygame.image.load(snail_pic_1).convert_alpha()
			snail_2 = pygame.image.load(snail_pic_2).convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = 300

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()


def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def obstacle_movement(obstacle_list):
	if obstacle_list:
		for obstacle_rect in obstacle_list:
			obstacle_rect.x -= 5

			if obstacle_rect.bottom == 300: screen.blit(snail_surf,obstacle_rect)
			else: screen.blit(fly_surf,obstacle_rect)

		obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

		return obstacle_list
	else: return []

def collisions(player,obstacles):
	if obstacles:
		for obstacle_rect in obstacles:
			if player.colliderect(obstacle_rect): return False
	return True

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True

def player_animation():
	global player_surf, player_index

	if player_rect.bottom < 300:
		player_surf = player_jump
	else:
		player_index += 0.1
		if player_index >= len(player_walk):player_index = 0
		player_surf = player_walk[int(player_index)]
class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = test_font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = test_font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)



pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('GEGE Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font(font_game, 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound(music_game)
bg_music.play(loops = -1)
input_box1 = InputBox(400-100, 100-10, 140, 30)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load(sky_pic).convert()
ground_surface = pygame.image.load(ground_pic).convert()

# score_surf = test_font.render('My game', False, (64,64,64))
# score_rect = score_surf.get_rect(center = (400,50))

# Snail 
snail_frame_1 = pygame.image.load(snail_pic_1).convert_alpha()
snail_frame_2 = pygame.image.load(snail_pic_2).convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame1 = pygame.image.load(fly_pic_1).convert_alpha()
fly_frame2 = pygame.image.load(fly_pic_2).convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []


player_walk_1 = pygame.image.load(player_walk_pic_1).convert_alpha()
player_walk_2 = pygame.image.load(player_walk_pic_2).convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load(player_jump_pic).convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load(player_stand_pic).convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('GEGE Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space bar to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)
resetjump = True
player_y = 99999


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		input_box1.handle_event(event)
		input_box1.update()
		if game_active:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300: 
					player_gravity = -20
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
					player_gravity = -20
		else:
			
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				
				start_time = int(pygame.time.get_ticks() / 1000)
				

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
				# if randint(0,2):
				# 	obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
				# else:
				# 	obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210)))

			if event.type == snail_animation_timer:
				if snail_frame_index == 0: snail_frame_index = 1
				else: snail_frame_index = 0
				snail_surf = snail_frames[snail_frame_index] 

			if event.type == fly_animation_timer:
				if fly_frame_index == 0: fly_frame_index = 1
				else: fly_frame_index = 0
				fly_surf = fly_frames[fly_frame_index] 


	if game_active:
		screen.blit(sky_surface,(0,0))
		screen.blit(ground_surface,(0,300))
		# pygame.draw.rect(screen,'#c0e8ec',score_rect)
		# pygame.draw.rect(screen,'#c0e8ec',score_rect,10)
		# screen.blit(score_surf,score_rect)
		score = display_score()
		
		# snail_rect.x -= 4
		# if snail_rect.right <= 0: snail_rect.left = 800
		# screen.blit(snail_surf,snail_rect)

		# Player 
		# player_gravity += 1
		# player_rect.y += player_gravity
		# if player_rect.bottom >= 300: player_rect.bottom = 300
		# player_animation()
		# screen.blit(player_surf,player_rect)
		ret, frame = cap.read()
		image = frame
		gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		detector = cv2.aruco.ArucoDetector(dictionary, parameters)
		_, thresholded = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
		corners, ids, rejectedImgPoints = detector.detectMarkers(thresholded)
			# delta time
		if ids is not None:
       		 # Loop through each dextected marker
			for i in range(len(ids)):
            		# Extract the corners of the marker
				marker_corners = corners[i][0].astype(np.int32)
            		# Reshape the marker corners to match the expected format
				marker_corners = marker_corners.reshape((-1, 1, 2)).astype(np.int32)
				cv2.polylines(frame, [marker_corners] , True, (0, 255, 0), thickness = 2)
				player_y  = (abs(marker_corners[0][0][1]))
			cv2.putText(frame, str(marker_corners[0][0][1]), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
			
		cv2.imshow('MediaPipe Pose', frame)    
		if cv2.waitKey(10) & 0xFF == ord('q'):
			break
		if player_y < 200 :
			resetjump = True
		elif player_y >= 400 :
			resetjump = False
		player.draw(screen)
		player.update(player_y,resetjump)
		obstacle_group.draw(screen)
		obstacle_group.update()

		# Obstacle movement 
		# obstacle_rect_list = obstacle_movement(obstacle_rect_list)

		# collision 
		game_active = collision_sprite()
		# game_active = collisions(player_rect,obstacle_rect_list)
		
	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)
		obstacle_rect_list.clear()
		player_rect.midbottom = (80,300)
		player_gravity = 0

		score_surf = test_font.render('Enter name: ',False,(64,64,64))
		score_rect = score_surf.get_rect(center = (210,107))
		screen.blit(score_surf,score_rect)

		input_box1.draw(screen)

		name_surf = test_font.render(f'Name: {input_box1.text}',False,(64,64,64))
		name_rect = name_surf.get_rect(center = (400,50))
		screen.blit(name_surf,name_rect)
	
		score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)
	pygame.display.update()
	clock.tick(60)