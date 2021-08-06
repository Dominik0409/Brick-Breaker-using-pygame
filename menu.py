import pygame

class Menu():
    def __init__(self, gra):
        self.gra = gra
        self.mid_w, self.mid_h = self.gra.DIS_W/2, self.gra.DIS_H/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.offset = -40
        
    def draw_cursor(self):
        self.gra.draw_text('*', 40, self.cursor_rect.x, self.cursor_rect.y, self.gra.PURPLE)
        
    def blit_screen(self):
        self.gra.window.blit(self.gra.display, (0,0))
        pygame.display.update()
        self.gra.reset_keys()
#klasa menu glownego        
class MainMenu(Menu):
    def __init__(self,gra):
        Menu.__init__(self, gra)
        self.state = "Kulka"
        self.kulkax, self.kulkay = 150, 200
        self.opcjex, self.opcjey = self.kulkax, self.kulkay + 40
        self.Wyjsciex, self.Wyjsciey = self.kulkax, self.kulkay + 80
        self.cursor_rect.midtop = (self.kulkax + self.offset, self.kulkay)
        
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.gra.check_events()
            self.check_input()
            self.gra.display.fill(self.gra.BLACK)
            self.gra.draw_text('Gra w Kulke', 70, 100, 100, self.gra.PURPLE)
            self.gra.draw_text('Graj', 40, self.kulkax,self.kulkay, self.gra.PURPLE)
            self.gra.draw_text('Opcje', 40, self.opcjex,self.opcjey, self.gra.PURPLE)
            self.gra.draw_text('Wyjscie', 40, self.Wyjsciex,self.Wyjsciey, self.gra.PURPLE)
            self.draw_cursor()
            self.blit_screen()
# ruch kursora po menu            
    def move_cursor(self):
        if self.gra.DOWN_KEY:
            if self.state == 'Kulka':
                self.cursor_rect.midtop= (self.opcjex + self.offset, self. opcjey)
                self.state = 'Opcje'
            elif self.state == 'Opcje':
                self.cursor_rect.midtop= (self.Wyjsciex + self.offset, self. Wyjsciey)
                self.state = 'Wyjscie'
            elif self.state == 'Wyjscie':
                self.cursor_rect.midtop= (self.kulkax + self.offset, self. kulkay)
                self.state = 'Kulka'
        
        elif self.gra.UP_KEY:
            if self.state == 'Kulka':
                self.cursor_rect.midtop= (self.Wyjsciex + self.offset, self. Wyjsciey)
                self.state = 'Wyjscie'
            elif self.state == 'Opcje':
                self.cursor_rect.midtop= (self.kulkax + self.offset, self. kulkay)
                self.state = 'Kulka'
            elif self.state == 'Wyjscie':
                self.cursor_rect.midtop= (self.opcjex + self.offset, self. opcjey)
                self.state = 'Opcje'
# wcisniecie klawisza enter powoduje wybranie gry             
    def check_input(self):
        self.move_cursor()
        if self.gra.START_KEY:
            if self.state == 'Kulka':
                self.gra.kulka_playing = True
            elif self.state == 'Opcje':
                pass
            elif self.state == 'Wyjscie':
                pygame.quit()
            self.run_display = False