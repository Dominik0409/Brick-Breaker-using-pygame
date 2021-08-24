import pygame
import gra

class Menu():
    def __init__(self, gra):
        self.gra = gra
        self.mid_w, self.mid_h = self.gra.DIS_W/2, self.gra.DIS_H/2
        self.run_display = True
                
    def blit_screen(self):
        self.gra.window.blit(self.gra.display, (0,0))
        pygame.display.update()
        self.gra.reset_keys()
     
class MainMenu(Menu):
    def __init__(self,gra):
        Menu.__init__(self, gra)
        self.state = "Play"
        self.bg = pygame.image.load("resources/menubg.png").convert()
        self.bg = pygame.transform.scale(self.bg,(1280,720))
        self.gra.window.blit(self.bg,(0,0))
        self.Playx, self.Playy = 350, 250
        self.Optionsx, self.Optionsy = self.Playx, self.Playy + 65
        self.Exitx, self.Exity = self.Playx, self.Playy + 130
        
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.gra.check_events()
            self.check_input()
            self.gra.display.blit(self.bg,(0,0))
            self.gra.draw_text('BRICK BREAKER', 100, 300, 100, self.gra.WHITE)
            self.gra.draw_text('Play', 60, self.Playx,self.Playy, self.gra.WHITE)
            self.gra.draw_text('Options', 60, self.Optionsx,self.Optionsy, self.gra.WHITE)
            self.gra.draw_text('Exit', 60, self.Exitx,self.Exity, self.gra.WHITE)
            if self.state == 'Play': self.gra.draw_text('Play', 60, self.Playx,self.Playy, self.gra.BLACK)
            elif  self.state == 'Options': self.gra.draw_text('Options', 60, self.Optionsx,self.Optionsy, self.gra.BLACK)
            elif  self.state == 'Exit': self.gra.draw_text('Exit', 60, self.Exitx,self.Exity, self.gra.BLACK)

            self.blit_screen()
# ruch kursora po menu            
    def move_cursor(self):
        if self.gra.DOWN_KEY:
            if self.state == 'Play':
                self.state = 'Options'
            elif self.state == 'Options':
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.state = 'Play'
        
        elif self.gra.UP_KEY:
            if self.state == 'Play':
                self.state = 'Exit'
            elif self.state == 'Options':
                self.state = 'Play'
            elif self.state == 'Exit':
                self.state = 'Options'           
    def check_input(self):
        self.move_cursor()
        if self.gra.START_KEY:
            if self.state == 'Play':
                self.gra.kulka_playing = True
            elif self.state == 'Options':
                self.gra.curr_menu = self.gra.optionsmenu
            elif self.state == 'Exit':
                pygame.quit()
            self.run_display = False
            
class OptionsMenu(Menu):
    def __init__(self,gra):
        Menu.__init__(self, gra)
        self.bg = pygame.image.load("resources/menubg.png").convert()
        self.bg = pygame.transform.scale(self.bg,(1280,720))
        self.state = "difficulty"
        self.state_dif = 'Easy'
        self.state_m = 'On'
        self.difficultyx, self.difficultyy = 150, 200
        self.Musicx, self.Musicy = self.difficultyx, self.difficultyy + 40
        self.Exitx, self.Exity = self.difficultyx, self.difficultyy + 80
        
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.gra.check_events()
            self.check_input()
            self.gra.display.blit(self.bg,(0,0))
            self.gra.draw_text('OPTIONS', 70, 150, 100, self.gra.WHITE)
            self.gra.draw_text('Difficulty', 40, self.difficultyx,self.difficultyy, self.gra.WHITE)
            self.gra.draw_text('Music', 40, self.Musicx,self.Musicy, self.gra.WHITE)
            self.gra.draw_text('Back', 40, self.Exitx,self.Exity, self.gra.WHITE)
            self.gra.draw_text(f'-   {self.state_dif}', 40, self.difficultyx + 240,self.difficultyy, self.gra.WHITE)
            self.gra.draw_text(f'-   {self.state_m}', 40, self.Musicx + 240,self.Musicy, self.gra.WHITE)
            if self.state == 'difficulty': self.gra.draw_text('Difficulty', 40, self.difficultyx,self.difficultyy, self.gra.BLACK)
            elif  self.state == 'Music': self.gra.draw_text('Music', 40, self.Musicx,self.Musicy, self.gra.BLACK)
            elif  self.state == 'Exit': self.gra.draw_text('Back', 40, self.Exitx,self.Exity, self.gra.BLACK)
            self.blit_screen()
           
    def move_cursor(self):
        if self.gra.DOWN_KEY:
            if self.state == 'difficulty':
                self.state = 'Music'
            elif self.state == 'Music':
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.state = 'difficulty'
        
        elif self.gra.UP_KEY:
            if self.state == 'difficulty':
                self.state = 'Exit'
            elif self.state == 'Music':
                self.state = 'difficulty'
            elif self.state == 'Exit':
                self.state = 'Music'
                
        elif self.gra.LEFT_KEY:
            if self.state == 'difficulty':
                if self.state_dif == 'Easy':
                    self.state_dif = 'Hard'
                elif self.state_dif == 'Hard':
                    self.state_dif = 'Medium'
                elif self.state_dif == 'Medium':
                    self.state_dif = 'Easy'
            elif self.state == 'Music':
                if self.state_m == 'On':
                    self.state_m = 'Off'
                elif self.state_m == 'Off':
                    self.state_m = 'On'
                
        elif self.gra.RIGHT_KEY:
            if self.state == 'difficulty':
                if self.state_dif == 'Easy':
                    self.state_dif = 'Medium'
                elif self.state_dif == 'Medium':
                    self.state_dif = 'Hard'
                elif self.state_dif == 'Hard':
                    self.state_dif = 'Easy'
            elif self.state == 'Music':
                if self.state_m == 'Off':
                    self.state_m = 'On'
                elif self.state_m == 'On':
                    self.state_m = 'Off'
                
    def check_input(self):
        self.move_cursor()
        if self.gra.START_KEY:
            if self.state == 'difficulty':
                pass
            elif self.state == 'Music':
                pass
            elif self.state == 'Exit':
                self.gra.curr_menu = self.gra.mainmenu
            self.run_display = False