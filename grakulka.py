import pygame, sys, random, math

bg_color = pygame.Color('grey12')
light_grey = (200,200,200)

class Game():
    def __init__(self, gra):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.gra = gra
        self.ball = pygame.Rect(self.gra.DIS_W/2 - 15,self.gra.DIS_H/2 - 15,30,30)
        self.player = pygame.Rect(self.gra.DIS_W/2 -70, self.gra.DIS_H - 70,140,20)
        self.bonus = []
        self.rectangles = []
        for j in range(0,5):
            for i in range(0,16):
                self.rectangles.append(pygame.Rect(0 + i*80,0 + j*40,80,20))
        self.clock = pygame.time.Clock()
        self.ball_speed_x = 7 * random.choice((1,-1))
        self.ball_speed_y = 7 * random.choice((1,-1))
        self.player_speed = 0
        self.running = True
        self.pause = False
        self.isbig = False
        self.player_png = pygame.image.load("platforma.png").convert()
        self.bg_png = pygame.image.load("bg1.png").convert()
        self.brick_png = pygame.image.load("klocek.png").convert()
        self.ball_png1 = pygame.image.load("kulka.png").convert_alpha()
        self.ball_png2 = pygame.image.load("kulka2.png").convert_alpha()
        self.bonus_png = pygame.image.load("plus.png").convert_alpha()
        self.curr_ball_image = self.ball_png1
        self.bonus_time = 0
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.SPACE_KEY, self.LEFT_KEY, self.RIGHT_KEY= False, False, False, False, False, False
        
    def ball_animation(self):
        if self.pause:
            if self.RIGHT_KEY == True:
                self.ball.x += 10
            if self.LEFT_KEY == True:
                self.ball.x -= 10
        else:    
            self.ball.x += self.ball_speed_x
            self.ball.y += self.ball_speed_y
            
            if self.ball.top <= 0:
                self.ball_speed_y *= -1
                
            if self.ball.left < 0 or self.ball.right >self.gra.DIS_W:
                self.ball_speed_x *= -1
                
            if self.ball_speed_x == 0:
                self.ball_speed_x = 0.1 * random.choice((1,-1))
                
            if self.ball.bottom >= self.gra.DIS_H:
                self.pause = True
                self.player_restart()
                self.ball_restart()
                self.reset_keys()
                
            if self.ball.colliderect(self.player):
                collidePoint = self.ball.centerx - (self.player.centerx)
                collidePoint = collidePoint/(self.player.w/2)
                angle = collidePoint * (math.pi/4)
                ball_speed = math.sqrt(self.ball_speed_x*self.ball_speed_x + self.ball_speed_y*self.ball_speed_y)
                self.ball_speed_x = ball_speed * math.sin(angle)
                self.ball_speed_y = - ball_speed * math.cos(angle)
                
            if self.ball.collidelist(self.rectangles) != -1 and self.isbig == False:
                    chance = random.randint(0,10)
                    if chance == 1:
                        self.bonus_spawn(self.rectangles[self.ball.collidelist(self.rectangles)].centerx, self.rectangles[self.ball.collidelist(self.rectangles)].centery)
                    self.rectangles.pop(self.ball.collidelist(self.rectangles))
                    collidePoint = self.ball.centerx - (self.rectangles[self.ball.collidelist(self.rectangles)].centerx)
                    collidePoint = collidePoint/(self.rectangles[self.ball.collidelist(self.rectangles)].w/2)
                    angle = collidePoint * (math.pi/4)
                    ball_speed = math.sqrt(self.ball_speed_x*self.ball_speed_x + self.ball_speed_y*self.ball_speed_y)
                    self.ball_speed_x = ball_speed * math.sin(angle+math.pi)
                    self.ball_speed_y = - ball_speed * math.cos(angle+math.pi)
                    
            if self.ball.collidelist(self.rectangles) != -1 and self.isbig == True:
                    chance = random.randint(0,10)
                    if chance == 1:
                        self.bonus_spawn(self.rectangles[self.ball.collidelist(self.rectangles)].centerx, self.rectangles[self.ball.collidelist(self.rectangles)].centery)
                    self.rectangles.pop(self.ball.collidelist(self.rectangles))
                
    def player_animation(self):
        if self.RIGHT_KEY == True:
            self.player.x += 10
        if self.LEFT_KEY == True:
            self.player.x -= 10
        if self.player.left <= 0:
            self.player.left = 0
        if self.player.right >= self.gra.DIS_W:
            self.player.right = self.gra.DIS_W
        if self.player.collidelist(self.bonus) != -1 and self.isbig == False:
            self.bonus.pop(self.player.collidelist(self.bonus))
            self.ball.inflate_ip(15, 15)
            self.curr_ball_image = self.ball_png2
            self.bonus_time = pygame.time.get_ticks()
            self.isbig = True
            
    def bonus_spawn(self,x,y):
        self.bonus.append(pygame.Rect(x,y,20,20))
        

        
    def bonus_animation(self):
        i = 0
        while i < len(self.bonus):
            if self.bonus[i].y > self.gra.DIS_H:
                self.bonus.pop(i)
            else:
                self.bonus[i].y += 5
            i += 1
    
    def get_back2normal(self):
        self.ball.inflate_ip(-15, -15)
        self.curr_ball_image = self.ball_png1
        self.bonus_time = 0
        self.isbig = False
              
    def ball_restart(self):
        self.ball.centerx = self.player.centerx
        self.ball.centery = self.player.centery - 20
        self.ball_speed_y = 0
        self.ball_speed_x = 0
        
    def player_restart(self):
        self.player.center = (self.gra.DIS_W/2,self.gra.DIS_H - 70)
        
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
                        self.running = False
                        self.gra.kulka_playing = False
                    if event.key == pygame.K_SPACE:
                        self.ball_speed_y = 7
                        self.ball_speed_x = 7 * random.choice((1,-1))
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
            if pygame.time.get_ticks() - self.bonus_time > 5000 and self.bonus_time != 0:
                self.get_back2normal()                 
            self.ball_animation()
            self.player_animation()
            self.bonus_animation()
            
            
            self.gra.window.blit(self.bg_png,(0,0))
            self.gra.window.blit(self.player_png, (self.player.x, self.player.y))
            i = 0
            while i < len(self.rectangles):
                self.gra.window.blit(self.brick_png,(self.rectangles[i].x,self.rectangles[i].y))
                i += 1
            i = 0
            while i < len(self.bonus):
                pygame.draw.rect(self.gra.window, self.gra.BLACK, self.bonus[i])
                self.gra.window.blit(self.bonus_png,(self.bonus[i].x,self.bonus[i].y))
                i += 1
            self.gra.window.blit(self.curr_ball_image, (self.ball.x, self.ball.y))

            pygame.display.flip()
            self.clock.tick(60)