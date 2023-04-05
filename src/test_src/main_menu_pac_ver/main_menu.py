# main_menu
import pygame, sys
from button import Button

# Rock, Papper, Scissors
import random
import threading
import serial
import time

# Pac-man
from pygame.locals import *
from constants import *
from pacman import Pacman
#ThreadProcess 클래스 pacman에서 불러와서 시리얼 통신 진행
from pacman import ThreadProcess as tp
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pauser import Pause
from text import TextGroup
from sprites import LifeSprites
from sprites import MazeSprites
from mazedata import MazeData
import pacman

pygame.init()

display_weight = 600
display_height = 400

SCREEN = pygame.display.set_mode((display_weight, display_height))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont('arial', size)

def rsp():
    global updateTime, updateIndex
    global win, lose, draw, choiceCom, choiceUser, clock, result
    global isActive, line, port, baud, ser, receivenumber
    global SCREEN_HEIGHT, SCREEN_WIDTH, CENTER_HEIGHT, CENTER_WIDTH

    line = ''
    port = '/dev/ttyUSB0'
    baud = 9600
    ser = serial.Serial(port, baud, timeout=0)
    receivenumber = 0

    ##함수
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
        thread = threading.Thread(target=readthread, args=(ser,))
        thread.start()
        thread.join()
        
    def eventProcess():
        global isActive, choiceUser, choiceCom, result, receivenumber
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    # ESC
                    ser.close()
                    isActive = False
                    main_menu()
                if result == -1:
                    if event.key == pygame.K_LEFT:  # 가위
                        choiceUser = 0
                    if event.key == pygame.K_DOWN:  # 바위
                        choiceUser = 1
                    if event.key == pygame.K_RIGHT:  # 보
                        choiceUser = 2
                    if choiceUser != -1:
                        resultProcess()
                else:
                    if event.key == pygame.K_SPACE:  # 재시작
                        result, choiceUser, choiceCom = -1, -1, -1

        # 데이터 수신
        if receivenumber > 0:
            if receivenumber == 5:      # 나가기(Double Tap)
                ser.close()
                isActive = False
                main_menu()
            if result == -1:
                if receivenumber == 2:  # 가위(Wave In)
                    choiceUser = 0
                if receivenumber == 1:  # 바위(Fist)
                    choiceUser = 1
                if receivenumber == 4:  # 보(Finger Spread)
                    choiceUser = 2
                if choiceUser != -1:
                    resultProcess()
            else:
                if (receivenumber == 3):  # 재시작(Wave Out)
                    result, choiceUser, choiceCom = -1, -1, -1
                        

    def resultProcess():
        global win, lose, draw, choiceCom, choiceUser, result
        choiceCom = random.randint(0, 2)
        if choiceCom == choiceUser:
            result = 0
            draw += 1
        elif (choiceUser == 0 and choiceCom == 2)\
                or (choiceUser == 1 and choiceCom == 0)\
                or (choiceUser == 2 and choiceCom == 1):
            result = 1
            win += 1
        else:
            result = 2
            lose += 1

    def setText():
        global win, lose, draw, result
        mFont = pygame.font.SysFont("굴림", 20)
        mtext = mFont.render(f'win {win}, lose {lose}, draw {draw}', True, green)
        SCREEN.blit(mtext, (10, 10, 0, 0))

        mFont = pygame.font.SysFont("arial", 15)
        mtext = mFont.render(
            f'(scissors : ←) (rock :  ↓) (paper : →) (continue : space)', True, white)
        SCREEN.blit(mtext, (CENTER_WIDTH-40, 10, 0, 0))

        mFont = pygame.font.SysFont("arial", 60)
        mtext = mFont.render(f'VS', True, yellow)
        SCREEN.blit(mtext, (CENTER_WIDTH-35, CENTER_HEIGHT-40, 0, 0))

        mFont = pygame.font.SysFont("arial", 40)
        mtext = mFont.render(f'Computer             User', True, white)
        SCREEN.blit(mtext, (CENTER_WIDTH-200, CENTER_HEIGHT-100, 0, 0))

        if result != -1:
            mFont = pygame.font.SysFont("arial", 60)
            resultText = ['Draw!!', 'Win!!', 'Lose']
            mtext = mFont.render(resultText[result], True, red)
            SCREEN.blit(mtext, (CENTER_WIDTH-80, CENTER_HEIGHT+100, 0, 0))

    def getIndex():
        global updateTime, updateIndex, result, choiceCom, choiceUser
        if result == -1:
            updateTime += 1
            if updateTime > 10:
                updateTime = 0
                updateIndex = (updateIndex+1) % len(player)
            return updateIndex, updateIndex
        else:
            return choiceCom, choiceUser

    def updatePlayer():
        idex1, idex2 = getIndex()

        recPlayer[idex1].centerx = CENTER_WIDTH-100
        recPlayer[idex1].centery = CENTER_HEIGHT
        SCREEN.blit(player[idex1], recPlayer[idex1])

        recPlayer[idex2].centerx = CENTER_WIDTH+100
        recPlayer[idex2].centery = CENTER_HEIGHT
        SCREEN.blit(player[idex2], recPlayer[idex2])

    ##변수 선언 및 초기화
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 400
    CENTER_WIDTH = SCREEN_WIDTH/2
    CENTER_HEIGHT = SCREEN_HEIGHT/2
    isActive = True
    updateTime = 0
    updateIndex = 0
    choiceUser, choiceCom = -1, -1
    result = -1
    win, lose, draw = 0, 0, 0
    clock = pygame.time.Clock()



    ##색상 변수 선언
    black = (0,0,0)
    white = (255,255,255)
    red = (255, 0 ,0)
    yellow = (255,255,0)
    green = (0,255,0)

    # 시리얼 읽을 쓰레드 생성

    ##pygmae init
    pygame.init()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("CodingNow!!")

    ##이미지 가져오기
    pIamges = ['scissors.bmp', 'rock.bmp', 'paper.bmp']
    player = [pygame.image.load(pIamges[i]) for i in range(len(pIamges))]
    player = [pygame.transform.scale(player[i], (100, 100)) for i in range(len(player))]
    recPlayer = [player[i].get_rect() for i in range(len(player))]

    #효과음
    pygame.mixer.init()
    pygame.mixer.music.load('Cat Shat in the Box - josh pan.mp3')
    pygame.mixer.music.play(-1)

    ##Loop
    while(isActive):
        doThread()
        SCREEN.fill((0, 0, 0))
        eventProcess()
        updatePlayer()
        setText()
        pygame.display.flip()
        receivenumber = 0
        clock.tick(100)
        pygame.display.update()
    
