import random,math,pygame,numpy.random
from pygame.locals import *

#INTERFACE METHODS
def draw_dashed_line(surf, color, start_pos, end_pos, width, dash_length):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)

#CONSTANTS and GLOBAL VARIABLES
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
SILVER = [192,192,192]
YELLOW = [255,255,0]

winwidth = 1500
winheight = 500
#65 mph
#1 pixel = .5 meters
speedlim = 13
LANE_WIDTH = 16

centery = round(winheight/2)

WINSIZE = [winwidth,winheight]

#Stuff to hold car data
carlist = []
#1 frame = .25 seconds
class humanDriver:
    def __init__(self,id):
        self.id = id
        self.driverReactionTime = round(numpy.random.normal(2.25,0.45) * 4)
        self.carLength = 10
        self.carWidth = 4
        self.carBody = [self.carLength,self.carWidth]
        self.position = 11
        self.accelerate = False
        self.deccelerate = False
        self.arate = 0
        self.speed = round((numpy.random.normal(74.05,5.03))*.25)
        self.maxspeed = self.speed
        self.waitTime = 0
        self.stopped = False
        self.maxarate = 3

        carlist.append(self)

    def move(self):
        if (self.waitTime == 0):
            self.speed += self.arate
            self.position += self.speed
            self.stopped = False
        else:
            self.waitTime -=1

    def check(self):
        if self.id >= 1:
            #if (carlist[self.id-1].arate <= 0):
            #    self.arate = round(((carlist[self.id-1].speed ** 2) - (self.speed ** 2)) / (2*(carlist[self.id-1].position-self.position)))
            #if (carlist[self.id-1].arate >= 0):
            #    self.arate = round(((carlist[self.id-1].speed ** 2) - (self.speed ** 2)) / (2*(carlist[self.id-1].position-self.position)))
            #if (carlist[self.id-1].speed == 0):
            #    self.arate = (-(self.speed ** 2) / (2*(carlist[self.id-1].position-self.position)))
            #if (carlist[self.id-1].speed < self.speed) and ((carlist[self.id-1].position-self.position-15) > 0):
            #    self.arate = - ((self.speed - carlist[self.id-1].speed) ** 2) / (2*(carlist[self.id-1].position-self.position-15))
            #else:
            #    if (carlist[self.id-1].position-self.position == 15):
            #        self.speed = carlist[self.id-1].speed
            #        self.arate = 0
            self.arate = ((carlist[self.id-1].position-self.position-carlist[self.id-1].carLength)/self.driverReactionTime) - self.speed
        #if self.speed < self.maxspeed:
        #    self.arate = 10

        #if self.speed >= self.maxspeed:
        #    self.arate = 0
        if self.speed < 0:
            self.speed = 0
            self.arate = 0
        
        if self.arate > 0:
            self.accel()
        if self.arate < 0:
            self.deccel()
        if self.arate == 0:
            self.accelerate = False
            self.deccelerate = False
        if self.speed < 0.1 and self.stopped == False:
            self.waitTime = self.driverReactionTime
            self.stopped = True
        if self.speed > self.maxspeed:
            self.speed = self.maxspeed
        #if self.arate>self.maxarate:
        #    self.arate = self.maxarate
 
    def accel(self):
        self.accelerate = True
        self.deccelerate = False
    def deccel(self):
        self.accelerate = False
        self.deccelerate = True



#INITIALIZE SCREEN
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINSIZE)

pygame.draw.rect(screen,GREEN,Rect([0,0],WINSIZE))

roadRect = Rect(0,centery,winwidth,LANE_WIDTH)
pygame.draw.rect(screen,WHITE,roadRect)

pygame.display.flip()

vehicleNum = 0

indexrange = 0


#MAIN LOOP BODY
curTime = 0
endTime = 10000000000000000000
while curTime<endTime:
    pygame.event.get()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: 
        pygame.quit()
    if keys[K_f]:
        break

    if vehicleNum == 0:
        humanDriver(vehicleNum)
        vehicleNum += 1
    elif (carlist[vehicleNum-1].position >= carlist[vehicleNum-1].carLength):
        humanDriver(vehicleNum)
        vehicleNum += 1

    if curTime == 50:
        carlist[0].arate = 0
        carlist[0].speed = 0
    
    if curTime == 200:
        carlist[0].arate = 1

    for car in carlist:
        oldCar = Rect((car.position - car.carLength),(centery+ (car.carWidth)),car.carLength,car.carWidth)
        pygame.draw.rect(screen,WHITE,oldCar)
        car.check() ; car.move()
        curColor = RED
        if (car.arate > 0):
            curColor = BLUE
        if (car.arate < 0):
            curColor = RED
        if (car.arate == 0):
            curColor = BLACK
        curCar = Rect((car.position - car.carLength),(centery + (car.carWidth)),car.carLength,car.carWidth)
        if car.position > winwidth:
            indexrange = car.id
        pygame.draw.rect(screen,curColor,curCar)

    pygame.display.flip()

    clock.tick(10)
    curTime+=1
while 1:
    pygame.event.get()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: 
        pygame.quit()
