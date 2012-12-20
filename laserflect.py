import pygame, sys, math, os
from pygame.locals import *

# set up pygame
pygame.init()

# font
font = pygame.font.Font(None, 36)

# set up the window
window = pygame.display.set_mode((640,480),0,32)
pygame.display.set_caption('Lasers')

# time
clock = pygame.time.Clock()
timer = 0 #global time

# score
score = 0

# set up colours
WHITE = (255, 255, 255)
BLACK = (30,30,30)
RED = (255,81,77)
GREEN = (113, 255, 16)
BLUE = (38, 111, 255)
YELLOW = (250, 255, 106)
GREY = (100,100,100)
PURPLE = (204,0,102)

# positions

def position(gridx, gridy):
    return (gridx * 32), (gridy * 32)

# draw the background and walls

def bg_and_walls():
    window.fill(BLACK)

    yellowrect = pygame.Rect (position(19,0),(32,640))
    greenrect = pygame.Rect (position(0,0),(32,640))
    bluerect = pygame.Rect (position(0,14),(640,32))
    redrect = pygame.Rect (position(0,0),(640,32))

    pygame.draw.rect(window, YELLOW, yellowrect)
    pygame.draw.rect(window, GREEN, greenrect)
    pygame.draw.rect(window, BLUE, bluerect)
    pygame.draw.rect(window, RED, redrect)

# robot starting position and direction

robotx = 3
roboty = 3
robotydir = 1

# laser start values

laserx = robotx
lasery = roboty
laserxdir = 1
laserydir = 0
lasercolour = PURPLE
laser_exists = False


# class for all game objects with location

class GameObject:
    def __init__(self,inputx, inputy):
        self.x = inputx
        self.y = inputy

    def location (self):
        return (self.x * 32 + 16), (self.y * 32 + 16)
        

# class for all mirrors 

class Mirror (GameObject):
    
    def __init__(self, inputx, inputy, inputorient):
        GameObject.__init__(self, inputx, inputy)
        self.orient = inputorient
       
        

    def point_start(self):
        if self.orient == "tlbr":
            return self.location()[0] - 16, self.location()[1] - 16

        elif self.orient == "trbl":
            return self.location()[0] + 16, self.location()[1] - 16


    def point_end(self):
        if self.orient == "tlbr":
            return self.location()[0] + 16, self.location()[1] + 16

        elif self.orient == "trbl":
            return self.location()[0] - 16, self.location()[1] + 16        
                            
    
    def draw(self):
        pygame.draw.line(window, WHITE,
                            self.point_start()
                            ,self.point_end())


# class for all robots

class Robot (GameObject):
    
    def __init__(self, inputx, inputy, startdirection):
        GameObject.__init__(self, inputx, inputy)
        self.direction = startdirection

        
    def draw (self):
        
        robotrect = pygame.Rect((self.x * 32, self.y * 32),(32,32))
        pygame.draw.rect (window, GREY, robotrect)

    def update_down (self):

        self.y += 1

    def update_up (self):

        self.y += -1

    def make_laser(self):

        laserrect = pygame.Rect((self.x * 32, self.y * 32),(8,8))
        pygame.draw.rect (window, PURPLE, laserrect)


        



# class for all lasers

class Laser (GameObject):
    
    def __init__(self, inputx, inputy):
        GameObject.__init__(self, inputx, inputy)
        
        
    def draw (self):
        
        laserrect = pygame.Rect((self.x * 32, self.y * 32),(8,8))
        pygame.draw.rect (window, PURPLE, laserrect)

    def update_left (self):

        self.x += 1

    def update_right (self):

        self.x += -1

   


# Create mirrors

mirrorlist = []

mirrorlist.append (Mirror (8, 7, "tlbr"))
mirrorlist.append (Mirror (12, 11, "tlbr"))
mirrorlist.append (Mirror (9, 6, "trbl"))


# Create robots

robotlist = []

robotlist.append (Robot (3, 3, 'down'))
robotlist.append (Robot (7, 3, 'up'))


for robot in robotlist:
    robot.make_laser()

# filter start values

filter1x = 8
filter1y = 4
filter1colour = YELLOW

# draw the window onto the screen
pygame.display.update()

# game loop

while True:
    dt = clock.tick(10)

    timer += dt
    time = math.floor(timer/1000)

    # draw backgrounds
    bg_and_walls()

    # draw mirrors     

    for mirror in mirrorlist:
        mirror.draw()
   
               
        

    # draw filter
    filterrect = pygame.Rect (position(filter1x, filter1y),(16,16))
    pygame.draw.rect (window, filter1colour, filterrect)
    
    
    # draw and move robot

    for robot in robotlist:

        if robot.direction == "down":
            robot.update_down()
            robot.draw()

        elif robot.direction == "up":
            robot.update_up()
            robot.draw()

        if robot.y > 12:
            robot.direction = "up"

        elif robot.y < 2:
            robot.direction = "down"
       
        

        
    # check if laser left screen
    #if laserx >19:
     #   laser_exists = False
      #  if lasercolour == YELLOW:
       #     score += 1
    #if lasery > 14:
     #   laser_exists = False
      #  if lasercolour == BLUE:
       #     score += 1
    #if lasery < 1:
     #   laser_exists = False
      #  if lasercolour == RED:
       #     score += 1
    #if laserx < 1:
     #   laser_exists = False
      #  if lasercolour == GREEN:
       #     score += 1

    # create new laser if not there    
    #if laser_exists == False:
     #   laser_exists = True
      #  laserx = robotx
       # lasery = roboty
        #laserxdir = 1
        #laserydir = 0
    #    lasercolour = PURPLE



        
    
    # draw laser
    laserrect = pygame.Rect (position (laserx,lasery),(8,8))
    pygame.draw.rect (window, lasercolour, laserrect)

    # move laser
    laserx += laserxdir
    lasery += laserydir

    # check for filter
    if laserx == filter1x and lasery == filter1y:
        lasercolour = filter1colour
        
    # check for mirror
    
    for mirror in mirrorlist:

        if laserx == mirror.x and lasery == mirror.y:

            if mirror.orient == "tlbr":
                laserxdir = 0
                laserydir = 1
            elif mirror.orient == "trbl":
                laserxdir = 0
                laserydir = -1
    

    # print score
    text2 = font.render("Score: " + str(score), 1, BLUE)
    text1 = font.render("TIME: " + str(time), 1, GREEN)
    text1pos = text1.get_rect()
    text1pos.centerx = window.get_rect().centerx
    text2pos = text2.get_rect()
    text2pos.right = window.get_rect().right
    window.blit(text1, text1pos)
    window.blit(text2, text2pos)

    # interaction (move filter using keys, change color using keys)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        if down:
          if event.key == K_RIGHT: filter1x += 1
          if event.key == K_LEFT: filter1x -= 1
          if event.key == K_UP: filter1y -= 1
          if event.key == K_DOWN:  filter1y += 1
          if event.key == K_y:  filter1colour = YELLOW
          if event.key == K_r:  filter1colour = RED
          if event.key == K_g:  filter1colour = GREEN
          if event.key == K_b:  filter1colour = BLUE
  
    pygame.display.flip()
