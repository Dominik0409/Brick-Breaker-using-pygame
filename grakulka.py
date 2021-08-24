import pygame, sys, random, math
import data
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)

Data = [data.lvl1,data.lvl2,data.lvl3,data.lvl4,data.lvl5]

class Level():
    def __init__(self, data, screen):
        self.tile_list_green = []
        self.tile_list_blue = []
        self.tile_list_red = []
        self.tile_list_in = []
        self.screen = screen
        self.klocekg_png = pygame.image.load('resources/klocek_green.png')
        self.klocekg_png = pygame.transform.scale(self.klocekg_png,(80,30))
        self.klocekb_png = pygame.image.load('resources/klocek.png')
        self.klocekb_png = pygame.transform.scale(self.klocekb_png,(80,30))
        self.klocekr_png = pygame.image.load('resources/klocek_red.png')
        self.klocekr_png = pygame.transform.scale(self.klocekr_png,(80,30))
        self.klocekin_png = pygame.image.load('resources/inbrick.png')
        
        row_count = 0
        
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    rect = pygame.Rect(col_count * 80 +160,row_count * 30,80,30)
                    self.tile_list_green.append(rect)
                if tile == 2:
                    rect = pygame.Rect(col_count * 80 +160,row_count * 30,80,30)
                    self.tile_list_blue.append(rect)
                if tile == 3:
                    rect = pygame.Rect(col_count * 80 +160,row_count * 30,80,30)
                    self.tile_list_red.append(rect)
                if tile == 4:
                    rect = pygame.Rect(col_count * 80 +160,row_count * 30,80,30)
                    self.tile_list_in.append(rect)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list_green:
            self.screen.blit(self.klocekg_png, tile)
        for tile in self.tile_list_blue:
            self.screen.blit(self.klocekb_png, tile)
        for tile in self.tile_list_red:
            self.screen.blit(self.klocekr_png, tile)
        for tile in self.tile_list_in:
            self.screen.blit(self.klocekin_png, tile)
            
