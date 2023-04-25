# Author: Swapnil Srivastava
# Game controls:
#   Use mouse to  shoot by clicking.
#   Arrows to move.
#   Tap the up arrow to double jump when in the air.

import pygame
from pygame.locals import *

import sys
import time

#Initialize the constructor
pygame.init()

#Window dimensions
X = 1900
Y = 1280

#Colors
BLUE  = (0, 0, 255)
LRED   = (255, 204, 203)
GREEN = (0, 255, 0) 
BLACK = (0, 0, 0)
GREY = (36, 36, 36)
WHITE = (255, 255, 255)
SKY_BLUE = (135,206,235)   

FPS = 120
Clock = pygame.time.Clock()

scene = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Survive forest, survive!")


print("This is a shooting game, so beware! Many monsters lurk in the shadows...")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("storm_trooper.png")
        self.image = pygame.transform.scale(self.image, (75,125))
        self.rect = self.image.get_rect()
        self.rect.center = (50,650) #so the feet should be at y = 700 + 62.5

        self.vert = 20 #vertical jumping ability
        self.v_speed = 0 # vertical speed
        self.speed = 5 #horizontal speed
        self.gravity = 1
        self.onground = True
        self.can_jump = True 
        self.doublejump = False 
        self.facing_left = False
    
    def move(self, x, y):
        self.rect.move_ip([x,y])

    def get_pos(self):
        return self.rect.center
    
    def set_pos(self, x, y):
        self.rect.center = x, y
    
    def jump(self):
        if  self.doublejump:
            self.doublejump = False  #Does not allow the player to double jump more than once
            self.v_speed -= 20
            print(self.doublejump)
        if self.can_jump:
            self.can_jump = False
            self.doublejump = True  #Allows the player to double jump
            print(self.doublejump)
            self.v_speed = -self.vert #Apply force upwards

    def update(self, boxes):
        x_movement = 0
        onground = pygame.sprite.spritecollideany(self,boxes)
        # #What keys are currently being pressed?
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x_movement = -self.speed
            self.facing_left = True
        elif keys[pygame.K_RIGHT]:
            x_movement = self.speed
            self.facing_left = False
         #gravity
        if self.v_speed < 10 and not onground:
            self.v_speed += self.gravity

        if self.v_speed >0 and onground:
            self.v_speed = 0
            self.doublejump = False
            self.can_jump = True
       
        
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

class Monster(pygame.sprite.Sprite):
    def __init__(self, pos, lvl):
        super().__init__()
        if(lvl ==1):
            self.image = pygame.image.load("monster_images/lvl_1.png")    
            self.image = pygame.transform.scale(self.image, (80,80))
            self.health = 200
            self.velocity = 5
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.lvl = lvl
        
        self.left_facing = True

    def turn(self):
        self.left_facing = not(self.left_facing)

    def update(self):
        if(self.lvl == 1):
            if(self.left_facing):
                #self.rect.center =  (self.rect.center[0]-self.velocity,self.rect.center[1])
                self.rect.move_ip(-self.velocity, 0)
            else:
                #self.rect.center =  (self.rect.center[0]+self.velocity,self.rect.center[1])
                self.rect.move_ip(self.velocity, 0)
    
    def get_pos(self):
        return self.rect.center
    
    def draw(self,surface):
        if(self.left_facing):
            surface.blit(self.image, self.rect)
        else:
            temp_image = pygame.transform.flip(self.image, True, False)
            surface.blit(temp_image, self.rect)

