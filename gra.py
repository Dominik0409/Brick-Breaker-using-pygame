import pygame, random
from menu import MainMenu,OptionsMenu
from grakulka import Game

class Gra():
    def __init__(self):
        pygame.init()
        self.FPS = 15
        self.running, self.kulka_playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY= False, False, False, False, False, False
        self.DIS_W, self.DIS_H = 1280, 720
        self.display = pygame.Surface((self.DIS_W,self.DIS_H))
        self.window = pygame.display.set_mode((self.DIS_W,self.DIS_H),pygame.FULLSCREEN)
        self.font = 'resources/Font1.ttf'
        self.BLACK, self.WHITE, self.PURPLE = (0,0,0) , (255,255,255) , (119,65,235)
        self.mainmenu = MainMenu(self)
        self.optionsmenu = OptionsMenu(self)
        self.curr_menu = self.mainmenu
        
    def game_loop(self):
        if self.kulka_playing:
            self.GraKulka = Game(self)
            self.GraKulka.running = True
            self.GraKulka.run()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY =  True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY =  True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY =  True
                    
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY= False, False, False, False, False, False
        
    def draw_text(self, text, size, x, y, color):
        font_1 = pygame.font.Font(self.font, size)
        text_surface_1 = font_1.render(text, True, color)
        text_rect_1 = text_surface_1.get_rect()
        text_rect_1.topleft = (x,y)
        self.display.blit(text_surface_1,text_rect_1)
        self.window.blit(text_surface_1,text_rect_1)
