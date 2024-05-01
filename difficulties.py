import pygame
import sys
from button import Button

class DifficultyMenu:
    def __init__(self):
        pygame.init()
        # Window size and title
        self.screen_width = 800
        self.screen_height = 400
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Difficulty")
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        # Font
        self.font = pygame.font.Font(None, 36)

        self.selected_option = "Normal"  # Start with Normal

    def draw(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_buttons(self):
        self.easy_img = pygame.image.load('./easy.png').convert_alpha()
        self.nor_img = pygame.image.load('./normal.png').convert_alpha()
        self.chal_img = pygame.image.load('./chal.png').convert_alpha()
        self.easy_button = Button(self.screen_width // 2, 250,self.easy_img,0.5)
        self.normal_button = Button(self.screen_width // 2, 300,self.nor_img,0.5)
        self.challenge_buttom = Button(self.screen_width // 2, 350,self.chal_img,0.5)
    def run(self):
        while True:
            self.screen.fill(self.WHITE)
            self.draw("Choose your difficulty...", self.BLACK, self.screen_width // 2, 100)
            self.draw("Easy", self.BLACK, self.screen_width // 2, 250)
            self.draw("Normal", self.BLACK, self.screen_width // 2, 300)
            self.draw("Hard", self.BLACK, self.screen_width // 2, 350)
            self.draw("->", self.BLACK, self.screen_width // 2 - 100, 250 + (50 * ["Easy", "Normal", "Hard"].index(self.selected_option)))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        # Press "up"
                        if self.selected_option == "Normal":
                            self.selected_option = "Easy"
                        elif self.selected_option == "Hard":
                            self.selected_option = "Normal"
                    elif event.key == pygame.K_DOWN:
                        # Press "down"
                        if self.selected_option == "Normal":
                            self.selected_option = "Hard"
                        elif self.selected_option == "Easy":
                            self.selected_option = "Normal"
                    elif event.key == pygame.K_RETURN:
                        # เลือกระดับความยาก
                        # print("คุณเลือกระดับความยาก:", self.selected_option)
                        return self.selected_option

# if __name__ == "__main__":
#     menu = DifficultyMenu()
#     selected_difficulty = menu.run()
#     print("คุณเลือกระดับความยาก:", selected_difficulty)
