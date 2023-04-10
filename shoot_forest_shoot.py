# Author: Swapnil Srivastava
# Game controls:
#   Use mouse to  shoot by clicking.
#   Arrows to move.
#   Spacebar to double jump when in the air.

import pygame
from pygame.locals import *

import sys
import time

pygame.init()
FPS = 120
Clock = pygame.time.Clock()

#Colors
BLUE  = (0, 0, 255)
LRED   = (255, 204, 203)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (135,206,235)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("storm_trooper.png")
        self.image = pygame.transform.scale(self.image, (75,125))
        self.rect = self.image.get_rect()
        self.rect.center = (50,650) #so the feet should be at y = 700 + 62.5

        self.vert = 15 #vertical jumping ability
        self.v_speed = 0 # vertical speed
        self.speed = 5 #horizontal speed
        self.gravity = 1
        self.doublejump = True 
        self.facing_left = False
    
    def move(self, x, y):
        self.rect.move_ip([x,y])

    def get_pos(self):
        return self.rect.center
    
    def set_pos(self, x, y):
        self.rect.center = x, y
    def update(self, boxes):
        x_movement = 0
        onground = pygame.sprite.spritecollideany(self,boxes)
        #What keys are currently being pressed?
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x_movement = -self.speed
            self.facing_left = True
        elif keys[pygame.K_RIGHT]:
            x_movement = self.speed
            self.facing_left = False

        if keys[pygame.K_UP] and onground:
            self.v_speed = -self.vert
        elif keys[pygame.K_SPACE] and  (not onground) and self.doublejump:
            self.doublejump = False  
            self.v_speed -= self.vert 

        #gravity
        if self.v_speed < 10 and not onground:
            self.v_speed += self.gravity

        if self.v_speed >0 and onground:
            self.v_speed = 0
            self.doublejump = True
        
        self.move(x_movement,self.v_speed)

    def draw(self,surface):
        if self.facing_left:
            temp_image = pygame.transform.flip(self.image, True, False)
            surface.blit(temp_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("box_image_collection/box_1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y) #if the box is 50 X 50 then the intersection of feet of player and top of the box should happen at y = 700 + 62.5 + 25

    def draw(self, surface):
        surface.blit(self.image, self.rect)

#Our bullet object created upon mouse click 
# Note to self: Look at how the player move function was implemented. This can be helpful in getting the intended bullet functionality.
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, aim):
        super().__init__()
        self.color = BLACK
        #self.position = pos
        self.velocity = 18
        self.size = 7,5
        self.rect = pygame.Rect([start_pos[0]+10,start_pos[1] -40],self.size)
        self.x = start_pos[0]+10
        # self.slope = (aim[1] - start_pos[1]) / (aim[0] - start_pos[0])
        # self.y_intercept = start_pos[1]
    
    def update(self):
        # Work on the below code to implement shooting in any direction
        # y_temp = self.y #old y value
        # self.x += self.velocity #update current x 
        # self.y = (self.slope * self.x) + self.y_intercept #update current y
        
        # y = self.y -y_temp  #y offset
        self.x += self.velocity
        self.rect.move_ip(self.velocity, 1)
    def check_collision_box(self, boxes):
        return pygame.sprite.spritecollideany(self,boxes)
    def out_of_screen(self):
        if(self.x>1900): # out of screen
            return True
        return False
    def draw(self,surface):
        pygame.draw.rect(surface, BLACK, self.rect)

def main():
    print("This is a shooting game, so beware! Many monsters lurk in the shadows...")

    #Set up the scene
    X = 1900
    Y = 1280
    scene = pygame.display.set_mode((X, Y))
    scene.fill(SKY_BLUE)
    pygame.display.set_caption("Survive forest, survive!")

    #Initialize player
    player = Player()
    floor_boxes = pygame.sprite.Group()
    step = 96
    for box in range(48, X, step):
        if(box>950):
            floor_boxes.add(Box(box+(step*2), 700)) #All these boxes are at y = 700, but the player has to jump the gap of width = step*2
        else:
            floor_boxes.add(Box(box,800)) #All these boxes are at y = 800
    alive = True
    bullets = []
    while alive:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # if(len(bullets)<10):
                    bullets.append(Bullet(player.get_pos(), pygame.mouse.get_pos()))
                # else:
                #     pygame.event.post(pygame.event.Event(GAMEOVER))
       
        scene.fill(SKY_BLUE)
        player.update(floor_boxes)
        player.draw(scene)
        floor_boxes.draw(scene)

        for bullet in bullets:
            bullet.draw(scene)
            bullet.update()
            
            if(bullet.check_collision_box(floor_boxes) or bullet.out_of_screen()): #remove bullet from this array when it collides with the floor of is out of the screen.
                bullets.remove(bullet)
        
        if(player.get_pos()[1]>Y):
            alive = False

        if(player.get_pos()[0]>1280):
            player.set_pos(50,650)
        pygame.display.update()
        Clock.tick(FPS)

main()
