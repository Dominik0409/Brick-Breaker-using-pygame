import pygame, sys, random

pygame.init()
clock = pygame.time.Clock()
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Kulka")

ball = pygame.Rect(screen_width/2 - 15,screen_height/2 - 15,30,30)
player = pygame.Rect(screen_width/2 -70, screen_height - 70,140,10)
rectangles = []
for j in range(0,5):
    for i in range(0,32):
        rectangles.append(pygame.Rect(0 + i*40,0 + j*40,40,40))
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)


class Game():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.ball_speed_x = 7 * random.choice((1,-1))
        self.ball_speed_y = 7 * random.choice((1,-1))
        self.player_speed = 0
        self.running = True
        
    def ball_animation(self):
        ball.x += self.ball_speed_x
        ball.y += self.ball_speed_y
        
        if ball.top <= 0:
            self.ball_speed_y *= -1
        if ball.left <= 0 or ball.right >= screen_width:
            self.ball_speed_x *= -1
        if ball.bottom >= screen_height:
            self.ball_restart()
        if ball.colliderect(player):
            self.ball_speed_y *= -1
        i = 0
        while i < len(rectangles):
            if ball.colliderect(rectangles[i]):
                rectangles.pop(i)
                self.ball_speed_y *= -1
                self.ball_speed_x *= -1
            i += 1
            
    def player_animation(self):
        player.x += self.player_speed
        if player.left <= 0:
            player.left = 0
        if player.right >= screen_width:
            player.right = screen_width
              
    def ball_restart(self):
        ball.center = (screen_width/2,screen_height/2)
        self.ball_speed_y *= random.choice((1,-1))
        self.ball_speed_x *= random.choice((1,-1))
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.player_speed += 10
                    if event.key == pygame.K_LEFT:
                        self.player_speed -= 10
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.player_speed -= 10
                    if event.key == pygame.K_LEFT:
                        self.player_speed += 10
                        
                    
            self.ball_animation()
            self.player_animation()
            
            
            screen.fill(bg_color)
            pygame.draw.rect(screen,light_grey, player)
            i = 0
            while i < len(rectangles):
                pygame.draw.rect(screen,light_grey, rectangles[i])
                i += 1
            pygame.draw.ellipse(screen,light_grey, ball)
            
            pygame.display.flip()
            clock.tick(60)
g = Game()
g.run()