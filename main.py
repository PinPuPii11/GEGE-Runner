import pygame
from sys import exit
from random import choice
from player import Player
from obstacle import Obstacle

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800,400))
        pygame.display.set_caption('GEGE Runner')
        self.clock = pygame.time.Clock()
        self.running = True
        self.test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)
        self.game_active = True
        self.start_time = 0
        self.score = 0
        self.play_music()
        self.set_player()
        self.obstacle_group = pygame.sprite.Group()
        self.set_background()
        self.set_intro_screen()
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer,1500)

    def play_music(self):
        self.bg_music = pygame.mixer.Sound('./audio/music.wav')
        self.bg_music.play(loops = -1)

    def set_player(self):
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

    def set_background(self):
        self.sky_surface = pygame.image.load('./graphics/Sky.png').convert()
        self.ground_surface = pygame.image.load('./graphics/ground.png').convert()

    def set_intro_screen(self):
        # Game's name
        self.game_name = self.test_font.render('GEGE Runner',False,(111,196,169))
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

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
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
                self.player.draw(self.screen)
                self.player.update()
                # Obstacles
                self.obstacle_group.draw(self.screen)
                self.obstacle_group.update()
                # Check collision
                self.game_active = self.collision_sprite()
            else:
                self.screen.fill((94,129,162))
                self.screen.blit(self.player_stand, self.player_stand_rect)
                self.score_message = self.test_font.render(f'Your score: {self.score}',False,(111,196,169))
                self.score_message_rect = self.score_message.get_rect(center = (400,330))
                self.screen.blit(self.game_name, self.game_name_rect)
                if self.score == 0: self.screen.blit(self.game_message, self.game_message_rect)
                else:
                    self.screen.blit(self.score_message, self.score_message_rect)
                    self.player.remove()
                    self.player.add(Player())
            pygame.display.update()
            self.clock.tick(60)

game = Game()
game.run()