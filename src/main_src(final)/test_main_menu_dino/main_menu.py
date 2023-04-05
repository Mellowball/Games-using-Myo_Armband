# main_menu
import pygame, sys, os
from button import Button

# Rock, Papper, Scissors
import random
import threading
import serial
import time

line = ''
port = '/dev/ttyUSB0'
baud = 9600
ser = serial.Serial(port, baud, timeout=0)
receivenumber = 0

# 함수
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

def do0():
    receivenumber = 0
    #print('receivenum0 =', receivenumber)

pygame.init()

display_weight = 800
display_height = 480

SCREEN = pygame.display.set_mode((display_weight, display_height))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont('assets/font.ttf', size)

def rsp():
    global updateTime, updateIndex
    global result, win, lose, draw, choiceCom, choiceUser
    global isActive
        
    def eventProcess():
        # 혹여나 마이오 수신했을 때 제대로 동작 안 하면 여기서 receivenum 선언
        global isActive, choiceUser, choiceCom, result
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for button in [QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ser.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    isActive = False
                    main_menu()
                result, choiceUser, choiceCom = -1, -1, -1
        # 데이터 수신
        if receivenumber > 0:
            # if receivenumber == 5:      # 나가기(Double Tap)
            #     do0()
            #     isActive = False
            #     main_menu()
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
        global result, win, lose, draw, choiceCom, choiceUser
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
        global result, win, lose, draw
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
        global updateTime, updateIndex
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
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 480
    CENTER_WIDTH = SCREEN_WIDTH/2
    CENTER_HEIGHT = SCREEN_HEIGHT/2
    isActive = True
    updateTime = 0
    updateIndex = 0
    choiceUser, choiceCom = -1, -1
    result = -1
    win, lose, draw = 0, 0, 0
    clock = pygame.time.Clock()

    QUIT_BUTTON = Button(image=pygame.image.load("assets/Myo Reset.png"), pos=(display_weight/2 + 300, 350), 
                            text_input="Quit", font=get_font(40), base_color="#FF0000", hovering_color="White")
                    
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

    ##효과음
    # pygame.mixer.init()
    # pygame.mixer.music.load('Cat Shat in the Box - josh pan.mp3')
    # pygame.mixer.music.play(-1)

    ##Loop
    while(isActive):
        doThread()
        SCREEN.fill((0, 0, 0))
        eventProcess()
        updatePlayer()
        setText()
        pygame.display.flip()
        do0()
        clock.tick(100)
        pygame.display.update()
    
def dinosaur():
    # Global Constants
    SCREEN_HEIGHT = 480
    SCREEN_WIDTH = 800
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    RUNNING = [pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")),
            pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png"))]
    JUMPING = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))
    DUCKING = [pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")),
            pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png"))]

    SMALL_CACTUS = [pygame.image.load(os.path.join("assets/Cactus", "SmallCactus1.png")),
                    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus2.png")),
                    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus3.png"))]
    LARGE_CACTUS = [pygame.image.load(os.path.join("assets/Cactus", "LargeCactus1.png")),
                    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus2.png")),
                    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus3.png"))]

    BIRD = [pygame.image.load(os.path.join("assets/Bird", "Bird1.png")),
            pygame.image.load(os.path.join("assets/Bird", "Bird2.png"))]

    CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))

    BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))


    class Dinosaur:
        X_POS = 80
        Y_POS = 310
        Y_POS_DUCK = 340
        JUMP_VEL = 8.5

        def __init__(self):
            self.duck_img = DUCKING
            self.run_img = RUNNING
            self.jump_img = JUMPING

            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

            self.step_index = 0
            self.jump_vel = self.JUMP_VEL
            self.image = self.run_img[0]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS

        def update(self, userInput):
            if self.dino_duck:
                self.duck()
            if self.dino_run:
                self.run()
            if self.dino_jump:
                self.jump()

            if self.step_index >= 10:
                self.step_index = 0

            # 공룡 조작 키, 마이오 번호 집어넣으면 될듯 
            if receivenumber == 3 or userInput[pygame.K_UP] and not self.dino_jump:
                print(self.dino_jump)
                print("jump")
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True
            elif receivenumber == 2 or userInput[pygame.K_DOWN] and not self.dino_jump:
                print(self.dino_jump)
                print("down")
                self.dino_duck = True
                self.dino_run = False
                self.dino_jump = False
            elif not (self.dino_jump or userInput[pygame.K_DOWN]):
                self.dino_duck = False
                self.dino_run = True
                self.dino_jump = False

        def duck(self):
            self.image = self.duck_img[self.step_index // 5]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS_DUCK
            self.step_index += 1

        def run(self):
            self.image = self.run_img[self.step_index // 5]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS
            self.step_index += 1

        def jump(self):
            self.image = self.jump_img
            if self.dino_jump:
                self.dino_rect.y -= self.jump_vel * 4
                self.jump_vel -= 0.8
            if self.jump_vel < - self.JUMP_VEL:
                self.jump_vel = self.JUMP_VEL
                self.dino_jump = False

        def draw(self, SCREEN):
            SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


    class Cloud:
        def __init__(self):
            self.x = SCREEN_WIDTH + random.randint(800, 1000)
            self.y = random.randint(50, 100)
            self.image = CLOUD
            self.width = self.image.get_width()

        def update(self):
            self.x -= game_speed
            if self.x < -self.width:
                self.x = SCREEN_WIDTH + random.randint(2500, 3000)
                self.y = random.randint(50, 100)

        def draw(self, SCREEN):
            SCREEN.blit(self.image, (self.x, self.y))

    class Obstacle:
        def __init__(self, image, type):
            self.image = image
            self.type = type
            self.rect = self.image[self.type].get_rect()
            self.rect.x = SCREEN_WIDTH

        def update(self):
            self.rect.x -= game_speed
            if self.rect.x < -self.rect.width:
                obstacles.pop()

        def draw(self, SCREEN):
            SCREEN.blit(self.image[self.type], self.rect)


    class SmallCactus(Obstacle):
        def __init__(self, image):
            self.type = random.randint(0, 2)
            super().__init__(image, self.type)
            # self.rect.y = 325
            self.rect.y = 360


    class LargeCactus(Obstacle):
        def __init__(self, image):
            self.type = random.randint(0, 2)
            super().__init__(image, self.type)
            # self.rect.y = 300
            self.rect.y = 350


    class Bird(Obstacle):
        def __init__(self, image):
            self.type = 0
            super().__init__(image, self.type)
            self.rect.y = 250
            self.index = 0

        def draw(self, SCREEN):
            if self.index >= 9:
                self.index = 0
            SCREEN.blit(self.image[self.index//5], self.rect)
            self.index += 1


    def main():
        global game_speed, x_pos_bg, y_pos_bg, points, obstacles
        run = True
        clock = pygame.time.Clock()
        player = Dinosaur()
        cloud = Cloud()
        game_speed = 10
        x_pos_bg = 0
        y_pos_bg = 380
        points = 0
        font = pygame.font.Font('freesansbold.ttf', 20)
        obstacles = []
        death_count = 0

        def score():
            global points, game_speed
            points += 1
            if points % 100 == 0:
                game_speed += 1

            text = font.render("Points: " + str(points), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (1000, 40)
            SCREEN.blit(text, textRect)

        def background():
            global x_pos_bg, y_pos_bg
            image_width = BG.get_width()
            SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            if x_pos_bg <= -image_width:
                SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
                x_pos_bg = 0
            x_pos_bg -= game_speed

        while run:
            doThread()

            # 게임 중단 키입력 부분
            for event in pygame.event.get():
                # 창 닫기 눌렀을 때
                if event.type == pygame.QUIT:
                    run = False
                    ser.close()
                    pygame.quit()
                    sys.exit()
                # ESC 눌렀을 때(마이오 추가?)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        menu(death_count)
            
            # if receivenumber == 5:
            #     do0()
            #     run = False
            #     menu(death_count)

            SCREEN.fill((255, 255, 255))
            userInput = pygame.key.get_pressed()
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Myo Reset.png"), pos=(display_weight/2 + 300, 350), 
                            text_input="Quit", font=get_font(40), base_color="#FF0000", hovering_color="White")
            player.draw(SCREEN)
            player.update(userInput)

            if len(obstacles) == 0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird(BIRD))

            for obstacle in obstacles:
                obstacle.draw(SCREEN)
                obstacle.update()
                if player.dino_rect.colliderect(obstacle.rect):
                    pygame.time.delay(2000)
                    death_count += 1
                    menu(death_count)

            background()

            cloud.draw(SCREEN)
            cloud.update()

            score()
            do0()

            clock.tick(30)
            pygame.display.update()


    def menu(death_count):
        global points

        # QUIT_BUTTON = Button(image=pygame.image.load("assets/Myo Reset.png"), pos=(display_weight/2 + 300, 350), 
        #                     text_input="Quit", font=get_font(40), base_color="#FF0000", hovering_color="White")
        run = True
        while run:

            doThread()
            SCREEN.fill((255, 255, 255))
            font = pygame.font.Font('freesansbold.ttf', 30)
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Myo Reset.png"), pos=(display_weight/2 + 300, 350), 
                            text_input="Quit", font=get_font(40), base_color="#FF0000", hovering_color="White")
            if death_count == 0:
                text = font.render("Press any Key to Start", True, (0, 0, 0))
            elif death_count > 0:
                text = font.render("Press any Key to Restart", True, (0, 0, 0))
                score = font.render("Your Score: " + str(points), True, (0, 0, 0))
                scoreRect = score.get_rect()
                scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
                SCREEN.blit(score, scoreRect)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
            
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            for button in [QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    ser.close()
                    pygame.quit()
                    sys.exit()
                # 게임시작 키 입력, ESC = 나가기(마이오 추가?)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_menu()
                    main()
                MENU_MOUSE_POS = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        isActive = False
                        main_menu()
                    main()
            # if receivenumber == 5:
            #     do0()
            #     main_menu() 
        
            do0() # 초기화     
            pygame.display.update()

    menu(death_count=0)

# def myo_reset():
#     sendnum = '<1>'
#     sendnum = sendnum.encode('utf-8')
#     ser.write(sendnum)
#     print("Arduino Reset")
#     time.sleep(1)
#     main_menu()


def main_menu():
    while True:
        doThread() # 초기화화 초기화
        do0() # 초기화 초기화화

        SCREEN = pygame.display.set_mode((display_weight, display_height))
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#00FF00")
        MENU_RECT = MENU_TEXT.get_rect(center=(display_weight/2, 50))
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(display_weight/2, 150), 
                            text_input="Rock Paper Scissors", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(display_weight/2, 250), 
                            text_input="Jumping Dino", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(display_weight/2, 350), 
                            text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        # MyoReset_BUTTON = Button(image=pygame.image.load("assets/Myo Reset.png"), pos=(display_weight/2 + 300, 350), 
        #                     text_input="Myo Reset", font=get_font(18), base_color="#FF0000", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ser.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    rsp()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    dinosaur()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ser.close()
                    pygame.quit()
                    sys.exit()
                # if MyoReset_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     myo_reset()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ser.close()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()