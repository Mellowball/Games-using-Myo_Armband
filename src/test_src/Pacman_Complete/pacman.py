import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites

import threading
import random
import serial
import time

line = ''
port = '/dev/ttyUSB0'
baud = 115200
ser = serial.Serial(port, baud, timeout=0)
receivenumber = 0

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node )
        self.name = PACMAN    
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def die(self):
        self.alive = False
        self.direction = STOP

    def update(self, dt):	
        self.sprites.update(dt)
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        global receivenumber
        if key_pressed[K_UP] or receivenumber == 1:
            return UP
        if key_pressed[K_DOWN] or receivenumber == 2:
            return DOWN
        if key_pressed[K_LEFT] or receivenumber == 3:
            return LEFT
        if key_pressed[K_RIGHT] or receivenumber == 4:
            return RIGHT
        return STOP  

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None    
    
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False
class ThreadProcess(object):   
    def readthread(ser):
        global line, receivenumber
        for c in ser.read():
            # line 변수에 차곡차곡 추가하여 넣는다.
            line += (chr(c))
            if line.startswith('[') and line.endswith(']'):  # 라인의 끝을 만나면..
                # 데이터 처리 함수로 호출
                print('receive data=' + line)
                receivenumber = int(line[1:2])
                line = ''
               
    def doThread():
        # 시리얼 읽을 쓰레드 생성
        thread = threading.Thread(target=ThreadProcess.readthread, args=(ser,))
        thread.start()
        thread.join()
        return receivenumber
    def do0():
        receivenumber = 0
        #print('receivenum0 =', receivenumber)