#This method sets up the Box sprites that make up our floor for different sections of the map
def generate_floor():
    #Groups of boxes that make up the floor. Each group represents the floor layout as the player progresses through the game.
    #TODO: Generate the groups using a loop.
    floor_boxes_1 = pygame.sprite.Group()
    floor_boxes_2 = pygame.sprite.Group()
    floor_boxes_3 = pygame.sprite.Group()
    floor_boxes_4 = pygame.sprite.Group()
    floor_boxes_5 = pygame.sprite.Group()

    step = 96 #TODO clean this up.
    for box in range(48, X, step): #TODO clean this up
        if(box>950):
            floor_boxes_1.add(Box(box+(step*2), 700)) #First section of the map
            floor_boxes_2.add(Box(box+(step), 900))
            
            #floor_boxes_3.add()
            #floor_boxes_4.add()
            #floor_boxes_5.add()
        elif(box<=950):
            floor_boxes_1.add(Box(box,800)) #First section of the map
            if(box<600):
                floor_boxes_2.add(Box(box,700)) #Second section of the map
                floor_boxes_3.add(Box(box, 900))
            else:
                floor_boxes_2.add(Box(box+(step*2), 500))
                floor_boxes_2.add(Box(box+(step), 900))
            #floor_boxes_2.add(Box(box,700))
        else:
            break
    
    floor = []
    floor.append(floor_boxes_1)
    floor.append(floor_boxes_2)
    floor.append(floor_boxes_3)
    return floor      


#This function handles the start menu view
def start_menu(scene):
    scene.fill(GREY)
    # defining a font 
    font = pygame.font.SysFont('Corbel',50)
    title_font = pygame.font.SysFont('Arial', 100)
    sub_title_font = pygame.font.SysFont('Arial', 70)
    title = title_font.render('Shoot! Forest, Shoot!!' , True , WHITE)
    sub_title1 = sub_title_font.render('This is a shooting game, so beware! ' , True , GREEN)
    sub_title2 = sub_title_font.render('Many monsters lurk in the shadows...' , True , GREEN)
    start_button = font.render("Press the Spacebar to Start Your Adventure" , True, WHITE)
    scene.blit(title, (X/2 - title.get_width()/2, 150))
    scene.blit(sub_title1, (X/2-sub_title1.get_width()/2, 300))
    scene.blit(sub_title2, (X/2-sub_title2.get_width()/2, 370))
    scene.blit(start_button, (X/2 - start_button.get_width()/2, Y/2 + start_button.get_height()))
    pygame.display.update()


def main():
    #Set the game state to the start menu
    game_state =  "start_menu"
    scene.fill(SKY_BLUE)
    #Initialize player
    player = Player()
    floor = generate_floor()
    alive = True
    bullets = []
    map_section = 0; # Used to update map based on player position. Starts with the first floor boxes group

    monsters = []
    monsters.append(Monster([1300,613], 1))

    
    print(pygame.key.get_repeat())
    while alive:
        
        #Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # if(len(bullets)<10):
                    bullets.append(Bullet(player.get_pos(), pygame.mouse.get_pos()))
                # else:
                #     pygame.event.post(pygame.event.Event(GAMEOVER))
            if event.type == KEYDOWN:
                if game_state == "start_menu" and event.key==K_SPACE:
                    game_state = "game"
                if(event.key==K_UP):
                    player.jump()
        if game_state == "start_menu":
            #Display start menu 
            start_menu(scene)
        if game_state == "game":
            scene.fill(SKY_BLUE) #Background color

            player.update(floor[map_section])
            player.draw(scene)

            #Dray appropriate map based on player location
            if(map_section == 0):
                floor[0].draw(scene)
            elif(map_section == 1):
                floor[1].draw(scene)
            elif(map_section == 2):
                floor[2].draw(scene)

            #Monsters view
            if(monsters[0].get_pos()[0]<=1180 or monsters[0].get_pos()[0]>(X-50)):
                monsters[0].turn()  #Set the path for the first monster
            for i in range(len(monsters)):
                if(map_section==0 and i==0):
                    monsters[i].update()
                    if(pygame.sprite.spritecollideany(player, monsters)):
                        alive = False
                    monsters[i].draw(scene)

            for bullet in bullets: #TODO: House all of the bullets in a group.
                bullet.draw(scene)
                bullet.update()
                
                if(bullet.check_collision_box(floor[map_section]) or bullet.out_of_screen()): #remove bullet from this array when it collides with the floor of is out of the screen.
                    bullets.remove(bullet)
            
            if(player.get_pos()[1]>Y):
                alive = False

            if(player.get_pos()[0]>X):
                player.set_pos(50,player.get_pos()[1])
                map_section+=1
            elif(player.get_pos()[0]<0):
                player.set_pos(X-20, player.get_pos()[1])
                map_section -= 1
            
            pygame.display.update()
            Clock.tick(FPS)

main()