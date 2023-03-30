# Author: Swapnil Srivastava
# Game controls:
#   Use mouse to aim and shoot by clicking.
#   Arrows to move.
#   Spacebar to jump.

import pygame
from pygame.locals import *

import sys
import time

pygame.init()
FPS = 60
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
    
    def move(self, x, y):
        self.rect.move_ip([x,y])

    def update(self, boxes):
        x_movement = 0
        onground = pygame.sprite.spritecollideany(self,boxes)
        #What keys are currently being pressed?
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x_movement = -self.speed
        elif keys[pygame.K_RIGHT]:
            x_movement = self.speed

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
        surface.blit(self.image, self.rect)

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("box_image_collection/box_1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y) #if the buc is 50 X 50 then the intersection of feet of player and top of the box should happen at y = 700 + 62.5 + 25

    def draw(self, surface):
        surface.blit(self.image, self.rect)

#Our bullet object created upon mouse click 
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, direction):
        super().__init__()
        self.color = BLACK
        #self.position = pos
        self.velocity = 5
        self.size = 5,5
        self.rect = pygame.Rect(start_pos,self.size)
    
    def update(self):
        self.rect.move_ip(10,0)
    
    def draw(self,surface):
        pygame.draw.rect(surface, BLACK, self.rect)

def main():
    print("This is a shooting game, so beware! Many monsters lurk in the shadows...")

    #Set up the scene
    scene = pygame.display.set_mode((1900, 1280))
    scene.fill(SKY_BLUE)
    pygame.display.set_caption("Survive forest, survive!")

    #Initialize player
    player = Player()
    floor_boxes = pygame.sprite.Group()
    for box in range(48, 1900, 96):
        floor_boxes.add(Box(box,800))
    alive = True
    bullets = []
    while alive:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # if(len(bullets)<10):
                    bullets.append(Bullet(pygame.mouse.get_pos()))
                # else:
                #     pygame.event.post(pygame.event.Event(GAMEOVER))
        
        player.update(floor_boxes)
        for bullet in bullets:
            bullet.draw(scene)
            bullet.update()
        scene.fill(SKY_BLUE)

        player.draw(scene)
        floor_boxes.draw(scene)
        pygame.display.update()

        Clock.tick(FPS)

main()