class Game():
    def __init__(self, gra):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.gra = gra
        self.player = pygame.Rect(self.gra.DIS_W/2 -70, self.gra.DIS_H - 70,140,20)
        self.ball = pygame.Rect(self.player.x + 55,self.player.y-20,30,30)
        self.bonus = []
        self.extra_life = []
        self.level_index = 0
        self.level = Level(Data[self.level_index],self.gra.window)
        self.clock = pygame.time.Clock()
        self.ball_speed_x = 0
        self.ball_speed_y = 0
        self.player_speed = 0
        pygame.mixer.init()
        if self.gra.optionsmenu.state_dif == 'Easy':
            self.lives = 4
            self.speed_multiplier = 0.8
        elif self.gra.optionsmenu.state_dif == 'Medium':
            self.lives = 3
            self.speed_multiplier = 1
        elif self.gra.optionsmenu.state_dif == 'Hard':  
            self.lives = 2
            self.speed_multiplier = 1.3
        self.initial_speed = 7
        self.initial_speed *= self.speed_multiplier
        self.running = True
        self.pause = False
        self.isbig = False
        self.ball_in_motion = False
        self.player_png = pygame.image.load("resources/platforma.png").convert()
        self.bg_png = pygame.image.load("resources/newbg.png").convert()
        self.bg_png = pygame.transform.scale(self.bg_png,(1280,720))
        self.ball_png1 = pygame.image.load("resources/kulka.png").convert_alpha()
        self.ball_png2 = pygame.image.load("resources/kulka2.png").convert_alpha()
        self.bonus_png = pygame.image.load("resources/plus.png").convert_alpha()
        self.trace1 = pygame.image.load("resources/trace1.png").convert_alpha()
        self.trace2 = pygame.image.load("resources/trace2.png").convert_alpha()
        self.trace3 = pygame.image.load("resources/trace3.png").convert_alpha()
        self.des1 = pygame.image.load("resources/desg1.png").convert_alpha()
        self.des2 = pygame.image.load("resources/desg2.png").convert_alpha()
        self.des3 = pygame.image.load("resources/desg3.png").convert_alpha()
        self.des4 = pygame.image.load("resources/desg4.png").convert_alpha()
        self.des5 = pygame.image.load("resources/desg5.png").convert_alpha()
        self.des6 = pygame.image.load("resources/desg6.png").convert_alpha()
        self.des7 = pygame.image.load("resources/desg7.png").convert_alpha()
        self.des8 = pygame.image.load("resources/desg8.png").convert_alpha()
        self.des9 = pygame.image.load("resources/desg9.png").convert_alpha()
        self.des10 = pygame.image.load("resources/desg10.png").convert_alpha()
        self.des = [self.des1,self.des2,self.des3,self.des4,self.des5,self.des6,self.des7,self.des8,self.des9,self.des10]
        self.heart_png = pygame.image.load("resources/heart.png").convert_alpha()
        self.extra_life_png = pygame.transform.scale(self.heart_png,(20,20))
        self.heart_png = pygame.transform.scale(self.heart_png,(20,20))
        self.animation = []
        self.curr_ball_image = self.ball_png1
        self.bonus_time = 0
        self.score = 0
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.SPACE_KEY, self.LEFT_KEY, self.RIGHT_KEY= False, False, False, False, False, False
        
    def ball_animation(self):
        if not self.ball_in_motion:
            if self.RIGHT_KEY == True:
                self.ball.x += 10
            if self.LEFT_KEY == True:
                self.ball.x -= 10
            if self.ball.left <= 230:
                self.ball.left = 230
            if self.ball.right >= self.gra.DIS_W-230:
                self.ball.right = self.gra.DIS_W-230
        else:    
            self.ball.x += self.ball_speed_x
            self.ball.y += self.ball_speed_y
            
            if self.ball.top < 0:
                self.ball_speed_y *= -1
                self.dzwiek('bounce')
                
            if self.ball.left < 160:
                self.ball.x = 160
                self.ball_speed_x *= -1
                self.dzwiek('bounce')
                
            if self.ball.right > (self.gra.DIS_W-160):
                self.ball.right = self.gra.DIS_W-160
                self.ball_speed_x *= -1
                self.dzwiek('bounce')
                
            if self.ball_speed_x == 0:
                self.ball_speed_x = 0.1 * random.choice((1,-1))
                
            if self.ball.bottom >= self.gra.DIS_H+200:
                self.game_over()
                
            if self.ball.colliderect(self.player):
                collidePoint = self.ball.centerx - (self.player.centerx)
                collidePoint = collidePoint/(self.player.w/2)
                angle = collidePoint * (math.pi/4)
                ball_speed = math.sqrt(self.ball_speed_x*self.ball_speed_x + self.ball_speed_y*self.ball_speed_y)
                self.ball_speed_x = ball_speed * math.sin(angle)
                self.ball_speed_y = - ball_speed * math.cos(angle)
                self.dzwiek('bounce')
                
            if self.ball.collidelist(self.level.tile_list_green) != -1 and self.isbig == False:
                    currtile = self.level.tile_list_green[self.ball.collidelist(self.level.tile_list_green)]
                    if self.chance() == 1:
                        self.bonus_spawn(currtile.centerx, currtile.centery)
                    if self.chance() == 1:
                        self.extra_life_spawn(currtile.centerx, currtile.centery)
                    if abs(self.ball.bottom - currtile.top) < 15 and self.ball_speed_y > 0:
                        self.ball_speed_y *= -1
                    if abs(self.ball.top - currtile.bottom) < 15 and self.ball_speed_y < 0:
                        self.ball_speed_y *= -1
                    if abs(self.ball.right - currtile.left) < 15 and self.ball_speed_x > 0:
                        self.ball_speed_x *= -1
                    if abs(self.ball.left - currtile.right) < 15 and self.ball_speed_x < 0:
                        self.ball_speed_x *= -1
                    
                    self.level.tile_list_green.pop(self.ball.collidelist(self.level.tile_list_green))
                    self.animation.append([0,currtile.x-20,currtile.y+10])
                    self.score += 1
                    self.dzwiek('break')
                    
            if self.ball.collidelist(self.level.tile_list_green) != -1 and self.isbig == True:
                    currtile = self.level.tile_list_green[self.ball.collidelist(self.level.tile_list_green)]
                    if self.chance() == 1:
                        self.bonus_spawn(currtile.centerx, currtile.centery)
                    if self.chance() == 1:
                        self.extra_life_spawn(currtile.centerx, currtile.centery)
                    self.level.tile_list_green.pop(self.ball.collidelist(self.level.tile_list_green))
                    self.score += 1
                    self.dzwiek('break')
                    
            if self.ball.collidelist(self.level.tile_list_blue) != -1 and self.isbig == False:
                    currtile = self.level.tile_list_blue[self.ball.collidelist(self.level.tile_list_blue)]
                    if self.chance() == 1:
                        self.bonus_spawn(currtile.centerx, currtile.centery)
                    if self.chance() == 1:
                        self.extra_life_spawn(currtile.centerx, currtile.centery)
                    self.level.tile_list_green.append(pygame.Rect(self.level.tile_list_blue[self.ball.collidelist(self.level.tile_list_blue)].x, self.level.tile_list_blue[self.ball.collidelist(self.level.tile_list_blue)].y,80,30))
                    if abs(self.ball.bottom - currtile.top) < 15 and self.ball_speed_y > 0:
                        self.ball_speed_y *= -1
                    if abs(self.ball.top - currtile.bottom) < 15 and self.ball_speed_y < 0:
                        self.ball_speed_y *= -1
                    if abs(self.ball.right - currtile.left) < 15 and self.ball_speed_x > 0:
                        self.ball_speed_x *= -1
                    if abs(self.ball.left - currtile.right) < 15 and self.ball_speed_x < 0:
                        self.ball_speed_x *= -1
                    self.level.tile_list_blue.pop(self.ball.collidelist(self.level.tile_list_blue))
                    self.score += 1
                    self.dzwiek('break')
                    
            if self.ball.collidelist(self.level.tile_list_blue) != -1 and self.isbig == True:
                    currtile = self.level.tile_list_blue[self.ball.collidelist(self.level.tile_list_blue)]
                    if self.chance() == 1:
                        self.bonus_spawn(currtile.centerx, currtile.centery)
                    if self.chance() == 1:
                        self.extra_life_spawn(currtile.centerx, currtile.centery)
                    self.level.tile_list_blue.pop(self.ball.collidelist(self.level.tile_list_blue))
                    self.score += 1
                    self.dzwiek('break')
                    
            if self.ball.collidelist(self.level.tile_list_red) != -1 and self.isbig == False:
                    currtile = self.level.tile_list_red[self.ball.collidelist(self.level.tile_list_red)]
                    if self.chance() == 1:
                        self.bonus_spawn(currtile.centerx, currtile.centery)
                    if self.chance() == 1:
                        self.extra_life_spawn(currtile.centerx, currtile.centery)
                    self.level.tile_list_blue.append(pygame.Rect(self.level.tile_list_red[self.ball.collidelist(self.level.tile_list_red)].x, self.level.tile_list_red[self.ball.collidelist(self.level.tile_list_red)].y,80,30))
                    if abs(self.ball.bottom - currtile.top) < 15 and self.ball_speed_y > 0:
                        self.ball_speed_y *= -1
                    if abs(self.ball.top - currtile.bottom) < 15 and self.ball_speed_y < 0:
                        self.ball_speed_y *= -1
                    if abs(self.ball.right - currtile.left) < 15 and self.ball_speed_x > 0:
                        self.ball_speed_x *= -1
                    if abs(self.ball.left - currtile.right) < 15 and self.ball_speed_x < 0:
                        self.ball_speed_x *= -1
                    self.level.tile_list_red.pop(self.ball.collidelist(self.level.tile_list_red))
                    self.score += 1
                    self.dzwiek('break')
                    
            if self.ball.collidelist(self.level.tile_list_red) != -1 and self.isbig == True:
                    currtile = self.level.tile_list_red[self.ball.collidelist(self.level.tile_list_red)]
                    if self.chance() == 1:
                        self.bonus_spawn(currtile.centerx, currtile.centery)
                    if self.chance() == 1:
                        self.extra_life_spawn(currtile.centerx, currtile.centery)
                    self.level.tile_list_red.pop(self.ball.collidelist(self.level.tile_list_red))
                    self.score += 1
                    self.dzwiek('break')
                    
            if self.ball.collidelist(self.level.tile_list_in) != -1:
                    currtile = self.level.tile_list_in[self.ball.collidelist(self.level.tile_list_in)]
                    if abs(self.ball.bottom - currtile.top) < 15 and self.ball_speed_y > 0:
                        self.ball_speed_y *= -1
                    if abs(self.ball.top - currtile.bottom) < 15 and self.ball_speed_y < 0:
                        self.ball_speed_y *= -1
                    if abs(self.ball.right - currtile.left) < 15 and self.ball_speed_x > 0:
                        self.ball_speed_x *= -1
                    if abs(self.ball.left - currtile.right) < 15 and self.ball_speed_x < 0:
                        self.ball_speed_x *= -1
                    self.dzwiek('bounce')
                    
                
    def player_animation(self):
        if self.RIGHT_KEY == True:
            self.player.x += 10
        if self.LEFT_KEY == True:
            self.player.x -= 10
        if self.player.left <= 160:
            self.player.left = 160
        if self.player.right >= self.gra.DIS_W-160:
            self.player.right = self.gra.DIS_W-160
        if self.player.collidelist(self.bonus) != -1 and self.isbig == False:
            self.bonus.pop(self.player.collidelist(self.bonus))
            self.ball.inflate_ip(15, 15)
            self.trace1 = pygame.transform.scale(self.trace1,(45,45))
            self.trace2 = pygame.transform.scale(self.trace2,(45,45))
            self.trace3 = pygame.transform.scale(self.trace3,(45,45))
            self.curr_ball_image = self.ball_png2
            self.bonus_time = pygame.time.get_ticks()
            self.isbig = True
        if self.player.collidelist(self.bonus) != -1 and self.isbig == True:
            self.bonus.pop(self.player.collidelist(self.bonus))
            self.bonus_time = pygame.time.get_ticks()
            self.isbig = True
        if self.player.collidelist(self.extra_life) != -1:
            self.extra_life.pop(self.player.collidelist(self.extra_life))
            self.lives += 1
            
    def bonus_spawn(self,x,y):
        self.bonus.append(pygame.Rect(x,y,20,20))
        

        
    def bonus_animation(self):
        i = 0
        while i < len(self.bonus):
            if self.bonus[i].y > self.gra.DIS_H:
                self.bonus.pop(i)
            else:
                self.bonus[i].y += 5
                self.gra.window.blit(self.bonus_png,(self.bonus[i].x,self.bonus[i].y))
            i += 1
    
    def extra_life_spawn(self,x,y):
        self.extra_life.append(pygame.Rect(x,y,20,20))
        

        
    def extra_life_animation(self):
        i = 0
        while i < len(self.extra_life):
            if self.extra_life[i].y > self.gra.DIS_H:
                self.extra_life.pop(i)
            else:
                self.extra_life[i].y += 5
                self.gra.window.blit(self.extra_life_png,(self.extra_life[i].x,self.extra_life[i].y))
            i += 1
    
    def get_back2normal(self):
        self.ball.inflate_ip(-15, -15)
        self.trace1 = pygame.transform.scale(self.trace1,(30,30))
        self.trace2 = pygame.transform.scale(self.trace2,(30,30))
        self.trace3 = pygame.transform.scale(self.trace3,(30,30))
        self.curr_ball_image = self.ball_png1
        self.bonus_time = 0
        self.isbig = False
              
    def ball_restart(self):
        self.ball.centerx = self.player.centerx
        self.ball.centery = self.player.centery - 25
        self.ball_speed_y = 0
        self.ball_speed_x = 0
        self.ball_in_motion = False
        
    def player_restart(self):
        self.player.center = (self.gra.DIS_W/2,self.gra.DIS_H - 70)
        
    def wynik(self):
        self.gra.draw_text(f'SCORE {self.score}', 20 , 10 , 10, self.gra.WHITE)
        
    def esc_info(self):
        self.gra.draw_text('PRESS ESC', 15 , self.gra.DIS_W-120 , 10, self.gra.WHITE)
        self.gra.draw_text('TO GO BACK', 15 , self.gra.DIS_W-120 , 25, self.gra.WHITE)
        
    def velocity(self):
        v = round(math.sqrt(self.ball_speed_x*self.ball_speed_x + self.ball_speed_y*self.ball_speed_y))
        self.gra.draw_text(f'BALL SPEED {v}', 20 , 10 , 35, self.gra.WHITE)
        
    def livesleft(self):
        self.gra.window.blit(self.heart_png, (10, 65))
        self.gra.draw_text(f'- {self.lives}', 20 , 35 , 60, self.gra.WHITE)
        
    def dzwiek(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.wav")
        if self.gra.optionsmenu.state_m == 'On':
            pygame.mixer.Sound.play(sound)
    
    def game_over(self):
        if self.isclear() == True:
            if self.level_index != len(Data)-1:
                self.level_index += 1
                self.hard_reset()
                self.gra.draw_text(f"Level {self.level_index} completed!", 30, 450, self.gra.DIS_H/2 - 50, self.gra.WHITE)
                self.gra.draw_text("Press Enter for the next level",  20, 450, self.gra.DIS_H/2, self.gra.WHITE)
                self.pause = True
            else:
                self.level_index = 0
                self.hard_reset()
                self.lives = 2
                self.gra.draw_text(f"CONGRATULATIONS! YOUR FINAL SCORE IS{self.score}", 30, 450, self.gra.DIS_H/2 - 50, self.gra.WHITE)
                self.gra.draw_text("TO PLAY AGAIN PRESS ENTER",  20, 480, self.gra.DIS_H/2, self.gra.WHITE)
                self.score = 0
                self.pause = True
            
        elif self.lives == 0 and self.isclear() == False:
            self.level_index = 0
            self.hard_reset()
            self.lives = 2
            self.gra.draw_text(f"GAME OVER         SCORE {self.score}", 30, 450, self.gra.DIS_H/2 - 50, self.gra.WHITE)
            self.gra.draw_text("TO PLAY AGAIN PRESS ENTER",  20, 480, self.gra.DIS_H/2, self.gra.WHITE)
            self.score = 0
            self.pause = True
            
        else:
            self.lives -= 1
            self.reset_game()
    
    def reset_game(self):
        self.player_restart()
        self.ball_restart()
        self.reset_keys()
        
    def hard_reset(self):
        self.reset_game()
        self.level = Level(Data[self.level_index],self.gra.window)
        
    def animation_crush(self):
        for i in self.animation:
            self.gra.window.blit(self.des[i[0]], (i[1], i[2]))
            i[0] += 1
            if i[0] == 9:
                self.animation.pop(self.animation.index(i))
                    
    
    def isclear(self):
        if len(self.level.tile_list_blue) == 0 and len(self.level.tile_list_green) == 0 and len(self.level.tile_list_red) == 0: return True
        else: return False
        
    def chance(self):
        return random.randint(0,50)

        
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.SPACE_KEY, self.LEFT_KEY, self.RIGHT_KEY= False, False, False, False, False, False
        
        
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.reset_game()
                        self.running = False
                        self.gra.kulka_playing = False
                        self.reset_keys()
                    if event.key == pygame.K_SPACE and self.ball_in_motion == False:
                        self.ball_speed_y = self.initial_speed
                        self.ball_speed_x = self.initial_speed
                        self.ball_in_motion = True
                    if event.key == pygame.K_RETURN:
                        self.pause = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.RIGHT_KEY = True
                    if event.key == pygame.K_LEFT:
                        self.LEFT_KEY = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.RIGHT_KEY = False
                    if event.key == pygame.K_LEFT:
                        self.LEFT_KEY = False
            if not self.pause:
                if pygame.time.get_ticks() - self.bonus_time > 5000 and self.bonus_time != 0:
                    self.get_back2normal()
                self.gra.window.blit(self.bg_png,(0,0))                 
                self.ball_animation()
                self.player_animation()
                self.bonus_animation()
                self.extra_life_animation()
                self.gra.window.blit(self.player_png, (self.player.x, self.player.y))
                self.gra.window.blit(self.trace1, (self.ball.x-self.ball_speed_x*1, self.ball.y-self.ball_speed_y*1))
                self.gra.window.blit(self.trace2, (self.ball.x-self.ball_speed_x*2, self.ball.y-self.ball_speed_y*2))
                self.gra.window.blit(self.trace3, (self.ball.x-self.ball_speed_x*3, self.ball.y-self.ball_speed_y*3))
                self.gra.window.blit(self.curr_ball_image, (self.ball.x, self.ball.y))
                self.level.draw()
                self.animation_crush()
                    
                self.wynik()
                self.velocity()
                self.esc_info()
                self.livesleft()
                if self.isclear() == True:                   
                    self.game_over()

            pygame.display.flip()
            self.clock.tick(60)