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


# class for all game objects with location

class GameObject:
    def __init__(self,inputx, inputy):
        self.x = inputx
        self.y = inputy

    def location (self):
        return (self.x * 32), (self.y * 32)

# class for all walls

class Wall (GameObject):

    def __init__(self, inputx, inputy, direction, colour):
        GameObject.__init__(self, inputx, inputy)
        self.direction = direction
        self.colour = colour
        self.wall_here = []
        n=0

        if self.direction == "horizontal":
           while n<19:
              self.wall_here.append ((self.x + n,self.y))
              n +=1
           
        if self.direction == "vertical":
           while n<12:
              self.wall_here.append ((self.x ,self.y + n))
              n +=1
                                     
    def draw (self):

        if self.direction == "horizontal":

            wallrect = pygame.Rect((self.location() [0], self.location() [1]),(576,32))
            pygame.draw.rect (window, self.colour, wallrect)

        
        if self.direction == "vertical":

            wallrect = pygame.Rect((self.location() [0] , self.location() [1]),(32,416))
            pygame.draw.rect (window, self.colour, wallrect)

    
        



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
        pygame.draw.line(window, WHITE, self.point_start(),self.point_end())


# class for all robots

class Robot (GameObject):
    
    def __init__(self, inputx, inputy, startdirection):
        GameObject.__init__(self, inputx, inputy)
        self.direction = startdirection

        
    def draw (self):
        
        robotrect = pygame.Rect((self.location() [0], self.location() [1]),(32,32))
        pygame.draw.rect (window, GREY, robotrect)

    def update_down (self):

        self.y += 1

    def update_up (self):

        self.y += -1

     


# class for all lasers

class Laser (GameObject):
    
    def __init__(self, inputx, inputy, colour):
        GameObject.__init__(self, inputx, inputy)
        self.laser_exists = True
        self.colour = colour
        
        
    def draw (self):
     
        laserrect = pygame.Rect((self.location() [0] + 24, self.location() [1]),(8,8))
        pygame.draw.rect (window, self.colour, laserrect)

        
    def update_left (self):

        self.x += -1

    def update_right (self):

        self.x += 1
    

# create walls and remember where walls are

wall_list = []

wall_list.append (Wall(1,0,"horizontal",RED))
wall_list.append (Wall(1,14,"horizontal",GREEN))
wall_list.append (Wall(0,1,"vertical",BLUE))
wall_list.append (Wall(19,1,"vertical",YELLOW))


    
# Create mirrors

mirrorlist = []

mirrorlist.append (Mirror (8, 7, "tlbr"))
mirrorlist.append (Mirror (12, 11, "tlbr"))
mirrorlist.append (Mirror (9, 6, "trbl"))


# Create robots

robotlist = []

robotlist.append (Robot (3, 6, 'down'))
robotlist.append (Robot (7, 3, 'up'))


# Create lasers

laserlist = []

for robot in robotlist:
    laserlist.append (Laser (robot.x, robot.y, PURPLE))



# filter start values

filter1x = 8
filter1y = 4
filter1colour = YELLOW

# draw the window onto the screen
pygame.display.update()

# game loop

while True:
    dt = clock.tick(5)

    timer += dt
    time = math.floor(timer/1000)

    # draw background and walls
    
    window.fill(BLACK)

    for wall in wall_list:
        wall.draw()

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
       
    # draw and move laser

    for laser in laserlist:
            
         if laser.laser_exists == True:

            laser.draw()
            laser.update_right()
               


         # check if laser hits wall, if so, remove from screen
         # check if laser colour matches wall colour, adapt score
               
            for wall in wall_list:
               if (laser.x,laser.y) in wall.wall_here:
                     laser.laser_exists = False

                     if laser.colour == wall.colour:
                        score +=1




    
    # create new laser if not there    
    #if laser_exists == False:
     #   laser_exists = True
      #  laserx = robotx
       # lasery = roboty
        #laserxdir = 1
        #laserydir = 0
    #    lasercolour = PURPLE




    # check for filter
   # if laserx == filter1x and lasery == filter1y:
    #       lasercolour = filter1colour
        
    # check for mirror
    
    #for mirror in mirrorlist:

     #   if laserx == mirror.x and lasery == mirror.y:

      #      if mirror.orient == "tlbr":
       #         laserxdir = 0
        #        laserydir = 1
         #   elif mirror.orient == "trbl":
          #      laserxdir = 0
           #     laserydir = -1
    

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