def pac_man():
    class GameController(object):
        def __init__(self):
            pygame.init()
            self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
            self.background = None
            self.background_norm = None
            self.background_flash = None
            self.clock = pygame.time.Clock()
            self.fruit = None
            self.pause = Pause(True)
            self.level = 0
            self.lives = 5
            self.score = 0
            self.textgroup = TextGroup()
            self.lifesprites = LifeSprites(self.lives)
            self.flashBG = False
            self.flashTime = 0.2
            self.flashTimer = 0
            self.fruitCaptured = []
            self.fruitNode = None
            self.mazedata = MazeData()

        def setBackground(self):
            self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
            self.background_norm.fill(BLACK)
            self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
            self.background_flash.fill(BLACK)
            self.background_norm = self.mazesprites.constructBackground(self.background_norm, self.level%5)
            self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
            self.flashBG = False
            self.background = self.background_norm

        def startGame(self):      
            self.mazedata.loadMaze(self.level)
            self.mazesprites = MazeSprites(self.mazedata.obj.name+".txt", self.mazedata.obj.name+"_rotation.txt")
            self.setBackground()
            self.nodes = NodeGroup(self.mazedata.obj.name+".txt")
            self.mazedata.obj.setPortalPairs(self.nodes)
            self.mazedata.obj.connectHomeNodes(self.nodes)
            self.pacman = Pacman(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart))
            self.pellets = PelletGroup(self.mazedata.obj.name+".txt")
            self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)

            self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
            self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3)))
            self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3)))
            self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
            self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 0)))

            self.nodes.denyHomeAccess(self.pacman)
            self.nodes.denyHomeAccessList(self.ghosts)
            self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
            self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
            self.mazedata.obj.denyGhostsAccess(self.ghosts, self.nodes)

        def startGame_old(self):      
            self.mazedata.loadMaze(self.level)#######
            self.mazesprites = MazeSprites("maze1.txt", "maze1_rotation.txt")
            self.setBackground()
            self.nodes = NodeGroup("maze1.txt")
            self.nodes.setPortalPair((0,17), (27,17))
            homekey = self.nodes.createHomeNodes(11.5, 14)
            self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
            self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
            self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))
            self.pellets = PelletGroup("maze1.txt")
            self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
            self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 0+14))
            self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
            self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(0+11.5, 3+14))
            self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(4+11.5, 3+14))
            self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))

            self.nodes.denyHomeAccess(self.pacman)
            self.nodes.denyHomeAccessList(self.ghosts)
            self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
            self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)
            self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
            self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
            self.nodes.denyAccessList(12, 14, UP, self.ghosts)
            self.nodes.denyAccessList(15, 14, UP, self.ghosts)
            self.nodes.denyAccessList(12, 26, UP, self.ghosts)
            self.nodes.denyAccessList(15, 26, UP, self.ghosts)

        
        def update(self):
            dt = self.clock.tick(30) / 1000.0
            self.textgroup.update(dt)
            self.pellets.update(dt)
            if not self.pause.paused:
                self.ghosts.update(dt)      
                if self.fruit is not None:
                    self.fruit.update(dt)
                self.checkPelletEvents()
                self.checkGhostEvents()
                self.checkFruitEvents()

            if self.pacman.alive:
                if not self.pause.paused:
                    self.pacman.update(dt)
            else:
                self.pacman.update(dt)

            if self.flashBG:
                self.flashTimer += dt
                if self.flashTimer >= self.flashTime:
                    self.flashTimer = 0
                    if self.background == self.background_norm:
                        self.background = self.background_flash
                    else:
                        self.background = self.background_norm

            afterPauseMethod = self.pause.update(dt)
            if afterPauseMethod is not None:
                afterPauseMethod()
            self.checkEvents()
            self.render()

        def checkEvents(self):
            for event in pygame.event.get():
                if event.type == QUIT:
                    main_menu()
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if self.pacman.alive:
                            self.pause.setPause(playerPaused=True)
                            if not self.pause.paused:
                                self.textgroup.hideText()
                                self.showEntities()
                            else:
                                self.textgroup.showText(PAUSETXT)
                                #self.hideEntities()
                    if event.key == K_ESCAPE:
                        pacman.ser.close()
                        main_menu()

        def checkPelletEvents(self):
            pellet = self.pacman.eatPellets(self.pellets.pelletList)
            if pellet:
                self.pellets.numEaten += 1
                self.updateScore(pellet.points)
                if self.pellets.numEaten == 30:
                    self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
                if self.pellets.numEaten == 70:
                    self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
                self.pellets.pelletList.remove(pellet)
                if pellet.name == POWERPELLET:
                    self.ghosts.startFreight()
                if self.pellets.isEmpty():
                    self.flashBG = True
                    self.hideEntities()
                    self.pause.setPause(pauseTime=3, func=self.nextLevel)

        def checkGhostEvents(self):
            for ghost in self.ghosts:
                if self.pacman.collideGhost(ghost):
                    if ghost.mode.current is FREIGHT:
                        self.pacman.visible = False
                        ghost.visible = False
                        self.updateScore(ghost.points)                  
                        self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                        self.ghosts.updatePoints()
                        self.pause.setPause(pauseTime=1, func=self.showEntities)
                        ghost.startSpawn()
                        self.nodes.allowHomeAccess(ghost)
                    elif ghost.mode.current is not SPAWN:
                        if self.pacman.alive:
                            self.lives -=  1
                            self.lifesprites.removeImage()
                            self.pacman.die()               
                            self.ghosts.hide()
                            if self.lives <= 0:
                                self.textgroup.showText(GAMEOVERTXT)
                                self.pause.setPause(pauseTime=3, func=self.restartGame)
                            else:
                                self.pause.setPause(pauseTime=3, func=self.resetLevel)
        
        def checkFruitEvents(self):
            if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
                if self.fruit is None:
                    self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20), self.level)
                    print(self.fruit)
            if self.fruit is not None:
                if self.pacman.collideCheck(self.fruit):
                    self.updateScore(self.fruit.points)
                    self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                    fruitCaptured = False
                    for fruit in self.fruitCaptured:
                        if fruit.get_offset() == self.fruit.image.get_offset():
                            fruitCaptured = True
                            break
                    if not fruitCaptured:
                        self.fruitCaptured.append(self.fruit.image)
                    self.fruit = None
                elif self.fruit.destroy:
                    self.fruit = None

        def showEntities(self):
            self.pacman.visible = True
            self.ghosts.show()

        def hideEntities(self):
            self.pacman.visible = False
            self.ghosts.hide()

        def nextLevel(self):
            self.showEntities()
            self.level += 1
            self.pause.paused = True
            self.startGame()
            self.textgroup.updateLevel(self.level)

        def restartGame(self):
            self.lives = 5
            self.level = 0
            self.pause.paused = True
            self.fruit = None
            self.startGame()
            self.score = 0
            self.textgroup.updateScore(self.score)
            self.textgroup.updateLevel(self.level)
            self.textgroup.showText(READYTXT)
            self.lifesprites.resetLives(self.lives)
            self.fruitCaptured = []

        def resetLevel(self):
            self.pause.paused = True
            self.pacman.reset()
            self.ghosts.reset()
            self.fruit = None
            self.textgroup.showText(READYTXT)

        def updateScore(self, points):
            self.score += points
            self.textgroup.updateScore(self.score)

        def render(self):
            self.screen.blit(self.background, (0, 0))
            #self.nodes.render(self.screen)
            self.pellets.render(self.screen)
            if self.fruit is not None:
                self.fruit.render(self.screen)
            self.pacman.render(self.screen)
            self.ghosts.render(self.screen)
            self.textgroup.render(self.screen)

            for i in range(len(self.lifesprites.images)):
                x = self.lifesprites.images[i].get_width() * i
                y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
                self.screen.blit(self.lifesprites.images[i], (x, y))

            for i in range(len(self.fruitCaptured)):
                x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i+1)
                y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
                self.screen.blit(self.fruitCaptured[i], (x, y))

            pygame.display.update()
        

    if __name__ == "__main__":
        game = GameController()
        game.startGame()
        while True:
            game.update()
            tp.doThread()
            tp.do0()


def main_menu():
    while True:
        SCREEN = pygame.display.set_mode((display_weight, display_height))
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#00FF00")
        MENU_RECT = MENU_TEXT.get_rect(center=(display_weight/2, 50))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(display_weight/2, 150), 
                            text_input="Rock Paper Scissors", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(display_weight/2, 250), 
                            text_input="Pac-man", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(display_weight/2, 350), 
                            text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    rsp()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pac_man()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()