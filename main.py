import pygame
from sys import exit
from random import choice
from player import Player
from obstacle import Obstacle
from difficulties import DifficultyMenu
from inputbox import InputBox
from button import Button
import cv2
import cv2.aruco as aruco
import numpy as np

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
parameters = aruco.DetectorParameters()
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = cv2.aruco.ArucoDetector(dictionary, parameters)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen_height = 400
        self.screen_width = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)
        self.running = True
        self.game_active = False
        self.start_time = 0
        self.score = 0
        self.play_music()
        self.set_player()
        self.obstacle_group = pygame.sprite.Group()
        self.load_background()
        # Difficulty Menu at first time
        # self.difficulty_menu = DifficultyMenu()
        # self.difficulty_menu.run()
        # self.mode = self.difficulty_menu.run()
        self.mode = "normal"
        self.ez_mode = 6000
        self.normal_mode = 4000
        self.hard_mode = 2000
        self.first_screen_pass = False
        pygame.display.set_caption('GEGE Runner')
        self.set_intro_screen()
        self.obstacle_timer = pygame.USEREVENT + 1
        self.input_box = InputBox(400-100, 100-10, 140, 30)
        self.f_input_box = InputBox(400-100, 140, 185, 30)

        pygame.time.set_timer(self.obstacle_timer,2000)

        self.easy_img = pygame.image.load('./easy.png').convert_alpha()
        self.nor_img = pygame.image.load('./normal.png').convert_alpha()
        self.chal_img = pygame.image.load('./chal.png').convert_alpha()
        self.ez_btn = Button(0,0,self.easy_img,0.5)
        self.normal_btn = Button(0,60,self.nor_img,0.5)
        self.hard_btn = Button(0,120,self.chal_img,0.5)
        self.resetjump = True
        self.player_y = 999999
        
        

    def play_music(self):
        self.bg_music = pygame.mixer.Sound('./audio/music.wav')
        self.bg_music.play(loops = -1)

    def set_player(self):
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

    def load_background(self):
        self.sky_surface = pygame.image.load('./graphics/Sky.png').convert()
        self.ground_surface = pygame.image.load('./graphics/ground.png').convert()

    def set_intro_screen(self):
        # Game's name
        self.game_name = self.test_font.render('GEGE Runner',False,(0,0,0))
        self.game_name_rect = self.game_name.get_rect(center = (400,80))
        # Player stand in the middle
        self.player_stand = pygame.image.load('./graphics/Player/herobrine.png').convert_alpha()
        self.player_stand = pygame.transform.rotozoom(self.player_stand,0,2)
        self.player_stand_rect = self.player_stand.get_rect(center = (400,200))
        # Message: Spacebar to run
        self.game_message = self.test_font.render('Press space bar to run',False,(111,196,169))
        self.game_message_rect = self.game_message.get_rect(center = (400,330))

    def display_score(self):
        self.current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        self.score_surf = self.test_font.render(f'Score: {self.current_time}',False,(64,64,64))
        self.score_rect = self.score_surf.get_rect(center = (400,50))
        self.screen.blit(self.score_surf, self.score_rect)
        return self.current_time
    
    def collision_sprite(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False):
            self.obstacle_group.empty()
            return False
        else: return True

    def intro_screen(self):
        self.bg_img = pygame.image.load('./graphics/intro_bg_2.png').convert()
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(self.player_stand, self.player_stand_rect)
        self.score_message = self.test_font.render(f'Your score: {self.score}',False,(0,0,0))
        self.mode_message = self.test_font.render(f'Your mode: {self.mode}',False,(0,0,0))
        self.score_message_rect = self.score_message.get_rect(center = (400,330))
        self.mode_message_rect = self.mode_message.get_rect(center = (400,360))
        self.screen.blit(self.game_name, self.game_name_rect)
        self.input_box.draw(self.screen)
        if self.ez_btn.draw(self.screen):
            pygame.time.set_timer(self.obstacle_timer, self.ez_mode )
            print("easy")
            self.mode = "easy"
        if self.normal_btn.draw(self.screen):
            pygame.time.set_timer(self.obstacle_timer, self.normal_mode)
            print("normal")
            self.mode = "normal"
        if self.hard_btn.draw(self.screen):
            pygame.time.set_timer(self.obstacle_timer, self.hard_mode)
            print("challenge")
            self.mode = "challenge"

        if self.score == 0 and self.first_screen_pass:
            self.first_intro()
        else:
            self.screen.blit(self.score_message, self.score_message_rect)
            self.screen.blit(self.mode_message, self.mode_message_rect)
            self.player.remove()
            self.player.add(Player())

    def first_intro(self):
        self.first_bg = pygame.image.load('./graphics/introBg2.png').convert()
        self.ezy_btn = Button(self.screen_width / 2 - 100, 180,self.easy_img,0.5)
        self.nor_btn = Button(self.screen_width / 2 - 100, 250,self.nor_img,0.5)
        self.hrd_btn = Button(self.screen_width / 2 - 100, 320,self.chal_img,0.5)
        self.screen.blit(self.first_bg, (0, 0))
        self.f_input_box.draw(self.screen)
        if self.ezy_btn.draw(self.screen):
            pygame.time.set_timer(self.obstacle_timer, self.ez_mode)
            print("easy")
            self.mode = "easy"
            self.first_screen_pass = True
        if self.nor_btn.draw(self.screen):
            pygame.time.set_timer(self.obstacle_timer, self.normal_mode)
            print("normal")
            self.mode = "normal"
            self.first_screen_pass = True
        if self.hrd_btn.draw(self.screen):
            pygame.time.set_timer(self.obstacle_timer, self.hard_mode)
            print("challenge")
            self.mode = "challenge"
            self.first_screen_pass = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                self.input_box.handle_event(event)
                self.input_box.update()
                self.f_input_box.handle_event(event)
                self.f_input_box.update()
                if event.type == self.obstacle_timer and self.game_active:
                    self.obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
                if not self.game_active and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.game_active = True
                    self.start_time = int(pygame.time.get_ticks() / 1000)
                    self.player.add(Player())  # Reset player
                    self.obstacle_group.empty()  # Clear obstacles


            if self.game_active:
                # Screen
                self.screen.blit(self.sky_surface,(0,0))
                self.screen.blit(self.ground_surface,(0,300))
                self.score = self.display_score()
                # Play
                ret, frame = cap.read()
                image = frame
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                detector = cv2.aruco.ArucoDetector(dictionary, parameters)
                _, thresholded = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
                corners, ids, rejectedImgPoints = detector.detectMarkers(thresholded)
			        # delta time
                if ids is not None:
                    for i in range(len(ids)):
                        marker_corners = corners[i][0].astype(np.int32)
                        marker_corners = marker_corners.reshape((-1, 1, 2)).astype(np.int32)
                        cv2.polylines(frame, [marker_corners] , True, (0, 255, 0), thickness = 2)
                        self.player_y  = (abs(marker_corners[0][0][1]))
                    cv2.putText(frame, str(marker_corners[0][0][1]), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                cv2.imshow('MediaPipe Pose', frame)    
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
                if self.player_y < 200 :
                    self.resetjump = True
                elif self.player_y >= 400 :
                    self.resetjump = False
                self.player.draw(self.screen)
                self.player.update(self.player_y,self.resetjump)

                # self.player.draw(self.screen)
                # self.player.update()
                # Obstacles
                self.obstacle_group.draw(self.screen)
                self.obstacle_group.update()
                # Check collision
                self.game_active = self.collision_sprite()
            else:
                if self.first_screen_pass:
                    self.intro_screen()
                else:
                    self.first_intro()
                    
            pygame.display.update()
            self.clock.tick(60)

game = Game()
game.run()