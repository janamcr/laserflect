import pygame, sys, math, os, random
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
timer = 60000 #global time
time_move = 0

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

        # these grids are wall

        if self.direction == "horizontal":
           while n<=19:
              self.wall_here.append ((self.x + n,self.y))
              n +=1
           
        if self.direction == "vertical":
           while n<=12:
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
            return self.location()[0], self.location()[1]

        elif self.orient == "trbl":
            return self.location()[0] + 32, self.location()[1]


    def point_end(self):
        if self.orient == "tlbr":
            return self.location()[0] + 32, self.location()[1] + 32

        elif self.orient == "trbl":
            return self.location()[0], self.location()[1] + 32        
                            
    
    def draw(self):
        pygame.draw.line(window, WHITE, self.point_start(),self.point_end())


# class for filter

class Filter (GameObject):

   def __init__(self, inputx, inputy, colour):
        GameObject.__init__(self, inputx, inputy)
        self.colour = colour

   def draw (self):
        
        filterrect = pygame.Rect((self.location()[0] + 8, self.location()[1] + 8),(16,16))
        pygame.draw.rect (window, self.colour, filterrect)



# class for all robots

class SuperRobot(pygame.sprite.Sprite):
    def __init__(self, position, direction, path):
       pygame.sprite.Sprite.__init__(self)

       self.image = pygame.image.load("robothead.png")

       self.rect = self.image.get_rect()
       self.rect.topleft = [position[0]*32, position[1] *32]

       self.position = position
       self.direction = direction
       self.path = path


    def update(self):
       
       if self.position == self.path[0] or self.position == self.path[1]:
          self.direction[0] = self.direction[0] *-1
          self.direction[1] = self.direction[1] *-1
      
       self.position [0] += self.direction[0]
       self.position [1] += self.direction[1]

       self.rect.topleft = [self.position[0]*32, self.position[1] *32]



# class for all lasers

class Laser (GameObject):
    
    def __init__(self, inputx, inputy, inputdirection, colour):
        GameObject.__init__(self, inputx, inputy)
        self.laser_exists = True
        self.direction = inputdirection
        self.colour = colour
         
        
    def draw (self):
     
        laserrect = pygame.Rect((self.location() [0] +12, self.location() [1] +12),(8,8))
        pygame.draw.rect (window, self.colour, laserrect)

        
    def update(self):

        self.x += self.direction [0]
        self.y += self.direction [1]


    def update_dir (self, mirror_orient):

      if mirror_orient == "tlbr":
         self.direction = (self.direction[1], self.direction [0])   
                     
      elif mirror.orient == "trbl":
         self.direction = (self.direction[1] *-1, self.direction [0] *-1)
       


    

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
mirrorlist.append (Mirror (17, 2, "tlbr"))
mirrorlist.append (Mirror (17, 5, "trbl"))


# Create filter

game_filter = Filter(8, 4, YELLOW)

# Create robots

robotlist = []

robotlist.append (SuperRobot ([3, 6],[0,-1], [[3,1],[3,13]]))
robotlist.append (SuperRobot ([2,12], [1,0], [[1,12],[18,12]]))                      


# Create lasers

laserlist = []

for robot in robotlist:
    laserlist.append (Laser (robot.position[0], robot.position[1], (1,0), PURPLE))



# draw the window onto the screen
pygame.display.update()

# game loop

while True:
    dt = clock.tick(60)

    timer -= dt
    time_move += dt
    
    # draw background and walls
    
    window.fill(BLACK)

   
    for wall in wall_list:
        wall.draw()

    # draw mirrors     

    for mirror in mirrorlist:
        mirror.draw()
   

    # draw filter
    game_filter.draw()
   
    
    if time_move >= 250:

       time_move -=250
       # draw and move robot

       
       for robot in robotlist:
          robot.update()
          
          
           
          
       # draw and move laser

       for laser in laserlist:
             
            if laser.laser_exists == False:
               robot_shoot = random.randint(0, len(robotlist)-1)
               laser.x = robotlist[robot_shoot].position[0]
               laser.y = robotlist[robot_shoot].position[1]
               laser.direction = (1,0)
               laser.colour = PURPLE
               laser.laser_exists = True

            if laser.laser_exists == True:

               laser.update()
               

            # check if laser hits wall, if so, remove from screen
            # check if laser colour matches wall colour, adapt score
                  
               for wall in wall_list:
                  if (laser.x,laser.y) in wall.wall_here:
                        laser.laser_exists = False

                        if laser.colour == wall.colour:
                           score +=1

             # check for mirror             

               for mirror in mirrorlist:
                  

                  if laser.x == mirror.x and laser.y == mirror.y:
                     laser.update_dir (mirror.orient)

             
    for robot in robotlist:   
        window.blit(robot.image, robot.rect)

    for laser in laserlist:
       # check for filter

        if laser.x == game_filter.x and laser.y == game_filter.y:
            laser.colour = game_filter.colour

        laser.draw()


    # print score
    text2 = font.render("Score: " + str(score), 1, BLACK)
    text1 = font.render("TIME: " + str(timer/100), 1, BLACK)
    text1pos = text1.get_rect()
    text1pos.centerx = window.get_rect().centerx
    text2pos = text2.get_rect()
    text2pos.right = window.get_rect().right -32
    window.blit(text1, text1pos)
    window.blit(text2, text2pos)

    # interaction (move filter using keys, change color using keys)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        
        if event.type == KEYDOWN:
          if event.key == K_RIGHT: game_filter.x += 1
          if event.key == K_LEFT: game_filter.x -= 1
          if event.key == K_UP: game_filter.y -= 1
          if event.key == K_DOWN:  game_filter.y += 1
          if event.key == K_1:  game_filter.colour = YELLOW
          if event.key == K_2:  game_filter.colour = RED
          if event.key == K_3:  game_filter.colour = GREEN
          if event.key == K_4:  game_filter.colour = BLUE
  
    pygame.display.flip()
